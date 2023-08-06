from ior.iorsdk import IORSdk, IORConfig
from ior.util.web3_utils import keccak256,to_hex,to_address
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
print(ior.tempctrl)



pub = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"
pk = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"


ior.registerService('contract2',TZContractTemplateService(ior.w3, config
    , '0x8A791620dd6260079BF849Dc5567aDC3F2FdC318'))
contract = ior.get('contract2')

#初始化模板Id
tmp_id = 1
#只需要启动一次
#ior.tempctrl.start(tmp_id, pub,pk)

#注册的结果返回0，需要根据实际结果查看, pub和pk可以是任意用户, 根据模板设计
_,ins_id = ior.tempctrl.request_template(tmp_id,'测试',2669296503, pub,pk)

contract.init(ins_id, ['0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266']
    , '0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266'
    , ['0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266']
    , [10000]
    , pub, pk)

contract.start(ins_id, pub, pk)
contract.sign(ins_id, pub, pk)
contract.end(ins_id, pub, pk)

payees = contract.get_payees(ins_id)
for payee in payees:
    addr = to_address(to_hex(payee[12:]))
    ratio = contract.get_ratio(ins_id, addr)


#data = "你好，世界！"
#data = data.encode("UTF-8")
#print(keccak256(data))