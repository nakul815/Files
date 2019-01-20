# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 15:34:41 2019

@author: nakul
"""

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

os.chdir("C:/Nakul/UCLA Coursework/5. Fall 2018/Full Time/Lending CLub/Case Study/Payments_Made_to_Investors_2019_01")

#Reading Data
mylist = []

for chunk in  pd.read_csv('PMTHIST_INVESTOR_201901.csv', chunksize=20000, low_memory=False):
    mylist.append(chunk)

big_data = pd.concat(mylist, axis= 0)
del mylist

#Copying Original Data

original_data=big_data.copy()
big_data.shape
big_data.head()

#Exploring Data
a=big_data.loc[big_data['LOAN_ID']==54734]

###################################################
#Fully Paid
fully_paid_loans=big_data.loc[big_data['PERIOD_END_LSTAT']=='Fully Paid'].drop_duplicates()
fully_paid_loans.IssuedDate = pd.to_datetime(fully_paid_loans.IssuedDate)
fully_paid_loans['Issued_Yr'] = fully_paid_loans.IssuedDate.dt.year
f1=fully_paid_loans.head(20)

## Term 36 months
fpaid_36m=fully_paid_loans.loc[fully_paid_loans['term']==36]
fpaid_60m=fully_paid_loans.loc[fully_paid_loans['term']==60]

fpaid_36m['grade'].value_counts() #Number of loan given by grade
fpaid_60m['grade'].value_counts() #Number of loan given by grade

#Fetching Issue Year
fpaid_36m.IssuedDate = pd.to_datetime(fpaid_36m.IssuedDate)
fpaid_36m['Issued_Yr'] = fpaid_36m.IssuedDate.dt.year
fpaid_36m['Issued_Yr'].plot.hist()

fpaid_60m.IssuedDate = pd.to_datetime(fpaid_60m.IssuedDate)
fpaid_60m['Issued_Yr'] = fpaid_60m.IssuedDate.dt.year
fpaid_60m['Issued_Yr'].plot.hist()


# Interest Rates by different features
fully_paid_loans.groupby("term")["InterestRate"].mean() #Overall
fully_paid_loans.groupby(["term","Issued_Yr"])["InterestRate"].mean() #Overall

#######################

## Loan Returns by grade and year for 36 month loans

rate_36 = pd.pivot_table( fpaid_36m,index=["grade","Issued_Yr"],values=["InterestRate"], aggfunc=np.mean)
rate_36 = rate_36.reset_index()
rate_36.head(2)

g = sns.FacetGrid(rate_36, col = 'grade', col_wrap = 4)
g = g.map(sns.pointplot,"Issued_Yr","InterestRate")

labels = np.arange(2007, 2018, 1)
labels = [str(i) for i in labels]
g = g.set_xticklabels(labels, rotation=70)
g = g.set_ylabels("3yr loans interest rate")

plt.subplots_adjust(top=0.9)
g.fig.suptitle('Interest Rate of 36 months loan over time and grade')

## Loan Returns by grade and year for 60 month loans

rate_60 = pd.pivot_table( fpaid_60m,index=["grade","Issued_Yr"],values=["InterestRate"], aggfunc=np.mean)
rate_60 = rate_60.reset_index()
rate_60.head(2)

g = sns.FacetGrid(rate_60, col = 'grade', col_wrap = 3)
g = g.map(sns.pointplot,"Issued_Yr","InterestRate")

labels = np.arange(2007, 2018, 1)
labels = [str(i) for i in labels]
g = g.set_xticklabels(labels, rotation=70)
g = g.set_ylabels("interest rate")

plt.subplots_adjust(top=0.9)
g.fig.suptitle('Interest Rate of 60 months loan over time and grade')


##################################

##Unique Loans 
unique_loans=big_data[['LOAN_ID','grade','term','EmploymentLength','State','IssuedDate','HomeOwnership']].drop_duplicates()
loan_ids2.loc[loan_ids2['grade']=='A']

#Charged Off loans

coff_loans=big_data.loc[big_data['PERIOD_END_LSTAT']=='Charged Off'].drop_duplicates()
coff_loans.IssuedDate = pd.to_datetime(coff_loans.IssuedDate)
coff_loans['Issued_Yr'] = coff_loans.IssuedDate.dt.year
c1=coff_loans.head(20)

#Percentage Charge-Offs by Grade
cvalues=coff_loans['grade'].value_counts().sort_index()/loan_ids2['grade'].value_counts().sort_index()
#tvalues=loan_ids2['grade'].value_counts().sort_index()
#pd.merge(cvalues,tvalues)

#Charged-off Loans by Year
coff_loans.groupby("term")["grade"].value_counts().sort_index() #Overall
coff_loans.groupby("term")["grade"].value_counts().sort_index() #Overall

#####################################


big_data.loc[big_data['grade']=='A']

a2=big_data.loc[big_data['LOAN_ID']==66128]
a2=big_data.loc[big_data['LOAN_ID']==40]

big_data['PERIOD_END_LSTAT'].unique()

