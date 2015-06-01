from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from problems import models
from problems import forms


def problem_report(request):
    form = forms.ProblemSubmitForm()
    if request.user.is_authenticated():
        form.username = request.user.get_full_name()
    return render(request, 'problem_report.html', {'form': form})


def problem_submit(request):
    pass


def problem_view(request, pk):
    pass


@login_required
def problem_edit(request, pk):
    pass