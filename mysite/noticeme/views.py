from django.shortcuts import render
from django.template import loader
from .modules.deckjson import buscadecks
# Create your views here.

from django.http import HttpResponse
def index(request):  
    template =loader.get_template("noticeme/index.html")
    #return HttpResponse( "Hello, world. This is my first Django app." )
    return HttpResponse(template.render())
def about(request):  
    template =loader.get_template("noticeme/about.html")
    #return HttpResponse( "Hello, world. This is my first Django app." )
    return HttpResponse(template.render())

def search(request):  
    template =loader.get_template("noticeme/search.html")
    pA = request.GET.get('deckId')
    resultado=buscadecks(pA)
    return HttpResponse(template.render({'content':pA ,'content_result':resultado}))