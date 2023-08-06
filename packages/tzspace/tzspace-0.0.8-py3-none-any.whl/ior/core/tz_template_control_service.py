from web3.logs import DISCARD

from ..config.consts import tz_template_control_path
from ..util.web3_utils import get_abi, contract_instance, func_send_raw_transaction, contract_functions, \
    contract_events


class TZTemplateControlService(object):
    def __init__(self, w3, config):
        self.w3 = w3
        self.config = config
        self.abi = get_abi(tz_template_control_path)
        self.contract_instance = contract_instance(self.w3, self.config.contract_addresses['TZTemplateControl'], self.abi)

    @property
    def functions(self):
        if not self.contract_instance:
            raise RuntimeError("合约获取失败【tz_template_control_contract】")
        return contract_functions(self.contract_instance)

    def indexes_item(self, key):
        """
        合约属性 mapping(address => uint256) public indexes
        :param key:
        :return:
        """
        res = self.functions.indexes(key).call()
        if self.config.is_print:
            print(res)
        return res

    def get_template(self, template_id: int):
        """
        合约方法 getTemplate(uint256 templateId)
        合约放回 (ins.template, ins.name, ins.category, ins.owner, ins.ratio, ins.status)
        :param template_id:
        :return:
        """
        res = self.functions.getTemplate(template_id).call()
        if self.config.is_print:
            print(res)
        return res

    def process_receipt_for(self,event,receipt,key):
        logs = event.process_receipt(receipt)
        if self.config.is_print:
            print(logs)
        key = logs[0]['args'][key]
        return receipt, key

    def register(self, template: str, category: int, name: str, ratio: int, public_key: str, private_key: str) -> int:
        """
        合约方法 register(address template, uint256 category, bytes32 name, uint256 ratio)
        事件返回 TzTemplateRegistered(templateId,ins.owner,ins.template,ins.category)
        :param template:
        :param category:
        :param name:
        :param ratio:
        :param public_key:
        :param private_key:
        :return:
        """
        func = self.functions.register(template, category, name, ratio)
        receipt = func_send_raw_transaction(self.w3, func, public_key, private_key, self.config.timeout, self.config.poll_latency)
        return self.process_receipt_for(contract_events(self.contract_instance).TzTemplateInstanceCreated(),receipt,'templateId')

    def start(self, template_id: int, public_key: str, private_key: str):
        """
        合约方法 end(uint256 templateId)
        事件返回 TzTemplateStateChanged(templateId, ins.owner, ins.status)
        :param template_id:
        :param public_key:
        :param private_key:
        :return:
        """
        func = self.functions.start(template_id)
        receipt = func_send_raw_transaction(self.w3, func, public_key, private_key, self.config.timeout, self.config.poll_latency)
        return self.process_receipt_for(contract_events(self.contract_instance).TzTemplateStateChanged(),receipt,'state')

    def end(self, template_id: int, public_key: str, private_key: str):
        """
        合约方法 end(uint256 templateId)
        事件返回 TzTemplateStateChanged(templateId, ins.owner, ins.status)
        :param template_id:
        :param public_key:
        :param private_key:
        :return:
        """
        func = self.functions.end(template_id)
        receipt = func_send_raw_transaction(self.w3, func, public_key, private_key, self.config.timeout, self.config.poll_latency)
        return self.process_receipt_for(contract_events(self.contract_instance).TzTemplateStateChanged(),receipt,'state')

    def request_template(self, template_id: int, hash_value: str, end_time: int, public_key: str,
                         private_key: str) -> int:
        """
        合约方法 requestTemplate(uint256 templateId, bytes32 hash, uint256 endTime)
        事件返回 TzTemplateInstanceCreated(templateId, ins.template, instanceId, _msgSender(), endTime, hash)
        :param template_id:
        :param hash_value:
        :param end_time:
        :param public_key:
        :param private_key:
        :return:
        """
        hash_bytes = f"{hash_value.encode().hex()}"
        func = self.functions.requestTemplate(template_id, hash_bytes, end_time)
        receipt = func_send_raw_transaction(self.w3, func, public_key, private_key, self.config.timeout, self.config.poll_latency)
        return self.process_receipt_for(contract_events(self.contract_instance).TzTemplateInstanceCreated(),receipt,'instanceId')
        
    def pay(self, template_id: int, instance_id: int, token: str, total_income: int, public_key: str,
            private_key: str) -> dict:
        """
        合约方法 pay(uint256 templateId,uint256 instanceId,address token,uint256 totalIncome)
        事件返回 CommissionPaid(templateId, instanceId, ins.template, _msgSender(), token, totalIncome)
        :param template_id:
        :param instance_id:
        :param token:
        :param total_income:
        :param public_key:
        :param private_key:
        :return:
        """
        func = self.functions.pay(template_id, instance_id, token, total_income)
        receipt = func_send_raw_transaction(self.w3, func, public_key, private_key, self.config.timeout, self.config.poll_latency)
        if self.config.is_print:
            print(receipt)
        return receipt
