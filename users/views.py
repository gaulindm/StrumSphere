from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import UserPreference
from django.urls import reverse
from .forms import UserPreferenceForm
from songbook.models import SongFormatting


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')

            messages.success(
                request,
                f'Compte créé pour {username} ! Visitez votre page <a href="{reverse("users:user_preferences")}">Préférences</a> pour personnaliser vos paramètres si vous prévoyez de générer des fichiers PDF avec des diagrammes d\'accords.'
            )

            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html',{'form':form})


@login_required
def user_preferences_view(request):
    user_pref, created = UserPreference.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = UserPreferenceForm(request.POST, instance=user_pref)
        if form.is_valid():
            form.save()
            return render(request, "partials/close_modal.html")  # Close modal after saving
    else:
        form = UserPreferenceForm(instance=user_pref)

    return render(request, "partials/user_preferences_modal.html", {"form": form})
