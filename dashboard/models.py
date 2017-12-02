from django.db import models

# Create your models here.
class Parameters(models.Model):
	#file = forms.FileField()
	eps1 = models.FloatField()
	eps2 = models.FloatField()
	minPts = models.IntegerField()
	de = models.FloatField()