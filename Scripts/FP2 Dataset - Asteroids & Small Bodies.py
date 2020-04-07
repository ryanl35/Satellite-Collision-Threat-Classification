#!/usr/bin/env python
# coding: utf-8

# # Asteroids, Comets, and Small Body Spitzer Dataset

# In[1]:


import pandas as pd

import urllib.request as urllib
from bs4 import BeautifulSoup

bodies = urllib.urlopen("https://pdssbn.astro.umd.edu/data_other/Spitzer.shtml")
soup = BeautifulSoup(bodies.read())
classifications = urllib.urlopen("https://pdssbn.astro.umd.edu/data_other/objclass.shtml")
soup2 = BeautifulSoup(classifications.read())

bodydf = pd.DataFrame(columns = ["Name", "NAIF ID Number", "Classification", "Distance", "Records", "Link"])
classificationdf = pd.DataFrame(columns = ["Abbreviation", "Title", "Distance", "Description"])


# In[2]:


atags = soup.find_all("a")
bodytypes = []

for atag in atags:
    if atag.get("href") != None:
        if "sptz_01_COMET" in atag.get("href"):
            bodytypes.append("Comet")
        elif "sptz_02_INNER" in atag.get("href"):
            bodytypes.append("Inner Solar System Asteroids")
        elif "sptz_03_MAIN" in atag.get("href"):
            bodytypes.append("Main Belt Asteroids")
        elif "sptz_04_OUTER" in atag.get("href"):
            bodytypes.append("Outer Solar System Asteroids")
        elif "sptz_05_SAT" in atag.get("href"):
            bodytypes.append("Satellite")
            
bodydf = pd.DataFrame(index = bodytypes, columns = ["Name", "NAIF ID Number", "Classification", "Records", "Link"])


# In[3]:


trtags = soup.find_all("tr")
names = []

for tag in trtags:
    if tag.find("td").get_text() != "Object Name":
        names.append(tag.find("td").get_text())
        
bodydf["Name"] = names


# In[4]:


trtags = soup.find_all("tr")
atags = []
idnumbers = []
for tag in trtags:
    if tag.find("a", {"onclick":"this.target='_blank'"}) != None:
        idnumbers.append(tag.find("a", {"onclick":"this.target='_blank'"}).get_text())

bodydf["NAIF ID Number"] = idnumbers


# In[5]:


atags = soup.find_all("a")
classifications = []
for atag in atags:
    if atag.get("href") != None:
        if "objclass" in atag.get("href"):
            classifications.append(atag.get_text())

bodydf["Classification"] = classifications


# In[32]:


trtags = soup2.find_all("tr")
classdistance = []

for trtag in trtags:
    for tdtag in (trtag.find_all("td"))[2:3]:
        if tdtag.get_text() != "Description":
            left, delimit, right = tdtag.get_text().partition("(")
            left2, delimit2, right2 = right.partition(")")
            classdistance.append(left2)

classificationdf["Distance"] = classdistance


# In[33]:


trtags = soup.find_all("tr")
records = []

for trtag in trtags:
    for tdtag in (trtag.find_all("td"))[3:]:
        if tdtag.get_text() != "Records":
            records.append(tdtag.get_text())
            
bodydf["Records"] = records


# In[34]:


trtags = soup.find_all("tr")
links = []

for tag in trtags:
    if tag.find("td").find("a") != None:
        links.append("https://pdssbn.astro.umd.edu/data_other/" + tag.find("td").find("a").get("href"))
    
bodydf["Link"] = links


# In[35]:


trtags = soup2.find_all("tr")
abbreviations = []

for trtag in trtags:
    if trtag.find("td").find("a") != None:
        abbreviations.append(trtag.find("td").find("a").get("name"))

classificationdf["Abbreviation"] = abbreviations


# In[36]:


trtags = soup2.find_all("tr")
titles = []

for trtag in trtags:
    for tdtag in (trtag.find_all("td"))[1:2]:
        if tdtag.get_text() != "Title":
            titles.append(tdtag.get_text())
            
classificationdf["Title"] = titles


# In[37]:


trtags = soup2.find_all("tr")
descriptions = []

for trtag in trtags:
    for tdtag in (trtag.find_all("td"))[2:3]:
        if tdtag.get_text() != "Description":
            descriptions.append(tdtag.get_text())
            
classificationdf["Description"] = descriptions


# In[119]:


bodydistance = []
abbrevstrings = []
distancestrings = []
alltuples = []

for abbrev in classificationdf["Abbreviation"]:
    abbrevstrings.append(abbrev)
for distance in classificationdf["Distance"]:
    distancestrings.append(distance)
for i in range(0, len(abbrevstrings)):
    alltuples.append((abbrevstrings[i], distancestrings[i]))

for classification in bodydf["Classification"]:
    if classification != "":
        for etuple in alltuples:
            if etuple[0] == classification:
                bodydistance.append(etuple[1])
    else:
        bodydistance.append("N/A")
            
bodydf["Distance"] = bodydistance


# In[120]:


classificationdf


# In[121]:


bodydf


# In[122]:


bodydf.to_csv('res/asteroids_comets_bodies_dataset1.csv')


# In[123]:


classificationdf.to_csv('res/classifications_dataset2.csv')


# In[ ]:




