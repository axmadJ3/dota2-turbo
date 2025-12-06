from django.shortcuts import render


def leaderboard(request):
    context = {
        'title': 'Leaderboard - Dota 2 Turbo Stats'
    }
    return render(
        request,
        'leaderboard/leaderboard.html',
        context=context
    )
