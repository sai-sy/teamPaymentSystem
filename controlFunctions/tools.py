from operator import index
from os import path, chdir
import sys
import pandas as pd

def deleteNaN(mylist):
    newlist = [x for x in mylist if pd.isnull(x) == False]
    return newlist

def setWorkingDirectoryToSelf():
    '''Sets working directory to the directory of this script'''
    abspath = path.abspath(sys.argv[0])
    dname = path.dirname(abspath)
    chdir(dname)

def loadSheetAsDf(filename, sheet) -> pd.DataFrame:
    filenameSplit, filename_extension = path.splitext(filename)
    if filename_extension == '.csv':
        df =  pd.read_csv(filename, sheet, engine='python', index=False)
    else:
        df = pd.read_excel(filename, sheet)
    return df

def returnUniqueValues(df: pd.DataFrame, columnName):
    series = pd.Series(df[columnName])
    values = [] 
    for item in series:
        if item in values:
            continue
        else:
            values.append(item)
    
    return deleteNaN(values)

def main():
    df = pd.DataFrame({'name': ['Akash', 'Ayush', 'Ashish',
                            'Diksha', 'Shivani', 'Ayush'],
                     
                   'Age': [21, 25, 23, 22, 18, 14],
                     
                   'MotherTongue': ['Hindi', 'English', 'Marathi',
                                    'Bhojpuri', 'Oriya', 'French']})
  
    print("The original data frame")
    print(returnUniqueValues(df, 'name'))

if __name__ == '__main__':
    main()