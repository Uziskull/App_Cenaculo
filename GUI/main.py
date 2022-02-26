import tkinter as tk
from tkinter import ttk
from tkinter import *
from turtle import bgcolor
import matplotlib, numpy, sys
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from modelos import Proposta
import servidor

db = servidor.DB()
lista_propostas = []

# this is a function to get the selected list box value
def onClick():
	desc = entry.get(1.0, 'end-1c')
	if len(desc) > 0:
		# try:
		prop = db.criar_proposta(desc)
		lista_propostas.append(prop)
		listBoxOn.insert(END, desc)
		# except Exception as e:
		# 	print(e)
		entry.delete(1.0, "end-1c")

def onListboxSelect(e):
	w = e.widget
	index = int(w.curselection()[0])
	value = w.get(index) if index >= 0 else "Seleciona uma proposta"
	proposal.config(text = value)

root = Tk()

# This is the section of code which creates the main window
root.geometry('820x448')
root.configure(background='#F0F8FF')
root.title('App Cenáculo')

label = Label(bg='WHITE', font=('arial', 12, 'normal'), text='Cria uma nova proposta')
label.place(relx=0.1, rely=0.05, relwidth=0.3, relheight=0.05)
entry = Text(height=6)
entry.place(relx=0.05, rely=0.13, relwidth=0.4, relheight=0.2)

create_button = Button(bg='RED', command=onClick, fg='WHITE', height=3, text='Criar')
create_button.place(relx=0.22, rely=0.35, relwidth=0.06, relheight=0.05)

open_button = Button(bg='RED', fg='WHITE', height=3, text='Abrir Votação')
open_button.place(relx=0.63, rely=0.8, relwidth=0.11, relheight=0.05)

close_button = Button(bg='RED', fg='WHITE', height=3, text='Fechar Votação')
close_button.place(relx=0.77, rely=0.8, relwidth=0.11, relheight=0.05)

listBoxOn=Listbox(root, bg='#FFFFFF', font=('arial', 12, 'normal'), width=0, height=0)
listBoxOn.place(relx=0.05, rely=0.45, relwidth=0.4, relheight=0.5)
listBoxOn.bind("<<ListboxSelect>>", onListboxSelect)

def update_list():
	lista_propostas = db.ver_todas_propostas_e_votos()
	for proposta in lista_propostas:
		listBoxOn.insert(END, proposta)

proposal = Label(text = "Seleciona uma proposta")
proposal.place(relx=0.6, rely=0.15, relwidth=0.3, relheight=0.05)

f = Figure(figsize=(3,2), dpi=100)
ax = f.add_subplot(111)

data = (1,2,3)

ind = ('Favor', 'Contra', 'Abstenções') 
width = 0.5

rects1 = ax.bar(ind, data, width)

canvas = FigureCanvasTkAgg(f, master=root)
canvas.draw()
canvas.get_tk_widget().place(relx=0.55, rely=0.25, relwidth=0.4, relheight=0.5)


root.mainloop()
