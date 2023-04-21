#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import re


# In[2]:


url = "http://svn.code.sf.net/p/cmusphinx/code/trunk/cmudict/cmudict-0.7b"

# download and decode the data
content = requests.get(url).content.decode('ISO-8859-1')

syllable_dict = {}

# extract word and syllable count
for line in content.splitlines():
    if not line.startswith(';;;'):
        word, phones = line.split('  ')
        syllables = len(re.findall(r'\d', phones))
        syllable_dict[word.lower()] = syllables

# save the dictionary as a text file
with open('syllable_data.txt', 'w', encoding='utf-8') as file:
    for word, syllables in syllable_dict.items():
        file.write(f"{word}: {syllables}\n")

