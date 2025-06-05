from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Ingestion, Batch
from .tasks import process_batch, schedule_batches
from django.http import HttpResponse
class IngestAPIView(APIView):
    def get(self, request):  # <-- Added this method for testing 
        return Response({"message": "GET allowed here for testing."})
    def post(self, request):
        ids = request.data.get("ids", [])
        priority = request.data.get("priority", "MEDIUM").upper()
        ingestion = Ingestion.objects.create(priority=priority)

        for i in range(0, len(ids), 3):
            batch_ids = ids[i:i+3]
            Batch.objects.create(ingestion=ingestion, ids=batch_ids)

        schedule_batches.delay()

        return Response({"ingestion_id": str(ingestion.ingestion_id)})

class StatusAPIView(APIView):
    def get(self, request, ingestion_id):
        ingestion = Ingestion.objects.get(pk=ingestion_id)
        batches = ingestion.batches.all()

        return Response({
            "ingestion_id": str(ingestion.ingestion_id),
            "status": ingestion.get_status(),
            "batches": [
                {
                    "batch_id": str(b.batch_id),
                    "ids": b.ids,
                    "status": b.status
                } for b in batches
            ]
        })


def home_view(request):
    return HttpResponse("Welcome to the Home Page!")
