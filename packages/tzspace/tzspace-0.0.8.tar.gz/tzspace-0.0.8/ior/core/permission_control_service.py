from ..config.consts import permission_control_path
from ..util.web3_utils import get_abi, get_abi_bytecode, contract_instance, func_send_raw_transaction, contract_functions, keccak256
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

class PermissionControlService(object):
    @classmethod
    def deploy_instance(cls, w3, config, public_key: str, private_key: str):
        abi,bytecode = get_abi_bytecode(permission_control_path)
        receipt = func_send_raw_transaction(w3.eth.contract(abi=abi, bytecode=bytecode).constructor()
            , w3, private_key, public_key, config.timeout, config.poll_latency)

        if config.is_print:
            print(receipt)
        return receipt.contractAddress


    def __init__(self, w3, config, address=None):
        self.w3 = w3
        self.config = config
        self.abi = get_abi(permission_control_path)
        
        if address is None:
            self.address = self.config.contract_addresses['PermissionControl']
        else:
            self.address = address
        self.contract_instance = contract_instance(self.w3, self.address, self.abi) 
                     
    @property
    def functions(self):
        if not self.contract_instance:
            raise RuntimeError("合约获取失败【permission_control_contract】")
        return contract_functions(self.contract_instance)

    def datas_item(self, key):
        """
        合约属性 mapping(bytes32=>mapping(bytes32 =>TzPermissionData)) public datas
        :param key:
        :return:
        """
        res = self.functions.datas(key).call()
        if self.config.is_print:
            print(res)
        return res

    @error_handler
    def grant_role(self, role_name: str, to: str, public_key: str, private_key: str):

        role_name_bytes = keccak256(role_name)
        func = self.functions.grantRole(role_name_bytes, to)
        receipt = func_send_raw_transaction(self.w3, func, public_key, private_key, self.config.timeout, self.config.poll_latency)
        if self.config.is_print:
            print(receipt)
        return receipt

    @error_handler
    def revoke_role(self, role_name: str, to: str, public_key: str, private_key: str):

        role_name_bytes = keccak256(role_name)
        func = self.functions.revokeRole(role_name_bytes, to)
        receipt = func_send_raw_transaction(self.w3, func, public_key, private_key, self.config.timeout, self.config.poll_latency)
        if self.config.is_print:
            print(receipt)
        return receipt

    def has_role(self, role_name: str, to: str):

        role_name_bytes = keccak256(role_name)
        res = self.functions.hasRole(role_name_bytes,to).call()
        if self.config.is_print:
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
        permission_name_bytes = keccak256(permission_name)
        data_bytes = [keccak256(d) for d in data]
        parent_bytes = [keccak256(p) for p in parent]
        hash_values_bytes = [keccak256(h) for h in hash_values]
        func = self.functions.addPermission(permission_name_bytes, data_bytes, operations, default_operations, parent_bytes,
                                            hash_values_bytes)
        receipt = func_send_raw_transaction(self.w3, func, public_key, private_key, self.config.timeout, self.config.poll_latency)
        if self.config.is_print:
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
        permission_name_bytes = keccak256(permission_name)
        data_bytes = [keccak256(d) for d in data]
        func = self.functions.delPermission(permission_name_bytes, data_bytes)
        receipt = func_send_raw_transaction(self.w3, func, public_key, private_key, self.config.timeout, self.config.poll_latency)
        if self.config.is_print:
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
        data_bytes = keccak256(data)
        res = self.functions.checkPermission(permission_name_bytes, data_bytes, operations).call()
        if self.config.is_print:
            print(res)
        return res
