# -*- coding: utf-8 -*-
"""
Ars Magica Character Parser

let's see what I can do...
"""

#import pyparsing as pyp
#from pyparsing import Word, alphas, nums, Suppress, LineEnd, OneOrMore, commaSeparatedList, oneOf, StringStart, restOfLine, Keyword
from pyparsing import *

#%%

import os
os.getcwd()
#os.chdir("D:\\github\\vampire")
os.chdir("/home/csafferling/Documents/github/ArMparser")

# read Aurutentus data 
with open("aurulentus.txt", 'r') as file:
    aurulentus = file.read()
    # first line
    #aurulentus_name = file.readline().strip()
    # everything but the first
    #aurulentus_stats = "".join(file.readlines()[1:])


with open("test.txt", "r") as file:
    aurulentus = file.read()



#%%

# ease of use
word = Word(alphas)
words = OneOrMore(Word(alphas))#Word(alphas + " ")# OneOrMore(word)
# http://stackoverflow.com/questions/26600333/pyparsing-whitespace-match-issues
combWords = Combine(OneOrMore(Word(alphas) | White(' ',max=1) + ~White()))

# ArM dictionaries
# check pyparser.Dict
characteristic = oneOf("Int Per Pre Com Str Sta Dex Qik Cun")
technique      = oneOf("Cr In Mu Pe Re")
form           = oneOf("An Au Aq Co He Ig Im Me Te Vi")

#value = Word(nums+"+-")
value = Combine(Optional(oneOf("+ -")) + Word(nums))
# score+xp: e.g. "5(20)"
score = Combine(Word(nums)+Optional(oneOf("+2 +3")))
xp    = Optional(Suppress("(")+nums+Suppress(")"))

# Combine requires the matching tokens to all be adjacent with no intervening whitespace
ability        = combWords#Combine(words)
specialisation = Literal("(")+Word(alphas)+Literal(")")
#Optional(Combine(Literal("(")+words+Literal(")")))

# convert all to integer
value.setParseAction(lambda t:int(t[0]))
## TODO: Puissant() cannot convert to Int
#score.setParseAction(lambda t:int(t[0]))
xp.setParseAction(lambda t:int(t[0]))

# ArM parsing

# A “Word” is a sequence of characters surrounded by white space or punctuation.



## ArM magus format

# first line
name = StringStart()+restOfLine().setResultsName("Name") #OneOrMore(word)+LineEnd()

characteristics = Group(Suppress("Characteristics: ")
                        +delimitedList(characteristic+value)
            ).setResultsName("Characteristics")#("char")

abilities = Group(Suppress("Abilities: ")
                  #+delimitedList(ability+score+xp+specialisation)
                  +delimitedList(ability+score+xp)
            ).setResultsName("Abilities")



## http://stackoverflow.com/questions/9995627/cant-get-pyparsing-dict-to-return-nested-dictionary
## nestedExpr: parser for nested lists





# all in one parser
parser = (
    name 
    + characteristics
    + abilities
)

#result = parser.parseFile()


with open("test.txt", "r") as file:
    aurulentus = file.read()

result = parser.parseString(aurulentus)
print(result)
#result["Abilities"]








#%%

   
    

# integer = Word(nums).setParseAction(convertIntegers)
# intNumber = Word(nums).setParseAction( lambda s,l,t: [ int(t[0]) ] )
#def convertNumber(t):
#    """Convert a string matching a number to a python number"""
#    if t.float1 or t.float2 or t.float3 : return [float(t[0])]
#    else                                : return [int(t[0])  ]
#number.setParseAction(convertNumber)