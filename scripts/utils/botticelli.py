from webbot import Browser
from bs4 import BeautifulSoup
import time
import numpy as np
import pandas as pd
import spacy
from collections import Counter
from itertools import combinations
from flair.data import Sentence
from flair.models import SequenceTagger
import networkx as nx
import json
import ast
from Levenshtein import distance as lev
from unidecode import unidecode
import seaborn as sns
from matplotlib import pyplot as plt

# -- ETAPE 0 : Connexion à Atom

def access_atom(driver):
    driver.go_to('https://atom-archives.unil.ch/')
    driver.click('Ouverture de session', tag='button')
    
    with open('credentials.json', 'r') as jsonFile:
        credentials = json.load(jsonFile)
        
    driver.type(credentials['email'], id='email')
    driver.type(credentials['password'], id='password')
    time.sleep(2)
    driver.click('Ouverture de session')

## -- ETAPE 1 : Acquisition des données
    
def browse_pages(driver, tagger, mode, excludeList=None, includeList=None):
    entryList = [] # List to which every entry will be added
    driver.go_to("https://atom-archives.unil.ch/index.php/informationobject/browse")
    time.sleep(3)
    content = driver.get_page_source()
    soup = BeautifulSoup(content, features='lxml')
    numberPage = int(soup.find('li', {'class' : 'last'}).text) # si message d'erreur pour ligne 41 .text -> sur AtoM, aller Paramètres/Généralités/Résultats par page : choisir 10. 
    entryList = browse_entries(driver, tagger, soup, entryList, mode, excludeList, includeList)
    
    for page in range(2, numberPage + 1):
        pageUrl = "https://atom-archives.unil.ch/index.php/informationobject/browse?page=" + str(page)
        driver.go_to(pageUrl)
        time.sleep(3)
        
        content = driver.get_page_source()
        soup = BeautifulSoup(content, features='lxml')
        entryList = browse_entries(driver, tagger, soup, entryList, mode, excludeList, includeList)
        
    entryDF = pd.DataFrame(entryList)
    entryDF.to_csv('CLSR_Correspondance.csv', index=False)
        
def browse_entries(driver, tagger, soup, entryList, mode, excludeList, includeList):
    
    entries = soup.find_all('article', {'class' : 'search-result'})
    
    for entry in entries:
        title = entry.find('p', {'class' : 'title'})
        href = title.find('a')['href']
        if mode == 'Correspondance':
            entryUrl = 'https://atom-archives.unil.ch' + href + ';ead?sf_format=xml'
        driver.go_to(entryUrl)
        time.sleep(3)
        content = driver.get_page_source()
        soup = BeautifulSoup(content, features='lxml')
        if mode == 'Correspondance':
            entryList = correspondance_retrieval(soup, tagger, entryList, excludeList, includeList)
        
    return entryList

def correspondance_retrieval(soup, tagger, entryList, excludeList, includeList):
    
    fonds = soup.find('eadid').text
    
    if excludeList:
        if fonds in excludeList:
            return entryList
        
    elif includeList:
        if fonds not in includeList:
            return entryList
        
    title = soup.find('titleproper').text
    if ',' in title:
        producteur = title.split(', ')[1] + ' ' + title.split(', ')[0]
    else:
        producteur = title
        
    # 1ère étape : Détecter les dossiers ayant attrait à de la correspondance, et obtenir leurs cotes
    
    correspondanceFolders = [folder for folder in soup.find_all('unittitle') if 'correspondance' in folder.text.lower()]
    correspondanceCotes = [folder.parent.find('unitid').text for folder in correspondanceFolders]
    
    # 2ème étape : Récolter toutes les entrées présentes dans le fond et conserver celles comprises dans les correspondance
    
    coteList = [entry for entry in soup.find_all('unitid') if any(cote in entry.text for cote in correspondanceCotes)]
    folderList = [entry.parent for entry in coteList]
    
    # 3ème étape : Pour chaque entrée, lancer la détection de noms et l'ajouter aux entrées à conserver 
    
    for folder in folderList:
        flairList = []
        title = Sentence(folder.find('unittitle').text)
        tagger.predict(title)
        for entity in title.to_dict(tag_type='ner')['entities']:
            for label in entity['labels']:
                if label.value == 'PER' and len(entity['text'].split(' ')) > 1:
                    flairList.append(entity['text'])
        
        # Si aucun nom n'est détecté, on regarde si le titre suit la structure "NOM DE FAMILLE Prénom"
        if len(flairList) == 0:
            folderTitle = folder.find('unittitle').text
            if len(folderTitle.split(' ')) >= 2 and folderTitle.split(' ')[0].isupper():
                flairList.append(folderTitle)
                
        flairList = [flair for flair in flairList if not name_comparison(producteur, flair)[0]]
            
        entryList.append({'Titre' : folder.find('unittitle').text,
                          'Cote' : folder.find('unitid').text,
                          'Profondeur' : len(folder.find('unitid').text.split('-')) - 1,
                          'Acteurs' : flairList})
    
    return entryList

## -- ETAPE 2 : Filtrage des noms

def name_comparison(name, autoriteList):
    for autorite in autoriteList:
        if lev(''.join(sorted(unidecode(name.replace(' ', '').lower()))), 
               ''.join(sorted(unidecode(autorite.replace(',', '').replace(' ', '').lower())))) < 1:
            return True, autorite
        
    return False, name

def name_cleaning(entryDF, changeDict):
    actorList = []
    entryDF = entryDF.drop_duplicates(subset=['Cote'])
    for index, row in entryDF.iterrows():
        rowActors = []
        if type(row.Acteurs) is str:
            flairList = [flair for flair in ast.literal_eval(row.Acteurs)]
            for name in flairList:
                if name.lower() in [key.lower() for key in changeDict.keys()]:
                    key = list(changeDict.keys())[[key.lower() for key in changeDict.keys()].index(name.lower())]
                    name = changeDict[key]
                duplicate, newname = name_comparison(name, actorList)
                rowActors.append(newname)
                if not duplicate:
                    actorList.append(newname)

            entryDF.at[index, 'Acteurs'] = list(set(rowActors))
            
    entryDF.to_csv('CLSR_Correspondance.csv', index=False)

def remove_duplicate_names(entryDF):
    
    for depth in range(1, np.max(list(entryDF.Profondeur.values))):
        depthDF = entryDF[entryDF.Profondeur == depth]
        for index, row in depthDF.iterrows():
            if type(row.Acteurs) == str:
                parentFlair = ast.literal_eval(row.Acteurs)
            else:
                parentFlair = row.Acteurs
            childDF = entryDF[entryDF['Cote'].str.contains(row.Cote)]
            for index2, row2 in childDF.iterrows():
                if not row.equals(row2):
                    if row2.Acteurs == []:
                        childFlair = []
                    else:
                        if type(row2.Acteurs) == str:
                            childFlair = [name for name in eval(row2.Acteurs) if name not in parentFlair]
                        else:
                            childFlair = [name for name in row2.Acteurs if name not in parentFlair]

                    entryDF.at[index2, 'Acteurs'] = childFlair
                    
    entryDF.to_csv('CLSR_Correspondance.csv', index=False)

## -- ETAPE 4 : Comparaison avec les notices d'autorité

def autorite_retrieval(driver):
    autoriteList = []
    driver.go_to('https://atom-archives.unil.ch/index.php/actor/browse')
    content = driver.get_page_source()
    soup = BeautifulSoup(content, features='lxml')
    autoriteList.extend([title.find('a').text for title in soup.find_all('p', {'class' : 'title'})])
    time.sleep(3)
   
    numberPages = int(soup.find('li', {'class' : 'last'}).find('a').text)
    for page in range(2, numberPages + 1):
        link = 'https://atom-archives.unil.ch/index.php/actor/browse?page=' + str(page) + '&sort=alphabetic&sortDir=asc'
        driver.go_to(link)
        content = driver.get_page_source()
        soup = BeautifulSoup(content, features='lxml')
        autoriteList.extend([title.find('a').text for title in soup.find_all('p', {'class' : 'title'})])
        time.sleep(3)
        
    return autoriteList

def autorite_comparison(entryDF, autoriteList):
    entryNames, entryFound = [], []
    for index, row in entryDF.iterrows():
        rowNames, rowFound = [], []
        for name in ast.literal_eval(row.Acteurs):
            found, newname = name_comparison(name, autoriteList)
            rowNames.append(newname)
            rowFound.append(found)
        
        entryNames.append(rowNames)
        entryFound.append(rowFound)
        
    entryDF = entryDF.assign(Autorites=entryNames,Found=entryFound)
    entryDF.to_csv('CLSR_Correspondance.csv', index=False)
    
def find_previous_appearance(entryDF):
    for index, row in entryDF.iterrows():
        rowDF = entryDF.head(index)
        foundRow = []
        autoriteList = [autorite for index2, row2 in rowDF.iterrows() for autorite in ast.literal_eval(row2.Autorites)]
        
        for autorite, found in zip(ast.literal_eval(row.Autorites), ast.literal_eval(row.Found)):
            if found:
                foundRow.append(True)
            else:
                if autorite in autoriteList:
                    foundRow.append(True)
                else:
                    foundRow.append(False)
                
        entryDF.at[index, 'Found'] = foundRow
        
    entryDF = entryDF.drop(['Acteurs'], axis=1)    
    entryDF.to_csv('CLSR_Correspondance.csv', index=False)
        
## -- ETAPE 5 : Indexation automatique

def indexation_automatique(driver, entryDF):
    for index, row in entryDF.iterrows():
        href = ''
        if np.mod(index, 100) == 0:
            print('Index: ', index)
        if len(ast.literal_eval(row.Autorites)) > 0:
            queryList = ['+'.join(row.Cote.split('/')), '+'.join(row.Titre.split(' ') + row.Cote.split('/'))]
            for query in queryList:
                link = 'https://atom-archives.unil.ch/index.php/informationobject/browse?topLod=0&sort=relevance&query=' + query
                driver.go_to(link)
                time.sleep(4) ## -- temps d'attente dans le menu déroulant du bot
                content = driver.get_page_source()
                soup = BeautifulSoup(content, features='lxml')
                if soup.find('a', {'title' : row.Titre}):
                    href = soup.find('a', {'title' : row.Titre})['href']
                    break

            if href == '':
                print('Error: ', row.Cote)

            driver.go_to('https://atom-archives.unil.ch' + href)
            time.sleep(1)
            editUrl = driver.get_current_url() + '/edit#accessPointsArea'
            driver.go_to(editUrl)
            for autorite, found in zip(ast.literal_eval(row.Autorites), ast.literal_eval(row.Found)):
                if found:
                    driver.type(autorite, id='nameAccessPoints')
                    time.sleep(2) ## -- temps d'attente dans le menu déroulant du bot
                    driver.press(driver.Key.ENTER)
                else:
                    driver.type(autorite, id='nameAccessPoints')
                    driver.press(driver.Key.TAB)
            
            time.sleep(1)
            driver.click('Sauvegarder', tag='input')

            
            
  
            
    
      