from celery import shared_task
from .services.log_ingestion_service import LogIngestionService
import logging

logger = logging.getLogger(__name__)

@shared_task
def process_log_ingestion(timestamp, service_name, log_content):
    try:
        ingestion_service = LogIngestionService()
        result = ingestion_service.ingest_log(
            timestamp=timestamp,
            service_name=service_name,
            log_content=log_content
        )
        # Convert to dict before returning
        return result.to_dict() if result else None
    except Exception as exc:
        logger.error(f"Error processing log: {str(exc)}", exc_info=True)