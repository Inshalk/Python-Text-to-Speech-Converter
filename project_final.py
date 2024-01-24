from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import tkinter as tk
from gtts import gTTS
import os
import pymysql

def front():
    top=tk.Tk()
    top.geometry("1067x580")
    top.title("Audio Book")
    frame = Frame(top, width=1067, height=580)
    frame.pack()
    frame.place(anchor='center', relx=0.5, rely=0.5)
    img = ImageTk.PhotoImage(Image.open("forest.jpg"))
    label1=tk.Label(top,font=('Cooper Black',40),text="Audio Book ",bg="gold",fg="black")
    label1.pack(padx=0.5,pady=0.5)
    label = Label(frame, image = img,bd=0)
    label.pack()
    T = tk.Text(top, height = 5, width = 52)
    Font_tuple=("Comic Sans MS",10,'italic')
    T.configure(font = Font_tuple)
    statement = """Enter any text..."""
    T.pack()
    T.insert(tk.END, statement)
   
    def audio():
        mytext = T.get(1.0, "end-1c")
        language = 'en' 
        myobj = gTTS(text=mytext, lang=language, slow=False)    
        myobj.save("Sample.mp3")
        mydb=pymysql.connect(host="localhost",user="root",password="user",database="mydb")
        cur=mydb.cursor()
        cur.execute("create database if not exists mydb")
        cur.execute("CREATE TABLE IF NOT EXISTS Userdata(ID int AUTO_INCREMENT PRIMARY KEY,Previous_recodings varchar(255) NOT NULL)")
        sql="insert into userdata(Previous_recodings)values(%s)"
        values=(mytext)
        cur.execute(sql,values)
        mydb.commit()
    
    def play_audio():
        os.system("Sample.mp3") 
    
    def Popup_Window1():
        popupwindow =Toplevel(top)
        popupwindow.title("info")
        popupwindow.geometry("400x200")
        alert = Label(popupwindow,text="Successfully Converted to MP3",fg="green")
        alert.pack()
        Btn = tk.Button(popupwindow, text="Okay", command = popupwindow.destroy)
        Btn.pack()
        alert.place(relx=0.5, rely=0.3, anchor=N)
        Btn.place(relx=0.5, rely=0.5, anchor=CENTER)
        popupwindow.mainloop()
   
    def Popup_Window2():
        popupwindow =Toplevel(top)
        popupwindow.title("info")
        popupwindow.geometry("400x200")
        alert = Label(popupwindow,text="Audio Played Successfully",fg="green")
        alert.pack()
        Btn = tk.Button(popupwindow, text="Okay", command = popupwindow.destroy)
        Btn.pack()
        alert.place(relx=0.5, rely=0.3, anchor=N)
        Btn.place(relx=0.5, rely=0.5, anchor=CENTER)
        popupwindow.mainloop()
    
    def Popup_Window3():
        popupwindow =Toplevel(top)
        popupwindow.geometry("400x400")
        popupwindow.title("info")
        alert = Label(popupwindow,text="Successfully Displayed Previous Recodings",fg="green")
        alert.pack()
        Btn = tk.Button(popupwindow, text="Okay", command = popupwindow.destroy)
        Btn.pack()
        alert.place(relx=0.5, rely=0.3, anchor=N)
        Btn.place(relx=0.5, rely=0.5, anchor=CENTER)
        popupwindow.mainloop()
    
    def Fetch_Data():
        mydb=pymysql.connect(host="localhost",user="root",password="user",database="mydb")
        cur=mydb.cursor()
        cur.execute("SELECT id, Previous_recodings FROM userdata")
        global records
        records=cur.fetchall()
    
    def Display_Records():
        root = tk.Tk()
        root.title("Previous Recordings")
        label = tk.Label(root, text="Previous Recordings", font=("Arial",20)).grid(row=0, columnspan=3)
        cols = ('id','Previous_recodings')
        listBox = ttk.Treeview(root, columns=cols, show='headings')
        for i, (id, Previous_recodings) in enumerate(records, start=1):
            listBox.insert("", "end", values=(id,Previous_recodings))
        for col in cols:
            listBox.heading(col, text=col)
            listBox.grid(row=1, column=0, columnspan=2)
            closeButton = tk.Button(root, text="Close", width=15, command=root.destroy).grid(row=4, column=1)
        Popup_Window3()
        root.mainloop()
        
    b1=tk.Button(top,font=('Comic Sans MS',10),text="Convert to mp3",bg="#EED2EE",width=50,padx=10,pady=10,command=lambda:[audio(),Popup_Window1()])
    b1.pack(padx=17,pady=16)
    b2=tk.Button(top,font=('Comic Sans MS',10),text="Play Audio",bg="#C1FFC1",width=40,padx=10,pady=10,command=lambda:[play_audio(),Popup_Window2()])
    b2.pack(padx=15,pady=10)
    b3=tk.Button(top,font=('Comic Sans MS',10),text="Previous Recordings",bg="#DCDCDC",width=30,padx=10,pady=10,command=lambda:[Fetch_Data(),Display_Records()])
    b3.pack(padx=15,pady=10)
    b4=tk.Button(top,font=('Comic Sans MS',10),text="EXIT",bg="#CD2626",width=20,padx=10,pady=10,command=top.destroy)
    b4.pack(padx=15,pady=10)
    top.mainloop()

front()