
from elasticsearch_dsl import Search
from elasticsearch_dsl.connections import connections
from .blockchain_service import BlockchainService
from datetime import datetime
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
import json
from web3 import Web3
from .utils import standardize_log_data

class ValidationService:
    def __init__(self):
        self.blockchain_service = BlockchainService()
        connections.create_connection(hosts=['localhost:9200'])

    
    def calculate_hash(self, log_data):
        """Calculate keccak256 hash of log entry"""
        message = standardize_log_data(
            log_data['log_content'],
            log_data['service_name'],
            log_data['timestamp']
        )
        return str(Web3.solidity_keccak(['string'], [message]).hex())

    def query_logs(self, start_time: datetime, end_time: datetime, service_name: str = None):

        start_iso = start_time.isoformat()
        end_iso = end_time.isoformat()

        # return end_iso
        search = Search(index='logs')
        search = search.filter('range', timestamp={
            'gte': start_iso,
            'lte': end_iso,
        })
        if service_name:
            search = search.filter('term', service_name=service_name)

        response = search.execute()
        
        validated_logs = []


        for hit in response:

            # actual log data and its entries
            log_entry_data = {
                'log_content': str(hit.log_content).strip(),
                'service_name': str(hit.service_name).strip(),
                'timestamp': str(hit.timestamp).strip()
            }

            # message in the database entry for debug
            message = standardize_log_data(
                log_entry_data['log_content'],
                log_entry_data['service_name'],
                log_entry_data['timestamp']
            )

            #standardize_log_data returns a string

            #calculate_hash a standard standardize_log_data and hashes on it web3.solidity_keccak(['string',[message]) returns a hex byte we which then converted to 
            calculated_hash = self.calculate_hash(log_entry_data)
            is_valid = self.blockchain_service.verify_hash(calculated_hash)
            
            validated_logs.append({
                'timestamp': hit.timestamp,
                'service_name': hit.service_name,
                'log_content': hit.log_content,
                'is_valid': is_valid,
                'log_hash': hit.log_hash,
                'calculated_hash': calculated_hash,
                'log_entry_data': log_entry_data,
                'message': message
            })

        return validated_logs