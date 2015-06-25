import json

import django.http
from django.http import JsonResponse
from django.shortcuts import render
from problems import models
from api.models import RequestToken
from api.libs.validate import ValidateApiRequest, ValidateToken


@ValidateApiRequest
def problem_highest_id(request, user, data):
    try:
        highest_id = models.Problem.objects.order_by('-pk')[0].pk
        return JsonResponse({'id': highest_id})
    except IndexError:
        return JsonResponse({'id': 0})


@ValidateApiRequest
@ValidateToken
def problem_reply(request, user, data):
    try:
        problem = models.Problem.objects.get(pk=data['id'])
        reply = models.Reply(user=user, text=data['text'])
    except IndexError:
        return django.http.HttpResponse('Key missing from JSON data')
    except models.Problem.DoesNotExist:
        return django.http.HttpResponseNotFound('Could not find problem')

    reply.save()
    problem.add_response(reply)

    return JsonResponse({'problemid': problem.pk, 'replyid': reply.pk})


@ValidateApiRequest
def problem_get_replies(request, user, data):
    try:
        problem = models.Problem.objects.get(pk=data['id'])
    except IndexError:
        return django.http.HttpResponse('Key missing from JSON data')
    except models.Problem.DoesNotExist:
        return django.http.HttpResponseNotFound('Could not find problem')

    return JsonResponse({
        'problemid': problem.pk,
        'replies': [reply.serialize() for reply in problem.replies()]
    })


@ValidateApiRequest
def api_get_tokens(request, user, data):
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
        'expires': tokens[0].expires.isoformat(),
        'tokens': [token.token for token in tokens]
    })


@ValidateApiRequest
def tag_get(request, user, data):
    '''
    Get a specific tag by looking up the ID or name.
    '''
    pass


@ValidateApiRequest
def tag_problems(request, user, data):
    '''
    Get all problems that have a specific tag.
    '''
    pass


@ValidateApiRequest
def tag_all(request, user, data):
    '''
    Get a list of all tags and their IDs.
    '''
    pass
