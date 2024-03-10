#requires pyserial installed 
#requires ttkbootstrap installed

from tkinter import *
import ttkbootstrap as ttkb
from ttkbootstrap.dialogs  import Messagebox
from ttkbootstrap.scrolled import ScrolledText
import tkinter as tk


import serial
import threading
import time
import csv
import webbrowser
import os


baud_rate        = 0

csv_delimiter    = ','
log_int = 0


#create Dropdown options
baudrates    = [0,600,1200,2400,4800,9600,19200,38400]
log_interval = [0,0.5,1,1.5,2,2.5,3,4,5,10,20,30,60,120]

tutorial_text = ''' Tutorial

  Select Serial Port number like COM3 or COM12 in Windows
  Select Serial Port number like ttyUSB0 or ttyACM0 in Linux
  Select Baudrate from Drop Down Menu
  Select Logging interval from Drop Down Menu
  
  Click Start Logging to start datalog
  Click Stop  Logging to stop datalog
  
  Data saved in disk\n'''

def acquire_arduino_data(serialport_name,baud_rate,logging_interval):
    
    serialport_obj = None #declared here so accessible inside and outside try/catch
    log_count      = 1
    
    
    
    #Create the Serial port object
    try:
        serialport_obj = serial.Serial(serialport_name,baud_rate)       #open the serial port
        text_log.insert(END,f'{serialport_name} selected,at {baud_rate} ,\n')
        text_log.insert(END,f'Logging Interval = {logging_interval} seconds,\n')
        text_log.insert(END,f'Wait for Arduino to Reset,\n')
        time.sleep(2)                                                   #Some time for Arduino board to reset
        text_log.insert(END,f'Arduino Ready Now ,\n\n')
                
    except serial.SerialException as var :                              #In case of error
        text_log.insert(END,f'{var} ,\n')
        
    log_file_name = create_filename_current_date_time()
    
    
    
    csv_header =['No','Date','Time','Unix Time','Humidity','Soil Moisture','Temperature','Light Intensity']
    
    with open(log_file_name,'a',newline ='') as File_obj:
        csvwriter_obj = csv.writer(File_obj, delimiter = csv_delimiter)
        csvwriter_obj.writerow(csv_header)
        
    text_log.insert(END,f'Log file -> {log_file_name}\n\n')
    text_log.insert(END,f'Starting Logging @{logging_interval} interval\n\n')
    text_log.insert(END,f'{csv_header}\n')
    
    csv_filename_loc.insert(END,f'{os.getcwd()}\n')
    csv_filename_loc.insert(END,f'{log_file_name}\n')
    
    
    while True:
        
        #print(start_logging_event.is_set())
        if start_logging_event.is_set() == True:
            
            arduino_sensor_data_list = read_arduino_sensors(serialport_obj)
            #print(arduino_sensor_data_list)
            unix_timestamp = int(time.time()) #get current unix time to time stamp data
            
            log_time_date  = time.localtime(unix_timestamp)          #Convert epoch time to human readable time,date format
            log_time       = time.strftime("%H:%M:%S",log_time_date) #hh:mm:ss
            log_date       = time.strftime("%d %B %Y",log_time_date) #dd MonthName Year
    
           
            
            arduino_sensor_data_list.insert(0,str(log_count))
            arduino_sensor_data_list.insert(1,str(log_date))
            arduino_sensor_data_list.insert(2,str(log_time))
            arduino_sensor_data_list.insert(3,str(unix_timestamp))
            
            #print(arduino_sensor_data_list)
            text_log.insert(END,f'{arduino_sensor_data_list} ,\n')
            text_log.see(tk.END) #for auto  scrolling
            
            with open(log_file_name,'a',newline='') as File_obj:
                csvwriter_obj = csv.writer(File_obj, delimiter = csv_delimiter)
                csvwriter_obj.writerow(arduino_sensor_data_list)
            
            #print('data acquiring')
            log_count = log_count + 1
            
            time.sleep(logging_interval)
        
            
        elif start_logging_event.is_set() != True:
            serialport_obj.close()
            text_log.insert(END,f'+==================================================+ \n')
            text_log.insert(END,f'Logging Ended \n')
            break
           

    
  


def read_arduino_sensors(serialport_obj):
    
    return_list =[0,0,0,0]
    
    polling_interval = 0.010 #In seconds,to give time for arduino to respond
    
    serialport_obj.write(b'@')
    time.sleep(polling_interval)
    humidity_value = serialport_obj.readline()
    humidity_value = humidity_value.strip()
        
    serialport_obj.write(b'#')
    time.sleep(polling_interval)
    soil_value = serialport_obj.readline()
    soil_value = soil_value.strip()
        
    serialport_obj.write(b'$')
    time.sleep(polling_interval)
    temp_value = serialport_obj.readline()
    temp_value = temp_value.strip()
        
    serialport_obj.write(b'&')
    time.sleep(polling_interval)
    light_value = serialport_obj.readline()
    light_value = light_value.strip()
        
    #print(humidity_value,soil_value,temp_value,light_value)
    
    return_list[0] = humidity_value.decode()
    return_list[1] = soil_value.decode()
    return_list[2] = temp_value.decode()
    return_list[3] = light_value.decode()
    
    return return_list

def create_filename_current_date_time():
    # Generate file name using Current Date and Time
    current_local_time = time.localtime() #Get Current date time
    filename           = time.strftime("%d_%B_%Y_%Hh_%Mm_%Ss",current_local_time)# 24hour clock format
    filename           = 'ard_'+ filename + '_daq_log.csv'
    #print(f'\nCreated Log File -> {filename}')
    return filename


def tutorial_btn_handler():
    webbrowser.open_new(r'https://www.xanthium.in/multithreading-serial-port-data-acquisition-to-csv-file-using-producer-consumer-pattern-python')



def start_log_btn_handler():
    start_logging_event.set()
    serialport_name = port_no_entry.get()
    t1 = threading.Thread(target = acquire_arduino_data,args=(serialport_name,baud_rate,log_int))
    t1.start()
    

def stop_log_btn_handler():
    start_logging_event.clear()
    
    

def on_select_option_bind_baudrates(e):
    global baud_rate
    baud_rate  = int(baud_rates_combo_box.get())
    #print(baud_rate)

def on_select_option_bind_log_interval(e):
    global log_int
    log_int  = float(log_interval_combo_box.get())
    print(log_int)
    

   
    
start_logging_event    = threading.Event()

# Main Window Creation
root = ttkb.Window(themename = 'superhero')        # theme = superhero
root.title('SerialPort Datalogging to CSV file')
root.geometry('650x660') # Width X Height

#Labels for naming boxes
head_label = ttkb.Label(text = 'Python Serial Port CSV Datalogger',font = ('Helvetica',15),bootstyle='light')
head_label.place(x=95,y=10)

website_label = ttkb.Label(text = 'www.xanthium.in',font = ('Helvetica',10),bootstyle='warning')
website_label.place(x=230,y=45)

serialport_label = ttkb.Label(text = 'Select Port',bootstyle = 'light')
serialport_label.place(x=20,y=90)

baudrate_label = ttkb.Label(text = 'Baudrate',bootstyle = 'light')
baudrate_label.place(x=220,y=90)

lograte_label = ttkb.Label(text = 'Log Interval (Seconds)',bootstyle = 'light')
lograte_label.place(x=440,y=90)

#Create COM portEntry Widget 
port_no_entry = ttkb.Entry(root)
port_no_entry.insert(0,'COMx')
port_no_entry.place(x=20,y=120)

#create Combobox for baudrates
baud_rates_combo_box = ttkb.Combobox(values = baudrates)
baud_rates_combo_box.place(x=220,y=120)
baud_rates_combo_box.current(0)#set the default value on combobox
#bind the combobox
baud_rates_combo_box.bind('<<ComboboxSelected>>',on_select_option_bind_baudrates)

#create Combobox for logging interval
log_interval_combo_box = ttkb.Combobox(values = log_interval)
log_interval_combo_box.place(x=440,y=120)
log_interval_combo_box.current(0)#set the default value on combobox
#bind the combobox
log_interval_combo_box.bind('<<ComboboxSelected>>',on_select_option_bind_log_interval)


#create button for controlling data acquisition and logging
start_log_btn  = ttkb.Button(text = 'Start Logging' ,command = start_log_btn_handler ).place(x=20, y=175)
stop_log_btn   = ttkb.Button(text = 'Stop Logging'  ,command = stop_log_btn_handler  ).place(x=220,y=175)
tutorial_btn   = ttkb.Button(text = 'Online Web Tutorial'  ,command = tutorial_btn_handler  ).place(x=440,y=175)

# Scrollable text box for CSV file name

file_loc_label = ttkb.Label(text = 'CSV file Name and Location',bootstyle = 'light').place(x=20,y=225)

csv_filename_loc = ScrolledText(root,height=2,width=74,wrap = WORD,autohide=False,)
csv_filename_loc.place(x=20,y=250)

# Define the font family and font size
font_family = 'Helvetica'
font_size = 10

log_label = ttkb.Label(text = 'Logging',bootstyle = 'light').place(x=20,y=318)

text_log = ScrolledText(root,height=15,width=66,wrap = WORD,autohide=False,font=(font_family, font_size))
text_log.place(x=20,y=340)
text_log.insert(END,tutorial_text)


root.mainloop()
