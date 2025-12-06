from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import LogoutView


urlpatterns = [
    path('logout/', login_required(LogoutView.as_view(), login_url='/'), name='logout')
]
