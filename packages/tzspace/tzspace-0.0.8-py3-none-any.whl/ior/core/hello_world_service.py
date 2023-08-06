from ..config.consts import provider, hello_world_path
from ..util.web3_utils import get_web3, get_abi, contract_instance, contract_functions


class HelloWorldService(object):

    def __init__(self, w3, address):
        self.w3 = get_web3(provider, True)
        self.abi = get_abi(hello_world_path)
        self.hello_world_contract_instance = contract_instance(self.w3, address, self.abi)

    @property
    def functions(self):
        if not self.hello_world_contract_instance:
            raise RuntimeError("合约获取失败【hello_world_contract】")
        return contract_functions(self.hello_world_contract_instance)

    def hello(self) -> str:
        """
        hello 沒有写操作
        :return:
        """
        return self.functions.hello().call()

    def say_hi(self, name: str) -> str:
        """
        say_hi 沒有写操作
        :param name:
        :return:
        """
        return self.functions.sayHi(name).call()

    def str_concat(self, s1: str, s2: str) -> str:
        """
        strConcat沒有写操作
        :param s1:
        :param s2:
        :return:
        """
        return self.functions.strConcat(s1, s2).call()

    def num_expand(self, num: int) -> str:
        """
        numExpand 沒有写操作
        :param num:
        :return:
        """
        return self.functions.numExpand(num).call()
