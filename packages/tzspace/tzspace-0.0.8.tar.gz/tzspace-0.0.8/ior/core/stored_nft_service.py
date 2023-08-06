from ..config.consts import stored_nft_path
from ..util.web3_utils import get_abi, contract_instance, func_send_raw_transaction


class StoredNFTService(object):
    def __init__(self, w3, config, address):
        self.w3 = w3
        self.config = config

        self.abi = get_abi(stored_nft_path)

    def get_nft_instance(self, address):
        return contract_instance(self.w3, address, self.abi)

    def update_base_uri(self, nft_address: str, uri: str, public_key: str, private_key: str):
        instance = self.get_nft_instance(nft_address)
        func = instance.functions.updateBaseUri(uri)
        receipt = func_send_raw_transaction(self.w3, func, public_key, private_key, self.config.timeout, self.config.poll_latency)
        print(receipt)

    def update_hash(self, nft_address: str, token_id: int, hash_value: str, public_key: str, private_key: str):
        hash_bytes = f"0x{hash_value.encode().hex()}"
        instance = self.get_nft_instance(nft_address)
        func = instance.functions.updateHash(token_id, hash_bytes)
        receipt = func_send_raw_transaction(self.w3, func, public_key, private_key, self.config.timeout, self.config.poll_latency)
        print(receipt)

    def verify_hash(self, nft_address: str, token_id: str, hash_value: str) -> bool:
        hash_bytes = f"0x{hash_value.encode().hex()}"
        res = self.get_nft_instance(nft_address).functions.verifyHash(token_id, hash_bytes).call()
        print(res)
        return res

    def verify_owner(self, nft_address, token_id: int, who_address: str) -> bool:
        res = self.get_nft_instance(nft_address).functions.verifyOwner(token_id, who_address).call()
        print(res)
        return res
