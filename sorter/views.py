from django.shortcuts import render
from django.db.models import Count
from django.http import HttpResponse, Http404
from django.http import FileResponse
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
import rest_framework
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
import json
from .query import *
from django.http import HttpResponse, Http404
from .file_parser import *
from .serializer import *


@api_view(['POST'])
@permission_classes((AllowAny, ))
def api_update_directory(request):
    try:
        directory = request.data.get('directory')
        resp = update_directory(directory)
        serializer = DirectoryGraphSerializer(resp)
        return Response({'status': 'ok', 'data': serializer.data})
    except Exception as e:
        log_error(request.path, request.method, e)
        return Response({'status': 'failed', 'error': 'Unknown_error'})


@api_view(['POST'])
@permission_classes((AllowAny, ))
def api_add_dir(request):
    path = request.data.get('path')
    try:
        result = add_directory(path)
        if result == 'Wrong_path':
            print("TYT")
            return Response({'status': 'failed', 'error': 'No_such_directory'})
        elif result == 'No_images':
            return Response({'status': 'failed', 'error': 'No_images_in_directory'})
        elif result == 'Directory_already_exists':
            return Response({'status': 'failed', 'error': 'Directory_already_exists'})
        else:
            serializer = DirectoryGraphSerializer(result)
            return Response({'status': 'ok', 'data': serializer.data})
    except Exception as e:
        log_error(request.path, request.method, e)
        return Response({'status': 'failed', 'error': 'Unknown_error'})


def api_get_image(request):
    path = request.GET['path']
    if path is None:
        return Response({'status': 'failed', 'error': 'Wrong_params'})
    try:
        img = open(path, 'rb')
        response = FileResponse(img)
        return response
    except Exception as e:
        log_error(request.path, request.method, e)
        return Response({'status': 'failed', 'error': 'Unknown_error'})


@api_view(['POST'])
@permission_classes((AllowAny, ))
def api_get_images(request):
    if request.data.get('directory') is None:
        return Response({'status': 'failed', 'error': 'Wrong_params'})
    try:
        images = new_comparsion(request.data.get('directory'))
        if images is None:
            return Response({'status': 'failed', 'error': 'Already_sorted'})
        serializer = ImageNodeSerializer(images, many=True)
        return Response({'status': 'ok', 'data': serializer.data})
    except Exception as e:
        log_error(request.path, request.method, e)
        return Response({'status': 'failed', 'error': 'Unknown_error'})


@api_view(['POST'])
@permission_classes((AllowAny, ))
def api_update_rates(request):
    response_list = request.data.get('data').get('rates')
    directory = request.data.get('data').get('directory')
    try:
        if response_list is not None:
            update_img_rates(response_list, directory)
        else:
            return HttpResponse(json.dumps({'status': 'failed', 'error': 'Already_sorted'}))
        return Response({'status': 'ok'})
    except Exception as e:
        log_error(request.path, request.method, str(e))
        return Response({'status': 'failed', 'error': 'Unknown_error'})


@api_view(['GET'])
@permission_classes((AllowAny, ))
def api_get_directories(request):
    try:
        serializer = DirectoryGraphSerializer(get_directories(), many=True)
        return Response({'status': 'ok', 'data': serializer.data})
    except Exception as e:
        log_error(request.path, request.method, str(e))
        return Response({'status': 'failed', 'error': 'Unknown_error'})
