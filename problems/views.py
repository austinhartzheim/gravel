import django.http
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from problems import models, forms, utils


def problem_report(request):
    form = utils.create_form_with_request(request)
    return render(request, 'problems/report.html', {'form': form})


def problem_submit(request):
    '''
    Create a new Problem and store it in the database.
    '''
    if request.method != 'POST':
        form = utils.create_form_with_request(request)
        error = 'Error: no form data submitted.'
        return render(request, 'problems/report.html',
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
    '''
    Return an HTML page for viewing a specific Problem.
    '''
    try:
        problem = models.Problem.objects.get(pk=pk)
    except models.Problem.DoesNotExist:
        # TODO: nicer error message
        return django.http.HttpResponseNotFound('Invalid problem ID')

    if request.user.is_authenticated():
        form = forms.ReplySubmit()
    else:
        form = None

    return render(request, 'problems/view.html',
                  {'problem': problem, 'form': form})


def problem_list(request, subset):
    '''
    Return a page listing all the problems.
    '''
    if subset == 'all':
        problems = models.Problem.objects.all()
        return render(request, 'problems/list.html',
                      {'problems': problems, 'subset': 'All'})

    else:
        raise django.http.Http404()

@login_required
def problem_reply_submit(request, pk):
    '''
    Submit a reply to a problem and save it in the database.
    '''
    try:
        problem = models.Problem.objects.get(pk=pk)
    except models.Problem.DoesNotExist:
        # TODO: nicer error message
        return django.http.Http404('Invalid problem ID')

    if request.method != 'POST':
        error = 'Your request is missing POST data.'
        return django.http.HttpResponseNotAllowed(['POST'], error)

    form = forms.ReplySubmit(request.POST)
    if not form.is_valid():
        return render(request, 'problems/view.html',
                      {'problem': problem, 'form': form})

    reply = form.save(commit=False)
    reply.user = request.user
    reply.save()

    problem.add_response(reply)

    return django.http.HttpResponseRedirect('/problem/view/%i/' % problem.pk)


@login_required
def problem_edit(request, pk):
    '''
    Return a page with a form that allows editing of a problem.
    '''
    pass


def tag_view(request, tag):
    '''
    Display a tag and the related problems.
    '''
    try:
        tagobj = models.ProblemTag.objects.get(name=tag)
    except models.ProblemTag.DoesNotExist:
        return django.http.HttpResponseNotFound('Tag does not exist')

    problems = models.Problem.objects.filter(tags__name=tag)

    return render(request, 'problems/tag_view.html',
                  {'problems': problems, 'tag': tag})
