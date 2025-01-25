from django.conf import settings
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_GET, require_POST, require_http_methods
import json
from http import HTTPStatus

from telescope.json.agent_json import AgentData, AgentDataBody


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
    @csrf_exempt
    def agent_data(request: HttpRequest):
        # try:
        agent_data = AgentDataBody()
        agent_data.load(json.loads(request.body))
        print(agent_data.errors())
        # except:
        #     return JsonResponse({}, status=HTTPStatus.BAD_REQUEST)
        
        return JsonResponse(agent_data.value())
