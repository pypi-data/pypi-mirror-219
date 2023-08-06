class IORConfig(object):


	# 合约地址
	contract_address = {
	    "RoleControl": "0x6347953b40A12C6E06627Ea9b20E3845Add120dc",
	    "PermissionControl": "0x1146eA73f6df2B4e4383035890Ed4245978CE191",
	    "STCCertificate": "0x9B2c7f3222e483Ff5c563286fE7510497B836007",
	    "DATACertificate": "0x3F1bAcb104F4852cAa12Fd042764191C7eF71d94",
	    "CTCCertificate": "0x3D203807D70a72A27F4eEED56c61e220E51E0a61",
	    "MDCCertificate": "0xeF778EcDbd6D174c70CBf8d5943e10e1053A5565",
	    "GNCCertificate": "0x6603492b0A02C958fD933BdC0dEDe786d11751af",
	    "INFT1Certificate": "0x88Ee1aa55C8eD81DB4366077D65a86Abb440FA54",
	    "TZTemplateControl": "0xec5cac5A170C8c5a96efC0D669A4C15b6D5A7D44",
	    "TZContractTemplate": "0x59400c0ad731d23032B68E6B3f5ac0F8862eb83f",
	    "TZExchange": "0x59400c0ad731d23032B68E6B3f5ac0F8862eb83f"
	}


	def __init__(self, contract_addresses):
        if contract_addresses!=None:
        	self.contract_address = contract_addresses
