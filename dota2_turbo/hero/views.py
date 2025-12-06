from django.shortcuts import render


def heroes(request):
    context = {
        'title': 'Heroes - Dota 2 Turbo Stats'
    }
    return render(
        request,
        'hero/heroes.html',
        context=context 
    )
