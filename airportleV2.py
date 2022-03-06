import numpy as np
import pandas as pd
import xarray as xr

#Check if char is valid within the game (letter or ?)
def isValidChar(input: str):
    if input[0].isalpha() or input[0] == '?':
        return True
    else:
        return False

#Check if code is valid (letters or ?)
def isValidCode(input: str):
    if len(input) > 3:
        return False
    if not isValidChar(input[0]) or not isValidChar(input[1]) or not isValidChar(input[2]):
        return False
    else:
        return True

#Check if code is "???" because you are helpless if so
def isHelpless(input: str):
    if input[0] == '?' and input[1] == '?' and input[2] == '?':
        return True
    else:
        return False

#Search array on one char
def searchOnChar(input, charToSearch: str, searchCharNum: int):

    #Length wrapping
    if searchCharNum < 0:
        searchCharNum = 0
    elif searchCharNum > 2:
        searchCharNum = 2

    numID = 0 #Counter

    #Check array
    for n in input["Code"]:
        if n[searchCharNum] != charToSearch:
            input = input.drop([numID])
        numID += 1

    input = input.reset_index(drop=True) #Reset length because .drop is strange

    return input

def searchOnInvalid(input, invalidArray):

    numID = 0  # Counter

    # Check array
    for n in input["Code"]:
        if n[0] in invalidLetters or n[1] in invalidLetters or n[2] in invalidLetters:
            input = input.drop([numID])
        numID += 1

    input = input.reset_index(drop=True)  # Reset length because .drop is strange

    return input

filenames = ["airportCodes.txt"] #File names to read in
columns = ["City", "Code"] #Columns for pandas array

print("Reading in files...")

#Read files
for filename in filenames:
    dataframe = pd.read_csv(filename, header = None, delimiter="(", names=columns)

dataframe["Code"] = dataframe["Code"].str[:-1] #Delete ) from end of string
dataframe.sort_values("Code") #Sort values by code... does this do anything?

print("Welcome to Airportle Solver")
print("by William McGovern-Fagg")
print("Type 'exit' at any time to exit")
print("Read in file")

isDone = False #Flag for done

#Repeat until exited
while(not isDone):

    code = input("Please input the current airport code:").upper() #Get input

    if code == 'EXIT':
        print("Exiting!")
        isDone = True

    #Check for validity of airport code
    elif not isValidCode(code):
        print(f"{code} is not a valid airport code, please try again")
    #Check if airport code has one letter filled in
    elif isHelpless(code):
        print("You need at least one letter to be filled in")
    else:
        tempDataFrame = dataframe.copy()
        print(f"Code {code} is valid...!")
        invalidLetters = input("Please input a list of letters that cannot be in the answer").upper()
        if code[0] != '?':
            tempDataFrame = searchOnChar(tempDataFrame, code[0], 0)
        if code[1] != '?':
            tempDataFrame = searchOnChar(tempDataFrame, code[1], 1)
        if code[2] != '?':
            tempDataFrame = searchOnChar(tempDataFrame, code[2], 2)

        tempDataFrame = searchOnInvalid(tempDataFrame, invalidLetters)

        index = 0
        print("\n******************************************\n")
        while index < len(tempDataFrame["Code"]):
            print(f"{tempDataFrame['Code'][index]}: {tempDataFrame['City'][index]}")
            index += 1
        print("\n******************************************\n")
