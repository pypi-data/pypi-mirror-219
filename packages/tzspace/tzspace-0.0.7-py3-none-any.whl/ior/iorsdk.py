
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

		self.registerService('contract1',TZContractTemplateService(self._w3, self._config, self._config.default_service_contract_addresses['TZContractTemplate']))

	@property
	def w3(self):
		return self._w3

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
