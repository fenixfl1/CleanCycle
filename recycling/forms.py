from django import forms

from recycling.models import RecyclingPoints


class RecyclingPointsForm(forms.ModelForm):
    class Meta:
        model = RecyclingPoints
        fields = "__all__"
