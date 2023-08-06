from ..config.consts import role_control_path
from ..util.web3_utils import get_abi, contract_instance, func_send_raw_transaction, contract_functions, keccak256
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

class RoleControlService(object):
    @classmethod
    def deploy_instance(cls, w3, config, public_key: str, private_key: str):
        abi,bytecode = get_abi_bytecode(role_control_path)
        receipt = func_send_raw_transaction(w3.eth.contract(abi=abi, bytecode=bytecode).constructor()
            , w3, public_key, private_key, config.timeout, config.poll_latency)

        if config.is_print:
            print(receipt)
        return receipt.contractAddress


    def __init__(self, w3, config, address=None):
        self.w3 = w3
        self.config = config
        self.abi = get_abi(role_control_path)

        if address is None:
            self.address = self.config.contract_addresses['RoleControl']
        else:
            self.address = address
        self.contract_instance = contract_instance(self.w3, self.address, self.abi) 

    @property
    def functions(self):
        if not self.contract_instance:
            raise RuntimeError("合约获取失败【role_control_contract】")
        return contract_functions(self.contract_instance)


    
    def roles_item(self, key):
        """
        合约属性 mapping(bytes32 => TzRoleData) public roles
        :param key:
        :return:
        """
        res = self.functions.roles(key).call()
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

    def add_role(self, role_name: str, admin_role: str, permission_role: str, permissions: list[str],
                 permission_contract_addrs: list[str], public_key: str, private_key: str):
        """
        合约方法 addRole(bytes32 roleName, bytes32 adminRole, bytes32 permissionRole,
                            bytes32[] calldata permissions, address[] calldata permissionContractAddrs)
        合约返回 无
        :param role_name:
        :param admin_role:
        :param permission_role:
        :param permissions:
        :param permission_contract_addrs:
        :param public_key:
        :param private_key:
        :return:
        """
        role_name_bytes = keccak256(role_name)
        admin_role_bytes = keccak256(admin_role)
        permission_role_bytes = keccak256(permission_role)
        permissions_bytes = [keccak256(p) for p in permissions]
        func = self.functions.addRole(role_name_bytes, admin_role_bytes, permission_role_bytes, permissions_bytes,
                                      permission_contract_addrs)
        receipt = func_send_raw_transaction(self.w3, func, public_key, private_key, self.config.timeout, self.config.poll_latency)
        if self.config.is_print:
            print(receipt)
        return receipt

    def add_permission(self, role_name: str, permissions: list[str], permission_contract_addrs: list[str],
                public_key: str, private_key: str):
        """
        合约方法 addPermission(bytes32 roleName, bytes32[] calldata permissions, address[] calldata permissionContractAddrs)
        合约返回 无
        :param role_name:
        :param permissions:
        :param permission_contract_addrs:
        :param public_key:
        :param private_key:
        :return:
        """
        role_name_bytes = keccak256(role_name)
        permissions_bytes = [keccak256(p) for p in permissions]
        func = self.functions.addPermission(role_name_bytes, permissions_bytes, permission_contract_addrs)
        receipt = func_send_raw_transaction(self.w3, func, public_key, private_key, self.config.timeout, self.config.poll_latency)
        if self.config.is_print:
            print(receipt)
        return receipt

    def del_permission(self, role_name: str, permissions: list[str], public_key: str, private_key: str):
        """
        合约方法 delPermission(bytes32 roleName, bytes32[] calldata permissions)
        合约返回 无
        :param role_name:
        :param permissions:
        :param public_key:
        :param private_key:
        :return:
        """
        role_name_bytes = keccak256(role_name)
        permissions_bytes = [keccak256(p) for p in permissions]
        func = self.functions.delPermission(role_name_bytes, permissions_bytes)
        receipt = func_send_raw_transaction(self.w3, func, public_key, private_key, self.config.timeout, self.config.poll_latency)
        if self.config.is_print:
            print(receipt)
        return receipt

    def check_permission(self, role_name: str, permission_name: str, data: str, operations: int) -> bool:
        """
        合约方法 checkPermission(bytes32 roleName, bytes32 permissionName, bytes32 dataHash, uint32 operations)
        合约返回 bool
        :param role_name:
        :param permission_name:
        :param data:
        :param operations:
        :return:
        """
        role_name_bytes = keccak256(role_name)
        permission_name_bytes = keccak256(permission_name)
        data_bytes = keccak256(data)
        res = self.functions.checkPermission(role_name_bytes, permission_name_bytes, data_bytes, operations).call()
        if self.config.is_print:
            print(res)
        return res
