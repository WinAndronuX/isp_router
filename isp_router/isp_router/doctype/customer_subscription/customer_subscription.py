import re
import random
import string
import ipaddress
import frappe
from frappe import Document, _
from isp_router.isp_router.api.mikrotik_client import mikrotik_client_factory

class CustomerSubscription(Document):
	def before_save(self):
		if not self.is_new():
			return
			
		if not self.get_doc_before_save():
			# Es un documento nuevo, forzar estado borrador
			self.docstatus = 0
			
			# Generar credenciales si no existen
			if not self.router_username or not self.router_password:
				self.generate_router_credentials()

	def validate(self):
		self.validate_coordinates()
		self.validate_ip_addresses()
		self.validate_limit_uptime()
		
		if self.docstatus == 1:  # Si está siendo validado
			self.provision_subscription()
			
	def generate_router_credentials(self):
		# Obtener información del cliente
		customer = frappe.get_doc("Customer", self.customer)
		
		# Generar username: nombre-apellido-XXXX
		if not self.router_username:
			# Obtener nombre y apellido del cliente
			name_parts = customer.customer_name.lower().split()
			if len(name_parts) >= 2:
				name = name_parts[0]
				lastname = name_parts[-1]
				# Generar 4 caracteres aleatorios
				random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
				self.router_username = f"{name}-{lastname}-{random_suffix}"
			else:
				# Si no hay apellido, usar solo el nombre
				name = name_parts[0]
				random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
				self.router_username = f"{name}-{random_suffix}"
		
		# Generar password aleatorio de 6 caracteres
		if not self.router_password:
			self.router_password = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
			
	def provision_subscription(self):
		"""Aprovisionar la suscripción en el router"""
		
		router = frappe.get_doc("Router", self.router_link)
		internet_plan = frappe.get_doc("Internet Plan", self.internet_plan)

		mk_client = mikrotik_client_factory(
			router.router_version,
			router.api_host,
			router.api_port,
			router.username,
			router.password,
			router.use_ssl
		)

		try:
			match internet_plan.connection_type:
				case 'Simple Queue':
					mk_client.provision_service_simple_queue(self.router_username, self.target, internet_plan.upload_speed, internet_plan.download_speed)
				case 'PPPoE':
					mk_client.provision_service_pppoe(self.router_username, self.router_password, self.local_address, self.remote_address, internet_plan.upload_speed, internet_plan.download_speed)
				case 'Hotspot':
					mk_client.provision_service_hotspot(self.router_username, self.router_password, self.limit_uptime, internet_plan.upload_speed, internet_plan.download_speed)
				case 'PCQ':
					mk_client.provision_service_pcq(self.router_username, self.target, internet_plan.upload_speed, internet_plan.download_speed)
				case 'OpenVPN':
					mk_client.provision_service_openvpn(self.router_username, self.router_password, self.local_address, self.remote_address)
				case 'L2TP':
					mk_client.provision_service_l2tp(self.router_username, self.router_password, self.local_address, self.remote_address)
				case _:
					frappe.throw(_('Connection type not supported'))

		except Exception as e:
			frappe.throw(_('Failed to provision subscription: {}').format(str(e)))


	def validate_coordinates(self):
		if self.coordinates:
			pattern = r'^-?\d+\.\d+,-?\d+\.\d+$'
			if not re.match(pattern, self.coordinates):
				frappe.throw(
					_('Invalid coordinates. Use the format: latitude,longitude (e.g.: 4.710989,-74.072092)')
				)

	def validate_ip_addresses(self):
		ip_fields = {
			'target': self.target,
			'local_address': self.local_address,
			'remote_address': self.remote_address
		}
		
		for field_name, value in ip_fields.items():
			if value:
				try:
					ipaddress.ip_address(value)
				except ValueError:
					frappe.throw(
						_('Invalid IP address in field {0}. Use the format: xxx.xxx.xxx.xxx').format(_(field_name))
					)

	def validate_limit_uptime(self):
		if self.limit_uptime:
			pattern = r'^(?:\d+w)?(?:\d+d)?(?:\d+h)?(?:\d+m)?$'
			if not re.match(pattern, self.limit_uptime):
				frappe.throw(
					_('Invalid Limit Uptime format. Use the format: 1w2d3h4m (weeks, days, hours, minutes)')
				)
