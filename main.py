#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pickle
import random


# In[2]:


def main():
    print("Welcome to the Haiku generator!")
    print("The Haiku will be generated automaticlly with the start word!")
    tree = read_tree_from_file("Haikus.txt")
    while True:
        word = input("Enter the word you would like to start with: ")
        asw1 = input("Would you like to see the generated Haikus or get a new one？Enter 'read' or 'new'.")
        if asw1 == "read":
            try:
                a=0
                for node in tree[1:]:
                    if node[0] == word:
                        a=1
                        for haikus in node:
                            print(haikus)
            except:
                continue
            if a==0:
                print("No Haikus for this word has been generated yet.")
                continue
            asw3 = input("Would you like to continue or quit? Enter 'continue' or 'quit'.")
            if asw3 == "continue":
                continue
            elif asw3 == "quit":
                print("Bye!")
                break
            else:
                print("Invalid input")
                continue
        elif asw1 == "new":
            newHaiku = writeHaiku(word)
            print(newHaiku)
            asw2 = input("Would you like to save this Haiku for further review? Enter 'yes' or 'no'.")
            if asw2 == "yes":
                a = 0
                for node in tree[1:]:
                    if node[0] == word:
                        node.append(newHaiku)
                        a = 1
                if a==0:
                    node = [word,newHaiku]
                    tree.append(node)
                save_tree_to_file(tree, "Haikus.txt")
                asw3 = input("Would you like to continue or quit? Enter 'continue' or 'quit'.")
                if asw3 == "continue":
                    continue
                elif asw3 == "quit":
                    print("Bye!")
                    break
                else:
                    print("Invalid input")
                    continue
            elif asw2 == "no":
                asw3 = input("Would you like to continue or quit? Enter 'continue' or 'quit'.")
                if asw3 == "continue":
                    continue
                elif asw3 == "quit":
                    print("Bye!")
                    break
                else:
                    print("Invalid input")
                    continue
            else:
                print("Invalid input")
                continue
        else:
            print("Invalid input")
            continue


# In[3]:


def save_tree_to_file(tree, filename):
    with open(filename, 'w') as f:
        for node in tree:
            f.write(str(node[0]) + '.' + '.'.join(str(l) for l in node[1:]) + '\n')

def read_tree_from_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        tree = [lines[0].strip()]
        for line in lines[1:]:
            parts = line.strip().split('.')
            node = [parts[0]]
            node.extend(parts[1:])
            tree.append(node)
        return tree


# In[4]:


syllablesDict = {}

# read the file into a dictionary
with open('syllable_data.txt', 'r', encoding='utf-8') as file:
    for line in file:
        word, syllables = line.strip().split(': ')
        syllables = int(syllables)
        syllablesDict[word] = syllables


# In[5]:


def wordFrequencies(text):
    '''
    create a dictionary of dictionaries(word graph)containing each word that appears in 
    the text and the number of times other words appear after it
    '''
    text_file = open (text, "r", encoding = 'utf-8')
    word_dict = {}
    previous = 'the'
    for line in text_file:
        words = line.split()
        for word in words:
            word = word.lower()
            if previous in word_dict:
                entry = word_dict[previous]
                if word in entry :
                    entry[word] += 1
                else :
                    entry[word] = 1
            else:
                word_dict[previous] = {word:1}
            previous = word
    return word_dict


# In[6]:


def generateProbabilityList(Wordsdict) : 
    '''
    Takes a dict namd Words and creates a list of words containing each key in the dict repeated
    the number of times listed in the corresponding value of the times listed in the 
    corresponding value of the key.
    '''
    result = []
    theList = Wordsdict.keys()
    for i in theList : 
        for j in range(0, Wordsdict.get(i)) : 
            result = result + [i]
    return result


# In[7]:


def checkSyllables(theword, lineSyl, maxSyl):
    '''
    Check whether theWord that may be used next will make the sentence exceed the max syllable.
    '''
    sylCount = 0
    try:
        sylCount = syllablesDict.get(theword)
        
    except Exception as e:#when the word is not included in the syllablesDict
        print(e)
        return 0
    if (sylCount is None) or (int(sylCount) + lineSyl > maxSyl):
        return 0
    else:
        return sylCount


# In[8]:


def getLine(theWord, Wordsdict, totalSyllables) :
    '''
    Writes a line starting with Wordsdict and with a syllable length of totalSyllables
using words from Wordsdict
    '''
    line = ""
    # syllables represents the current length of line in syllables 
    syllables = 0
    while(syllables < totalSyllables) : 
#         randomly selects a word that was next to theWord in the sample 
#         text, with a higher probability for words that ppear more 
#         frequently next to theWord
        nextWordDict = Wordsdict.get(theWord)
        probabilityList = generateProbabilityList(nextWordDict)
        theWord = random.choice(probabilityList).lower()
#         continues picking words that appeared next to theWord in the
#         sample text until it finds a word that can be added to line
#         without exceeding totalSyllables
        numSyllables = checkSyllables(theWord, syllables, totalSyllables)
        while (numSyllables == 0 and len(probabilityList) != 0) : 
            theWord = random.choice(probabilityList).lower()
#         removes the word so that it doesn't waste time testing it again
            probabilityList.remove(theWord)
            numSyllables = checkSyllables(theWord, syllables, totalSyllables)
#         if probabilityList is empty, that means all the words that appear
#         next to theWord cannot fit in line without exceeding totalSyllables
        if(len(probabilityList) == 0) : 
            return False
        line += theWord + " "
        syllables += int(numSyllables)
#         Capitalize the first word in each line
    return line[0].upper() + line[1:-1]


# In[9]:


def writeline(theWord, Wordsdict, numSyl):
    '''
    repeatedly calls getLine until a valid line is generated. 
    '''
    line = getLine(theWord, Wordsdict, numSyl)
    if line == False : 
        while(line == False) : 
            line = getLine(theWord, Wordsdict, numSyl)
        return line
    else : 
        return line


# In[10]:


def writeHaiku(word):
    '''
    Write a Haiku(a 3-line poe with a syllable structure of 5-7-5)
    '''
    f = 'poems1200.txt'
    
    try:
        Wordsdict = wordFrequencies('poems1200.txt')
    except IOError:
        print("The raw file does't exist, please check the folder.")
        
    while True:
        word1 = word.lower()
        if not (word1 in Wordsdict and word1 in syllablesDict):
            word = input("Please enter a more common used word")
            continue
        else:
            break

    poem = word1[0].upper() + word1[1:]+' '
    firstWordSyllables = syllablesDict.get(word1)
#     because firstWord is part of the first line of the poem, need to subtract
#     the length of firstWord in syllables from the total syllable length of the
#     line.
    poem += writeline(word1.lower(), Wordsdict, 5 - firstWordSyllables).lower() + ','
    poem += writeline(poem[poem.rfind(' ')+1:-1], Wordsdict, 7) + ','
    poem += writeline(poem[poem.rfind(' ')+1:-1], Wordsdict, 5)
    return (poem)


# In[12]:


if __name__ == '__main__':
    main()

