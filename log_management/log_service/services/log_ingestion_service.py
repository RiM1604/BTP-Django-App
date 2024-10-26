
from elasticsearch_dsl import Document, Date, Keyword, Text
from elasticsearch_dsl.connections import connections
from .blockchain_service import BlockchainService
from ..models import LogEntry
from elasticsearch.exceptions import NotFoundError
from .utils import standardize_log_data

class LogDocument(Document):
    timestamp = Date()
    service_name = Keyword()
    log_content = Text()
    log_hash = Keyword()

    class Index:
        name = 'logs'


class LogIngestionService:
    def __init__(self):
        self.blockchain_service = BlockchainService()
        connections.create_connection(hosts=['localhost:9200'])
        LogDocument.init()

    def ingest_log(self, timestamp, service_name, log_content):
        # Create Django model instance
        log_entry = LogEntry.objects.create(
            timestamp=timestamp,
            service_name=service_name,
            log_content=log_content
        )

        # Ensure data is standardized before calculating hash
        message = standardize_log_data(log_content, service_name, timestamp)
        log_hash = self.blockchain_service.calculate_hash(log_entry)
        log_entry.log_hash = log_hash
        
        # Store in blockchain
        tx_hash = self.blockchain_service.store_hash(log_hash)
        log_entry.blockchain_tx_hash = tx_hash
        log_entry.save()

        # Index in Elasticsearch with standardized data
        log_doc = LogDocument(
            meta={'id': log_entry.id},
            timestamp=timestamp,
            service_name=str(service_name).strip(),
            log_content=str(log_content).strip(),
            log_hash=log_hash
        )
        log_doc.save()

        try:
            retrieved_doc = LogDocument.get(id=log_entry.id)
            print(f"Document retrieved: {retrieved_doc.to_dict()}")
        except NotFoundError:
            print("Document not found in Elasticsearch.")

        return log_entry