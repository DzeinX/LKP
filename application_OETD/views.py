from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def main(request):
    context = {}
    return render(request, 'lkp_logic/main.html', context)
