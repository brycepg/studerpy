# -*- coding: utf-8 -*-
"""
#  Version  2.1  june 2020
#  Moix P-O
#  Copyright Albedo-Engineering WWW.ALBEDO-ENGINEERING.COM
#

File: xt_all_datalog_viewer_pandas.py
Description: Convert multiple CSVs to pickled dataframes for graphing
"""


# reset of the workspace and close all existing figures
# from IPython import get_ipython
# get_ipython().magic('reset -sf')
# separate figures: %matplotlib qt


# import the necessary modules:
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.collections as collections

import tkinter as tk
from tkinter import filedialog

# import datetime
import time
import os


# import the function to convert each datalog file:
# from xt_log_day_import import xt_log_day_import
from xt_daylog_pandas_import import xt_daylog_pandas_import


# close all existing figures at start
plt.close("all")


# OPTIONS:
user_delimiter = ","  # ',' for english Excel display and ';' for french Excel option change in the RCC
# user_delimiter=';'  # ',' for english Excel display and ';' for french Excel option change in the RCC
# print('In case of error: have you checked the .csv delimiter? ')

user_delimiter = "[,|;]"  # for all types of files. work only with python engine in csv_read, to accelerate and use c engine, use a single delimiter

# Output Dataframe names for storage
MIN_DATAFRAME_NAME = "saved_dataframe_log_min"
QUARTERS_DATAFRAME_NAME = "saved_dataframe_log_quarters"
DAY_DATAFRAME_NAME = "saved_dataframe_log_day"
MONTH_DATAFRAME_NAME = "saved_dataframe_log_month"
YEAR_DATAFRAME_NAME = "saved_dataframe_log_year"

DAY_KWH_DATAFRAME_NAME='saved_dataframe_kWh_day'
MONTH_KWH_DATAFRAME_NAME='saved_dataframe_kWh_month'
YEAR_KWH_DATAFRAME_NAME='saved_dataframe_kWh_year'


def main():
    """Entry point for standalone usage"""
    # ***************************************
    # task 1: Choose the first .csv file
    # ****************************************

    # the dialog window to select the first file to import:
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    run(file_path)


def run(file_path):
    """API entrypoint

    Args:
        file_path(str): file path from which to start the import process"""
    filename = os.path.split(file_path)[1]
    folder_path = os.path.split(file_path)[0]

    ##the old way:
    # file_path_split=file_path.split('/')
    # filename=file_path_split[len(file_path.split('/'))-1]
    # folder_path=file_path[:-12]

    # path_name=file_path_split[0:len(file_path.split('/'))-1]
    # format LG180402.CSV

    # The date is at the end of the name:
    year_f = filename[-10:-8]
    month_f = filename[-8:-6]
    day_f = filename[-6:-4]
    headfilename = filename[:-10]

    print(file_path)

    # timing to optimize the code:
    start_time = old_time = time.time()

    #### TESTS of imports with pandas:
    #
    # mydateparser=lambda x: pd.datetime.strptime(x, "%d.%m.%Y %H:%M")
    #
    # pandatest = pd.read_csv(file_path,
    #                        encoding="ISO-8859-1",
    #                        delimiter=user_delimiter,
    #                        header=[0,1,2],
    #                        nrows=1440,
    #                        parse_dates=True,
    #                        date_parser=mydateparser,
    #                        index_col=0,
    #                        engine='c')
    #
    ##index_col=0,   index_col=False , index_col=None
    ##encoding="cp1252" "utf-8"
    ##skiprows=range(1, 10))
    #
    #
    #
    # print(pandatest.head(5))
    # print(" ")
    # pandatest.iloc[[2], [3]] #point one element to see
    # pandatest.index  #to see the time index of each line
    # pandatest.columns #to see the label of each column
    #
    ##theres is a unexpllanable shift with the labels of colums,
    ## no explaination, turn around to avoid it
    ##merge of the first three lines of headers:
    #
    #
    # newlabels=[]
    # for elem in list(pandatest.columns[1:]):
    #    print(elem[0] + ' ' +elem[1] + ' ' + elem[2])
    #    newlabels.append(elem[0] + ' ' +elem[1] + ' ' + elem[2])
    #    pandatest.columns[1:]
    #
    #
    ##selected_columns = pandatest.columns[0:len(pandatest.columns)-2]
    #
    #
    # datalog_values=pandatest.values[:,0:len(newlabels)]
    ##datalog_values[:,0:len(newlabels)]
    #
    #
    # daylog_df_test= pd.DataFrame(datalog_values,
    #                        index=pandatest.index,
    #                        columns=newlabels)
    #
    # print(daylog_df_test.head(5))
    #

    ##plot all the channels with battery voltage:
    # chanel_number = [i for i, elem in enumerate(newlabels) if 'Ubat' in elem]
    # fig100=plt.figure(100)
    #
    # daylog_df.plot(y=daylog_df.columns[chanel_number],figsize=(15,5))
    # plt.title('All Battery Voltages', fontsize=16, weight="bold")
    # plt.ylabel('Voltage [V]', fontsize=12)
    # plt.grid(True)

    # plot manually the channels with battery voltage:
    #
    # fig10=plt.figure(10)
    # plt.clf()
    # plt.plot(daylog_df.index, daylog_df.values[:,13], 'b')
    # plt.plot(daylog_df.index, daylog_df.values[:,35], 'g')
    # plt.plot(daylog_df.index, daylog_df.values[:,0], 'r')
    #
    # plt.xlabel('Time (days)', fontsize=12)
    # plt.ylabel('Voltage [V]', fontsize=12)
    # plt.title('Battery Voltage', fontsize=18, weight="bold")
    # plt.grid(True)
    #
    # fig10.legend(['mesure XT', 'mesure BSP', 'xt min'])
    # plt.show()

    # df.plot(subplots=True, figsize=(15,6))
    # df.plot(y=["R", "F10.7"], figsize=(15,4))
    # df.plot(x="R", y=["F10.7", "Dst"], style='.')
    #

    # ***************************************
    # task 2: Read and load results of the first .csv file
    # ****************************************
    if filename[0:2] == "nx":
        offsetcolumn = 0
    else:
        offsetcolumn = 1

    # day_datalog=xt_log_day_import(file_path, user_delimiter)
    daylog_df = xt_daylog_pandas_import(file_path, user_delimiter, offsetcolumn)

    # set that first element in the list of all days (if ther are many)
    # all_datalogs=[day_datalog]
    all_datalogs_df = [daylog_df]
    # all_datalogs_df.append(daylog_df)

    new_time = time.time()
    print("--- %s seconds ---" % (new_time - old_time))
    old_time = new_time
    print(" \n ")

    #%***************************************
    #% task 3: Check if they are other days after this one in the same folder (.csv file)
    #%****************************************
    #%start from the selected file date:
    last_cvs_filename_used = filename

    year_string = [
        "08",
        "09",
        "10",
        "11",
        "12",
        "13",
        "14",
        "15",
        "16",
        "17",
        "18",
        "19",
        "20",
        "21",
        "22",
        "23",
        "24",
        "25",
    ]  # until 2025 is enough for now...

    month_string = [
        "01",
        "02",
        "03",
        "04",
        "05",
        "06",
        "07",
        "08",
        "09",
        "10",
        "11",
        "12",
    ]

    day_string = [
        "01",
        "02",
        "03",
        "04",
        "05",
        "06",
        "07",
        "08",
        "09",
        "10",
        "11",
        "12",
        "13",
        "14",
        "15",
        "16",
        "17",
        "18",
        "19",
        "20",
        "21",
        "22",
        "23",
        "24",
        "25",
        "26",
        "27",
        "28",
        "29",
        "30",
        "31",
        "32",
    ]
    number_of_files = 1
    files_with_problems=[]

    for year in year_string:
        for month in month_string:
            for day in day_string:
                cvs_filename = headfilename + year + month + day + ".CSV"
                cvs_path = folder_path + "/" + cvs_filename

                # one more test to take only newer files than the one selected:
                first_file_date = str(year_f) + str(month_f) + str(day_f)
                test_date = year + month + day

                if int(test_date) > int(first_file_date):
                    file_exist = True
                    try:
                        f = open(cvs_path)
                        f.close()
                    except IOError:
                        # print('File ', cvs_filename, ' is not accessible')
                        file_exist = False

                    if file_exist is True:
                        # print('File ', cvs_path, ' is accessible')
                        print("File ", cvs_filename, " processed")
                        # day_datalog=xt_log_day_import(cvs_path, user_delimiter)
                        try:
                            daylog_df2 = xt_daylog_pandas_import(
                                cvs_path, user_delimiter, offsetcolumn
                            )
                            
                            #TODO: check of the size and coherence of the data 
                            #print(
                            #    " \n XX COHERENCE PROBLEM with File ",
                            #    cvs_filename,
                            #    "     XXXXXXXXX    \n ",
                            #)
                            # Add that day to the other datalogs in the list of datalogs
                            # all_datalogs.append(day_datalog)
                            
	                        #Add that day to the other datalogs in the list of datalogs
                            all_datalogs_df.append(daylog_df2)
                            number_of_files += 1
                        except:
                            print(
                                " \n XXXXXXXXX IMPORT PROBLEM with File ",
                                cvs_filename,
                                "     XXXXXXXXX    \n ",
                            )
                            files_with_problems.append(cvs_filename)

    print('\n Import finished, check corrupted files: ' , files_with_problems)

    #%***************************************
    #% task 4: Concatenate those datas in one array
    #%****************************************
    # Concatenate those data
	
    print(" \n__________ Check Validity and concatenate data   ")

	
    #To simplifiy for the moment, let's say there is 1440 min per day in a file, else reject. There is no NaN in file:
    #TODO: improve acceptance of valid data even if day is not full
        
    ref_df=all_datalogs_df[0]
    all_datalogs_list_cleaned_df=all_datalogs_df



    ##########
    clean_necessary=False
    indexes_to_remove=[]
    
    #supress1=0
    #supress2=0
    #supress3=0
    
    for i, tested_df in enumerate(all_datalogs_df):
        
        
        if len(tested_df)!=1440:
            clean_necessary=True
            indexes_to_remove.append(i)
            print(' tested ', str(i), '  missing data at end of file, check: ', str(tested_df.index[1])[0:10])
     
    
        elif np.isnan(tested_df.values[:,0]).any():
        #check that the first column is full of float numbers
             clean_necessary=True
             indexes_to_remove.append(i)
             print(' tested ', str(i), '  NaN in first column, check file of: ', str(tested_df.index[1])[0:10])
             #supress3+=1
             
    #    elif len(tested_df.columns)!=len(ref_df.columns):
    #        #try with any
    #         #print(' tested ', str(i), '  for concat NOT  OK')
    #         clean_necessary=True
    #         indexes_to_remove.append(i)
    #         supress1+=1
    #        ##print(' tested ', str(i), '  for concat')
    #        #if np.all(tested_df.columns==ref_df.columns):
    #        #     print(' tested ', str(i), '  for concat OK')
    #        #else:
    #        #     print(' tested ', str(i), '  for concat NOT  OK')
    #        #     clean_necessary=True
    #        #     indexes_to_remove.append(i)
    #        
    #    elif len(tested_df)!=1440:
    #        clean_necessary=True
    #        indexes_to_remove.append(i)
    #        print(' tested ', str(i), '  day has not 1440 min')
    #        supress2+=1
    
         
           
                 
    #suppress the days with problems (starting from the end else the indexes turn wrong)
    for k in reversed(indexes_to_remove):
        del all_datalogs_list_cleaned_df[k]
       
        
    
    #if clean_necessary:
    #    print(' \n XXXXXXXXX PROBLEM WITH CHANGING DATALOGS! NOT ALL ARE CONCATENATED     XXXXXXXXX    \n ')
    #    
    #    
    


    
    ##########################
    #Cleaning finished, we can assemble the multi days:                     
    #total_datalog_df=pd.concat(all_datalogs_df)  #concatenate all the daily dataFrames imported in a single one
    #total_datalog_df=pd.concat(all_datalogs_list_cleaned_df)  #concatenate all the daily dataFrames imported in a single one
    total_datalog_df=pd.concat(all_datalogs_list_cleaned_df, sort=True)  #concatenate all the daily dataFrames imported in a single one

    
    
    
    
    
    print("\n \n________________ ")
    print("DATA CLEANING ")
    #***************************************
    # task 5: Cleaning of data
    #****************************************      
    #there are often holes in the datas, with 0 instead of real datas
    #not so important for most of the values but for battery levels it is not OK
    #replace it with the value of the minute before.
    
    
    print("  CLEANING OF DATA FOR BATTERIES with 0V mesurements   ")
    
    channels_labels=list(total_datalog_df.columns)
    
    #scan for channels with Ubat in the name:
    #'BSP-Ubat [Vdc] I7030 1'
    #'XT-Ubat [Vdc] I3092 L1-1'
    #'VS-Ubat [Vdc] I15054 1'
    #'VT-UbaM [Vdc] I11039 1'
    #chanel_number_for_Ubat = [i for i, elem in enumerate(channels_labels) if 'Ubat' in elem]
    chanel_number_for_Ubat = [i for i, elem in enumerate(channels_labels) if ('Ubat' in elem )
                                                                            or ('I3092' in elem) 
                                                                            or ('I15054' in elem) 
                                                                            or ('I11039' in elem)]
    
    #REPLACE 0 values with previous value
    for chan in chanel_number_for_Ubat:
        k=0
        for tested_value in total_datalog_df.values[:,chan]:
            if tested_value<1.0:
                total_datalog_df.values[k,chan]=total_datalog_df.values[k-1,chan]
                if total_datalog_df.columns[chan]!='BSP-Ubat [Vdc] I7030 1':
                    print("Error in batt voltage ")  #if bsp missing, it gives an message for every minute
            k+=1   
                
    
    

    print("  PROCESS DATA FOR TRANSFERT RELAY  ")
    #REPLACE 2 values (undetermined) with 0.5 to estimate the transfert time
    #if there were a switch over during this minute, lets consider the transfer was like previously...
    #'XT-Transfert [] I3020 L1',   
    #Done only on the L1 which is transfer master in the system. 
    
    
    chanel_number_for_transfer=[i for i, elem in enumerate(channels_labels) if 'I3020 L1' in elem]
    
    #Check it is not empty: (for the case with solar chargers only)
    if chanel_number_for_transfer:
        k=0
        for tested_value in total_datalog_df.values[:,chanel_number_for_transfer[0]]:
            if tested_value>1.5:
                total_datalog_df.values[k,chanel_number_for_transfer[0]]=total_datalog_df.values[k-1,chanel_number_for_transfer[0]]
                #print("Transfer transition ")
            k+=1   
    
        #un deuxième check à cause des changement de langue pendant la vie de l'installation:
        if len(chanel_number_for_transfer)>1:
            k=0
            for tested_value in total_datalog_df.values[:,chanel_number_for_transfer[1]]:
                if tested_value>1.5:
                    total_datalog_df.values[k,chanel_number_for_transfer[1]]=total_datalog_df.values[k-1,chanel_number_for_transfer[1]]
                    #print("Transfer transition ")
                k+=1   
        
    
    
    #print(" ")
    print("  CLEANING OF MESURED POWER: ZERO on Pin and Iin in when there is no transfer...   ")
    
    
    #If the transfer relay is open, the input power and current is forced to zero:
    #     'XT-Iin [Aac] I3116 L1'  / L2 L3
    #     'XT-Pin a [kW] I3119 L1-1'  /  L1-2 L1-3 L2-2 ...
    
    chanel_number_for_Iin=[i for i, elem in enumerate(channels_labels) if 'I3116' in elem]
    chanel_number_for_Pin=[i for i, elem in enumerate(channels_labels) if 'I3119' in elem]
    
    
   #Check it is not empty to be sure there is an XT: for the case with solar chargers only:
    if chanel_number_for_Pin:
        
        for chan in chanel_number_for_Iin+chanel_number_for_Pin:
            k=0    
            for tested_value in total_datalog_df.values[:,chanel_number_for_transfer[0]]:
                if tested_value==0.0:
                    #total_datalog_df.values[k,chanel_number_for_Iin[m]]=0.0    
                    total_datalog_df.values[k,chan]=0.0    
                    #print("Transfer open, clean chan " , str(chan))
                k+=1
    
        #un deuxième check à cause des changement de langue pendant la vie de l'installation:
        if len(chanel_number_for_transfer)>1:  
            for chan in chanel_number_for_Iin+chanel_number_for_Pin:
                k=0    
                for tested_value in total_datalog_df.values[:,chanel_number_for_transfer[1]]:
                    if tested_value==0.0:
                        #total_datalog_df.values[k,chanel_number_for_Iin[m]]=0.0    
                        total_datalog_df.values[k,chan]=0.0    
                        #print("Transfer open, clean chan " , str(chan))
                    k+=1
     
            ##Clean of inputs currents: there are up to 3 in an system, one per phase
            #for chan in chanel_number_for_Iin:
            #    k=0    
            #    for tested_value in total_datalog_df.values[:,chanel_number_for_transfer[0]]:
            #        if tested_value==0.0:
            #            #total_datalog_df.values[k,chanel_number_for_Iin[m]]=0.0    
            #            total_datalog_df.values[k,chan]=0.0    
            #            #print("Transfer open ")
            #        k+=1
            #        
            ##Clean of inputs powers: there are up to 9 in an system, one per xtender
            #for chan in chanel_number_for_Pin:
            #    k=0    
            #    for tested_value in total_datalog_df.values[:,chanel_number_for_transfer[0]]:
            #        if tested_value==0.0:
            #            #total_datalog_df.values[k,chanel_number_for_Iin[m]]=0.0    
            #            total_datalog_df.values[k,chan]=0.0    
            #            #total_datalog_df.values[k,chanel_number_for_Pin[m]]=0.0
            #            #print("Transfer open ")
            #        k+=1
                
                
    

    print("  CLEANING OF MESURED POWER: ZERO on Pout and Iout in when inverter is OFF... ")
        ##If the Xtender is OFF the output current and powers are zero 
        ##       'XT-Modus [] I3028 L1',
        ##       'XT-Pout [kVA] I3098 L1',
        ##       'XT-Pout+ [kVA] I3097 L1',
        ##       'XT-Pout a [kW] I3101 L1-1',
        ##    
        #
        
        #TODO: speed-up that part, it takes time for multi units system.
    
   
    chanel_number_for_XTmode=[i for i, elem in enumerate(channels_labels) if 'I3028' in elem]
      
    
        
        
    chanel_number_for_Pout_s=[i for i, elem in enumerate(channels_labels) if 'I3098' in elem]
    chanel_number_for_Pout_smax=[i for i, elem in enumerate(channels_labels) if 'I3097' in elem]
    chanel_number_for_Pout_a=[i for i, elem in enumerate(channels_labels) if 'I3101' in elem]
    
        #Check it is not empty to be sure there is an XT: for the case with solar chargers only:
    if chanel_number_for_XTmode:
    
        for chan in chanel_number_for_Pout_s+chanel_number_for_Pout_smax+chanel_number_for_Pout_a:
            k=0    
            for tested_value in total_datalog_df.values[:,chanel_number_for_XTmode[0]]:
                if tested_value==6.0:
                    #total_datalog_df.values[k,chanel_number_for_Iin[m]]=0.0    
                    total_datalog_df.values[k,chan]=0.0    
                    #print("Inverter OFF, clean chan " , str(chan))
                k+=1
    
        #un deuxième check à cause des changement de langue pendant la vie de l'installation:
        if len(chanel_number_for_transfer)>1:  
            for chan in chanel_number_for_Pout_s+chanel_number_for_Pout_smax+chanel_number_for_Pout_a:
                k=0    
                for tested_value in total_datalog_df.values[:,chanel_number_for_XTmode[1]]:
                    if tested_value==6.0:
                        #total_datalog_df.values[k,chanel_number_for_Iin[m]]=0.0    
                        total_datalog_df.values[k,chan]=0.0    
                        #print("Inverter OFF, clean chan " , str(chan))
                    k+=1
        
    
        
    #    si xt mode ==6 c'est OFF; 
    
        #
        #if len(chanel_number_for_XTmode)>1:
        #    #raise Exception('CHANGEMENT LANGUE PAS TRAITE CORRECTEMENT NI MULTI UNITS! DEMULTIPLICATION DES CANAUX CONSTATEE!')
        #    print(" ")
        #    print(" __________ 'CHANGEMENT LANGUE PAS TRAITE CORRECTEMENT NI MULTI UNITS! DEMULTIPLICATION DES CANAUX CONSTATEE!... TODO _______________ ")
        #    print(" ")
    
        

    
      
    
    
    
    


    
    #%***************************************
    #% task 6: Assemble multiunits systems with totals: total per phase, total per installation, reference voltage, battery power (with and without bsp)
    #%****************************************
      
    #TODO: check le cas des VS et VT mixés
    chanel_number_for_solar = [i for i, elem in enumerate(channels_labels) if "Solar power (ALL) [kW]" in elem]
    PsolarTot=total_datalog_df.values[:,chanel_number_for_solar[0]]
    
    chanel_number_for_Pout_a=[i for i, elem in enumerate(channels_labels) if 'I3101' in elem]
    
    
    #faire la somme des canaux avec Pin et Pout: si il y a des xt, sinon tjrs 0
    
    #init à 0:
    #Check it is not empty to be sure there is an XT: for the case with solar chargers only:
    if chanel_number_for_Pin:
        length=len(total_datalog_df[channels_labels[chanel_number_for_Pin[0]]].values)
    else:
        length=len(total_datalog_df[channels_labels[chanel_number_for_solar[0]]].values)
    
    PinTot=np.zeros(length)
    PoutTot=np.zeros(length)
    
    
    for chan in chanel_number_for_Pin:
        PinTot=PinTot+total_datalog_df[channels_labels[chan]].values
    
    for chan in chanel_number_for_Pout_a:
        PoutTot=PoutTot+total_datalog_df[channels_labels[chan]].values
    
    
    #Create a new entry called System Pin Power [kW]
    total_datalog_df['System Pin power (ALL) [kW]']=PinTot
    
    #Create a new entry called System Pout Power [kW]
    total_datalog_df['System Pout power (ALL) [kW]']=PoutTot
    
    
    

    #Séparation des puissances positives et négative pour différentier injection consommation sur AC-IN et la conso de l'AC-coupling sur ac-out:
    PinTot_power_pos=np.zeros(length)* np.nan
    PinTot_power_neg=np.zeros(length)* np.nan
    PoutTot_power_pos=np.zeros(length)* np.nan
    PoutTot_power_neg=np.zeros(length)* np.nan

    
    
    for k, tested_value in enumerate(PinTot):
        if tested_value<0.0:
            PinTot_power_pos[k]=0.0
            PinTot_power_neg[k]=tested_value
        else:
            PinTot_power_pos[k]=tested_value
            PinTot_power_neg[k]=0.0
    
    for k, tested_value in enumerate(PoutTot):
        if tested_value<0.0:
            PoutTot_power_pos[k]=0.0
            PoutTot_power_neg[k]=tested_value
        else:
            PoutTot_power_pos[k]=tested_value
            PoutTot_power_neg[k]=0.0
    
    
          
    
    #Create a new entry called System Pin Power [kW]
    total_datalog_df['System Pin Consumption power (ALL) [kW]']=PinTot_power_pos
    total_datalog_df['System Pin Injection power (ALL) [kW]']=PinTot_power_neg
    
    #Create a new entry called System Pout Power [kW]
    total_datalog_df['System Pout Consumption power (ALL) [kW]']=PoutTot_power_pos
    total_datalog_df['System Pout AC-coupling back power (ALL) [kW]']=PoutTot_power_neg
    
            
            
    
    ############################        
    #reference_batt_voltage:
    #'BSP-Ubat [Vdc] I7030 1'
    #'XT-Ubat [Vdc] I3092 L1-1'
    #'VS-Ubat [Vdc] I15054 1'
    #'VT-UbaM [Vdc] I11039 1'
    
    
    channel_number_ubatbsp = [i for i, elem in enumerate(channels_labels) if 'BSP-Ubat' in elem]
    
    
    #check if there is an BSP or not (column filled with 0), else we take the battery voltage from the Xtender or other devices
    if total_datalog_df[channels_labels[channel_number_ubatbsp[0]]].sum()==0:
        #Here thers is no BSP... let's take another channel available
        channel_number_ubatbsp = [i for i, elem in enumerate(channels_labels) if ('XT-Ubat [Vdc] I3092 L1-1' in elem) 
                                                                                    or ('VS-Ubat [Vdc] I15054 1' in elem) 
                                                                                    or ('VT-UbaM [Vdc] I11039 1' in elem)]
        #In that case the battery power is assessed with the sum of 
        print(" ")
        print(" **** WARNING: THERE IS NO BSP, THE BATT POWER IS ESTIMATED BUT NOT MEASURED: this is wrong with external battery chargers ______")
        print(" ")
        
        #Bilan système: Pinvertertobatt+Psol avec Pinverter= Pin-Pout avec rendements si positif *0.95 si négatif /0.95
        #battery_power=total_datalog_df.values[:,channel_number_ubatbsp[0]]*total_datalog_df.values[:,channels_number_ibatbsp]/1000
    
        bilanAC_power=PinTot-PoutTot
        bilanAC_to_batt=np.zeros(length)
    
        for k, tested_value in enumerate(bilanAC_power):
            if tested_value<0.0:
                bilanAC_to_batt[k]=tested_value/0.95
            else:
                bilanAC_to_batt[k]=tested_value*0.95
    
            
            
        battery_power=PsolarTot+bilanAC_to_batt-0.005
    
        
    else:
        #Here there is a BSP... 
        channels_number_ibatbsp = [i for i, elem in enumerate(channels_labels) if 'BSP-Ibat' in elem]
        battery_power=total_datalog_df.values[:,channel_number_ubatbsp[0]]*total_datalog_df.values[:,channels_number_ibatbsp[0]]/1000
    
            
    
    
            
    channel_number_ubat_ref=channel_number_ubatbsp[0] #the first one in the list of available 
    
    
    #Create a new entry called System Ubat ref [Vdc]
    ubat_ref=total_datalog_df.values[:,channel_number_ubat_ref]
    total_datalog_df['System Ubat ref [Vdc]']=ubat_ref
    
    
    #Create a new entry called System Batt Power [kW]
    total_datalog_df['System Battery Power Pbatt [kW]']=battery_power
    
    
    #separate the charge power and the discharge power: to estimate battery through put:
    
    
    battery_power_pos=np.zeros(len(battery_power))
    battery_power_neg=np.zeros(len(battery_power))
    
    for k, tested_value in enumerate(battery_power):
        if tested_value<0.0:
            battery_power_pos[k]=0.0
            battery_power_neg[k]=tested_value
        else:
            battery_power_pos[k]=tested_value
            battery_power_neg[k]=0.0
    
    
            
   #
    #
    #k=0
    #for tested_value in total_datalog_df.values[:,chan]:
    #    if tested_value<1.0:
    #        total_datalog_df.values[k,chan]=total_datalog_df.values[k-1,chan]
    #        if total_datalog_df.columns[chan]!='BSP-Ubat [Vdc] I7030 1':
    #            print("Error in batt voltage ")  #if bsp missing, it gives an message for every minute
    #    k+=1   
    #        
    
    
    
    
    total_datalog_df['System Batt Charge Power Pbatt [kW]']=battery_power_pos
    
    total_datalog_df['System Batt Discharge Power Pbatt [kW]']=battery_power_neg
    
    
    
    
    #TODO
    ##Create a new entry called System Pin Power [kW]  with the sum of all inverters
    #total_datalog_df['System Pin Power [kW]']=pin_power
    #
    ##Create a new entry called System Pout Power [kW] with the sum of all inverters
    #total_datalog_df['System Pin Power [kW]']=pout_power
    
    
    
    
    
    
    








	#%***************************************
	#% task 7: resemple: day, month, year and put them in new dataframes
	#%****************************************

    quarters_mean_df = total_datalog_df.resample("15T", label="right").mean()
    day_mean_df = total_datalog_df.resample("1d").mean()
    month_mean_df = total_datalog_df.resample("1M").mean()
    year_mean_df = total_datalog_df.resample("1Y").mean()

    #change the names to distinguish (per example on graphs)
    newlabels_q=[]
    newlabels_d=[]
    newlabels_M=[]
    newlabels_Y=[]
    
    k=0
    for elem in list(total_datalog_df.columns):
        newlabels_q.append('15min mean ' + elem)
        newlabels_d.append('Day mean ' + elem)
        newlabels_M.append('Month mean ' + elem)
        newlabels_Y.append('Year mean ' + elem)
        k=k+1
        
    quarters_mean_df.columns=newlabels_q  
    day_mean_df.columns=newlabels_d     
    month_mean_df.columns=newlabels_M    
    year_mean_df.columns=newlabels_Y   
        
        
    print("_____________________")
    print(" SAVE DATA  ")

	# ***************************************
	# Save in file the precomputed datas for later for the graph display
	# ***************************************
    total_datalog_df.to_pickle(MIN_DATAFRAME_NAME)
    quarters_mean_df.to_pickle(QUARTERS_DATAFRAME_NAME)
    day_mean_df.to_pickle(DAY_DATAFRAME_NAME)
    month_mean_df.to_pickle(MONTH_DATAFRAME_NAME)
    year_mean_df.to_pickle(YEAR_DATAFRAME_NAME)
    
    

	#%***************************************
	#% Compute kWh
	# WARNING: it make sense only for P in KW !
	#TODO: make a dataframe for energies only without what is not needed (and not correct)
	#%****************************************

	# min to day: *60*24/1000
	# day to month: *60*24/1000

    #    day_kwh_df = total_datalog_df.resample("1d").sum() / 60
    #    month_kwh_df = total_datalog_df.resample("1M").sum() / 60
    #    year_kWh_df = total_datalog_df.resample("1Y").sum() / 60
    
    
    
    day_kwh_df=total_datalog_df.resample("1d").sum()/60
    #month_kwh_df=total_datalog_df.resample("1M").sum()/60
    #year_kwh_df=total_datalog_df.resample("1Y").sum()/60
       
    #If the day had no data (inexistant, corrupted or rejected)  fill with NaN
    # to see this, we check the sum of battery voltages, this indicates if all voltages were 0.0 
    #and then that there's no data, replace it with nan to indicate it is not a real 0.0
    
    battery_sum=day_kwh_df.values[:,channel_number_ubat_ref]
    
    #day_kwh_df.values[:,channel_number_ubat_ref]
    
    for k, tested_value in enumerate(battery_sum):
        if tested_value==0.0:
            day_kwh_df.values[k,:]=np.nan
    
    
    month_kwh_df=day_kwh_df.resample("1M").sum()
    year_kwh_df=day_kwh_df.resample("1Y").sum()
    
    
    
    
    
    
    day_kwh_df.to_pickle(DAY_KWH_DATAFRAME_NAME)
    month_kwh_df.to_pickle(MONTH_KWH_DATAFRAME_NAME)
    year_kwh_df.to_pickle(YEAR_KWH_DATAFRAME_NAME)
    
    
    
    
    
    
    list_of_colums_wanted= ['System Pout Consumption power (ALL) [kW]',
                            'System Pout AC-coupling back power (ALL) [kW]',
                            'System Pin Consumption power (ALL) [kW]',
                            'System Pin Injection power (ALL) [kW]',
                            'System Batt Charge Power Pbatt [kW]',
                            'System Batt Discharge Power Pbatt [kW]',
                            'Solar power (ALL) [kW] I17999 ALL' ]
    
    list_of_new_names= ['System Pout Consumption Energy [kWh]',
                        'System Pout AC-coupling Energy [kWh]',
                        'System Pin Consumption Energy [kWh]',
                        'System Pin Injection Energy [kWh]',
                        'System Batt Charge Energy [kWh]',
                        'System Batt Discharge Energy [kWh]',
                        'Solar Power Energy [kWh]' ]
    
    selected_day_kwh=day_kwh_df[list_of_colums_wanted]
    selected_day_kwh.columns=list_of_new_names
    
    
    
    selected_month_kwh=month_kwh_df[list_of_colums_wanted]
    selected_month_kwh.columns=list_of_new_names
    
    
    
    selected_year_kwh=year_kwh_df[list_of_colums_wanted]
    selected_year_kwh.columns=list_of_new_names
    
    
    
    
    print(" Estimate missing datalogs files for each month")
    
    
    #TODO: compter les jours présents/manquants par mois ou par année
    #TODO: estimer l'énergie manquante
    
    #Take all the days available in one month
    
    #for k in [1:12]
    first_year=month_kwh_df.index.year[0]
    last_year=month_kwh_df.index.year[-1]
    
    
    month_kwh_df.index.month
    
    #for testit in month_kwh_df.index:
    #    print('year: ', str(testit.year),'month: ', str(testit.month) )
        
        
    nombre_de_jours_du_mois_dans_dataframe=[]
    nombre_de_jours_corrompus=[]
    nombre_de_jours_total_du_mois=[]
    nombre_de_jours_valides=[]
    nombre_de_jours_du_mois_a_compenser=[]
    facteur_compensation=[]
    #nombre_de_jours_du_mois à calculer
    # df['days_in_month'] = df['date'].dt.daysinmonth
    #p = pd.Period('2018-2-17')
    #p = pd.Period('2016-2-17')
    #p.days_in_month
    
    #selected_day_kwh.index[1].days_in_month
    
    mois_de_lannee=list(range(1, 13))
    k=0
    
    for testit in month_kwh_df.index:
        n_year=testit.year
        n_month=testit.month
        temp2=selected_day_kwh[selected_day_kwh.index.year == n_year]
        temp3=temp2[temp2.index.month == n_month]
        
        temp4=total_datalog_df[(total_datalog_df.index.month == n_month)]
        temp5=temp4[(temp4.index.year == n_year)]
      
        p = pd.Period(str(n_year)+ '-'+str(n_month) +'-01')
        nombre_de_jours_total_du_mois.append(p.days_in_month)
        
        nombre_de_jours_du_mois_dans_dataframe.append(len(temp3)) #attention, uniquement pour premier et dernier mois, pour les mois au milieu les jours manquants sont remplis de nan
        nombre_de_jours_corrompus.append(temp3.isnull().sum(axis = 0)[1])
        nombre_de_jours_valides.append(nombre_de_jours_du_mois_dans_dataframe[k]-nombre_de_jours_corrompus[k])
    
        nombre_de_jours_du_mois_a_compenser.append(nombre_de_jours_total_du_mois[k]-nombre_de_jours_du_mois_dans_dataframe[k]+nombre_de_jours_corrompus[k])
        if nombre_de_jours_valides[k]==0:
            facteur_compensation.append(0.0)
        else:
            facteur_compensation.append(1.0+nombre_de_jours_du_mois_a_compenser[k]/nombre_de_jours_valides[k])
    
        print('  ', str(n_year), '-' ,str(n_month), 
              'has', str(nombre_de_jours_total_du_mois[k]),
              'days; ','valid: ', str(nombre_de_jours_valides[k]), 
              '; corrupted/missing: ', str(nombre_de_jours_corrompus[k]),
              '; to compensate:', str(nombre_de_jours_du_mois_a_compenser[k]),
              'with factor', str(facteur_compensation[k])
              )
              #'days; ','in dataframe: ', str(nombre_de_jours_du_mois_dans_dataframe[k]), 
    
        
        k=k+1
        
    
    # Using DataFrame.insert() to add a column  loc, column, value, allow_duplicates=False)
    selected_month_kwh.insert(0,"Month number of day", nombre_de_jours_total_du_mois,False) 
    selected_month_kwh.insert(1,"Missing/corrupted", nombre_de_jours_corrompus,False) 
    selected_month_kwh.insert(2,"Days to compensate", nombre_de_jours_du_mois_a_compenser,False) 
    selected_month_kwh.insert(3,"Comp factor", facteur_compensation,False) 
    
    
    
    
    ##addition of the channels in the month kWh       
    #selected_month_kwh['nombre_de_jours_total_du_mois']=nombre_de_jours_total_du_mois
    #selected_month_kwh['nombre_de_jours_corrompus']=nombre_de_jours_corrompus
    #selected_month_kwh['nombre_de_jours_du_mois_a_compenser']=nombre_de_jours_du_mois_a_compenser
    #
    #n_year=2019
    #n_month=5
    #temp4=total_datalog_df[(total_datalog_df.index.month == n_month)]
    #temp5=temp4[(temp4.index.year == n_year)]
    #temp2=selected_day_kwh[selected_day_kwh.index.year == n_year]
    #temp3=temp2[temp2.index.month == n_month]
    
            
            #TODO: c'est pas fini... mettre dans le dataframe des mois et des années!
            
            
    
    ##old way to do it, first try of implementation:
    #mois_de_lannee=list(range(1, 13))
    #k=0
    #for n_year in list(range(first_year, last_year+1)):
    #    temp2=selected_day_kwh[selected_day_kwh.index.year == n_year]
    #    for n_month in mois_de_lannee:
    #        temp3=temp2[temp2.index.month == n_month]
    #        
    #        p = pd.Period(str(n_year)+ '-'+str(n_month) +'-01')
    #        nombre_de_jours_total_du_mois.append(p.days_in_month)
    #        
    #        nombre_de_fichiers_importes_du_mois.append(len(temp3))
    #        nombre_de_jours_manquants.append(temp3.isnull().sum(axis = 0)[1])
    #        
    #        nombre_de_jours_du_mois_a_compenser.append(nombre_de_jours_total_du_mois[k]-nombre_de_fichiers_importes_du_mois[k]+nombre_de_jours_manquants[k])
    #        
    #        print(str(n_year), '-' ,str(n_month), 
    #              '- files available: ', str(nombre_de_fichiers_importes_du_mois[k]),
    #              'on', str(nombre_de_jours_total_du_mois[k]),
    #              'days; corrupted files: ', str(nombre_de_jours_manquants[k]),
    #              '; to compensate:', str(nombre_de_jours_du_mois_a_compenser[k]))
    #                
    #        k=k+1
    #        
    #        
            
            #TODO: c'est pas fini... mettre dans le dataframe des mois et des années!
            
            
    
    
    print(" SAVE CSV of daily, monthly and yearly energies   ")

    
    
    selected_day_kwh.to_csv('csvExport/day_kWh.csv', index=True)
    selected_month_kwh.to_csv('csvExport/month_kWh.csv', index=True)
    selected_year_kwh.to_csv('csvExport/year_kWh.csv', index=True)



    

	# ***************************************
	#%Timer
	# ***************************************

    new_time = time.time()
    #print("--- %s seconds ---" % (new_time - old_time))
    old_time = new_time
    print("\n ______________________________ ")

    print("--TOTAL TIME- %s seconds ---" % (new_time - start_time))
    print("--for  %s files converted ---" % (number_of_files))
    print("--performance:  %s files per second converted ---" % (number_of_files/(new_time - start_time)) )


    print(" ")
    print(" ______ IMPORT IS FINISHED  ___________ ")
		







if __name__ == "__main__":
    main()
	
	
	#***************************************
	# GRAPHS
	#***************************************
    print(" ")
    print(" __________ SIMPLE GRAPH DISPLAY  _______________ ")
    print(" \n \n \n ")


    total_datalog_df = pd.read_pickle(MIN_DATAFRAME_NAME)

    channels_labels = list(total_datalog_df.columns)

    ################################
    # plot all the channels with battery voltage and current:
    chanels_number_ubat = [
        i for i, elem in enumerate(channels_labels) if "Ubat" in elem
    ]
    chanels_number_ibat = [
        i for i, elem in enumerate(channels_labels) if "Ibat" in elem
    ]

    fig_batt, (axes_bat_u, axes_bat_i) = plt.subplots(nrows=2, ncols=1)

    total_datalog_df.plot(
        y=total_datalog_df.columns[chanels_number_ubat],
        grid=True,
        figsize=(15, 5),
        sharex=True,
        ax=axes_bat_u,
    )

    axes_bat_u.set_ylabel("Voltage [V]", fontsize=12)
    axes_bat_u.set_title("All Battery Voltages", fontsize=12, weight="bold")
    axes_bat_u.grid(True)
    plt.show

    total_datalog_df.plot(
        y=total_datalog_df.columns[chanels_number_ibat],
        figsize=(15, 8),
        grid=True,
        sharex=True,
        ax=axes_bat_i,
    )

    axes_bat_i.set_ylabel("Amperes [A]", fontsize=12)
    axes_bat_i.set_title("All Battery Currents", fontsize=12, weight="bold")
    axes_bat_i.grid(True)

    #
    #
    #
    # month_mean_df.plot(y=month_mean_df.columns[chanels_number_ubat[0]],
    #                      color='r',
    #                      figsize=(15,5),
    #                      grid=True,
    #                      sharex=True,
    #                      title='Mean Battery Voltages')

    print(" ")
    print(" *******  Run xt_graph_plotter_pandas.py for detailled graphs  ****** ")
    print(" \n \n \n ")
