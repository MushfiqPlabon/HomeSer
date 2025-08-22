from django import forms
from .models import ClientProfile


class ClientProfileForm(forms.ModelForm):
    class Meta:
        model = ClientProfile
        fields = ('bio', 'profile_picture', 'social_links')
        widgets = {
            'social_links': forms.Textarea(attrs={'rows': 3}),
        }