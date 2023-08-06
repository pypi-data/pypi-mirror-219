from web3.logs import DISCARD

from ..config.consts import tz_contract_template_path
from ..util.web3_utils import get_abi, contract_instance, func_send_raw_transaction, contract_functions, \
    contract_events


class TZContractTemplateService(object):
    def __init__(self, w3, config, address):
        self.w3 = w3
        self.config = config
        self.abi = get_abi(tz_contract_template_path)
        self.tz_contract_template_contract_instance = contract_instance(self.w3, address, self.abi)

    @property
    def functions(self):
        if not self.tz_contract_template_contract_instance:
            raise RuntimeError("合约获取失败【tz_contract_template_contract】")
        return contract_functions(self.tz_contract_template_contract_instance)

    def create_instance(self, hash_value: str, end_time: int, user: str, public_key: str, private_key: str):
        """
        合约方法 createInstance(bytes32 hash, uint256 endTime, address user)
        合约返回 uint256 insId
        :param hash_value:
        :param end_time:
        :param user:
        :param public_key:
        :param private_key:
        :return:
        """
        hash_bytes = f"{hash_value.encode().hex()}"
        func = self.functions.createInstance(hash_bytes, end_time, user)
        receipt = func_send_raw_transaction(self.w3, func, public_key, private_key, self.config.timeout, self.config.poll_latency)
        print(receipt)
        return receipt

    def init(self, ins_id: int, signatories: list[str], payer: str, payees: list[str],
             share_ratios: list[int], public_key: str, private_key: str):
        """
        合约方法 init(uint256 insId, address[] calldata signatories, address payer, address[] calldata payees, uint256[] calldata shareRatios)
        合约事件 insId, ins.owner, ins.endTime, ins.hash, ins.status
        :param ins_id:
        :param signatories:
        :param payer:
        :param payees:
        :param share_ratios:
        :param public_key:
        :param private_key:
        :return:
        """
        func = self.functions.init(ins_id, signatories, payer, payees, share_ratios)
        receipt = func_send_raw_transaction(self.w3, func, public_key, private_key, self.config.timeout, self.config.poll_latency)
        logs = contract_events(self.tz_contract_template_contract_instance). \
            TzContractStateChanged().process_receipt(receipt, errors=DISCARD)
        res = logs[0]['args']
        print(res)

    def start(self, ins_id: int, public_key: str, private_key: str):
        """
        合约方法 start(uint256 insId)
        合约事件 insId, ins.owner, ins.endTime, ins.hash, ins.status
        :param ins_id:
        :param public_key:
        :param private_key:
        :return:
        """
        func = self.functions.start(ins_id)
        receipt = func_send_raw_transaction(self.w3, func, public_key, private_key, self.config.timeout, self.config.poll_latency)
        logs = contract_events(self.tz_contract_template_contract_instance). \
            TzContractStateChanged().process_receipt(receipt, errors=DISCARD)
        res = logs[0]['args']
        print(res)

    def sign(self, ins_id: int, public_key: str, private_key: str):
        """
        合约方法 sign(uint256 insId)
        合约事件 insId, ins.owner, ins.endTime, ins.hash, ins.status, _msgSender()
        :param ins_id:
        :param public_key:
        :param private_key:
        :return:
        """
        func = self.functions.sign(ins_id)
        receipt = func_send_raw_transaction(self.w3, func, public_key, private_key, self.config.timeout, self.config.poll_latency)
        logs = contract_events(self.tz_contract_template_contract_instance). \
            TzContractSigned().process_receipt(receipt, errors=DISCARD)
        res = logs[0]['args']
        print(res)

    def end(self, ins_id: int, public_key: str, private_key: str):
        """
        合约方法 end(uint256 insId)
        合约事件 insId, ins.owner, ins.endTime, ins.hash, ins.status
        :param ins_id:
        :param public_key:
        :param private_key:
        :return:
        """
        func = self.functions.end(ins_id)
        receipt = func_send_raw_transaction(self.w3, func, public_key, private_key, self.config.timeout, self.config.poll_latency)
        logs = contract_events(self.tz_contract_template_contract_instance). \
            TzContractStateChanged().process_receipt(receipt, errors=DISCARD)
        res = logs[0]['args']
        print(res)

    def can_pay(self, ins_id: int, addr: str) -> bool:
        """
        合约方法 canPay(uint256 insId,address addr)
        合约返回 bool
        :param ins_id:
        :param addr:
        :return:
        """
        res = self.functions.canPay(ins_id, addr).call()
        print(res)
        return res

    def get_payees(self, ins_id: int) -> list[str]:
        """
        合约方法 getPayees(uint256 insId)
        合约返回 bytes32[] memory
        :param ins_id:
        :return:
        """
        res = self.functions.getPayees(ins_id).call()
        print(res)
        return res

    def get_ratio(self, ins_id: int, payee: str) -> int:
        """
        合约方法 getRatio(uint256 insId,address payee)
        合约返回 uint256
        :param ins_id:
        :param payee:
        :return:
        """
        res = self.functions.getRatio(ins_id, payee).call()
        print(res)
        return res
