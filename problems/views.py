import django.http
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from problems import models, forms, utils


def problem_report(request):
    form = utils.create_form_with_request(request)
    return render(request, 'problems/report.html', {'form': form})


def problem_submit(request):
    if request.method != 'POST':
        form = utils.create_form_with_request(request)
        error = 'Error: no form data submitted.'
        return render(request, 'problem_report.html',
                      {'form': form, 'error': error})

    form = forms.ProblemSubmitForm(request.POST)
    if not form.is_valid():
        return render(request, 'problems/report.html', {'form': form})

    problem = form.save(commit=False)
    if request.user.is_authenticated():
        problem.userref = request.user
        problem.username = request.user.get_full_name()
        problem.userauthed = True
    problem.save()

    return django.http.HttpResponseRedirect('/problem/view/%i/' % problem.pk)


def problem_view(request, pk):
    try:
        problem = models.Problem.objects.get(pk=pk)
    except models.Problem.DoesNotExist:
        # TODO: nicer error message
        return django.http.Http404('Invalid problem ID')

    return render(request, 'problems/view.html', {'problem': problem})


@login_required
def problem_edit(request, pk):
    pass
