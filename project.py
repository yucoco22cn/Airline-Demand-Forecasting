#project Yue Yu
import os, pandas as pd, numpy as np
os.chdir("/Users/cocoyu/Dropbox/SU courses/IS5201/Project")

def airlineForecast(trainingDataFileName,validationDataFileName):
    train = pd.read_csv(trainingDataFileName, sep=',', header=0)
    valid = pd.read_csv(validationDataFileName, sep=',', header=0)
    train['departure_date'] = pd.to_datetime(train['departure_date'])
    train['booking_date'] = pd.to_datetime(train['booking_date'])
    valid['departure_date'] = pd.to_datetime(valid['departure_date'])
    valid['booking_date'] = pd.to_datetime(valid['booking_date'])

    #find the final demand
    train['final_demand']=train.groupby('departure_date',as_index=False)['cum_bookings'].transform('max')

    #find the remaining demand
    train['remain_demand']=train['final_demand']-train['cum_bookings']

    #add a new col Days_Prior
    train['Days_Prior']=train['departure_date']-train['booking_date']
   

    #add a col to show days of week
    train['day_of_week'] = train['departure_date'].dt.weekday_name
   

    #group the group the 'remaining demand' by 'day prior' AND 'day of week',get the mean
    FRD=train.groupby(['day_of_week','Days_Prior'], as_index=False)['remain_demand'].mean()
    


    #deal with the validating data
    valid['Days_Prior']=valid['departure_date']-valid['booking_date']
    valid['day_of_week'] = valid['departure_date'].dt.weekday_name
    #print(valid.head())

    ##merge the valid and FRD data
    FRDdf=pd.DataFrame(FRD)

    
    new=valid.merge(FRDdf,left_on=['Days_Prior','day_of_week'],right_on=['Days_Prior','day_of_week'])
    
    ####get the forcast data
    new['forecast']=new['remain_demand']+new['cum_bookings']
    
    #remove the days_piror=0
    new1=new[new['Days_Prior']!='0 days']
   

    #Caculate the MASE
    #1.caculate the numerator sum(A-F)
    Num=sum(abs(new1['forecast']-new1['final_demand']))
    

    #2.caculate the denominator 
    Den=sum(abs(new1['naive_forecast']-new1['final_demand']))
    

    #3. get MASE
    MASE=Num/Den
    print('MASE:'+ str(MASE))

    #The Forecast error of your model is 78.6% of that of benchmark.
    #We reduced errors by 21.4%

    #dataFrame which contains departure date, booking date, and forecasts
    Result=new1[['departure_date','booking_date','forecast']]
    print(Result)

    #MFE
    MFE=sum(new1['forecast']-new1['final_demand'])/len(new1)
    #print(MFE)
    #MAD
    MAD=sum(abs(new1['naive_forecast']-new1['final_demand']))/len(new1)
    #print(MAD)
airlineForecast('airline_booking_trainingData.csv','airline_booking_validationData_revised.csv')
#additive model
#Days_Prior=departure_date-booking_date
#FRD
#Forecast=FRD+cum_bookings
