import ssl

import librouteros
from isp_router.isp_router.api.mikrotik_base import MikrotikBase


class MikrotikClientV6(MikrotikBase):

	def __init__(self, host: str, port: int, username: str, password: str, use_ssl= False):

		ctx = None
		if use_ssl:
			ctx = ssl.create_default_context()
			ctx.check_hostname = False
			ctx.set_ciphers('ADH:@SECLEVEL=0')

		try:

			self.api = librouteros.connect(
				host=host,
				port=port,
				username=username,
				password=password,
				context=ctx
			)

		except Exception as e:
			raise Exception(f"Failed to connect to MikroTik: {e}")

	def test_connection(self):

		try:

			_ = self.api.path("system", "resource", "print")

		except Exception as e:
			raise Exception(f"Failed to connect to MikroTik: {e}")


	def provision_service_simple_queue(self, name: str, target: str, upload_speed: str,
									   download_speed: str):

		# /ip firewall address-list
		# add list=clients name=Juan address=192.168.88.10
		cmd1_params = {
			'list': 'clients',
			'name': name,
			'address': target.split('/')[0],
		}

		# /queue simple
		# add name=Juan target=192.168.88.10/32 max-limit=5M/5M
		cmd2_params = {
			'name': name,
			'target': target,
			'max-limit': f'{upload_speed}/{download_speed}',
		}

		try:

			self.api.path('ip', 'firewall', 'address-list').add(cmd1_params)

			self.api.path('queue', 'simple').add(cmd2_params)

		except Exception as e:
			raise Exception(f'Failed to connect to MikroTik: {e}')


	def provision_service_pppoe(self, username: str, password: str, local_address: str,
								remote_address: str, upload_speed: str, download_speed: str):

		# /ppp profile
		# add name=Juan local-address=192.168.89.1 remote-address=192.168.89.10 rate-limit=5M/5M
		cmd1_params = {
			'name': f'profile-{username}',
			'local-address': local_address,
			'remote-address': remote_address,
			'rate-limit': f'{upload_speed}/{download_speed}',
		}

		# /ppp secret
		# add name=Juan password=clave profile=Juan service=pppoe
		cmd2_params = {
			'name': username,
			'password': password,
			'profile': f'profile-{username}',
			'service': 'pppoe',
		}

		try:

			self.api.path('ppp', 'profile').add(cmd1_params)

			self.api.path('ppp', 'secret').add(cmd2_params)

		except Exception as e:
			raise Exception(f'Failed to connect to MikroTik: {e}')


	def provision_service_hotspot(self, username: str, password: str, limit_uptime: str,
								  upload_speed: str, download_speed: str):

		# /ip hotspot user
		# add name=Juan password=clave limit-uptime=1d rate-limit=2M/2M
		params = {
			'name': username,
			'password': password,
			'limit-uptime': limit_uptime or '0s',
			'rate-limit': f'{upload_speed}/{download_speed}',
		}

		try:

			self.api.path('ip', 'hotspot', 'user').add(params)

		except Exception as e:
			raise Exception(f'Failed to connect to MikroTik: {e}')


	def provision_service_pcq(self, username: str, target: str, upload_speed: str,
							  download_speed: str):

		# /queue type
		# add name=pcq-upload kind=pcq pcq-rate=5M pcq-classifier=src-address
		cmd1_params = {
			'name': f'pcq-upload-{username}',
			'kind': 'pcq',
			'pcq-rate': upload_speed,
			'pcq-classifier': 'src-address',
		}

		# /queue type
		# add name=pcq-download kind=pcq pcq-rate=5M pcq-classifier=dst-address
		cmd2_params = {
			'name': f'pcq-download-{username}',
			'kind': 'pcq',
			'pcq-rate': download_speed,
			'pcq-classifier': 'dst-address',
		}

		# /queue simple
		# add name=Juan target=192.168.88.10/32 queue=pcq-upload/pcq-download
		cmd3_params = {
			'name': username,
			'target': target,
			'queue': f'pcq-upload-{username}/pcq-download-{username}',
		}

		try:

			self.api.path('queue', 'type').add(cmd1_params)

			self.api.path('queue', 'type').add(cmd2_params)

			self.api.path('queue', 'simple').add(cmd3_params)

		except Exception as e:
			raise Exception(f'Failed to connect to MikroTik: {e}')


	def provision_service_openvpn(self, username: str, password: str, local_address: str,
								  remote_address: str):

		# /ppp profile
		# add name=Juan local-address=10.8.0.1 remote-address=10.8.0.2
		cmd1_params = {
			'name': f'profile-{username}',
			'local-address': local_address,
			'remote-address': remote_address,
		}

		# /ppp secret
		# add name=Juan password=clave profile=Juan service=ovpn
		cmd2_params = {
			'name': username,
			'password': password,
			'profile': f'profile-{username}',
			'service': 'ovpn',
		}

		try:

			self.api.path('ppp', 'profile').add(cmd1_params)

			self.api.path('ppp', 'secret').add(cmd2_params)

		except Exception as e:
			raise Exception(f'Failed to connect to MikroTik: {e}')


	def provision_service_l2tp(self, username: str, password: str, local_address: str,
							   remote_address: str):

		# /ppp profile
		# add name=Juan local-address=10.9.0.1 remote-address=10.9.0.2
		cmd1_params = {
			'name': f'profile-{username}',
			'local-address': local_address,
			'remote-address': remote_address,
		}

		# /ppp secret
		# add name=Juan password=clave profile=Juan service=l2tp
		cmd2_params = {
			'name': username,
			'password': password,
			'profile': f'profile-{username}',
			'service': 'l2tp',
		}

		try:

			self.api.path('ppp', 'profile').add(cmd1_params)

			self.api.path('ppp', 'secret').add(cmd2_params)

		except Exception as e:
			raise Exception(f'Failed to connect to MikroTik: {e}')


	def disable_service(self, name, connection_type):
		pass

	def enable_service(self, name, connection_type):
		pass

	def ping(self):
		pass
