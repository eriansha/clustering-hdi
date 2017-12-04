from django.db import models

# Create your models here.
class Parameters(models.Model):
	IPM_file = models.FileField(upload_to='datasets/', default="")
	eps1 = models.FloatField()
	eps2 = models.FloatField()
	minPts = models.IntegerField()
	de = models.FloatField()