from django.conf import settings
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_GET, require_POST, require_http_methods
import json
from http import HTTPStatus

from telescope.json.agent_json import AgentData, AgentDataBody
from telescope.models import Snapshot, System


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
        agent_data = AgentData()
        agent_data.load(json.loads(request.body))
        print(request.body)
        print(agent_data.errors())
        if not agent_data.valid():
            return JsonResponse(agent_data.errors(), status=HTTPStatus.BAD_REQUEST)
        print(agent_data.value())
        system = System.objects.first()
        if system is None:
            system = System.objects.create(name="a", agent_id="a", agent_secret="a")
        s = Snapshot.objects.create(system=system)
        s.load_json(agent_data.value())
        # except:
        #     return JsonResponse({}, status=HTTPStatus.BAD_REQUEST)
        
        return JsonResponse(agent_data.value())
