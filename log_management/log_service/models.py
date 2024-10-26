from django.db import models

# Create your models here.
class LogEntry(models.Model):
    timestamp = models.DateTimeField()
    service_name = models.CharField(max_length=100)
    log_content = models.TextField()
    log_hash = models.CharField(max_length=66)  # For storing Ethereum keccak256 hash
    blockchain_tx_hash = models.CharField(max_length=66, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


    def to_dict(self):
        """Convert model instance to JSON-serializable dictionary"""
        return {
            'id': str(self.id),
            'timestamp': self.timestamp.isoformat(),
            'service_name': self.service_name,
            'log_content': self.log_content,
            'log_hash': self.log_hash,
            'blockchain_tx_hash': self.blockchain_tx_hash,
            'is_verified': self.is_verified,
            'created_at': self.created_at.isoformat()
        }

    class Meta:
        indexes = [
            models.Index(fields=['timestamp']),
            models.Index(fields=['service_name']),
        ]