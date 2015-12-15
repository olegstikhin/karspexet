from django import forms
from django.core.mail import send_mail
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
        spex = request.POST.get('spex', False)
        nachspex = request.POST.get('nachspex', False)
        student_str = request.POST.get('student', False)
        student = (student_str != "normal")
        alcoholfree = request.POST.get('alcoholfree', False)
        diet = request.POST['diet']
        comment = request.POST['comment']
        new_participant = Participant(name=name, email=email, spex=spex, nachspex=nachspex, student=student, alcoholfree=alcoholfree, diet=diet, comment=comment)
        new_participant.save()
        subject, sender, recipient = 'Anmälan till Kårspexets föreställning', 'Kårspexambassaden <karspex@teknolog.fi>', email
        if spex:
            if student:
                sum = 15
            else:
                sum = 25
            if nachspex:
                sum += 15
        else:
            if nachspex:
                sum = 18
            else:
                return HttpResponse("<p>Du har inte valt varken föreställningen eller nachspexet.</p><p><a href='./'>Tillbaka</a></p>")
        content = "Tack för din anmälan till Kårspexets Finlandsföreställning den 20 februari.\nVänligen betala " + str(sum) + " € till konto FI13 1309 3000 0570 75.\n\nMed vänliga hälsningar,\nKårspexambassaden"
        send_mail(subject, content, sender, [email], fail_silently=False)
        return render(request, "index.html")
    else:
        return render(request, "index.html")
