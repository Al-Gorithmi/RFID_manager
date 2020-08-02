import tkinter as tk #GUI library
from tkinter import filedialog, Text, StringVar #GUI options
import tkinter.ttk as ttk #GUI table module
from tkinter.ttk import Treeview #import table module
import os #OS access to open file
import interface
import sqlite3


def rfidkeytext():
    global card_key
    card_key.set(interface.rfidkey_get())
    return card_key

#get item from textbox where 1.0 means line 1 char 0 and end -1c means read to end of doccument -the last charachter \n or\r
def NameSave(argz):
    FullName.set(argz.get('1.0', 'end -1c'))
    return FullName.get()
    
def addToDb(name,rfid_id):
    name = name.upper()
    try:
        db_conn = sqlite3.connect('test.db')
        db_currsor = db_conn.cursor()
        print('SQL CONNECTION PASSED!')
    except sqlite3.Error as error:
        print(f'SQL CONNECTION FAILED! ERROR : {error}')
    Check = db_conn.execute(
        "SELECT id FROM rfid_acess WHERE b_key IS ? OR full_name IS ?;", (rfid_id, name))
    Check = Check.fetchone()
    if Check == None:
        db_currsor.execute(f"INSERT INTO rfid_acess (b_key, full_name) VALUES (?,?);", (rfid_id, name))
        db_conn.commit()
        Add_Status.set('Sucess')
    else:
        Add_Status.set(f'Name or ID exist in database with id = {Check[0]}')
    if db_conn:
        db_conn.close()
    

def rmFromDb(name, rfid_id):
    name = name.upper()
    try:
        db_conn = sqlite3.connect('test.db')
        db_currsor = db_conn.cursor()
        print('SQL CONNECTION PASSED!')
    except sqlite3.Error as error:
        print(f'SQL CONNECTION FAILED! ERROR : {error}')
    Check = db_conn.execute(
        "SELECT id FROM rfid_acess WHERE b_key IS ? OR full_name IS ?;" , (rfid_id, name))
    Check = Check.fetchone()
    if Check != None:
        db_currsor.execute(
            f"DELETE FROM rfid_acess WHERE b_key IS ? OR full_name IS ?;" , (rfid_id, name))
        db_conn.commit()
        Add_Status.set('Sucess')
    else:
        Add_Status.set('Name or ID does not exist in database')
    if db_conn:
        db_conn.close()

def list_acess():
    l_acess_window = tk.Tk()
    l_acess_window.title('RFID Acess Table')
    l_acess_window.geometry('400x800')
    try:
        db_conn = sqlite3.connect('test.db')
        print('SQL CONNECTION PASSED!')
    except sqlite3.Error as error:
        print(f'SQL CONNECTION FAILED! ERROR : {error}')
    acess = db_conn.execute('SELECT * FROM rfid_acess;')
    acess = acess.fetchall()
    list_table = ttk.Treeview(l_acess_window)
    list_table['columns'] = ('RFID Key', 'Name')
    
    list_table.column('#0', width = 50, minwidth = 25)
    list_table.column('RFID Key', width = 200, minwidth = 175)
    list_table.column('Name', width=200, minwidth=175)

    list_table.heading('#0', text='ID')
    list_table.heading('RFID Key', text = 'RFID Key')
    list_table.heading('Name', text='Name')
    
    for index, row in enumerate(acess):
        list_table.insert('',index,text =row[0], values = row[1:])
    list_table.pack(fill = 'both', expand = True)

def list_history():
    l_history_window = tk.Tk()
    l_history_window.title('RFID Acess Table')
    l_history_window.geometry('800x600')
    try:
        db_conn = sqlite3.connect('test.db')
        print('SQL CONNECTION PASSED!')
    except sqlite3.Error as error:
        print(f'SQL CONNECTION FAILED! ERROR : {error}')
    acess = db_conn.execute('SELECT * FROM rfid_history;')
    acess = acess.fetchall()
    list_table = ttk.Treeview(l_history_window)
    list_table['columns'] = ('RFID Key', 'Name')
    
    list_table.column('#0', width = 200, minwidth = 175)
    list_table.column('RFID Key', width = 200, minwidth = 175)
    list_table.column('Name', width=200, minwidth=175)

    list_table.heading('#0', text='Date and Time')
    list_table.heading('RFID Key', text = 'RFID Key')
    list_table.heading('Name', text='Name')
    
    for index, row in enumerate(acess):
        list_table.insert('',index,text =row[0], values = row[1:])
    list_table.pack(fill = 'both', expand = True)


#file structue
root = tk.Tk()
root.title('RFID Manager')

root['background'] = '#83C3C8'
#updatable stringvar variabler
card_key = StringVar() 
FullName = StringVar()
Add_Status = StringVar()

#prevent app resizability 
root.resizable(height = False, width = False)

#canvas options and commit canvas
canvas = tk.Canvas(root, height=240, width=600, bg='#83C3C8') 
canvas.pack() 

#palce and configure frame
frame = tk.Frame(root, bg ='white') #creare frame
frame.place(relwidth = 0.8, relheight = 0.8 , relx  = 0.1, rely = 0.1) 

Title_label = tk.Label(frame, text='RFID Manager', font=200, bg='white')
Title_label.grid(row = 0, column = 1, sticky = 'E')


# insert a table at coordiates x,y
Name_label = tk.Label(frame, text='Full Name : ', font=50, bg = 'white')
Name_label.grid(row = 1, column = 0 )

#Adds text editor
edit_name = tk.Text(frame, height = 1, width = 20, relief = 'solid')
edit_name.grid(row=1, column=1) 

key_label = tk.Label(frame, text='RFID_key : ', font=50, bg='white')
key_label.grid(row=2, column=0)

key_label = tk.Label(frame, textvariable=card_key, font=20, bg='white')
key_label.grid(row=2, column=1)

rfid_key_button = tk.Button(frame, text = 'Scan Card', padx = 10, pady = 5, bg = 'White', command = rfidkeytext)
rfid_key_button.grid(row = 2, column = 2)
        
#Adds Button and packs it to the master(root)
AddUserButton = tk.Button(frame, text='Add User', padx=10, pady=5,
                          bg='White', command=lambda: addToDb(NameSave(edit_name), card_key.get()))
AddUserButton.grid(row = 4, column = 2, sticky='W')
DeleteUserButton = tk.Button(frame, text='Delete User', padx=10, pady=5,
                          bg='White', command=lambda: rmFromDb(NameSave(edit_name), card_key.get()))
DeleteUserButton.grid(row=4, column=3, sticky = 'E' )

Status_adduser_txt = tk.Label(frame, text = 'Status: ', font=50, bg='white')
Status_adduser = tk.Label(
    frame, textvariable=Add_Status, font=50, bg='white', wraplength=200)
Status_adduser_txt.grid(row=3, column=0 )
Status_adduser.grid(row=3, column=1)

List_RFID_Acess = tk.Button(frame, text='Show Users',
                            padx=10, pady=5, bg='White', command= list_acess)
List_RFID_Acess.grid(row = 5, column = 0, sticky = 'E')

List_RFID_History = tk.Button(frame, text='Show History',
                            padx=10, pady=5, bg='White', command=list_history)
List_RFID_History.grid(row=5, column=1)
#runs software
root.mainloop()


