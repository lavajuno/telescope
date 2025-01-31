"""
URL configuration for telescope project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import include, path

from telescope.views import APIViews
from telescope.views import SystemViews

urlpatterns = [
    path(
        "api/",
        include(
            [
                path(
                    "",
                    APIViews.index,
                    name="api.index"
                ),
                path(
                    "agent/",
                    include(
                        [
                            path(
                                "data/",
                                APIViews.agent_data,
                                name="api.ingress",
                            )
                        ]
                    )
                )
            ]
        )
    ),
    path(
        "system/",
        include(
            [
                path(
                    "",
                    SystemViews.index,
                    name="system.index",
                ),
                path(
                    "add/",
                    SystemViews.add,
                    name="system.add",
                ),
                path(
                    "<int:system_id>/",
                    SystemViews.view,
                    name="system.view",
                ),
                path(
                    "<int:system_id>/edit/",
                    SystemViews.edit,
                    name="system.edit",
                ),
                path(
                    "<int:system_id>/delete/",
                    SystemViews.delete,
                    name="system.delete",
                ),
            ]
        )
    ),

]
