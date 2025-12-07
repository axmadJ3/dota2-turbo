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


def about(request):
    context = {
        'title': 'About - Dota 2 Turbo Stats'
    }
    return render(
        request,
        'leaderboard/about.html',
        context=context
    )
