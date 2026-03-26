from django.http import HttpResponse
from django.views import View
from app.services.analysis.analysis_methods_service import analysis_methods_service
import json

class AnalysisMethodsView(View):
    def get(self, request):
        data = analysis_methods_service(request)
        response = HttpResponse(json.dumps(data), content_type='application/json')
        return response