from django.urls import path
from helloworldapp.views import HelloWorldView
from helloworldapp.views import _get_barcode_data
# url
urlpatterns = [
    path('index/', HelloWorldView.as_view()),
    path('decode/', _get_barcode_data),
]
