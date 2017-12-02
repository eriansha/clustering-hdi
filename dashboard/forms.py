from django import forms
from .models import Parameters

class PostParam(forms.ModelForm):

	class Meta:
		model = Parameters
		fields = ('eps1', 'eps2', 'minPts', 'de')