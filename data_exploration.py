
#############################################
#           Kaggle Competition     			    
# 	  San Francisco Crime Classification     
#         Started in November 2015          
#                                           
#           LUISADA Marie-Laura             
#############################################


##### DATA EXPLORATION ######


### Load data and libraries

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

train = pd.read_csv("train.csv", sep = ",")

# get number of rows
nrow = len(train.index)


###########################
### Categories of crime ###
###########################


#In this section, we aggregate some categories of crimes (initally 39) into 16 more global categories. 
#Indeed, this will be easier to visualize some potential relationships

# summary of variable Category
train.Category.describe()

# occurence of the observations
train.Category.value_counts()

# aggregate crimes into several categories : it is an arbitrary choice but still very useful
crime_dict = {
    'THEFT':['LARCENY/THEFT','VEHICLE THEFT','STOLEN PROPERTY','RECOVERED VEHICLE'],
    'ROBBERY':['ROBBERY'],
    'DRUGS':['DRUG/NARCOTIC'],
    'ALCOHOL':['DRUNKENNESS', 'DRIVING UNDER THE INFLUENCE','LIQUOR LAWS',],
    'VIOLENCE':['WEAPON LAWS','ASSAULT', 'OTHER OFFENSES','FAMILY OFFENSES'],
    'FRAUD':['FRAUD', 'FORGERY/COUNTERFEITING','EMBEZZLEMENT', 'BAD CHECKS'], 
    'DEATH':['SUICIDE'], 
    'VANDALISM':['VANDALISM'],
    'FIRE':['ARSON'],
    'PROPERTY': ['WARRANTS', 'TRESPASS','BURGLARY', 'TREA'],
    'SEX':['PORNOGRAPHY/OBSCENE MAT', 'PROSTITUTION','SEX OFFENSES FORCIBLE'],
    'MISSING':['MISSING PERSON', 'KIDNAPPING', 'RUNAWAY'],
    'MISCONDUCT':['LOITERING', 'DISORDERLY CONDUCT', 'SEX OFFENSES NON FORCIBLE', 'SUSPICIOUS OCC'],
    'CORRUPTION':['BRIBERY'],
    'OTHER':['GAMBLING','SECONDARY CODES','EXTORTION'],
    'NON-CRIMINAL':['NON-CRIMINAL']
    }





# get list of categories of crimes
crime_values = []
for i in range(len(crime_dict.keys())):
    crime_values += list(crime_dict.values())[i]
print(crime_values) 
print(len(crime_values))


agg_Category = []
for i in range(nrow):
    if train.Category[i] not in crime_values:
        agg_Category.append('OTHER')
    else:
        for key in list(crime_dict.keys()):
            if train.Category[i] in crime_dict[key]:
                agg_Category.append(key)
    

# add column to data frame
train['agg_Category'] = agg_Category



##############################
### Descriptive statistics ###
##############################

#We first summarize these categories of crimes using graphs (histograms, pies). 
#Then we segment it by neighborhood or by month of the year or day in the week


### GLOBAL
## How many crimes happened from the beginning ? 
## What is the proportion of each type of crimes ?



### PER LOCATION
## How many crimes occured in each neighborhood ? 
## What type of crimes ?

train.PdDistrict.value_counts()


# number of crimes for each neigborhood (histogram for ex with % !!)



# map and color neighborhood (red means "high percentage of crimes", yellow not many)



# build an histograms per neighborhood with the occurrence of different types of crime
# For example, in Richmond, 10% of crimes were DRUG, 24% were ROBBERY etc
# give a contingency table too (maybe too big)




# map of types of crimes using coordinates. Project each observation on the geographical coordinates. 
# I doubt we might find something interting but we should try





### PER TIME
## When do crimes mostly happen ? 

# create list of months / days related to the dates in the tableau


# Histogram : count percentage of crimes which happen on Monday versus Tuesday etc


# Lines : per month (maybe detect a seasonal effect?)



#If there is a month or day when crimes tend to happen more frequently, analyze which type of crimes.




#### Export data table into csv file
# export document as a csv file
f = csv.writer(open("train_v1.csv","w"))
# write column names
f.writerow(list(train.columns.values))
for i in range(nrow):
    f.writerow(list(train.ix[i]))
