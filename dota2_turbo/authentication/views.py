from django.views import View
from django.contrib.auth.views import logout
from django.shortcuts import redirect

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('leaderboard:leaderboard')
