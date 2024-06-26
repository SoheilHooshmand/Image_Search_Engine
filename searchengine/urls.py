from django.urls import path
from .views import AddData, Search

urlpatterns = [
    path("upload-json-file/", AddData.as_view(), name="uploadJsonFile"),
    path("search/", Search.as_view(), name="search")
]