from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import STDBSCAN
from .forms import STDBSCANParam

from .models import KMeans
from .forms import KmeansParam

from django.conf import settings
from django.core.files.storage import FileSystemStorage
# Create your views here.

def menu(request):
	return render(request, 'dashboard/parameters/index.html')

def choose_algo(request):
	return render(request, 'dashboard/parameters/choose_algo.html')

# ST-DBSCAN
def stdbscan_input(request):
	if request.method == 'POST':
		form = STDBSCANParam(request.POST, request.FILES)
		if form.is_valid():
			STDBSCAN.objects.all().delete()
			form.save()
			return redirect(reverse('dashboard:stdbscan_dashboard'))
	else:
		form = STDBSCANParam()

	return render(request, 'dashboard/parameters/stdbscan_input.html', {'form': form})

def stdbscan_dashboard(request):
	parameters = STDBSCAN.objects.all()
	return render(request, 'dashboard/parameters/stdbscan_dashboard.html', {'parameters': parameters})

def stdbscan_charts(request):
	parameters = STDBSCAN.objects.all()
	return render(request, 'dashboard/parameters/stdbscan_charts.html', {'parameters': parameters})

def stdbscan_table(request):
	parameters = STDBSCAN.objects.all()
	return render(request, 'dashboard/parameters/stdbscan_table.html', {'parameters': parameters})

	
# K-means
def kmeans_input(request):
	if request.method == 'POST':
		form = KmeansParam(request.POST, request.FILES)
		if form.is_valid():
			KMeans.objects.all().delete()
			form.save()
			return redirect(reverse('dashboard:kmeans_dashboard'))
	else:
		form = KmeansParam()

	return render(request, 'dashboard/parameters/kmeans_input.html', {'form': form})

def kmeans_dashboard(request):
	parameters = KMeans.objects.all()
	return render(request, 'dashboard/parameters/kmeans_dashboard.html', {'parameters': parameters})

def kmeans_charts(request):
	parameters = KMeans.objects.all()
	return render(request, 'dashboard/parameters/kmeans_charts.html', {'parameters': parameters})

def kmeans_table(request):
	parameters = KMeans.objects.all()
	return render(request, 'dashboard/parameters/kmeans_table.html', {'parameters': parameters})


