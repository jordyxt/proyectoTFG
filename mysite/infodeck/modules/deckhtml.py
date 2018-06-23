from bs4 import BeautifulSoup
from datetime import datetime
absolutepath='c:/Users/F556UJ/Documents/Universidad fi/4º año fi/TFG/git/proyectoTFG/mysite/noticeme/static/Reuse/'

#id=2
def buscadecksapi(id):
    resultado={}
    with open(absolutepath+"Deck"+str(id)+"/D"+str(id)+".htm") as fp:
        soup = BeautifulSoup(fp,'html.parser')
    table=soup('a')
    for tag in table:
        with open(absolutepath+"Deck"+str(id)+"/"+tag.get('href',None)) as fp:
            soupaux = BeautifulSoup(fp,'html.parser')
        tr=soupaux('p')
        contador=0
        fechaattached=''
        encontradoattached=False
        for tagaux in tr:
            if tagaux.string=='attached':
                contador+=2
                encontradoattached=True
            elif contador>0 and tagaux.string !=' ' :
                if contador==2:
                    html=tagaux.a.get('href',None)[3:]
                else:
                    fechaattached=tagaux.string 
                contador-=1
        resultado[tag.string]={}
        if encontradoattached==True:
            with open(absolutepath+html) as fp:
                soupaux1 = BeautifulSoup(fp,'html.parser')
            tr1=soupaux1('p')
            encontrado=False
            fechamod=''
            resultado[tag.string]['attached']='yes'
            for tagaux1 in tr1:
                if tagaux1.string=='edited' and encontrado==False:
                    contador+=2
                    encontrado=True
                elif contador>0 and tagaux1.string !=' ' :
                    if contador==1:
                        fechamod=tagaux1.string 
                    contador-=1
            datetimefechaattached = datetime.strptime(fechaattached, '%d/%m/%Y, %H:%M:%S')
            datetimefechamod = datetime.strptime(fechamod, '%d/%m/%Y, %H:%M:%S')
            resultado[tag.string]['updated']=datetimefechamod<datetimefechaattached
        else:
            resultado[tag.string]['attached']='no'
    return resultado
        
def buscadecks(id):
    resultado={}
    with open(absolutepath+"Deck"+str(id)+"/D"+str(id)+".htm") as fp:
        soup = BeautifulSoup(fp,'html.parser')
    table=soup('a')
    for tag in table:
        with open(absolutepath+"Deck"+str(id)+"/"+tag.get('href',None)) as fp:
            soupaux = BeautifulSoup(fp,'html.parser')
        tr=soupaux('p')
        contador=0
        fechaattached=''
        encontradoattached=False
        for tagaux in tr:
            if tagaux.string=='attached':
                contador+=2
                encontradoattached=True
            elif contador>0 and tagaux.string !=' ' :
                if contador==2:
                    html=tagaux.a.get('href',None)[3:]
                else:
                    fechaattached=tagaux.string 
                contador-=1
        resultado[tag.string]={}
        if encontradoattached==True:
            with open(absolutepath+html) as fp:
                soupaux1 = BeautifulSoup(fp,'html.parser')
            tr1=soupaux1('p')
            encontrado=False
            fechamod=''
            resultado[tag.string]['attached']='yes'
            for tagaux1 in tr1:
                if tagaux1.string=='edited' and encontrado==False:
                    contador+=2
                    encontrado=True
                elif contador>0 and tagaux1.string !=' ' :
                    if contador==1:
                        fechamod=tagaux1.string 
                    contador-=1
            datetimefechaattached = datetime.strptime(fechaattached, '%d/%m/%Y, %H:%M:%S')
            datetimefechamod = datetime.strptime(fechamod, '%d/%m/%Y, %H:%M:%S')
            resultado[tag.string]['updated']=datetimefechamod<datetimefechaattached
        else:
            resultado[tag.string]['attached']='no'
    return resultado


#print(buscadecks(1))
#print(buscadecks(2))