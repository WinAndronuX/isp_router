from isp_router.isp_router.api.mikrotik_base import MikrotikBase
from isp_router.isp_router.api.mikrotik_client_v6 import MikrotikClientV6
from isp_router.isp_router.api.mikrotik_client_v7 import MikrotikClientV7



def mikrotik_client_factory(
	version: str,
	host: str,
	port: int,
	username: str,
	password: str,
	use_ssl: bool = False
) -> MikrotikBase:
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

