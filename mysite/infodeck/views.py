from django.shortcuts import render
from django.template import loader
from .modules.deckjson import buscadecks
#from .modules.deckhtml import buscadecks
# Create your views here.
from django.http import HttpResponse

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .serializers import UserSerializer, GroupSerializer
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from django.views.decorators.csrf import csrf_exempt

import requests

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)
        
@csrf_exempt
def deck_detail(request, pk):
    if request.method == 'GET':
         resultado=buscadecks(pk)
         return JSONResponse(resultado)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

from django.http import HttpResponse
def index(request):  
    template =loader.get_template("infodeck/index.html")
    #return HttpResponse( "Hello, world. This is my first Django app." )
    return HttpResponse(template.render())
def about(request):  
    template =loader.get_template("infodeck/about.html")
    #return HttpResponse( "Hello, world. This is my first Django app." )
    return HttpResponse(template.render())

def search(request):  
    template =loader.get_template("infodeck/search.html")
    pA = request.GET.get('deckId')
    resultado=buscadecks(pA)
    try:
        response = requests.get('http://localhost:8000/infodeck/deckinfo/'+pA).json()
    except ConnectionError:
        response={}
    return HttpResponse(template.render({'content':pA ,'content_result':response}))