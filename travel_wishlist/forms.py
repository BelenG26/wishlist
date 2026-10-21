from django import forms
from .models import Place

class NewPlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ('name', 'visited')

class DateInput(forms.DateInput):
    input_type = 'date' # tell our form the date

class TripReviewForm(forms.ModelForm):
    class Meta: # describing info about the object
        model = Place
        fields = ('notes', 'date_visited', 'photo') # 3 strings
        widgets = {
            'date_visited': DateInput() 
        }