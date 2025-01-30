from http import HTTPStatus
import json
import logging

from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from telescope.json.agent_json import AgentData
from telescope.models import Snapshot, System

_logger = logging.getLogger("telescope")

class APIViews:
    def index(request: HttpRequest):
        return JsonResponse(
            {
                "version": "0.0.0",
            }
        )

    @require_POST
    @csrf_exempt
    def agent_data(request: HttpRequest):
        try:
            request_json = AgentData()
            request_json.load(json.loads(request.body))
        except Exception as e:
            _logger.debug("Exception: %s", str(e))
            return JsonResponse({}, status=HTTPStatus.BAD_REQUEST)
        if not request_json.valid():
            return JsonResponse(request_json.errors(), status=HTTPStatus.BAD_REQUEST)
        system = __get_system(request_json["agent_id"], request_json["agent_secret"])
        if not system:
            return JsonResponse({}, status=HTTPStatus.FORBIDDEN)
        s = Snapshot.objects.create(system=system)
        s.load_json(request_json.value())
        return JsonResponse({}, status=HTTPStatus.OK)

def __get_system(agent_id: str, agent_secret: str) -> System:
    s = System.objects.filter(id=agent_id).first()
    if s and s.agent_secret == agent_secret:
        return s
    return None
