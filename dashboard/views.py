from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import STDBSCAN
from .forms import STDBSCANParam

from django.conf import settings
from django.core.files.storage import FileSystemStorage
# Create your views here.

def menu(request):
	return render(request, 'dashboard/parameters/index.html')

def dashboard(request):
	parameters = STDBSCAN.objects.all()
	return render(request, 'dashboard/parameters/dashboard.html', {'parameters': parameters})

def charts(request):
	parameters = STDBSCAN.objects.all()
	return render(request, 'dashboard/parameters/charts.html', {'parameters': parameters})

def result_table(request):
	parameters = STDBSCAN.objects.all()
	return render(request, 'dashboard/parameters/result_table.html', {'parameters': parameters})
	
def choose_algo(request):
	return render(request, 'dashboard/parameters/choose_algo.html')

def input_param(request):
	if request.method == 'POST':
		form = STDBSCANParam(request.POST, request.FILES)
		if form.is_valid():
			STDBSCAN.objects.all().delete()
			form.save()
			return redirect(reverse('dashboard:dashboard'))
	else:
		form = STDBSCANParam()

	return render(request, 'dashboard/parameters/input.html', {'form': form})


