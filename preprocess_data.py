# %% import modules
import pandas as pd
import numpy as np
import plotly.express as px
from datar.all import case_when, f, mutate, pivot_wider
from urllib.parse import unquote


# %%
#uploading dataset
LSMS1=pd.read_csv(r'Data/sect11b_harvestw3.csv')
LSMS1.rename(columns={'s11bq4': 'expenditure',},inplace=True)
LSMS1.dropna(subset=['expenditure'],inplace=True)

#%%
#Filtering out the required items for analysis
LSMS1_data_list=['KEROSENE', 'PALM KERNEL OIL', 'OTHER LIQUID COOKING FUEL', 'ELECTRICITY', 'CANDLES', 'FIREWOOD', 'CHARCOAL', 
                'PETROL','DIESEL']
LSMS1_List=LSMS1[LSMS1.item_desc.isin(LSMS1_data_list)]
#LSMS1_List

# %%
#Assigning names to states
LSMS_df=mutate(LSMS1_List,state_name=case_when(f.state==1,'Abia', f.state==2,'Adamawa',f.state==3,'Akwa Ibom',
                                                         f.state==4,'Anambra',f.state==5,'Bauchi',f.state==6,'Bayelsa',
                                                          f.state==7,'Benue',f.state==8,'Borno',f.state==9,'Cross River',
                                                       f.state==10,'Delta', f.state==11,'Ebonyi',f.state==12,'Edo', 
                                                        f.state==13,'Ekiti', f.state==14,'Enugu',f.state==15,'Gombe',
                                                        f.state==16,'Imo',f.state==17,'Jigawa',f.state==18,'Kaduna',
                                                          f.state==19,'Kano',f.state==20,'Katsina',f.state==21,'Kebbi',
                                                         f.state==22,'Kogi',f.state==23,'Kwara',f.state==24,'Lagos',
                                                         f.state==25,'Nasarawa',f.state==26,'Niger',f.state==27,'Ogun',
                                                         f.state==28,'Ondo',f.state==29,'Osun',f.state==30,'Oyo',
                                                         f.state==31,'Plateau',f.state==32,'Rivers',f.state==33,'Sokoto',
                                                        f.state==34,'Taraba',f.state==35,'Yobe',f.state==36,'Zamfara',
                                                         f.state==37,'FCT Abuja')
                                        #.drop(columns='state')
                                        )

#%%
#LSMS_df.to_csv('lsms_df.csv')

income_credit = pd.read_csv(r'income_credit.csv')
income_credit

#%%
data = pd.concat([LSMS_df, income_credit], join='outer')

#%%
#full_data.to_csv("predata.csv")

#%%
data_sector_name = mutate(
    data,
    sector_name=case_when(f.sector == 1, "URBAN", f.sector == 2, "RURAL"),
)#.drop(columns="sector")




#%%
full_data = data_sector_name[['lga', 'hhid', 'item_desc', 'sector_name',
                       'state_name', 'expenditure', 'income', 'credit'
                       ]]

#%%
full_data.to_csv('full_data.csv')



#%%
if full_data[full_data["state_name"]=='Oyo'].dropna()['income'].min():
  print("no value")
else:
  print("yes data")
  


#%%
len(full_data[full_data["state_name"]=='Oyo']['income'].unique())


#%%
full_data[full_data["state_name"]=='Lagos']['income'].mean()

#%%
full_data['income'].nunique()





# %%
