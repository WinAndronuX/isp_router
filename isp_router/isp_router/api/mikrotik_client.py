from abc import ABC, abstractmethod

from isp_router.isp_router.api.mikrotik_client_v6 import MikrotikClientV6
from isp_router.isp_router.api.mikrotik_client_v7 import MikrotikClientV7


class MikrotikClient(ABC):
	"""
	Clase base abstracta para clientes Mikrotik.
	Define la interfaz común para interactuar con routers Mikrotik de diferentes versiones.
	"""

	@abstractmethod
	def test_connection(self) -> bool:
		"""
		Prueba la conexión al router.
		Returns:
			bool: True si la conexión es exitosa
		Raises:
			ConnectionError: Si no se puede establecer la conexión
			TimeoutError: Si la conexión excede el tiempo de espera
		"""
		pass

	@abstractmethod
	def provision_service_simple_queue(
		self,
		name: str,
		target: str,
		upload_speed: str,
		download_speed: str
	) -> dict:
		"""
		Configura una cola simple en el router.
		Args:
			name: Nombre de la cola
			target: IP o rango de IPs objetivo
			upload_speed: Velocidad de subida (ej: "1M", "2M")
			download_speed: Velocidad de bajada (ej: "1M", "2M")
		Returns:
			dict: Información de la cola creada
		Raises:
			ValueError: Si los parámetros son inválidos
			ConnectionError: Si hay un error de conexión
		"""
		pass

	@abstractmethod
	def provision_service_pppoe(
		self,
		username: str,
		password: str,
		local_address: str,
		remote_address: str,
		upload_speed: str,
		download_speed: str
	) -> dict:
		"""
		Configura un servicio PPPoE en el router.
		Args:
			username: Nombre de usuario PPPoE
			password: Contraseña PPPoE
			local_address: Dirección IP local
			remote_address: Dirección IP remota
			upload_speed: Velocidad de subida (ej: "1M", "2M")
			download_speed: Velocidad de bajada (ej: "1M", "2M")
		Returns:
			dict: Información del servicio creado
		"""
		pass

	@abstractmethod
	def provision_service_hotspot(
		self,
		username: str,
		password: str,
		limit_uptime: str,
		upload_speed: str,
		download_speed: str
	) -> dict:
		"""
		Configura un usuario de Hotspot en el router.
		Args:
			username: Nombre de usuario
			password: Contraseña
			limit_uptime: Límite de tiempo de uso
			upload_speed: Velocidad de subida (ej: "1M", "2M")
			download_speed: Velocidad de bajada (ej: "1M", "2M")
		Returns:
			dict: Información del usuario creado
		"""
		pass

	@abstractmethod
	def provision_service_pcq(
		self,
		username: str,
		target: str,
		upload_speed: str,
		download_speed: str
	) -> dict:
		"""
		Configura una cola PCQ en el router.
		Args:
			username: Nombre de usuario
			target: IP o rango de IPs objetivo
			upload_speed: Velocidad de subida (ej: "1M", "2M")
			download_speed: Velocidad de bajada (ej: "1M", "2M")
		Returns:
			dict: Información de la cola creada
		"""
		pass

	@abstractmethod
	def provision_service_openvpn(
		self,
		username: str,
		password: str,
		local_address: str,
		remote_address: str
	) -> dict:
		"""
		Configura un cliente OpenVPN en el router.
		Args:
			username: Nombre de usuario
			password: Contraseña
			local_address: Dirección IP local
			remote_address: Dirección IP remota
		Returns:
			dict: Información del cliente creado
		"""
		pass

	@abstractmethod
	def provision_service_l2tp(
		self,
		username: str,
		password: str,
		local_address: str,
		remote_address: str
	) -> dict:
		"""
		Configura un cliente L2TP en el router.
		Args:
			username: Nombre de usuario
			password: Contraseña
			local_address: Dirección IP local
			remote_address: Dirección IP remota
		Returns:
			dict: Información del cliente creado
		"""
		pass

	@abstractmethod
	def disable_service(self, name: str, connection_type: str) -> bool:
		"""
		Deshabilita un servicio en el router.
		Args:
			name: Nombre del servicio
			connection_type: Tipo de conexión (simple-queue, pppoe, hotspot, etc)
		Returns:
			bool: True si se deshabilitó correctamente
		"""
		pass

	@abstractmethod
	def enable_service(self, name: str, connection_type: str) -> bool:
		"""
		Habilita un servicio en el router.
		Args:
			name: Nombre del servicio
			connection_type: Tipo de conexión (simple-queue, pppoe, hotspot, etc)
		Returns:
			bool: True si se habilitó correctamente
		"""
		pass

	@abstractmethod
	def ping(self) -> bool:
		"""
		Verifica si el router responde.
		Returns:
			bool: True si el router responde
		"""
		pass



def mikrotik_client_factory(
	version: str,
	host: str,
	port: int,
	username: str,
	password: str,
	use_ssl: bool = False
) -> MikrotikClient:
	"""
	Factory para crear instancias de clientes Mikrotik según la versión.
	Args:
		version: Versión del router ('v6' o 'v7')
		host: Dirección IP o hostname del router
		port: Puerto API del router
		username: Usuario para autenticación
		password: Contraseña para autenticación
		use_ssl: Si se debe usar SSL para la conexión
	Returns:
		MikrotikClient: Instancia del cliente específico para la versión
	Raises:
		ValueError: Si la versión no es soportada
	"""
	if version == 'v6':
		return MikrotikClientV6(host, port, username, password, use_ssl)
	elif version == 'v7':
		return MikrotikClientV7(host, port, username, password, use_ssl)
	else:
		raise ValueError(f'Unsupported MikroTik version: {version}. Please use "v6" or "v7".')

