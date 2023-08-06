from ..config.consts import role_control_path
from ..util.web3_utils import get_abi, contract_instance, func_send_raw_transaction, contract_functions


class RoleControlService(object):
    def __init__(self, w3, config):
        self.w3 = w3
        self.config = config
        self.abi = get_abi(role_control_path)
        self.role_control_contract_instance = contract_instance(self.w3, self.config.contract_addresses['RoleControl'], self.abi)

    @property
    def functions(self):
        if not self.role_control_contract_instance:
            raise RuntimeError("合约获取失败【role_control_contract】")
        return contract_functions(self.role_control_contract_instance)

    def roles_item(self, key):
        """
        合约属性 mapping(bytes32 => TzRoleData) public roles
        :param key:
        :return:
        """
        res = self.functions.roles(key).call()
        print(res)
        return res


    def grant_role(self, role_name: str, to: str, public_key: str, private_key: str):

        role_name_bytes = f"0x{role_name.encode().hex()}"
        func = self.functions.grantRole(role_name_bytes, to)
        receipt = func_send_raw_transaction(func, self.w3, private_key, public_key, self.config.timeout, self.config.poll_latency)
        print(receipt)

    def revoke_role(self, role_name: str, to: str, public_key: str, private_key: str):

        role_name_bytes = f"0x{role_name.encode().hex()}"
        func = self.functions.revokeRole(role_name_bytes, to)
        receipt = func_send_raw_transaction(func, self.w3, private_key, public_key, self.config.timeout, self.config.poll_latency)
        print(receipt)

    def has_role(self, role_name: str, to: str):

        role_name_bytes = f"0x{role_name.encode().hex()}"
        res = self.functions.hasRole(role_name_bytes,to).call()
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
        role_name_bytes = f"0x{role_name.encode().hex()}"
        admin_role_bytes = f"0x{admin_role.encode().hex()}"
        permission_role_bytes = f"0x{permission_role.encode().hex()}"
        permissions_bytes = [f"0x{p.encode().hex()}" for p in permissions]
        func = self.functions.addRole(role_name_bytes, admin_role_bytes, permission_role_bytes, permissions_bytes,
                                      permission_contract_addrs)
        receipt = func_send_raw_transaction(func, self.w3, private_key, public_key, self.config.timeout, self.config.poll_latency)
        print(receipt)

    def add_permission(self, role_name, permissions, permission_contract_addrs, public_key, private_key):
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
        role_name_bytes = f"0x{role_name.encode().hex()}"
        permissions_bytes = [p.encode().hex() for p in permissions]
        func = self.functions.addPermission(role_name_bytes, permissions_bytes, permission_contract_addrs)
        receipt = func_send_raw_transaction(func, self.w3, private_key, public_key, self.config.timeout, self.config.poll_latency)
        print(receipt)

    def del_permission(self, role_name, permissions, public_key, private_key):
        """
        合约方法 delPermission(bytes32 roleName, bytes32[] calldata permissions)
        合约返回 无
        :param role_name:
        :param permissions:
        :param public_key:
        :param private_key:
        :return:
        """
        role_name_bytes = f"0x{role_name.encode().hex()}"
        permissions_bytes = [p.encode().hex() for p in permissions]
        func = self.functions.delPermission(role_name_bytes, permissions_bytes)
        receipt = func_send_raw_transaction(func, self.w3, private_key, public_key, self.config.timeout, self.config.poll_latency)
        print(receipt)

    def check_permission(self, role_name, permission_name, data_hash, operations) -> bool:
        """
        合约方法 checkPermission(bytes32 roleName, bytes32 permissionName, bytes32 dataHash, uint32 operations)
        合约返回 bool
        :param role_name:
        :param permission_name:
        :param data_hash:
        :param operations:
        :return:
        """
        role_name_bytes = f"0x{role_name.encode().hex()}"
        permission_name_bytes = f"0x{permission_name.encode().hex()}"
        data_hash_bytes = f"0x{data_hash.encode().hex()}"
        res = self.functions.checkPermission(role_name_bytes, permission_name_bytes, data_hash_bytes, operations).call()
        print(res)
        return res
