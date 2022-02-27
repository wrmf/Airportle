import numpy as np
import pandas as pd
import xarray as xr

def isValidChar(input: str):
    if input[0].isalpha() or input[0] == '?':
        return True
    else:
        return False

def isValidCode(input: str):
    if len(input) > 3:
        return False
    if not isValidChar(input[0]) or not isValidChar(input[1]) or not isValidChar(input[2]):
        return False
    else:
        return True

def isHelpless(input: str):
    if input[0] == '?' and input[1] == '?' and input[2] == '?':
        return True
    else:
        return False

def searchOnChar(input, charToSearch: str, searchCharNum: int):

    if searchCharNum < 0:
        searchCharNum = 0
    elif searchCharNum > 2:
        searchCharNum = 2

    numID = 0

    for n in input["Code"]:
        if not len(n) > 0:
            pass
        elif n[searchCharNum] != charToSearch:
            input = input.drop([numID])
        numID += 1

    input = input.reset_index(drop=True)

    return input





filenames = ["airportCodes.txt"]
columns = ["City", "Code"]

print("Reading in files...")

for filename in filenames:
    dataframe = pd.read_csv(filename, header = None, delimiter="(", names=columns)

dataframe["Code"] = dataframe["Code"].str[:-1]
dataframe.sort_values("Code")

print("Welcome to Airportle Solver")
print("by William McGovern-Fagg")
print("Type 'exit' at any time to exit")
print("Read in file")

isDone = False

while(not isDone):
    code = input("Please input the current airport code:").upper()
    if code == 'EXIT':
        isDone = True

    #Check for validity of airport code
    if not isValidCode(code):
        print(f"{code} is not a valid airport code, please try again")
    #Check if airport code has one letter filled in
    elif isHelpless(code):
        print("You need at least one letter to be filled in")
    else:
        tempDataFrame = dataframe.copy()
        print(f"Code {code} is valid... Searching!")
        if code[0] != '?':
            tempDataFrame = searchOnChar(tempDataFrame, code[0], 0)
        if code[1] != '?':
            tempDataFrame = searchOnChar(tempDataFrame, code[1], 1)
        if code[2] != '?':
            tempDataFrame = searchOnChar(tempDataFrame, code[2], 2)

        index = 0
        while index < len(tempDataFrame["Code"]):
            print(f"{tempDataFrame['Code'][index]}: {tempDataFrame['City'][index]}")
            index += 1
