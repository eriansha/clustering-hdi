from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Parameters
from .forms import PostParam
#from django.http import HttpResponseRedirect
#from .forms import UploadFileForm
# Create your views here.

def dashboard(request):
	parameters = Parameters.objects.all()
	return render(request, 'dashboard/parameters/dashboard.html', {'parameters': parameters})

def input_param(request):
	if request.method == 'POST':
		form = PostParam(request.POST)
		if form.is_valid():
			Parameters.objects.all().delete()
			form.save()
			return redirect(reverse('dashboard:dashboard'))
	else:
		form = PostParam()

	return render(request, 'dashboard/parameters/input.html', {'form': form})


