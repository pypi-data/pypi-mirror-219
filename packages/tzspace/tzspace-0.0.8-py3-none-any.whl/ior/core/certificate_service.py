
from ..config.consts import certificate_path
from ..util.web3_utils import get_abi, contract_instance, func_send_raw_transaction, contract_functions, \
    contract_events
from hexbytes import HexBytes
import traceback

def error_handler(func):
    def execute(self,*args,**kwargs):
        try:
            return func(self,*args,**kwargs),0
        except:
            msg = traceback.format_exc()
            if self.config.is_print:
                print(msg)
            return f'error:{msg}',1
    return execute

class CertificateService(object):
    @classmethod
    def deploy_instance(cls, w3, config, public_key: str, private_key: str):
        abi,bytecode = get_abi_bytecode(certificate_path)
        receipt = func_send_raw_transaction(w3.eth.contract(abi=abi, bytecode=bytecode).constructor()
            , w3, public_key, private_key, config.timeout, config.poll_latency)

        if config.is_print:
            print(receipt)
        return receipt.contractAddress

    def __init__(self, w3, config, address):
        self.w3 = w3
        self.config = config
        self.address = address
        self.abi = get_abi(certificate_path)
        self.contract_instance = contract_instance(self.w3, address, self.abi)

    @property
    def functions(self):
        if not self.contract_instance:
            raise RuntimeError("合约获取失败【certificate_contract】")
        return contract_functions(self.contract_instance)

    def token_id_mapping_item(self, key):
        """
        合约属性 mapping(uint256 => uint256) public tokenIdMapping
        :param key:
        :return:
        """
        res = self.functions.tokenIdMapping(key).call()
        if self.config.is_print:
            print(res)
        return res

    def recreations_item(self, key):
        """
        合约属性 mapping(uint256 => DataTypes.AuthorizeData) public recreations
        :param key:
        :return:
        """
        res = self.functions.recreations(key).call()
        if self.config.is_print:
            print(res)
        return res

    def process_receipt_for(self,event,receipt,key):
        logs = event.process_receipt(receipt)
        if self.config.is_print:
            print(receipt)
        key = logs[0]['args'][key]
        return receipt, key


    def approve(self, to, token_id, public_key, private_key):
        func = self.functions.approve(to, token_id)
        receipt = func_send_raw_transaction(self.w3, func, public_key, private_key, self.config.timeout, self.config.poll_latency)
        if self.config.is_print:
            print(receipt)
        return receipt

    def set_approve_for_all(self, operator, approved, public_key, private_key):
        func = self.functions.setApprovalForAll(operator, approved)
        receipt = func_send_raw_transaction(self.w3, func, public_key, private_key, self.config.timeout, self.config.poll_latency)
        if self.config.is_print:
            print(receipt)
        return receipt

    def mint(self, to: str, public_key: str, private_key: str):
        """
        合约方法 mint(address to) 【继承】
        方法返回 无
        :param to:
        :param public_key:
        :param private_key:
        :return:
        """
        func = self.functions.mint(to)
        receipt = func_send_raw_transaction(self.w3, func, public_key, private_key, self.config.timeout, self.config.poll_latency)
        return self.process_receipt_for(contract_events(self.contract_instance).Transfer(),receipt,'tokenId')

    def safeTransferFrom(self, fromAddr: str, toAddr: str, tokenId: int, public_key: str, private_key: str):
        """
        合约方法 mint(address to) 【继承】
        方法返回 无
        :param to:
        :param public_key:
        :param private_key:
        :return:
        """
        func = self.functions.safeTransferFrom(fromAddr,toAddr,tokenId)
        receipt = func_send_raw_transaction(self.w3, func, public_key, private_key, self.config.timeout, self.config.poll_latency)
        if self.config.is_print:
            print(receipt)
        return receipt


    def bind_option(self, option, public_key, private_key):
        """
        合约方法 bindOption(address option_)
        合约返回 无
        :param option:
        :param public_key:
        :param private_key:
        :return:
        """
        func = self.functions.bindOption(option)
        receipt = func_send_raw_transaction(self.w3, func, public_key, private_key, self.config.timeout, self.config.poll_latency)
        if self.config.is_print:
            print(receipt)
        return receipt

    def set_authorize_approval(self, token_id, operator, approved, public_key, private_key):
        """
        合约方法 setAuthorizeApproval(uint256 tokenId, address operator, bool approved)
        合约返回 无
        :param token_id:
        :param operator:
        :param approved:
        :param public_key:
        :param private_key:
        :return:
        """
        func = self.functions.setAuthorizeApproval(token_id, operator, approved)
        receipt = func_send_raw_transaction(self.w3, func, public_key, private_key, self.config.timeout, self.config.poll_latency)
        if self.config.is_print:
            print(receipt)
        return receipt

    def is_authorize_approved(self, token_id: int, operator: str) -> bool:
        """
        合约方法 isAuthorizeApproved(uint256 tokenId, address operator)
        合约返回 bool
        :param token_id:
        :param operator:
        :return:
        """
        res = self.functions.isAuthorizeApproved(token_id, operator).call()
        if self.config.is_print:
            print(res)
        return res

    def authorize(self, to: str, original_token_id: int, public_key: str, private_key: str):
        """
        合约方法 authorize(address to, uint256 originalTokenId)
        合约返回 uint256 tokenId
        :param to:
        :param original_token_id:
        :param public_key:
        :param private_key:
        :return:
        """
        func = self.functions.authorize(to, original_token_id)
        receipt = func_send_raw_transaction(self.w3, func, public_key, private_key, self.config.timeout, self.config.poll_latency)
        return self.process_receipt_for(contract_events(self.contract_instance).Transfer(),receipt,'tokenId')

    def create_option(self, to, original_token_id, price, effect_date, public_key, private_key):
        func = self.functions.createOption(to, original_token_id, price, effect_date)
        receipt = func_send_raw_transaction(self.w3, func, public_key, private_key, self.config.timeout, self.config.poll_latency)
        return self.process_receipt_for(contract_events(self.contract_instance).Transfer(),receipt,'tokenId')

    def authorize_option(self, to, original_token_id, option_token_id, public_key, private_key):
        func = self.functions.authorizeOption(to, original_token_id, option_token_id)
        receipt = func_send_raw_transaction(self.w3, func, public_key, private_key, self.config.timeout, self.config.poll_latency)
        return self.process_receipt_for(contract_events(self.contract_instance).Transfer(),receipt,'tokenId')

    def recreate(self, to, ref_token_ids, public_key, private_key):
        func = self.functions.recreate(to, ref_token_ids)
        receipt = func_send_raw_transaction(self.w3, func, public_key, private_key, self.config.timeout, self.config.poll_latency)
        return self.process_receipt_for(contract_events(self.contract_instance).Transfer(),receipt,'tokenId')

    def recreate_in_chain(self, to, certificates, ref_token_ids, public_key, private_key):
        func = self.functions.recreateInChain(to, certificates, ref_token_ids)
        receipt = func_send_raw_transaction(self.w3, func, public_key, private_key, self.config.timeout, self.config.poll_latency)
        return self.process_receipt_for(contract_events(self.contract_instance).Transfer(),receipt,'tokenId')

    def recreate_cross_chain(self, to, chain_ids, certificates, ref_token_ids, public_key, private_key):
        func = self.functions.recreateCrossChain(to, chain_ids, certificates, ref_token_ids)
        receipt = func_send_raw_transaction(self.w3, func, public_key, private_key, self.config.timeout, self.config.poll_latency)
        return self.process_receipt_for(contract_events(self.contract_instance).Transfer(),receipt,'tokenId')

    def update_token_id_mapping(self, token_id, original_token_id, public_key, private_key):
        func = self.functions.updateTokenIdMapping(token_id, original_token_id)
        receipt = func_send_raw_transaction(self.w3, func, public_key, private_key, self.config.timeout, self.config.poll_latency)
        if self.config.is_print:
            print(receipt)
        return receipt

    def token_uri(self, token_id):
        res = self.functions.tokenURI(token_id).call()
        if self.config.is_print:
            print(res)
        return res
