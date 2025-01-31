import logging

from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET, require_http_methods

from telescope.models import System

_logger = logging.getLogger("telescope")

class SystemViews:

    @require_GET
    def index(request: HttpRequest):
        context = {
            "systems": System.objects.all().order_by("name").prefetch_related("snapshots")
        }
        return render(request, "telescope/system/index.html", context)

    @require_http_methods(["GET", "POST"])
    def add(request: HttpRequest):
        match request.method:
            case "GET":
                return render(request, "telescope/system/add.html")
            case "POST":
                System.objects.create(
                    name=request.POST.get("nickname"),
                    agent_id=request.POST.get("agent_id"),
                    agent_secret=request.POST.get("agent_secret"),
                )
                raise NotImplementedError

    @require_GET
    def view(request: HttpRequest, system_id: int):
        system = System.objects.filter(id=system_id).prefetch_related("snapshots").first()
        if not system:
            raise NotImplementedError
        context = {
            "system": system,
        }
        return render(request, "telescope/system/view.html", context)

    @require_http_methods(["GET", "POST"])
    def edit(request: HttpRequest, system_id: int):
        system = System.objects.filter(id=system_id).prefetch_related("snapshots").first()
        if not system:
            raise NotImplementedError
        match request.method:
            case "GET":
                context = {
                    "system": system,
                }
                return render(request, "telescope/system/edit.html", context)
            case "POST":
                raise NotImplementedError
    
    @require_http_methods(["GET", "POST"])
    def delete(request: HttpRequest , system_id: int):
        system = System.objects.filter(id=system_id).prefetch_related("snapshots").first()
        if not system:
            raise NotImplementedError()
        match request.method:
            case "GET":
                context = {
                    "system": system,
                }
                return render(request, "telescope/system/delete.html", context)
            case "POST":
                raise NotImplementedError
