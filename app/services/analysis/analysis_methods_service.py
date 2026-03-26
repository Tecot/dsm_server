from django.conf import settings

def analysis_methods_service(request):
    result = {
        'code': 0,
        'data': settings.ANALYSIS_ITEM_MAP
    }
    return result