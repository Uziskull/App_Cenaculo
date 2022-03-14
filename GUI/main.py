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
from modelos import Proposta, Utilizador, ESTADOS_PROPOSTA, ESTADOS_PROPOSTA_CORES
import textwrap
import threading

#db = DB("http://192.168.43.72:7777/api")
db = DB()


lista_propostas = db.ver_todas_propostas_e_votos()
lista_utilizadores = db.ver_utilizadores()
aberta = None

def get_current_poll():
    index_list = listBoxOn.curselection()
    if len(index_list) == 1:
        index = index_list[0]
        return lista_propostas[index]

def getListboxValue(event):
	cs = listBoxOn.curselection()
	if len(cs) == 1:
		item = cs[0]
		proposal.config(text="Proposta {}:\n{}".format(str(item+1), "\n".join(textwrap.wrap(listBoxOn.get(item), 50))))
		#messagebox.showinfo("Descrição da Proposta", listBoxOn.get(item))

		ax.clear()
		ax.bar(ind, lista_propostas[item].votos, width)
		canvas.draw()
		
		poll_status = lista_propostas[item].status
		if poll_status is None:
			vote_status_label.config(text='')
		else:
			vote_status_label.config(text="Estado: {}".format(ESTADOS_PROPOSTA[poll_status]), fg=ESTADOS_PROPOSTA_CORES[poll_status])

def onClick():
	if len(entry.get(1.0, 'end-1c')) > 0:
		nova_proposta = db.criar_proposta(entry.get(1.0, "end-1c"))
		lista_propostas.append(nova_proposta)
		listBoxOn.insert(END, entry.get(1.0, "end-1c"))
		entry.delete(1.0, "end-1c")
		

def open():
	global aberta
	try: 
		current_poll = get_current_poll()
		db.abrir_votos_proposta(current_poll)
		aberta = lista_propostas.index(current_poll)
	except AttributeError:
		messagebox.showerror('Erro', 'Não há nenhuma proposta selecionada!')
	except Exception as e:
		messagebox.showerror('Erro', e)

def close():
	global aberta
	try:
		current_poll = get_current_poll()
		index = lista_propostas.index(current_poll)
		updated_poll = db.fechar_votos_proposta(current_poll)
		lista_propostas[index] = updated_poll
		aberta = None

		# dar print a tudo outra vez
		getListboxValue(None)
	except AttributeError: 
		messagebox.showerror('Erro', 'Não há nenhuma proposta selecionada!')
	except Exception as e:
		messagebox.showerror('Erro', e)

def delete():
	try:
		db.apagar_proposta(get_current_poll())
		i = listBoxOn.curselection()[0]
		lista_propostas.pop(i)
		listBoxOn.delete(i)
	except AttributeError: 
		messagebox.showerror('Erro', 'Não há nenhuma proposta selecionada!')
	except Exception as e:
		messagebox.showerror('Erro', e)


def confirmar(novo_texto, id):
	if len(novo_texto.strip()) == 0:
		messagebox.showerror('Erro', 'Não alteraste nada da proposta!')
		return
	try:
		atual = lista_propostas[id]
		atual.description=novo_texto
		db.alterar_proposta(atual)
		lista_propostas[id] = atual
		listBoxOn.delete(id)
		listBoxOn.insert(id, novo_texto)
	except Exception as e:
		messagebox.showerror('Erro', e)


def edit(id_tuple):
	try:
		id = id_tuple[0]
	except Exception:
		messagebox.showerror('Erro', 'Não há nenhuma proposta selecionada!')
		return
	
	change = Toplevel()
	change.grab_set()
	change.title('Alteração')
	change.geometry('500x224')

	u_label = Label(change, font=('arial', 12, 'normal'), text='Escreve a proposta alterada')
	u_label.place(relx=0.25, rely=0.05, relwidth=0.5, relheight=0.05)

	u_entry = Text(change, height=4)
	u_entry.place(relx=0.3, rely=0.13, relwidth=0.4, relheight=0.2)
	u_entry.insert(1.0, lista_propostas[id].description)

	create_button = Button(change, bg='RED', command=lambda: confirmar(u_entry.get(1.0, "end-1c"), id), fg='WHITE', height=3, text='Prontíssimo!')
	create_button.place(relx=0.45, rely=0.35, relwidth=0.1, relheight=0.05)

	change.mainloop()

def ver_users():
	users = Toplevel()
	users.title("Utilizadores")
	users.geometry('400x500')
	
	u_label = Label(users, font=('arial', 12, 'normal'), text='Adiciona um novo utilizador')
	u_label.place(relx=0.25, rely=0.05, relwidth=0.5, relheight=0.05)

	u_entry = Text(users, height=6)
	u_entry.place(relx=0.2, rely=0.13, relwidth=0.6, relheight=0.2)

	listadeusers=Listbox(users, selectmode='SINGLE', bg='#FFFFFF', font=('arial', 12, 'normal'), width=0, height=0)
	listadeusers.place(relx=0.2, rely=0.45, relwidth=0.6, relheight=0.4)

	create_button = Button(users, bg='RED', command=lambda: addUser(listadeusers, u_entry), fg='WHITE', height=3, text='Adicionar')
	create_button.place(relx=0.425, rely=0.35, relwidth=0.15, relheight=0.06)

	delete_button = Button(users, bg='RED', fg='WHITE', height=3, text='Apagar', command=lambda: delete_user(listadeusers))
	delete_button.place(relx=0.44, rely=0.875, relwidth=0.12, relheight=0.06)

	
	for user in lista_utilizadores:
		listadeusers.insert(END, user.email)

	users.mainloop()

def delete_user(listadeusers):
	try:
		i = listadeusers.curselection()[0]
		db.remover_utilizador(lista_utilizadores[i])
		lista_utilizadores.pop(i)
		listadeusers.delete(i)
	except IndexError: 
		messagebox.showerror('Erro', 'Não há nenhum utilizador selecionado!')
	except Exception as e:
		messagebox.showerror('Erro', e)

def addUser(listbox_utilizadores, u_entry):
	emails = u_entry.get(1.0, 'end-1c')
	if len(emails) > 0:
		emails = [l for l in emails.splitlines() if len(l)>0]
		novo_user = db.adicionar_utilizadores(emails)
		lista_utilizadores.extend(novo_user)
		for email in emails:
			listbox_utilizadores.insert(END, email)
		u_entry.delete(1.0, "end-1c")

root = Tk()


root.geometry("1380x700")
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
for proposta in lista_propostas:
	listBoxOn.insert(END, proposta.description)

delete_button = Button(bg='RED', fg='WHITE', height=3, text='Apagar', command=delete)
delete_button.place(relx=0.165, rely=0.875, relwidth=0.07, relheight=0.05)

edit_button = Button(bg='RED', fg='WHITE', height=3, text='Editar', command=lambda: edit(listBoxOn.curselection()))
edit_button.place(relx=0.265, rely=0.875, relwidth=0.07, relheight=0.05)

proposal = Label(text='', bg='#F0F8FF', width=100, font=('arial', 12, 'normal'))
proposal.place(relx=0.5, rely=0.025, relwidth=0.5, relheight=0.15)

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
#canvas.draw()
canvas.get_tk_widget().place(relx=0.55, rely=0.25, relwidth=0.4, relheight=0.5)

vote_status_label = Label(text='', bg='#F0F8FF', width=100, font=('arial', 12, 'normal'))
vote_status_label.place(relx=0.55, rely=0.20, relwidth=0.1, relheight=0.05)

def atualizar_votos():
	global aberta
	timer_votos = threading.Timer(1.0, atualizar_votos)
	timer_votos.daemon = True
	timer_votos.start()

	if aberta is not None:
		try:
			prop = lista_propostas[aberta]
			prop = db.atualizar_votos_proposta(prop)
			lista_propostas[aberta] = prop
			ax.clear()
			ax.bar(ind, prop.votos, width)
			canvas.draw()
		except Exception as e:
			print("Erro ao atualizar votos: {}".format(e))
	
#atualizar_votos()

root.config(menu = menu)
root.mainloop()

