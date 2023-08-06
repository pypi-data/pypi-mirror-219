from ..config.consts import permission_control_path
from ..util.web3_utils import get_abi, contract_instance, func_send_raw_transaction, contract_functions


class PermissionControlService(object):
    def __init__(self, w3, config):
        self.w3 = w3
        self.config = config
        self.abi = get_abi(permission_control_path)
        self.permission_control_contract_instance = contract_instance(self.w3, self.config.contract_addresses['PermissionControl'], self.abi)

    @property
    def functions(self):
        if not self.permission_control_contract_instance:
            raise RuntimeError("合约获取失败【permission_control_contract】")
        return contract_functions(self.permission_control_contract_instance)

    def datas_item(self, key):
        """
        合约属性 mapping(bytes32=>mapping(bytes32 =>TzPermissionData)) public datas
        :param key:
        :return:
        """
        res = self.functions.datas(key).call()
        print(res)
        return res

    def add_permission(self, permission_name: str, data: list[str], operations: list[int],
                       default_operations: list[int], parent: list[int], hash_values: list[str], public_key: str,
                       private_key: str):
        """
        合约方法 addPermission(bytes32 permissionName, bytes32[] calldata data, uint32[] calldata operations,
                uint32[] calldata defaultOperations, bytes32[] calldata parent, bytes32[] calldata hash)
        合约返回 无
        :param permission_name:
        :param data:
        :param operations:
        :param default_operations:
        :param parent:
        :param hash_values:
        :param public_key:
        :param private_key:
        :return:
        """
        permission_name_bytes = f"0x{permission_name.encode().hex()}"
        data_bytes = [f"0x{d.encode().hex()}" for d in data]
        hash_values_bytes = [f"0x{h.encode().hex()}" for h in hash_values]
        func = self.functions.addPermission(permission_name_bytes, data_bytes, operations, default_operations, parent,
                                            hash_values_bytes)
        receipt = func_send_raw_transaction(func, self.w3, private_key, public_key, self.config.timeout, self.config.poll_latency)
        print(receipt)
        return receipt

    def del_permission(self, permission_name: str, data: list[str], public_key: str, private_key: str):
        """
        合约方法 delPermission(bytes32 permissionName, bytes32[] calldata data)
        合约返回 无
        :param permission_name:
        :param data:
        :param public_key:
        :param private_key:
        :return:
        """
        permission_name_bytes = f"0x{permission_name.encode().hex()}"
        data_bytes = [f"0x{d.encode().hex()}" for d in data]
        func = self.functions.delPermission(permission_name_bytes, data_bytes)
        receipt = func_send_raw_transaction(func, self.w3, private_key, public_key, self.config.timeout, self.config.poll_latency)
        print(receipt)
        return receipt

    def check_permission(self, permission_name: str, data: str, operations: int) -> bool:
        """
        合约方法 checkPermission(bytes32 permissionName, bytes32 data, uint32 operations)
        合约返回 bool
        :param permission_name:
        :param data_hash:
        :param operations:
        :return:
        """
        permission_name_bytes = f"0x{permission_name.encode().hex()}"
        data_bytes = f"0x{data.encode().hex()}"
        res = self.functions.checkPermission(permission_name_bytes, data_bytes, operations).call()
        print(res)
        return res
