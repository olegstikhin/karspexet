from django import forms
from django.core.validators import validate_email
from django.http import HttpResponse
from django.shortcuts import render
from booking.models import *

# Create your views here.
def form_page_view(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        try:
            validate_email(email)
        except forms.ValidationError:
            return HttpResponse("<p>Din e-postadress är inte giltig, vänligen försök på nytt</p><p><a href='./'>Tillbaka</a></p>")
        discount_code = request.POST['discount_code']
        nachspex = request.POST.get('nachspex', False)
        alcoholfree = request.POST.get('alcoholfree', False)
        diet = request.POST['diet']
        comment = request.POST['comment']
        new_participant = Participant(name=name, email=email, nachspex=nachspex, alcoholfree=alcoholfree, diet=diet, comment=comment)
        new_participant.save()
        return render(request, "index.html")
    else:
        return render(request, "index.html")
