from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Parameters
from .forms import PostParam
#from django.http import HttpResponseRedirect
#from .forms import UploadFileForm
# Create your views here.

def parameters_list(request):
	parameters = Parameters.objects.all()
	return render(request, 'dashboard/parameters/list.html', {'parameters': parameters})

def parameters_add(request):
	if request.method == 'POST':
		form = PostParam(request.POST)
		if form.is_valid():
			Parameters.objects.all().delete()
			form.save()
			return redirect(reverse('dashboard:parameters_list'))
	else:
		form = PostParam()

	return render(request, 'dashboard/parameters/add.html', {'form': form})


