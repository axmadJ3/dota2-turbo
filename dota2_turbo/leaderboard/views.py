from django.shortcuts import render


def leaderboard(request):
    return render(
        request,
        'leaderboard/leaderboard.html',
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
