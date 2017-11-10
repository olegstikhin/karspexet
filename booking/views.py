from django import forms
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from booking.models import *
import datetime, math

from .forms import registerForm

def determine_price(spex, nachspex, student, alcohol_free):
    price = 0
    if spex:
        if student:
            price += 15
        else:
            price += 25
    if nachspex:
        price += 15
    if alcohol_free:
        price -= 3

    return price

# Create your views here.
def form_page_view(request):
    return render(request, "index.html")

def register(request):
# if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = registerForm(request.POST)
        # check whether it's valid:
        if form.is_valid():

            form = form.cleaned_data
            if form['student'] == 'student':
                student = True
            else:
                student = False

            if form['register_choice'] == 'only_spex':
                register_choice = "Endast spex"
                spex = True
                nachspex = False
            elif form['register_choice'] == 'only_nachspex':
                register_choice = "Endast nachspex"
                spex = False
                nachspex = True
            else:
                register_choice = "Spex och nachspex"
                spex = True
                nachspex = True

            price = determine_price(spex, nachspex, student, form['alcoholFree'])

            final_price = price
            coupon_code = form['coupon']
            coupon_valid = False
            if coupon_code != "":
                coupon_entered = True

                if DiscountCode.objects.filter(code=coupon_code).exists(): #Check if a code exists
                    coupon_valid = True
                    coupon = DiscountCode.objects.get(code=form['coupon'])
                    final_price = coupon.price

                else:
                    coupon_valid = False
            else:
                coupon_entered = False

            context = {
                'name': form['name'],
                'email': form['email'],
                'avec': form['avec'],
                'diet': form['diet'],
                'alcohol_free' : form['alcoholFree'],
                'register_choice': register_choice,
                'spex': spex,
                'student': student,
                'nachspex': nachspex,
                'price': price,
                'coupon_valid': coupon_valid,
                'final_price': final_price,
                'coupon_code': coupon_code,
                'coupon_entered': coupon_entered,
                }
            return render(request, 'confirm.html', context)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = registerForm()
    return render(request, 'register.html', {'form': form})

def send(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        spex = request.POST['spex']
        nachspex = request.POST['nachspex']
        coupon = request.POST['coupon']
        alcohol_free = request.POST['alcohol_free']
        avec = request.POST['avec']
        diet = request.POST['diet']
        student = request.POST['student']
        comment = "none"

        price = determine_price(spex, nachspex, student, alcohol_free)

        coupon = None
        if DiscountCode.objects.filter(code=coupon).exists():
            coupon = DiscountCode.objects.get(code=form['coupon'])
            price = coupon.price #update price if a coupon exists
            coupon.used = True
            coupon.save()


        new_participant = Participant(name=name, email=email, spex=spex, nachspex=nachspex, alcoholfree=alcohol_free, diet=diet, avec=avec, comment=comment, discount_code=coupon)
        new_participant.save()
        subject, sender, recipient = 'Anmälan till Kårspexets föreställning', 'Kårspexambassaden <karspex@teknolog.fi>', email
        content = "Tack för din anmälan till Kårspexets Finlandsföreställning den 10 februari.\nVänligen betala " + str(price) + " € till konto FI45 4055 0012 3320 33 (mottagare Kårspexambassaden) med för- och efternamn som meddelande senast 8.2.2017.\n\nMed vänliga hälsningar,\nKårspexambassaden"
        send_mail(subject, content, sender, [email], fail_silently=False)

        return render(request, "thanks.html")
    else:
        return render(request, 'index.html', {'error_message': "Det skedde ett fel, vänligen försök pånytt"})
