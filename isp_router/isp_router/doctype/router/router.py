import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt

from isp_router.isp_router.api.mikrotik_client import mikrotik_client_factory


class Router(Document):
	"""
	Doctype que representa un router Mikrotik en el sistema.
	Maneja la configuración y validación de conexiones a routers Mikrotik.
	"""

	def validate(self):
		"""Valida los campos del documento antes de guardar"""
		self.validate_api_port()

	def validate_api_port(self):
		"""
		Valida que el puerto API esté en el rango válido y sea un número entero
		"""
		port = self.get('api_port')

		if not isinstance(port, int):
			frappe.throw(_("Port must be an integer"))

		if port < 0 or port > 65535:
			frappe.throw(_("Port must be between 0 and 65535"))

		# Validar puertos comunes de Mikrotik API
		if port not in [8728, 8729]:  # 8728 (API), 8729 (API-SSL)
			frappe.msgprint(
				_("Warning: Non-standard Mikrotik API port detected. Standard ports are 8728 (API) and 8729 (API-SSL)"),
				indicator='orange'
			)


	def mikrotik_validate_connection(self):
		"""
		Valida la conexión al router Mikrotik usando los parámetros configurados
		"""
		try:
			mk_client = mikrotik_client_factory(
				self.get('router_version'),
				self.get('api_host'),
				self.get('api_port'),
				self.get('username'),
				self.get('password'),
				self.get('use_ssl')
			)
		except ValueError as e:
			frappe.throw(_('Configuration Error: {}').format(str(e)))
		except Exception as e:
			frappe.throw(_('Unexpected error while creating client: {}').format(str(e)))

		try:
			mk_client.test_connection()
			frappe.msgprint(
				_('Connection successfully established'),
				indicator='green'
			)
		except ConnectionError as e:
			frappe.throw(
				_('Failed to connect: {}').format(str(e)),
				title=_('Connection Error')
			)
		except TimeoutError as e:
			frappe.throw(
				_('Connection attempt timed out: {}').format(str(e)),
				title=_('Timeout Error')
			)
		except Exception as e:
			frappe.throw(
				_('Unexpected error while testing connection: {}').format(str(e)),
				title=_('Error')
			)


	@frappe.whitelist()
	def test_connection(self):

		self.mikrotik_validate_connection()
