from django.http import HttpResponse
from django.views import View
import json
from app.services.download.read_download_list_data import read_download_list_data

class DownloadListView(View):

    def get(self, request):
        data = read_download_list_data()
        response = HttpResponse(json.dumps(data), content_type='application/json')
        return response