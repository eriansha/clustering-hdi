from django import forms
from .models import STDBSCAN

class STDBSCANParam(forms.ModelForm):

	class Meta:
		model = STDBSCAN
		fields = ('IPM_file', 'eps1', 'eps2', 'minPts', 'de')