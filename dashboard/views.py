from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Parameters
from .forms import PostParam

from django.conf import settings
from django.core.files.storage import FileSystemStorage
# Create your views here.

def menu(request):
	return render(request, 'dashboard/parameters/index.html')

def dashboard(request):
	parameters = Parameters.objects.all()
	return render(request, 'dashboard/parameters/dashboard.html', {'parameters': parameters})

def charts(request):
	parameters = Parameters.objects.all()
	return render(request, 'dashboard/parameters/charts.html', {'parameters': parameters})

def result_table(request):
	parameters = Parameters.objects.all()
	return render(request, 'dashboard/parameters/result_table.html', {'parameters': parameters})

def choose_algo(request):
	return render(request, 'dashboard/parameters/choose_algo.html')

def input_param(request):
	if request.method == 'POST':
		form = PostParam(request.POST, request.FILES)
		if form.is_valid():
			Parameters.objects.all().delete()
			form.save()
			return redirect(reverse('dashboard:dashboard'))
	else:
		form = PostParam()

	return render(request, 'dashboard/parameters/input.html', {'form': form})


