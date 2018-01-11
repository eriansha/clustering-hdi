from django.db import models
from dashboard.stdbscan import *
from dashboard.kmeans import *
import numpy as np
import pandas as pd
from sklearn.metrics import silhouette_score

# Create your models here.
class STDBSCAN(models.Model):
	IPM_file = models.FileField(upload_to='datasets/', default="")
	eps1 = models.FloatField()
	eps2 = models.FloatField()
	minPts = models.IntegerField()
	de = models.FloatField()

	def getKab(self, dataset):
		dataset_ipm_jawa = np.genfromtxt(dataset, delimiter=',', skip_header=1, dtype='U')
		kab_ipm = dataset_ipm_jawa[:,0]

		return kab_ipm

	def run_stdbscan(self):
		load_data = self.IPM_file
		dataset_ipm_jawa = np.genfromtxt(load_data, delimiter=',', skip_header=1)
		dataset_ipm_jawa = np.delete(dataset_ipm_jawa, 0, 1)

		result = st_dbscan(dataset_ipm_jawa, self.eps1, self.eps2, self.minPts, self.de)

		return result

	def resultToJson(self):

		kab_ipm = self.getKab(self.IPM_file)
		result = self.run_stdbscan()

		df_kab = pd.DataFrame(kab_ipm, columns=['kabupaten'])
		df_result = pd.DataFrame(result, columns =['longitude', 'latitude', 'tahun', 'ipm', 'cluster'])

		df = pd.concat((df_kab, df_result), axis=1)

		return df.to_json(orient='split')

	def stdbscan_score(self):
		# calculate Silhoutte Coeffecient
		result = self.run_stdbscan()
		score = silhouette_score(result[:,:4], result[:,4])

		return score

class KMeans(models.Model):
	IPM_file = models.FileField(upload_to='datasets/', default="")
	k = models.IntegerField()

	def run_kmeans(self):
		load_data = self.IPM_file
		dataset_ipm_jawa = np.genfromtxt(load_data, delimiter=',', skip_header=1)
		dataset_ipm_jawa = np.delete(dataset_ipm_jawa, 0, 1)

		result = kmeans(dataset_ipm_jawa, self.k)

		return result

	def resultToJson(self):
		df_dataset = pd.read_csv(self.IPM_file)
		df_result = pd.DataFrame(self.run_kmeans(), columns =['cluster'])

		df = pd.concat((df_dataset, df_result+1), axis=1)

		return df.to_json(orient='split')

	def kmeans_score(self):
		load_data = self.IPM_file
		dataset_ipm_jawa = np.genfromtxt(load_data, delimiter=',', skip_header=1)
		dataset_ipm_jawa = np.delete(dataset_ipm_jawa, 0, 1)
		result = self.run_kmeans()

		score = silhouette_score(dataset_ipm_jawa, result.ravel())

		return score
