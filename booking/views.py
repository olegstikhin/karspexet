from django import forms
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from booking.models import *

# Create your views here.
def form_page_view(request):
    return render(request, "index.html")

def confirm(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        try:
            validate_email(email)
        except forms.ValidationError:
            return HttpResponse("<p>Din e-postadress är inte giltig, vänligen försök på nytt</p><p><a href='./'>Tillbaka</a></p>")
        spex = request.POST.get('spex', False)
        nachspex = request.POST.get('nachspex', False)
        student_str = request.POST.get('student', False)
        student = (student_str != "normal")
        sum = 0
        if spex:
            spex_answer = "ja"
            if student:
                spex_answer += ", studerande (15 €)"
                sum += 15
            else:
                spex_answer += ", icke-studerande (25 €)"
                sum += 25
        else:
            spex_answer = "nej"
        if nachspex:
            nachspex_answer = "ja"
            if spex:
                nachspex_answer += " (15 €)"
                sum += 15
            else:
                nachspex_answer += " (18 €)"
                sum += 18
        else:
            nachspex_answer = "nej"
        if (not spex) and (not nachspex):
            return HttpResponse("<p>Du har inte valt varken föreställningen eller nachspexet.</p><p><a href='./'>Tillbaka</a></p>")
        discount_code = request.POST['discount_code']
        alcoholfree = request.POST.get('alcoholfree', False)
        if alcoholfree:
            alcoholfree_answer = "ja"
        else:
            alcoholfree_answer = "nej"
        diet = request.POST['diet']
        comment = request.POST['comment']
        #subject, sender, recipient = 'Anmälan till Kårspexets föreställning', 'Kårspexambassaden <karspex@teknolog.fi>', email
        #content = "Tack för din anmälan till Kårspexets Finlandsföreställning den 20 februari.\nVänligen betala " + str(sum) + " € till konto FI13 1309 3000 0570 75.\n\nMed vänliga hälsningar,\nKårspexambassaden"
        #send_mail(subject, content, sender, [email], fail_silently=False)
        return render_to_response("confirm.html", {'name': name, 'email': email, 'spex_answer': spex_answer, 'nachspex_answer': nachspex_answer, 'alcoholfree_answer': alcoholfree_answer, 'diet': diet, 'comment': comment, 'sum': sum, })
