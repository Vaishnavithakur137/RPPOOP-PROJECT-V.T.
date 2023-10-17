# import modules 
from tkinter import *
from tkinter import ttk
import datetime as dt
from rp_database import Database
from tkinter import messagebox
from tkinter import simpledialog

# object for database
data = Database(db='112103147_project_database.db')

# global variables
count = 0
selected_rowid = 0

# functions
def saveRecord():
    global data
    data.insertRecord(item_name=item_name.get(), item_price=item_amt.get(), purchase_date=transaction_date.get())
       
def setDate():
    date = dt.datetime.now()
    dopvar.set(f'{date:%d %B %Y}')

def clearEntries():
    item_name.delete(0, 'end')
    item_amt.delete(0, 'end')
    transaction_date.delete(0, 'end')

def fetch_records():
    f = data.fetchRecord('select rowid, * from expense_record')
    global count
    for rec in f:
        tv.insert(parent='', index='0', iid=count, values=(rec[0], rec[1], rec[2], rec[3]))
        count += 1
    tv.after(400, refreshData)

def select_record(event):
    global selected_rowid
    selected = tv.focus()    
    val = tv.item(selected, 'values')
  
    try:
        selected_rowid = val[0]
        d = val[3]
        namevar.set(val[1])
        amtvar.set(val[2])
        dopvar.set(str(d))
    except Exception as ep:
        pass


def update_record():
    global selected_rowid

def update_record():
    global selected_rowid

    selected = tv.focus()
	# Update record
    try:
        data.updateRecord(namevar.get(), amtvar.get(), dopvar.get(), selected_rowid)
        tv.item(selected, text="", values=(namevar.get(), amtvar.get(), dopvar.get()))
    except Exception as ep:
        messagebox.showerror('Error',  ep)

	# Clear entry boxes
    item_name.delete(0, END)
    item_amt.delete(0, END)
    transaction_date.delete(0, END)
    tv.after(400, refreshData)
    

def setTotalAmount():
    global total_amount
    total_amount = simpledialog.askinteger("Set Total Amount", "Enter your total amount:")

def totalBalance():
    global total_amount
    if not total_amount:
        messagebox.showinfo('Total Balance', 'Please set your total amount first.')
        return
    
    f = data.fetchRecord(query="SELECT SUM(item_price) FROM expense_record")
    for i in f:
        for j in i:
            balance = total_amount - j
            messagebox.showinfo('Total Balance', f"Total Expense: {j}\nRemaining Balance: {balance}")

def refreshData():
    for item in tv.get_children():
      tv.delete(item)
    fetch_records()
    
def deleteRow():
    global selected_rowid
    data.removeRecord(selected_rowid)
    refreshData()
def restoreRecord():
    global selected_rowid
    deleted_record = data.fetchdeleteRow(selected_rowid)

    if deleted_record:
        item_name, item_price, purchase_date = deleted_record
        data.restoreDeletedRecord(item_name, item_price, purchase_date)
        refreshData()
        messagebox.showinfo('Restored', 'Record Restored Successfully')
    else:
        messagebox.showwarning('Not Found', f"No record found for rowid {selected_rowid}")
# create tkinter object
ws = Tk()
ws.title('112103147_EXPENSE_TRACKER')
ws.resizable(False,False)
# variables
f = ('Helvetica', 16)
namevar = StringVar()
amtvar = IntVar()
dopvar = StringVar()

# Frame widget
f2 = Frame(ws,bg="black")
f2.pack() 

f1 = Frame(
    ws,
    padx=10,
    pady=10,
    bg="black"
)
f1.pack(expand=True, fill=BOTH)


# Label widget
Label(f1, text='Item_name', font=f).grid(row=0, column=0, sticky=W)
Label(f1, text='Item_price', font=f).grid(row=1, column=0, sticky=W)
Label(f1, text='Purchase_date', font=f).grid(row=2, column=0, sticky=W)

# Entry widgets 
item_name = Entry(f1, font=f, textvariable=namevar)
item_amt = Entry(f1, font=f, textvariable=amtvar)
transaction_date = Entry(f1, font=f, textvariable=dopvar)

# Entry grid placement
item_name.grid(row=0, column=1, sticky=EW, padx=(10, 0))
item_amt.grid(row=1, column=1, sticky=EW, padx=(10, 0))
transaction_date.grid(row=2, column=1, sticky=EW, padx=(10, 0))

# Action buttons
cur_date = Button(
    f1, 
    text='Today', 
    font=f, 
    bg='#04C4D9', 
    command=setDate,
    width=15
    )

submit_btn = Button(
    f1, 
    text='Save', 
    font=f, 
    command=saveRecord, 
    bg='grey19', 
    fg='white'
    )

clr_btn = Button(
    f1, 
    text='Clear', 
    font=f, 
    command=clearEntries, 
    bg='grey30', 
    fg='white'
    )

quit_btn = Button(
    f1, 
    text='Exit', 
    font=f, 
    command=lambda:ws.destroy(), 
    bg='grey40', 
    fg='white'
    )

total_bal = Button(
    f1,
    text='Total Balance',
    font=f,
    bg='grey90',
    command=totalBalance
)

total_spent = Button(
    f1,
    text='Total Spent',
    font=f,
    command=lambda:data.fetchRecord('select sum(ite)')
)

update_btn = Button(
    f1, 
    text='Update',
    bg='grey80',
    command=update_record,
    font=f
)

#Changes made for setting total amount
# Create a button to set total amount
set_total_amount_btn = Button(
    f1,
    text='Set Total Amount',
    font=f,
    command=setTotalAmount,
    bg='grey50'
)
set_total_amount_btn.grid(row=3, column=3, sticky=EW, padx=(10, 0))

del_btn = Button(
    f1, 
    text='Delete',
    bg='grey69',
    command=deleteRow,
    font=f
)

restore_btn = Button(
    f1,
    text='Restore',
    bg='grey69',
    command=restoreRecord,
    font=f
)
# grid placement
cur_date.grid(row=3, column=1, sticky=EW, padx=(10, 0))
submit_btn.grid(row=0, column=2, sticky=EW, padx=(10, 0))
clr_btn.grid(row=1, column=2, sticky=EW, padx=(10, 0))
quit_btn.grid(row=2, column=2, sticky=EW, padx=(10, 0))
total_bal.grid(row=0, column=3, sticky=EW, padx=(10, 0))
update_btn.grid(row=1, column=3, sticky=EW, padx=(10, 0))
del_btn.grid(row=2, column=3, sticky=EW, padx=(10, 0))
restore_btn.grid(row=3, column=3, sticky=EW, padx=(10, 0))
# Treeview widget
tv = ttk.Treeview(f2, columns=(1, 2, 3, 4), show='headings', height=8)
tv.pack(side="left")

# add heading to treeview
tv.column(1, anchor=CENTER, stretch=NO, width=70)
tv.column(2, anchor=CENTER)
tv.column(3, anchor=CENTER)
tv.column(4, anchor=CENTER)
tv.heading(1, text="Serial no")
tv.heading(2, text="Item Name", )
tv.heading(3, text="Item Price")
tv.heading(4, text="Purchase Date")

# binding treeview
tv.bind("<ButtonRelease-1>", select_record)

# style for treeview
style = ttk.Style()
style.theme_use("default")
style.map("Treeview")

# Vertical scrollbar
scrollbar = Scrollbar(f2, orient='vertical')
scrollbar.configure(command=tv.yview)
scrollbar.pack(side="right", fill="y")
tv.config(yscrollcommand=scrollbar.set)

# calling function 
fetch_records()

# infinite loop
ws.mainloop()

