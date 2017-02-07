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
words     = OneOrMore(Word(alphas) | White(' ', max=1))
abl_words = OneOrMore(Word(alphas+":") | White(' ', max=1))
# http://stackoverflow.com/questions/26600333/pyparsing-whitespace-match-issues

# ArM dictionaries
characteristic = oneOf("Int Per Pre Com Str Sta Dex Qik Cun")
technique      = oneOf("Cr In Mu Pe Re")
form           = oneOf("An Au Aq Co He Ig Im Me Te Vi")

# strip trailing whitespace from multiple-word-abilities ('Artes Liberales ')
ability        = Combine(abl_words).setParseAction(lambda x: x[0].strip())
# specialisations are in brackets
specialisation = Combine(Literal("(") + words + Literal(")"))
# Puissant Art/Ability adds potential +2/+3
score          = Combine(Word(nums) + Optional(oneOf("+2 +3")))
xp             = Optional(Combine(Literal("(") + Word(nums) + Literal(")")))
value          = Combine(Optional(oneOf("+ -")) + Word(nums))

# convert all to integer
value.setParseAction(lambda t:int(t[0]))
## TODO: Puissant() cannot convert to Int
#score.setParseAction(lambda t:int(t[0]))
#xp.setParseAction(lambda t:int(t[0]))

# ArM parsing

# A “Word” is a sequence of characters surrounded by white space or punctuation.
# Combine requires the matching tokens to all be adjacent with no intervening whitespace


## ArM magus format

# first line
name = StringStart() + restOfLine().setResultsName("Name")

characteristics = Group(Suppress("Characteristics: ")
                        + delimitedList(Group(characteristic + value))
            ).setResultsName("Characteristics")#("char")

abilities = Group(Suppress("Abilities: ")
                  + delimitedList(Group(ability
                                        + score
                                        + xp
                                        + specialisation))
                          ).setResultsName("Abilities")

arts = Group(Suppress("Arts: ")
                  + delimitedList(Group(technique+score))
                  + ";"
                  + delimitedList(Group(form+score))
                  ).setResultsName("Arts")

## http://stackoverflow.com/questions/9995627/cant-get-pyparsing-dict-to-return-nested-dictionary
## nestedExpr: parser for nested lists




# all in one parser
parser = (name 
          + characteristics
          + abilities
          + arts
)




with open("test.txt", "r") as file:
    aurulentus = file.read()

#result = parser.parseFile()
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
