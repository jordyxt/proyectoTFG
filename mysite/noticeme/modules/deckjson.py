try:
    from lxml.html.diff import htmldiff
except ImportError:
    print('error al importar funcion htmldiff')
import difflib

from bs4 import BeautifulSoup
import json 
import requests
def getjson(url):
    resp = requests.get(url=url)
    data = resp.json()
    return data



def buscadecks(deck):
    
    resultado={}
    resultado['id']=deck
    url = 'https://deckservice.slidewiki.org/deck/'+str(deck)
    resp = requests.get(url=url)
    data = resp.json()
    status = resp.status_code
    if status == 404:
        return resultado
    docker=data['revisions'][0]['contentItems']
    slideList=[]
    for slide in docker:
        slideitem={}
        slideitem['order']=slide['order']
        slideitem['kind']=slide['kind']
        if slide['kind']=='slide':
            url = 'https://deckservice.slidewiki.org/slide/'+str(slide['ref']['id'])
            data = getjson(url)
            #resultado['slide '+str(slide['order'])]['kind']='slide'
            #resultado['slide '+str(slide['order'])]['slide']=data['revisions'][-1]['content']
            if data['revisions'][0]['parent']==None:
                #"it's not an attached slide
                slideitem['attached']=False
            else:
                slideitem ['attached']=True
                oldrevision=data['revisions'][0]['parent']['revision']
                slideitem['origin']=data['revisions'][0]['parent']
                url = 'https://deckservice.slidewiki.org/slide/'+str(data['revisions'][0]['parent']['id'])
                resp = requests.get(url=url)
                data = resp.json()
                html=htmldiff(data['revisions'][oldrevision-1]['content'],data['revisions'][-1]['content'])
                #print('------------------------------')
                #print(data['revisions'][-1]['content'])
                #print('.............................')
                #print(data['revisions'][4]['content'])
                #print('..............................')
                parsed_html = BeautifulSoup(html,'lxml')
                insert=parsed_html.find_all('ins')
                delete=parsed_html.find_all('del')
                if(len(insert)==0 and len (delete)==0):
                    slideitem['updated']=True
                else:
                    #existe version mas actual de la slide
                    slideitem['updated']=False
                    slideitem['updated version'] = data['revisions'][-1]['id']
               
        else:
            #print(slide['ref']['id'])
            slideitem['slides']=buscadecks(slide['ref']['id'])
        slideList.append(slideitem)
    resultado['slides']=slideList
    return resultado

#print(buscadecks(105268))
#buscadecks(106865)
