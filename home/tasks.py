from celery import shared_task
from .models import Batch
import time

@shared_task
def process_batch(batch_id):
    batch = Batch.objects.get(batch_id=batch_id)
    if batch.status == 'completed':
        return
    batch.status = 'triggered'
    batch.save()

    for id in batch.ids:
        time.sleep(1)  # simulate external API
        print(f"Fetched data for ID {id}")
        
    batch.status = 'completed'
    batch.save()

@shared_task
def schedule_batches():
    from .models import Batch
    waiting = Batch.objects.filter(status='yet_to_start').select_related('ingestion') \
        .order_by('-ingestion__priority', 'created_at')[:1]  # limit: 1 batch per schedule

    if waiting:
        batch = waiting[0]
        process_batch.apply_async((str(batch.batch_id),), countdown=5)  # enforce 5-second delay
