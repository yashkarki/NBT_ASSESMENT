from django.urls import path
from .views import IndexPage

urlpatterns = [
    path('', IndexPage, name="index_func"),
    # path('convert', ConvertIntoInterval, name="convertData"),
]
