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
default_contract_addresses = {        
        "STCCertificate": "0x9fE46736679d2D9a65F0992F2272dE9f3c7fa6e0",
        "DATACertificate": "0xCf7Ed3AccA5a467e9e704C703E8D87F634fB0Fc9",
        "CTCCertificate": "0xDc64a140Aa3E981100a9becA4E685f962f0cF6C9",
        "MDCCertificate": "0x5FC8d32690cc91D4c39d9d3abcBD16989F875707",
        "GNCCertificate": "0x0165878A594ca255338adfa4d48449f69242Eb8F",
        "INFT1Certificate": "0xa513E6E4b8f2a923D98304ec87F64353C4D5C853"
}
config.set_contract_addresses(contract_addresses)
config.set_default_service_contract_addresses(default_contract_addresses)
#config.set_is_poa(True)
config.set_provider('http://127.0.0.1:8545/')
config.set_is_print(True)
ior = IORSdk(config)
ior.init_service()

cert = ior.get('stcc')

pub = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"
pk = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"

pub1,pk1 = ior.create_account()
pub2,pk2 = ior.create_account()
pub3,pk3 = ior.create_account()

_,tokenId = cert.mint(pub,pub,pk)
cert.set_authorize_approval(tokenId,pub1,True,pub,pk)
h = cert.is_authorize_approved(tokenId,pub1)
print(h)

mp = cert.token_id_mapping_item(tokenId)
print(mp)
_,nId=cert.authorize(pub2,tokenId,pub1,pk1)
mp = cert.token_id_mapping_item(tokenId)
print(mp)

cert.safeTransferFrom(pub2,pub3,nId,pub2,pk2)

#addr = to_address(to_text(payee[12:]))