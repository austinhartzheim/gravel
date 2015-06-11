from problems import forms


def create_form_with_request(request):
    form = forms.ProblemSubmitForm()
    if request.user.is_authenticated():
        form.username = request.user.get_username()
    return form
