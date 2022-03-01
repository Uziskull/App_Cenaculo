from re import I
import tkinter as tk
from tkinter import ttk
from tkinter import *
from turtle import bgcolor
import matplotlib, numpy, sys
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import messagebox
from servidor import DB
from modelos import Proposta, Utilizador

db = DB()


lista_propostas = []
lista_utilizadores = []

def getListboxValue(event):
	cs = listBoxOn.curselection()
	if len(cs) == 1:
		item = cs[0]
		proposal.config(text="Proposta " + str(item+1))
		messagebox.showinfo("Descrição da Proposta", listBoxOn.get(item))

def onClick():
	if len(entry.get(1.0, 'end-1c')) > 0:
		nova_proposta = db.criar_proposta(entry.get(1.0, "end-1c"))
		lista_propostas.append(nova_proposta)
		listBoxOn.insert(END, entry.get(1.0, "end-1c"))
		entry.delete(1.0, "end-1c")
		

def open():
	db.abrir_votos_proposta(listBoxOn.curselection())

def close():
	db.fechar_votos_proposta(listBoxOn.curselection())

def delete():
	db.apagar_proposta(listBoxOn.curselection())
	lista_propostas.remove(listBoxOn.curselection())
	listBoxOn.delete(listBoxOn.curselection())


def edit():
	db.alterar_proposta(listBoxOn.curselection())

def ver_users():
	users = Toplevel()
	users.title("Utilizadores")
	users.geometry('410x224')
	
	u_entry = Text(height=6)
	u_entry.place(relx=0.05, rely=0.13, relwidth=0.4, relheight=0.2)
	listadeusers=Listbox(users, selectmode='SINGLE', bg='#FFFFFF', font=('arial', 12, 'normal'), width=0, height=0)
	listadeusers.place(relx=0.05, rely=0.45, relwidth=0.4, relheight=0.4)
	create_button = Button(bg='RED', command=lambda: addUser(listadeusers, u_entry), fg='WHITE', height=3, text='Criar')
	create_button.place()
	db.ver_utilizadores()
	users.mainloop()

def addUser(listbox_utilizadores, u_entry):
	emails = u_entry.get(1.0, 'end-1c')
	if len(emails) > 0:
		emails = [l for l in emails.splitlines() if len(l)>0]
		novo_user = db.adicionar_utilizadores(emails)
		lista_utilizadores.extend(novo_user)
		listbox_utilizadores.insert(END, *emails)
		u_entry.delete(1.0, "end-1c")


root = Tk()

# This is the section of code which creates the main window
root.geometry('820x448')
root.configure(background='#F0F8FF')
root.title('App Cenáculo')

label = Label(bg='#F0F8FF', font=('arial', 12, 'normal'), text='Cria uma nova proposta')
label.place(relx=0.1, rely=0.05, relwidth=0.3, relheight=0.05)
entry = Text(height=6)
entry.place(relx=0.05, rely=0.13, relwidth=0.4, relheight=0.2)
entry.bind('<Return>', lambda x: 'break')

create_button = Button(bg='RED', command=onClick, fg='WHITE', height=3, text='Criar')
create_button.place(relx=0.22, rely=0.35, relwidth=0.06, relheight=0.05)

open_button = Button(bg='RED', fg='WHITE', height=3, text='Abrir Votação', command=open)
open_button.place(relx=0.63, rely=0.8, relwidth=0.11, relheight=0.05)

close_button = Button(bg='RED', fg='WHITE', height=3, text='Fechar Votação', command=close)
close_button.place(relx=0.77, rely=0.8, relwidth=0.11, relheight=0.05)

listBoxOn=Listbox(root, selectmode='SINGLE', bg='#FFFFFF', font=('arial', 12, 'normal'), width=0, height=0)
listBoxOn.bind('<Double-1>', getListboxValue)
listBoxOn.place(relx=0.05, rely=0.45, relwidth=0.4, relheight=0.4)

delete_button = Button(bg='RED', fg='WHITE', height=3, text='Apagar', command=delete)
delete_button.place(relx=0.165, rely=0.875, relwidth=0.07, relheight=0.05)

edit_button = Button(bg='RED', fg='WHITE', height=3, text='Editar', command=edit)
edit_button.place(relx=0.265, rely=0.875, relwidth=0.07, relheight=0.05)

proposal = Label(text='', bg='#F0F8FF', width=100, font=('arial', 12, 'normal'))
proposal.place(relx=0.6, rely=0.2, relwidth=0.3, relheight=0.05)

menu = Menu()
ver = Menu(menu, tearoff= 0)
ver.add_command(label="Utilizadores", command = ver_users)
ver.add_separator()
ver.add_command(label = "Exit", command = root.quit)
menu.add_cascade(label = "Ver", menu = ver)

f = Figure(figsize=(3,2), dpi=100, facecolor= '#F0F8FF')
ax = f.add_subplot(111)

data = (1,2,3)

ind = ('Favor', 'Contra', 'Abstenções') 
width = 0.5

rects1 = ax.bar(ind, data, width)

canvas = FigureCanvasTkAgg(f, master=root)
canvas.draw()
canvas.get_tk_widget().place(relx=0.55, rely=0.25, relwidth=0.4, relheight=0.5)

root.config(menu = menu)
root.mainloop()