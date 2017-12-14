from django import forms

REGISTERING_OPTIONS = (
    ('spex_and_nachspex', 'Spex och Nachspex'),
    ('only_spex', 'Endast Spex'),
    ('only_nachspex', 'Endast Nachspex')
)

STUDENT = (
    ('student', 'Studerande'),
    ('not_student', 'Inte studerande'),
)

class registerForm(forms.Form):
    name = forms.CharField(label="Namn", max_length = 100)
    email = forms.EmailField(label="E-postaddress")
    register_choice = forms.ChoiceField(
        widget = forms.Select,
        choices = REGISTERING_OPTIONS,
        label = "Välj biljettyp",
    )
    student = forms.ChoiceField(
        widget = forms.Select,
        choices = STUDENT,
        label = "Studerande",
        required = False,
    )
    alcoholFree = forms.BooleanField(label ="Alkoholfritt Nachspex", required = False)
    diet = forms.CharField(label="Specialdiet", max_length = 500, required = False)
    avec = forms.CharField(label="Avec", max_length = 100, required = False)
    coupon = forms.CharField(label="Rabattkod", max_length=100, required = False)
    comment = forms.CharField(label="Kommentar eller hälsning", max_length =500, widget=forms.Textarea, required = False)
