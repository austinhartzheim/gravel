import json

import django.http
from django.http import JsonResponse
from django.shortcuts import render
from problems import models
from api.models import RequestToken
from api.libs.validate import ValidateApiRequest


@ValidateApiRequest
def problem_highest_id(request, user):
    try:
        highest_id = models.Problem.objects.order_by('-pk')[0].pk
        return JsonResponse({'id': highest_id})
    except IndexError:
        return JsonResponse({'id': 0})


@ValidateApiRequest
def api_get_tokens(request, user):
    try:
        data = json.loads(request.body)
    except ValueError:
        return django.http.HttpResponseBadRequest('Invalid JSON data')

    count = 1
    try:
        if 'count' in data:
            count = int(data['count'])
    except ValueError:
        return django.http.HttpResponseBadRequest('Invalid number of tokens')

    if count > 1024:
        return django.http.HttpResponseBadRequest('Too many tokens requested')
    elif count < 0:
        return django.http.HttpResponseBadRequest('Too few tokens requested')

    tokens = RequestToken.build_tokens(user, count)
    return JsonResponse({
        'expires': tokens[0].isoformat(),
        'tokens': [token.token for token in tokens]
    })
