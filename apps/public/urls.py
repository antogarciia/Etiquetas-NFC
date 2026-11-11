from django.urls import path

from . import views

app_name = "public"

urlpatterns = [

    path(
        "t/<str:short_code>/",
        views.tag_detail,
        name="tag_detail",
    ),

]