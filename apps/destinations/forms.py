from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Category, Destination, PointsOfInterest


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Απαιτείται έγκυρη διεύθυνση email.')

    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class DestinationForm(forms.ModelForm):
    class Meta:
        model = Destination
        fields = ['title', 'country', 'description', 'cover_image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'cover_image':
                field.widget.attrs['class'] = 'form-control'
            else:
                field.widget.attrs['class'] = 'form-control-file'


class PointOfInterestForm(forms.ModelForm):
    class Meta:
        model = PointsOfInterest
        fields = ['title', 'categories', 'description', 'image', 'price_range', 'latitude', 'longitude']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'image':
                field.widget.attrs['class'] = 'form-control'
            else:
                field.widget.attrs['class'] = 'form-control-file'