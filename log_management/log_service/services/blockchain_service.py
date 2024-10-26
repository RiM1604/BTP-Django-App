
from web3 import Web3
from eth_account import Account
import hashlib
import json
from django.conf import settings
from .utils import standardize_log_data


class BlockchainService:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(settings.BLOCKCHAIN_NODE_URL))
        self.contract = self.w3.eth.contract(
            address=settings.CONTRACT_ADDRESS,
            abi=settings.CONTRACT_ABI
        )
        self.account = Account.from_key(settings.PRIVATE_KEY)

    def calculate_hash(self, log_entry):
        """Calculate keccak256 hash of log entry"""
        message = standardize_log_data(
            log_entry.log_content,
            log_entry.service_name,
            log_entry.timestamp
        )
        return str(Web3.solidity_keccak(['string'], [message]).hex())

    def store_hash(self, log_hash):
        """Store hash in blockchain"""
        transaction = self.contract.functions.storeLogHash(log_hash).build_transaction({
            'from': self.account.address,
            'nonce': self.w3.eth.get_transaction_count(self.account.address),
        })
        
        signed_txn = self.w3.eth.account.sign_transaction(
            transaction, self.account.key
        )
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return self.w3.to_hex(tx_hash)

    def verify_hash(self, log_hash):
        """Verify hash from blockchain"""
        return self.contract.functions.verifyLogHash(log_hash).call()