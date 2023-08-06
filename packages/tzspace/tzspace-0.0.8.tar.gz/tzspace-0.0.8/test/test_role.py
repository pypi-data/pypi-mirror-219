from ior.iorsdk import IORSdk, IORConfig
from ior.util.web3_utils import keccak256,to_text,to_address
from ior.core.tz_contract_template_service import TZContractTemplateService


#main test for example
config = IORConfig()
contract_addresses = {
        "RoleControl": "0x5FbDB2315678afecb367f032d93F642f64180aa3",
        "PermissionControl": "0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512",
	    "TZTemplateControl": "0x2279B7A0a67DB372996a5FaB50D91eAA73d2eBe6",
	    "TZExchange": "0x59400c0ad731d23032B68E6B3f5ac0F8862eb83f"
	}
config.set_contract_addresses(contract_addresses)
#config.set_is_poa(True)
config.set_provider('http://127.0.0.1:8545/')
config.set_is_print(True)
ior = IORSdk(config)
ior.init_service()
print(ior.role)



pub = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"
pk = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"

pub1,pk1 = ior.create_account()
pub2,pk2 = ior.create_account()
pub3,pk3 = ior.create_account()

permission = "AddData"
permissions = [permission]
roleName = "Role1"
adminRoleName = "AdminRole"
permissionRoleName = "PermissionRole"
rolectrl = ior.role
pctrl = ior.permission
permissionContractAddrs = [pctrl.address]

#只需要添加一次
#rolectrl.add_role(roleName,adminRoleName,permissionRoleName,permissions,permissionContractAddrs,pub,pk)

rolectrl.grant_role(adminRoleName,pub1,pub,pk)
rolectrl.grant_role(permissionRoleName,pub2,pub1,pk1)
rolectrl.grant_role(roleName,pub3,pub1,pk1)

permissionAdmin = "AdminRole"
pctrl.grant_role(permissionAdmin,pub2,pub,pk)

permissionAdmin2 = "AdminRole2"
pctrl.grant_role(permissionAdmin2,pub2,pub,pk)

addrs = [pctrl.address]
rolectrl.add_permission(roleName,permissions,addrs,pub2,pk2)


#read 0x01, write 0x02, read and write 0x03
data = ["username","idcard"]
operations = [0x02,0x03]
defaultOperations = [0x01,0x02]
parent = ["1.2.121.1.3.21.2","1.2.121.1.3.21.2"]
dhash = data;

pctrl.add_permission(permission,data,operations,defaultOperations,parent,dhash,pub2,pk2)

data1 = "username"
operation = 0x02
h = rolectrl.check_permission(roleName,permission,data1,operation)
print(h)


data2 = "idcard"
operation2 = 0x02
h = rolectrl.check_permission(roleName,permission,data2,operation2)
print(h)

operation3 = 0x01
h = rolectrl.check_permission(roleName,permission,data2,operation3)
print(h)

rolectrl.del_permission(roleName,[permission],pub2,pk2)

operation4 = 0x01
h = rolectrl.check_permission(roleName,permission,data1,operation4)
print(h)



#addr = to_address(to_text(payee[12:]))