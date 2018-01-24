# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 13:11:43 2018

@author: rafael

Part of the cousera assignment from data science with python project
"""
import pandas as pd

def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State", "RegionName"]  )
    
    The following cleaning needs to be done:

    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. '''
    
    with open("data/university_towns.txt") as f:
        data = f.read()
        names = list()
        for txt in data.split("\n"):
            if txt[-6:] == "[edit]":
                state = txt[:-6]
            else:
                names.append([state, txt.split("(" )[0]])
        df = pd.DataFrame(names, columns = ["States", "University Towns"])
    return df.drop(df.index.size-1)
    
def get_GDP_values(quarter = True):
    if quarter:
        GDP = pd.read_excel("data/gdplev.xlsx", "Sheet1", header = 5, skiprows = 2, parse_cols = [4,6])
        GDP.columns = ["year", "GDP"]
    else:
        GDP = pd.read_excel("data/gdplev.xlsx", "Sheet1", header = 5, skiprows = 2, parse_cols = [0,2], skip_footer=195)
        GDP.columns = ["year", "GDP"]
    return GDP
    
def detect_recession(data, cut_before_2000 = False):
    ## use data from year 2000 onwards
    if cut_before_2000:
        data = data.iloc[212:]
    
    flag1, flag2, flag3 = [False]*3
    Q1 = ""
    ## copying data and setting index
    n_data = data.copy()
    data.set_index("year", inplace = True)
    
    ## create new recession column
    data["recession"] = [False]*data.index.size
    ## get difference between lines in data
    n_data.iloc[:,1] = n_data.iloc[:,1].diff()
    ## remove first year
    n_data.iloc[0,1] = 0
    for index, frame in n_data.groupby("year"):
        if flag1 :
            if flag2 :
                if flag3 :
                    if frame.iloc[0,1] > 0:
                        data.loc[Q1:index, "recession"] = [True]*4
                    flag1 = False
                    flag2 = False
                    flag3 = False
                else:
                    if frame.iloc[0,1] > 0:
                        flag3 = True  
                    else:
                        flag1, flag2, flag3 = [False]*3
            else:
                if frame.iloc[0,1] < 0:
                    flag2 = True
                else:
                    flag2, flag3 = [False]*2
                    Q1 = index
        else:
            if frame.iloc[0,1] < 0:
                flag1 = True
                Q1 = index
            else:
                flag1, flag2, flag3 = [False]*3
                    
    return data
    
def get_recession_start():
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''
    data = detect_recession(get_GDP_values(), True)
    
    ## separate recession data
    res_data = data[data.loc[:,"recession"]].copy()
    
    ## returning the start
    start = list()
    for idx in range(0, res_data.index.size):
        if idx % 4 == 0:
            start.append(res_data.index[idx])
        
    return start
    
def get_recession_end():
    '''Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3'''
    data = detect_recession(get_GDP_values(), True)
    
    ## separate recession data
    res_data = data[data.loc[:,"recession"]].copy()
    
    ## returning the end
    end = list()
    for idx in range(0, res_data.index.size):
        if idx % 4 == 0:
            end.append(res_data.index[idx+3])
        
    return end
    
def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3'''
    data = detect_recession(get_GDP_values(), True)
    
    ## separate recession data
    res_data = data[data.loc[:,"recession"]].copy()
    res_data.reset_index(inplace = True)
    
    ## returning the end
    bottom = list()
    for idx in range(0, int(res_data.index.size/4)):
        bottom.append(res_data.iloc[res_data.iloc[4*idx:4*idx+4,1].argmin(),0])
        
    return bottom
    
def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].
    
    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.
    
    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
    
    ## reading the data
    housing_data = pd.read_csv("data/City_Zhvi_AllHomes.csv")
    
    ## getting data from year 2000 onward
    drop_cols = housing_data.loc[:,"1996-04":"1999-12"].columns
    housing_data = housing_data.drop(drop_cols, axis = 1)
    
    ## determining quarters
    quarter_data = housing_data.loc[:,["State","RegionName"]].copy()
    for period in housing_data.loc[:,"2000-01":].columns[::3]:
        year, month = period.split("-")
        if month == "01":
            ## we are in first quarter
            quarter_data[year+"q1"] = housing_data.loc[:,year+"-01":year+"-03"].sum(axis = 1)
        if month == "04":
            ## we are in second quarter
            quarter_data[year+"q2"] = housing_data.loc[:,year+"-04":year+"-06"].sum(axis = 1)
        if month == "07":
            ## we are in third quarter
            quarter_data[year+"q3"] = housing_data.loc[:,year+"-07":year+"-09"].sum(axis = 1)
        if month == "07":
            ## we are in fourth quarter
            quarter_data[year+"q4"] = housing_data.loc[:,year+"-10":year+"-12"].sum(axis = 1)
    return quarter_data.set_index(["State","RegionName"])



if __name__ == "__main__" :
    quarter_data = convert_housing_data_to_quarters()
    
