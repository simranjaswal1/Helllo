from django.db import models
import uuid

class Ingestion(models.Model):
    PRIORITY_CHOICES = [('HIGH', 'HIGH'), ('MEDIUM', 'MEDIUM'), ('LOW', 'LOW')]

    ingestion_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_status(self):
        statuses = list(self.batches.values_list('status', flat=True))
        if all(s == 'yet_to_start' for s in statuses):
            return 'yet_to_start'
        elif all(s == 'completed' for s in statuses):
            return 'completed'
        else:
            return 'triggered'

class Batch(models.Model):
    STATUS_CHOICES = [('yet_to_start', 'yet_to_start'), ('triggered', 'triggered'), ('completed', 'completed')]

    batch_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    ingestion = models.ForeignKey(Ingestion, related_name='batches', on_delete=models.CASCADE)
    ids = models.JSONField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='yet_to_start')
    created_at = models.DateTimeField(auto_now_add=True)
