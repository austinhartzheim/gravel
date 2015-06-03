import django.http
from django.http import JsonResponse
from django.shortcuts import render
from problems import models


def problem_highest_id(request):
    highest_id = models.Problem.objects.order_by('-pk')[0].pk
    return JsonResponse({'id': highest_id})