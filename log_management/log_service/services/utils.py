from datetime import datetime
import json

def standardize_log_data(log_content, service_name, timestamp):
    """
    Standardize log data format for consistent hashing
    """
    # Convert timestamp to ISO format if it's a datetime object
    if isinstance(timestamp, datetime):
        timestamp = timestamp.isoformat()
    
    # Ensure consistent string formatting
    log_data = {
        'log_content': str(log_content).strip(),
        'service_name': str(service_name).strip(),
        'timestamp': str(timestamp).strip()
}
    
    # Create deterministic JSON string
    return json.dumps(log_data, sort_keys=True)
