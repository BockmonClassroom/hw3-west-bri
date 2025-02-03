import numpy
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as stats
import datetime
table1 = pd.read_csv("Data/t1_user_active_min.csv")
table2 = pd.read_csv("Data/t2_user_variant.csv")
table3 = pd.read_csv("Data/t3_user_active_min_pre.csv")
table4 = pd.read_csv("Data/t4_user_attributes.csv")

maxDate = datetime.datetime.strptime(table1['dt'].max(),"%Y-%m-%d")
experimentStartDate = datetime.datetime(2019,2,6)
# #Part 2.5 Organize Data
# #get sum of time for each uid
# t1UsersTotalTime = table1.groupby("uid")['active_mins'].sum()
# #get variant by inner joining on table2 
# t1UsersTotalTime = pd.merge(t1UsersTotalTime,table2, on= 'uid', how='inner')

# #Part 3.1 Statistical difference between variants using a t test
# t1Variant0ActiveMinutes = t1UsersTotalTime[t1UsersTotalTime['variant_number'] == 0]['active_mins']
# t1Variant1ActiveMinutes = t1UsersTotalTime[t1UsersTotalTime['variant_number'] == 1]['active_mins']

# t,p = stats.ttest_ind(t1Variant0ActiveMinutes, t1Variant1ActiveMinutes)
# print("Tvalue: ", t)
# print("Pvalue: ", p)

# #Part 3.2 Mean/Median
# v0Mean = t1Variant0ActiveMinutes.mean()
# v0Median = t1Variant0ActiveMinutes.median()
# v1Mean = t1Variant1ActiveMinutes.mean()
# v1Median = t1Variant1ActiveMinutes.median()

# print("Variant 0 Mean: ", v0Mean)
# print("Variant 0 Median: ", v0Median)
# print("Variant 1 Mean: ", v1Mean)
# print("Variant 1 Median: ", v1Median)

# #Part 4.3 Conclusion
# plt.boxplot([t1Variant0ActiveMinutes,t1Variant1ActiveMinutes],positions= [1,2], labels=['Variant0', 'Variant1'])
# plt.show()

# #Part 4.5

# #check for bad data (time greater than minutes in a day)
# badData = table1.query('active_mins > 1440')
# print(len(badData.index))

#Part 4.6
table1 = table1[table1['active_mins'] <= 1440]
#print(table1)

# #Part 4.7

t1UsersTotalTime = table1.groupby("uid")['active_mins'].sum()

t1UsersTotalTime = pd.merge(t1UsersTotalTime,table2, on= 'uid', how='inner')

# t1Variant0ActiveMinutes = t1UsersTotalTime[t1UsersTotalTime['variant_number'] == 0]['active_mins']
# t1Variant1ActiveMinutes = t1UsersTotalTime[t1UsersTotalTime['variant_number'] == 1]['active_mins']

# t,p = stats.ttest_ind(t1Variant0ActiveMinutes, t1Variant1ActiveMinutes)
# print("Tvalue: ", t)
# print("Pvalue: ", p)


# v0Mean = t1Variant0ActiveMinutes.mean()
# v0Median = t1Variant0ActiveMinutes.median()
# v1Mean = t1Variant1ActiveMinutes.mean()
# v1Median = t1Variant1ActiveMinutes.median()

# print("Variant 0 Mean: ", v0Mean)
# print("Variant 0 Median: ", v0Median)
# print("Variant 1 Mean: ", v1Mean)
# print("Variant 1 Median: ", v1Median)


#Part 5.2
table3 = table3[table3['active_mins'] <= 1440]
t3UsersTotalTime = table3.groupby("uid")['active_mins'].sum()

t1UsersTotalTime = pd.merge(t1UsersTotalTime,t3UsersTotalTime, on= 'uid', how='inner', suffixes=['_t1','_t3'])
t1UsersTotalTime['delta'] = t1UsersTotalTime['active_mins_t1'] - t1UsersTotalTime['active_mins_t3'] 

t1Variant0ActiveMinutes = t1UsersTotalTime[t1UsersTotalTime['variant_number'] == 0]['delta']
t1Variant1ActiveMinutes = t1UsersTotalTime[t1UsersTotalTime['variant_number'] == 1]['delta']

# t,p = stats.ttest_ind(t1Variant0ActiveMinutes, t1Variant1ActiveMinutes)
# print("Tvalue: ", t)
# print("Pvalue: ", p)


# v0Mean = t1Variant0ActiveMinutes.mean()
# v0Median = t1Variant0ActiveMinutes.median()
# v1Mean = t1Variant1ActiveMinutes.mean()
# v1Median = t1Variant1ActiveMinutes.median()

# print("Variant 0 Mean: ", v0Mean)
# print("Variant 0 Median: ", v0Median)
# print("Variant 1 Mean: ", v1Mean)
# print("Variant 1 Median: ", v1Median)

# plt.boxplot([t1Variant0ActiveMinutes,t1Variant1ActiveMinutes],positions= [1,2], labels=['Variant0', 'Variant1'])
# plt.show()

#Part 6
t1UsersTotalTime = pd.merge(t1UsersTotalTime,table4, on= 'uid', how='inner')
experimentLengthDays = maxDate-experimentStartDate


#average time during experiment
experimentLengthDays = maxDate-experimentStartDate
t1UsersTotalTime['active_mins_t1'] = t1UsersTotalTime['active_mins_t1'] / experimentLengthDays.days

t1UsersTotalTime['signup_date'] = pd.to_datetime(t1UsersTotalTime['signup_date'])
t1UsersTotalTime['dt'] = pd.to_datetime(t1UsersTotalTime['dt'])

# average time on site from signup to before experiment
t1UsersTotalTime['active_mins_t3'] = t1UsersTotalTime['active_mins_t3'] / ((t1UsersTotalTime['dt']- t1UsersTotalTime['signup_date']).dt.days - 1) 

#delta of average times pre and post
t1UsersTotalTime['delta'] = t1UsersTotalTime['active_mins_t1'] - t1UsersTotalTime['active_mins_t3'] 


#iterate through different user_types
groupedData = t1UsersTotalTime.groupby("user_type")
for user_type, data in groupedData:
    print("Statistics for ", user_type)
    variant0ActiveMinutes = data[data['variant_number'] == 0]['delta']
    variant1ActiveMinutes = data[data['variant_number'] == 1]['delta']
    v1 = variant1ActiveMinutes[numpy.abs(stats.zscore(variant1ActiveMinutes) < 3)]
    v0 = variant0ActiveMinutes[numpy.abs(stats.zscore(variant0ActiveMinutes) < 3)]
    t,p = stats.ttest_ind(v0, v1)
    print("Tvalue: ", t)
    print("Pvalue: ", p)
    v0Mean = v0.mean()
    v0Median = v0.median()
    v1Mean = v1.mean()
    v1Median = v1.median()
    print("Variant 0 Mean: ", v0Mean)
    print("Variant 0 Median: ", v0Median)
    print("Variant 1 Mean: ", v1Mean)
    print("Variant 1 Median: ", v1Median)
    plt.boxplot([v0,v1],positions= [1,2], labels=['Variant0', 'Variant1'])
    plt.title(user_type)
    plt.show()