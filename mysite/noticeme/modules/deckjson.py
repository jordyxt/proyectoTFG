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
    url = 'https://deckservice.slidewiki.org/deck/'+str(deck)
    resp = requests.get(url=url)
    data = resp.json()
    status = resp.status_code
    if status == 404:
        return resultado
    docker=data['revisions'][0]['contentItems']
    for slide in docker:
        if slide['kind']=='slide':
            url = 'https://deckservice.slidewiki.org/slide/'+str(slide['ref']['id'])
            data = getjson(url)
            resultado['slide '+str(slide['order'])]={}
            resultado['slide '+str(slide['order'])]['kind']='slide'
            if data['revisions'][0]['parent']==None:
                #"it's not an attached slide
                resultado['slide '+str(slide['order'])]['attached']='no'
            else:
                resultado['slide '+str(slide['order'])]['attached']='yes'
                oldrevision=data['revisions'][0]['parent']['revision']
                resultado['slide '+str(slide['order'])]['origin']=data['revisions'][0]['parent']
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
                    resultado['slide '+str(slide['order'])]['updated']='yes'
                else:
                    #existe version mas actual de la slide
                    resultado['slide '+str(slide['order'])]['updated']='no'
                    resultado['slide '+str(slide['order'])]['updated slide'] = str(data['revisions'][-1]['id'])
               
        else:
            #print(slide['ref']['id'])
            resultado['deck '+str(slide['order'])]={}
            resultado['deck '+str(slide['order'])]['kind']='deck'
            resultado['deck '+str(slide['order'])]['slides']=buscadecks(slide['ref']['id'])
    return resultado

#print(buscadecks(105268))
#buscadecks(106865)
