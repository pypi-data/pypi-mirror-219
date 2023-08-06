import os

# 当前根目录
base_path = os.path.dirname(__file__)

# 账户
# https://testnet.bnbchain.org/faucet-smart
# https://faucet.quicknode.com/binance-smart-chain/bnb-testnet
accounts = [
    {
        "private_key": "0xbae01724c159525a2a20570371f83bbc72074225f184ef8a448944f5c861b69b",
        "address": "0xb5A3426f9AB8751B868f9492a56A35ccE8a8dBfb"
    }
]

# abi路径
hello_world_path = os.path.join(base_path, "contracts", "HelloWorld.json")
stored_nft_path = os.path.join(base_path, "contracts", "StoredNFT.json")
exchange_path = os.path.join(base_path, "contracts", "Exchange.json")
certificate_path = os.path.join(base_path, "contracts", "Certificate.json")
tz_template_control_path = os.path.join(base_path, "contracts", "TZTemplateControl.json")
tz_contract_template_path = os.path.join(base_path, "contracts", "TZContractTemplate.json")
role_control_path = os.path.join(base_path, "contracts", "RoleControl.json")
permission_control_path = os.path.join(base_path, "contracts", "PermissionControl.json")


