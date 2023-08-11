from django.urls import include, path

from . import departments, jobpositions, peoples, permissions, configuration

urls = (
    [
        # path(
        #     route="",
        #     view=appcomponents.application.get.page,
        #     name="page",
        # ),
        path("departments/", include(departments.urls)),
        path("jobpositions/", include(jobpositions.urls)),
        path("peoples/", include(peoples.urls)),
        path("permissions/", include(permissions.urls)),
        path("configuration/", include(configuration.urls)),
    ],
    "application",
)
