from django.shortcuts import render


# Create your views here.
def form_page_view(request):
    return render(request, "index.html")