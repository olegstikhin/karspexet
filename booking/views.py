from django import forms
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from booking.models import *
import datetime, math

# Create your views here.
def form_page_view(request):
    return render(request, "index.html")

def confirm(request):
    if request.method == 'POST':
        name = request.POST['name']
        if name == "":
            return HttpResponse("<p>Du har inte angett ditt namn!</p><p><a href='/'>Tillbaka</a></p>")
        email = request.POST['email']
        try:
            validate_email(email)
        except forms.ValidationError:
            return HttpResponse("<p>Din e-postadress är inte giltig, vänligen försök på nytt</p><p><a href='/'>Tillbaka</a></p>")
        spex = request.POST.get('spex', False)
        discount_code = request.POST.get('discount_code', "")
        check = DiscountCode.objects.filter(code=discount_code).count()
        nachspex = request.POST.get('nachspex', False)
        student_str = request.POST.get('student', False)
        student = (student_str != "normal")
        sum = 0
        dc = ""
        if spex:
            spex_answer = "ja"
            if check:
                dc = DiscountCode.objects.get(code=discount_code)
                if dc.used:
                    return HttpResponse("<p>Denna rabattkod har redan använts!</p><p><a href='/'>Tillbaka</a></p>")
                discount_price = dc.price
                sum += discount_price
                spex_answer += " (med rabattkoden: " + str(int(discount_price)) + " €)"
            else:
                if student:
                    spex_answer += ", studerande (15 €)"
                    sum += 15
                else:
                    spex_answer += ", icke-studerande (25 €)"
                    sum += 25
        else:
            spex_answer = "nej"
        alcoholfree = request.POST.get('alcoholfree', False)
        if nachspex:
            nachspex_answer = "ja"
            if alcoholfree:
                nachspex_answer += " (13 €)"
                sum += 13
            else:
                nachspex_answer += " (15 €)"
                sum += 15
        else:
            nachspex_answer = "nej"
        if (not spex) and (not nachspex):
            return HttpResponse("<p>Du har inte valt varken föreställningen eller nachspexet.</p><p><a href='/'>Tillbaka</a></p>")
        if alcoholfree:
            alcoholfree_answer = "ja"
        else:
            alcoholfree_answer = "nej"
        avec = request.POST.get('avec', "")
        diet = request.POST.get('diet', "")
        comment = request.POST.get('comment', "")
        return render_to_response("confirm.html", {'name': name, 'email': email, 'spex_answer': spex_answer, 'nachspex_answer': nachspex_answer, 'alcoholfree_answer': alcoholfree_answer, 'diet': diet, 'avec': avec, 'comment': comment, 'sum': sum, 'dc': dc, }, context_instance=RequestContext(request))
    else:
        return HttpResponse("<p>Fel</p>")

def send(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        try:
            validate_email(email)
        except forms.ValidationError:
            return HttpResponse("<p>Din e-postadress är inte giltig, vänligen försök på nytt</p><p><a href='/'>Tillbaka</a></p>")
        spex = request.POST['spex_answer']
        nachspex = request.POST['nachspex_answer']
        alcoholfree = request.POST['alcoholfree_answer']
        diet = request.POST['diet']
        avec = request.POST['avec']
        comment = request.POST['comment']
        sum = request.POST['sum']
        dc = DiscountCode.objects.filter(code=request.POST['dc']).first()
        subject, sender, recipient = 'Anmälan till Kårspexets föreställning', 'Kårspexambassaden <karspex@teknolog.fi>', email
        content = "Tack för din anmälan till Kårspexets Finlandsföreställning den 25 februari.\nVänligen betala " + sum + " € till konto FI45 4055 0012 3320 33 (mottagare Peter Leander) med för- och efternamn som meddelande senast 24.2.2017.\n\nMed vänliga hälsningar,\nKårspexambassaden"
        send_mail(subject, content, sender, [email], fail_silently=False)
        new_participant = Participant(name=name, email=email, spex=spex, nachspex=nachspex, alcoholfree=alcoholfree, diet=diet, avec=avec, comment=comment, discount_code=dc)
        new_participant.save()
        if dc is not None:
            dc.used = True
            dc.save()
        return render(request, "thanks.html")
    else:
        return HttpResponse("<p>Fel</p>")
