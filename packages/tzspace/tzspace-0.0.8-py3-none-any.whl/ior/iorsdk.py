
from .util.web3_utils import get_web3, create_account
from .core.tz_template_control_service import TZTemplateControlService
from .core.certificate_service import CertificateService
from .core.permission_control_service import PermissionControlService
from .core.role_control_service import RoleControlService
from .core.tz_contract_template_service import TZContractTemplateService
from .core.exchange_service import ExchangeService


from hexbytes import (
    HexBytes,
)

class IORConfig(object):


	# 合约地址
	contract_addresses = {
	    "RoleControl": "0x6347953b40A12C6E06627Ea9b20E3845Add120dc",
	    "PermissionControl": "0x1146eA73f6df2B4e4383035890Ed4245978CE191",	    
	    "TZTemplateControl": "0xec5cac5A170C8c5a96efC0D669A4C15b6D5A7D44",
	    "TZExchange": "0x59400c0ad731d23032B68E6B3f5ac0F8862eb83f"
	}


	default_service_contract_addresses={
		"STCCertificate": "0x9B2c7f3222e483Ff5c563286fE7510497B836007",
		"DATACertificate": "0x3F1bAcb104F4852cAa12Fd042764191C7eF71d94",
		"CTCCertificate": "0x3D203807D70a72A27F4eEED56c61e220E51E0a61",
		"MDCCertificate": "0xeF778EcDbd6D174c70CBf8d5943e10e1053A5565",
		"GNCCertificate": "0x6603492b0A02C958fD933BdC0dEDe786d11751af",
		"INFT1Certificate": "0x88Ee1aa55C8eD81DB4366077D65a86Abb440FA54",

		"TZContractTemplate": "0x59400c0ad731d23032B68E6B3f5ac0F8862eb83f"
	}


	# 连接地址
	provider = "https://data-seed-prebsc-2-s3.binance.org:8545/"

	is_poa = False

	is_print = False

	timeout = 10000 #ms
	poll_latency = 10000 #ms

	def __init__(self):
		None

	def set_contract_addresses(self, contract_addresses):
		if contract_addresses!=None:
			self.contract_addresses = contract_addresses

	def set_default_service_contract_addresses(self, contract_addresses):
		if contract_addresses!=None:
			self.default_service_contract_addresses = contract_addresses

	def set_provider(self, provider):
		self.provider = provider

	def set_is_poa(self, is_poa):
		self.is_poa = is_poa

	def set_is_print(self, is_print):
		self.is_print = is_print
		

class IORSdk(object):

	services = {}

	def __init__(self, config):
		self._config = config
		self._w3 = get_web3(config.provider, self._config.is_print, self._config.is_poa)

		self.services['tempctrl'] = TZTemplateControlService(self._w3, self._config)
		self.services['permission'] = PermissionControlService(self._w3, self._config)
		self.services['role'] = RoleControlService(self._w3, self._config)
		self.services['exchange'] = ExchangeService(self._w3, self._config)

	def init_service(self):
		self.registerService('stcc',CertificateService(self._w3, self._config, self._config.default_service_contract_addresses['STCCertificate']))
		self.registerService('datac',CertificateService(self._w3, self._config, self._config.default_service_contract_addresses['DATACertificate']))
		self.registerService('ctcc',CertificateService(self._w3, self._config, self._config.default_service_contract_addresses['CTCCertificate']))
		self.registerService('mdcc',CertificateService(self._w3, self._config, self._config.default_service_contract_addresses['MDCCertificate']))
		self.registerService('gncc',CertificateService(self._w3, self._config, self._config.default_service_contract_addresses['GNCCertificate']))
		self.registerService('inft1',CertificateService(self._w3, self._config, self._config.default_service_contract_addresses['INFT1Certificate']))
		if 'TZContractTemplate' in self._config.default_service_contract_addresses:
			self.registerService('contract1',TZContractTemplateService(self._w3, self._config, self._config.default_service_contract_addresses['TZContractTemplate']))

	@property
	def w3(self):
		return self._w3
	@property
	def config(self):
		return self._config

	@property
	def tempctrl(self):
		return self.services['tempctrl']
	@property
	def permission(self):
		return self.services['permission']
	@property
	def role(self):
		return self.services['role']
	@property
	def exchange(self):
		return self.services['exchange']
    

	def registerService(self, name, service):
		if name not in self.services:
			self.services[name] = service
		else:
			raise RuntimeError("合约已经存在:"+name)

	def set(self, name, service):
		self.services[name] = service

	def remove(self, name):
		self.services[name] = None

	def get(self, name):
		return self.services[name]

	def create_account(self):
		return create_account(self.w3)
