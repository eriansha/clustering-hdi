from django import forms
from .models import STDBSCAN
from .models import KMeans

class STDBSCANParam(forms.ModelForm):

	class Meta:
		model = STDBSCAN
		fields = ('IPM_file', 'eps1', 'eps2', 'minPts', 'de')

class KmeansParam(forms.ModelForm):

	class Meta:
		model = KMeans
		fields = ('IPM_file', 'k')