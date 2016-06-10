from django.shortcuts import render
from .forms import submitForm

def index(request):
	formClass = submitForm

	if (request.method == 'POST'):
		form = formClass(data=request.POST)

		if form.is_valid():
			ticker = request.POST.get('ticker','')

	return render(request, 'investIn/index.html', {})
