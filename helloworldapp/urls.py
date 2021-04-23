from django.urls import path
from helloworldapp.views import HelloWorldView

# url
urlpatterns = [
    path('index/', HelloWorldView.as_view()),
]
