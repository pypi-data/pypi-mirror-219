from ..config.consts import  exchange_path
from ..util.web3_utils import get_abi, contract_instance, contract_functions, func_send_raw_transaction


class ExchangeService(object):

    def __init__(self, w3, config):
        self.w3 = w3
        self.config = config
        self.abi = get_abi(exchange_path)
        self.exchange_contract_instance = contract_instance(self.w3, self.config.contract_addresses['TZExchange'], self.abi)

    @property
    def functions(self):
        if not self.exchange_contract_instance:
            raise RuntimeError("合约获取失败【exchange_contract】")
        return contract_functions(self.exchange_contract_instance)

    def exchange(self, cert_address: str, token_id: int, from_address: str, to_address: str, price: int, public_key: str,
                 private_key: str):
        func = self.functions.exchange(cert_address, token_id, from_address, to_address, price)
        receipt = func_send_raw_transaction(self.w3, func, public_key, private_key, self.config.timeout, self.config.poll_latency)
        #print(receipt)
        return receipt

    def exchange_with_feed(self, cert_address: str, token_id: int, from_address: str, to_address: str, price: int,
                           fee: int, feeds: list[str], percents: list[int], public_key: str, private_key: str):
        func = self.functions.exchangeWithFeed(cert_address, token_id, from_address, to_address, price, fee, feeds,
                                               percents)
        receipt = func_send_raw_transaction(self.w3, func, public_key, private_key, self.config.timeout, self.config.poll_latency)
        #print(receipt)
        return receipt
