from django.conf import settings
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_GET, require_POST, require_http_methods
import json
from http import HTTPStatus

class APIViews:
    def index(request: HttpRequest):
        return JsonResponse(
            {
                "version": "0.0.0",
            }
        )

    @require_http_methods(["GET", "POST"])
    def agent_register(request: HttpRequest):
        if len(request.body) > 1024:
            return JsonResponse({}, status=HTTPStatus.REQUEST_ENTITY_TOO_LARGE)
        pass

    @require_POST
    def agent_data(request: HttpRequest):
        pass
