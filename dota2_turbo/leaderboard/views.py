from django.shortcuts import render


def leaderboard(request):
    context = {
        'title': 'Leaderboard - Dota 2 Stats Hub'
    }
    return render(
        request,
        'leaderboard/leaderboard.html',
        context=context
    )
