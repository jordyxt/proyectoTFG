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
    resultado['id']=data['_id']
    docker=data['revisions'][-1]['contentItems']

    if 'origin' not in data:
        resultado['attached']=False
    else:
        resultado['attached']=True
        auxDict={}
        auxDict['id']=data['origin']['id']
        auxDict['revision']=data['origin']['revision']
        resultado['origin']=auxDict
        deckOldId=data['origin']['id']
    slideList=[]  
    for slide in docker:
        slideitem={}
        slideitem['order']=slide['order']
        slideitem['kind']=slide['kind']
        if slide['kind']=='slide':
            url = 'https://deckservice.slidewiki.org/slide/'+str(slide['ref']['id'])
            data = getjson(url)
            if data['revisions'][0]['parent']==None:
                #"it's not an attached slide
                if resultado['attached']:
                    revisionList=data['revisions']
                    revisionList.reverse()
                    #slideitem ['attached']=True
                    versionOld_encontrada=False
                    for revisionDict in revisionList :
                        for usageDict in revisionDict['usage']:
                            if usageDict['id']==deckOldId :
                                versionOld_encontrada=True
                                revisionOld=usageDict['revision']
                                break
                        if(versionOld_encontrada):
                            htmlOld=revisionDict['content']
                            break

                    if(versionOld_encontrada):
                        slideitem ['attached']=True
                        if revisionOld==resultado['origin']['revision']:
                            slideitem['updated']=True
                        else:
                            version_encontrada=False
                            for revisionDict in revisionList :
                                for usageDict in revisionDict['usage']:
                                    if usageDict['id']==resultado['id'] :
                                        version_encontrada=True
                                        break
                                if(version_encontrada):
                                    htmlActual=revisionDict['content']
                                    break
                            html=htmldiff(htmlActual,htmlOld)
                            parsed_html = BeautifulSoup(html,'lxml')
                            insert=parsed_html.find_all('ins')
                            delete=parsed_html.find_all('del')
                            if(len(insert)==0 and len (delete)==0):
                                slideitem['updated']=True
                            else:
                                #existe version mas actual de la slide
                                slideitem['updated']=False
                                slideitem['updated version deck'] = revisionOld
                    else:
                        slideitem ['attached']=False                    
                else:
                    slideitem['attached']=False
            else:
                slideitem ['attached']=True
                slideitem['origin']=data['revisions'][0]['parent']
                parent_url = 'https://deckservice.slidewiki.org/slide/'+str(data['revisions'][0]['parent']['id'])
                parent_resp = requests.get(url=parent_url)
                parent_data = parent_resp.json()
                if data['revisions'][0]['parent']['revision']==len(parent_data['revisions']):
                    slideitem['updated']=True
                else:
                    html=htmldiff(data['revisions'][-1]['content'],parent_data['revisions'][-1]['content'])
                    parsed_html = BeautifulSoup(html,'lxml')
                    insert=parsed_html.find_all('ins')
                    delete=parsed_html.find_all('del')
                    if(len(insert)==0 and len (delete)==0):
                        slideitem['updated']=True
                    else:
                        #existe version mas actual de la slide
                        slideitem['updated']=False
                        slideitem['updated version'] = parent_data['revisions'][-1]['id']         
        else:
            #print(slide['ref']['id'])
            slideitem.update(buscadecks(str(slide['ref']['id'])+'-'+str(slide['ref']['revision'])))
        slideList.append(slideitem)
    resultado['slides']=slideList
    return resultado

#print(buscadecks(105268))
#print(buscadecks(112866))
#print(buscadecks(112619))
#print(buscadecks(112915))
print(buscadecks(112918))
#buscadecks(106865)
