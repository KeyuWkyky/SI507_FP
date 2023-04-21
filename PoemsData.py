#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import os
import json
import re


# In[14]:


cache_path = 'poems1200.txt'
if os.path.isfile(cache_path):
    with open(cache_path,'r', encoding = 'utf-8') as f:
        data = f.read()
else:
    resp = requests.get('https://poetrydb.org/title,random/Sonnet;1200')
    res_dict = resp.json()
    lst = ['i','to','there','o','of','to','is','are','--','on','in']
    with open(cache_path,'w', encoding = 'utf-8')as f:
        for i in res_dict:
            for j in i['lines']:
                if not j in lst:
                    f.write(j)
f.close


# In[19]:


def clean_file(file):
    p = re.compile(r'[,.:;!*?/#$—%^&()\[\]_-]')
    text = open(file, 'r', encoding = 'utf-8').read()
    text = p.sub(' ', text)
    with open(file, 'w', encoding = 'utf-8') as f:
        f.write(text.lower())


# In[20]:


clean_file('poems1200.txt')

