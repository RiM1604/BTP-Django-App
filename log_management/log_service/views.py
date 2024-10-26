from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import LogEntrySerializer, LogQuerySerializer, LogIngestionSerializer
from .services.log_ingestion_service import LogIngestionService
from .services.validation_service import ValidationService
from .tasks import process_log_ingestion
import requests
from django.shortcuts import render
from django.contrib import messages
from .forms import IngestLogForm, QueryLogsForm
import json



def log_management(request):
    ingest_form = IngestLogForm()
    query_form = QueryLogsForm()
    query_results = None
    
    if request.method == 'POST':
        if 'ingest_log' in request.POST:
            form = IngestLogForm(request.POST)
            if form.is_valid():
                data = {
                    'timestamp': form.cleaned_data['timestamp'].isoformat(),
                    'service_name': form.cleaned_data['service_name'],
                    'log_content': form.cleaned_data['log_content']
                }
                try:
                    response = requests.post(
                        'http://localhost:8000/api/logs/ingest_log/',
                        json=data,
                        headers={'Content-Type': 'application/json'}
                    )
                    messages.success(request,response.status_code)
                    if response.status_code == 200:
                        messages.success(request, 'Log ingested successfully!')
                    else:
                        messages.error(request, f'Error ingesting log: {response.text}')
                except requests.RequestException as e:
                    messages.error(request, f'Error connecting to the API: {str(e)}')
        
        elif 'query_logs' in request.POST:
            form = QueryLogsForm(request.POST)
            if form.is_valid():
                data = {
                    'start_time': form.cleaned_data['start_time'].isoformat(),
                    'end_time': form.cleaned_data['end_time'].isoformat(),
                }
                if form.cleaned_data['service_name']:
                    data['service_name'] = form.cleaned_data['service_name']
                try:
                    response = requests.post(
                        'http://localhost:8000/api/logs/query_logs/',
                        json=data,
                        headers={'Content-Type': 'application/json'}
                    )
                    if response.status_code == 200:
                        query_results = response.json()
                    else:
                        messages.error(request, f'Error querying logs: {response.text}')
                except requests.RequestException as e:
                    messages.error(request, f'Error connecting to the API: {str(e)}')
    
    return render(request, 'log_service/log_management.html', {
        'ingest_form': ingest_form,
        'query_form': query_form,
        'query_results': query_results
    })




class LogManagementViewSet(viewsets.ViewSet):
    # permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.validation_service = ValidationService()
        self.ingestion_service = LogIngestionService()
    
    @action(detail=False, methods=['POST'])
    def reply_back(self, request):
        return Response({"status": "Hello there you api is working!"}, 
                          status=status.HTTP_202_ACCEPTED)

    @action(detail=False, methods=['POST'])
    def ingest_log(self, request):
        serializer = LogIngestionSerializer(data=request.data)
        if serializer.is_valid():
            # Convert validated data to JSON-serializable format
            # data = serializer.validated_data
            # Ensure timestamp is in ISO format
            # data["timestamp"] = data["timestamp"].isoformat()
            # return Response(data)
            
            # Queue log processing in Celery
            # task = process_log_ingestion.delay(data["timestamp"],data["service_name"],data["log_content"])
            task = process_log_ingestion.delay(**serializer.validated_data) 
            
            return Response({
                "status": "Log queued for processing",
                "task_id": task.id
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def query_logs(self, request):
        serializer = LogQuerySerializer(data=request.data)
        if serializer.is_valid():
            logs = self.validation_service.query_logs(**serializer.validated_data)
            return Response(logs)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)