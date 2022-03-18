from re import I
import tkinter as tk
from tkinter import ttk
from tkinter import *
from turtle import bgcolor
import matplotlib, numpy, sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import messagebox
from servidor import DB
from modelos import Proposta, Utilizador, ESTADOS_PROPOSTA, ESTADOS_PROPOSTA_CORES
import textwrap
import threading

#db = DB("http://localhost:5000/api")
db = DB()


lista_propostas = db.ver_todas_propostas_e_votos()
lista_utilizadores = db.ver_utilizadores()
aberta = db.ver_proposta_ativa()
if aberta is not None:
	aberta = [i for i in range(len(lista_propostas)) if lista_propostas[i].id == aberta.id][0]

def get_current_poll():
    index_list = listBoxOn.curselection()
    if len(index_list) == 1:
        index = index_list[0]
        return lista_propostas[index]

#def getListboxValue(event):
#	global active
#	cs = listBoxOn.curselection()
#	if len(cs) == 1:
#		item = cs[0]

#		proposal.config(text="Proposta {}:\n{}".format(str(item+1), "\n".join(textwrap.wrap(listBoxOn.get(item), 50))))
#		#messagebox.showinfo("Descrição da Proposta", listBoxOn.get(item))

#		ax.clear()
#		ax.bar(ind, lista_propostas[item].votos, width)
#		canvas.draw()

#		vote_count.config(text="Votação {}".format("Aberta" if active == item else "Fechada"))
#		
#		poll_status = lista_propostas[item].status
#		if poll_status is None:
#			vote_status_label.config(text='')
#		else:
#			vote_status_label.config(text="Estado: {}".format(ESTADOS_PROPOSTA[poll_status]), fg=ESTADOS_PROPOSTA_CORES[poll_status])

def onClick():
	if len(entry.get(1.0, 'end-1c')) > 0:
		nova_proposta = db.criar_proposta(entry.get(1.0, "end-1c"))
		lista_propostas.append(nova_proposta)
		listBoxOn.insert(END, entry.get(1.0, "end-1c"))
		entry.delete(1.0, "end-1c")
		

#def open():
#	global aberta
#	try: 
#		current_poll = get_current_poll()
#		db.abrir_votos_proposta(current_poll)
#		aberta = lista_propostas.index(current_poll)
#	except AttributeError:
#		messagebox.showerror('Erro', 'Não há nenhuma proposta selecionada!')
#	except Exception as e:
#		messagebox.showerror('Erro', e)

#def close():
#	global aberta
#	try:
#		current_poll = get_current_poll()
#		index = lista_propostas.index(current_poll)
#		updated_poll = db.fechar_votos_proposta(current_poll)
#		lista_propostas[index] = updated_poll
#		aberta = None

		# dar print a tudo outra vez
#		getListboxValue(None)
#	except AttributeError: 
#		messagebox.showerror('Erro', 'Não há nenhuma proposta selecionada!')
#	except Exception as e:
#		messagebox.showerror('Erro', e)

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
	u_label.place(relx=0.25, rely=0.15, relwidth=0.5, relheight=0.1)

	u_entry = Text(change, height=6)
	u_entry.place(relx=0.2, rely=0.28, relwidth=0.6, relheight=0.4)
	u_entry.insert(1.0, lista_propostas[id].description)

	create_button = Button(change, bg='RED', command=lambda: confirmar(u_entry.get(1.0, "end-1c"), id), fg='WHITE', height=3, text='Prontíssimo!')
	create_button.place(relx=0.4, rely=0.72, relwidth=0.2, relheight=0.1)

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

def janela_nova(listbox_cursel):
	global aberta
	
	try:
		id = listbox_cursel[0]
	except Exception:
		messagebox.showerror('Erro', 'Não há nenhuma proposta selecionada!')
		return

	detalhes_proposta = Toplevel()
	detalhes_proposta.grab_set()
	detalhes_proposta.title('Proposta {}'.format(id + 1))
	detalhes_proposta.geometry('1000x700')
	detalhes_proposta.configure(background='#F0F8FF')

	def view_proposal_details():
		proposta = lista_propostas[id]

		proposal_label.config(text="Proposta {}:\n{}".format(str(id+1), "\n".join(textwrap.wrap(proposta.description, 50))))

		if proposta.status is not None:
			plt_fig_ax.clear()
			plt_fig_ax.bar(plt_fig_ind, proposta.votos, plt_fig_width)
			canvas.draw()

		if aberta == id:
			vote_count.config(text="Votação Aberta\nVotos: {}/{}".format(sum(list(proposta.votos)), len(lista_utilizadores)))
		else:
			vote_count.config(text="Votação Fechada")
		
		poll_status = proposta.status
		if poll_status is None:
			vote_status_label.config(text='')
		else:
			vote_status_label.config(text="Estado: {}".format(ESTADOS_PROPOSTA[poll_status]), fg=ESTADOS_PROPOSTA_CORES[poll_status])

	def open():
		global aberta
		try: 
			current_poll = lista_propostas[id]
			db.abrir_votos_proposta(current_poll)
			aberta = lista_propostas.index(current_poll)
			open_button["state"] = "disabled"
			close_button["state"] = "normal"
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
			open_button["state"] = "normal"
			close_button["state"] = "disabled"

			# dar print a tudo outra vez
			view_proposal_details()
		except AttributeError: 
			messagebox.showerror('Erro', 'Não há nenhuma proposta selecionada!')
		except Exception as e:
			messagebox.showerror('Erro', e)

	plt_fig = Figure(figsize=(3,2), dpi=150, facecolor= '#F0F8FF')
	plt_fig_ax = plt_fig.add_subplot(111)
	plt_fig_ax.set_ylim([0, max(len(lista_utilizadores), 5)])

	plt_fig_ind = ('Favor', 'Contra', 'Abstenções') 
	plt_fig_width = 0.5
	plt_fig_ax.bar(plt_fig_ind, (0,0,0), plt_fig_width)

	canvas = FigureCanvasTkAgg(plt_fig, master=detalhes_proposta)
	canvas_widget = canvas.get_tk_widget()
	canvas_widget.place(relx=0.2, rely=0.25, relwidth=0.6, relheight=0.5)

	proposal_label = Label(detalhes_proposta, text='', bg='#F0F8FF', width=100, font=('arial', 12, 'normal'))
	proposal_label.place(relx=0.25, rely=0.025, relwidth=0.5, relheight=0.15)

	vote_count = Label(detalhes_proposta, text='Votação Fechada', bg='#F0F8FF', width=100, font=('arial', 12, 'normal'))
	vote_count.place(relx=0.25, rely=0.25, relwidth=0.15, relheight=0.05)

	vote_status_label = Label(detalhes_proposta, text='', bg='#F0F8FF', width=100, font=('arial', 12, 'normal'))
	vote_status_label.place(relx=0.65, rely=0.25, relwidth=0.2, relheight=0.05)

	open_button = Button(detalhes_proposta, bg='RED', fg='WHITE', height=3, text='Abrir Votação', command=open)
	open_button.place(relx=0.33, rely=0.8, relwidth=0.15, relheight=0.07)

	close_button = Button(detalhes_proposta, bg='RED', fg='WHITE', height=3, text='Fechar Votação', command=close)
	close_button.place(relx=0.52, rely=0.8, relwidth=0.15, relheight=0.07)

	# desativar botões se necessário
	print("aberta: " + str(aberta))
	print("id: " + str(id))
	if aberta == id:
		open_button["state"] = "disabled"
	elif aberta != None: # se existir outra aberta, não abrir nem fechar esta
		open_button["state"] = "disabled"
		close_button["state"] = "disabled"
	else:
		close_button["state"] = "disabled"

	def atualizar_votos():
		if aberta == id:
			try:
				prop = lista_propostas[aberta]
				prop = db.atualizar_votos_proposta(prop)
				lista_propostas[aberta] = prop
				# ax.clear()
				# ax.bar(ind, prop.votos, width)
				# canvas.draw()
				vote_count.config(text="Votação Aberta\nVotos: {}/{}".format(sum(list(prop.votos)), len(lista_utilizadores)))
			except TclError:
				# ignorar
				return
			except Exception as e:
				print("Erro ao atualizar votos: {}".format(e))
		
		timer_votos = threading.Timer(1.0, atualizar_votos)
		timer_votos.daemon = True
		timer_votos.start()
		
	atualizar_votos()

	# ver detalhes de proposta
	view_proposal_details()

	def on_close():
		detalhes_proposta.destroy()

	detalhes_proposta.protocol('WM_DELETE_WINDOW', on_close)

	detalhes_proposta.mainloop()

root = Tk()


root.geometry("1000x700")
root.configure(background='#F0F8FF')
root.title('App Cenáculo')

label = Label(bg='#F0F8FF', font=('arial', 12, 'normal'), text='Cria uma nova proposta')
label.place(relx=0.35, rely=0.05, relwidth=0.3, relheight=0.05)
entry = Text(height=6)
entry.place(relx=0.3, rely=0.13, relwidth=0.4, relheight=0.2)
entry.bind('<Return>', lambda x: 'break')

create_button = Button(bg='RED', command=onClick, fg='WHITE', height=3, text='Criar')
create_button.place(relx=0.47, rely=0.35, relwidth=0.06, relheight=0.05)

#open_button = Button(bg='RED', fg='WHITE', height=3, text='Abrir Votação', command=open)
#open_button.place(relx=0.63, rely=0.8, relwidth=0.11, relheight=0.05)

#close_button = Button(bg='RED', fg='WHITE', height=3, text='Fechar Votação', command=close)
#close_button.place(relx=0.77, rely=0.8, relwidth=0.11, relheight=0.05)

listBoxOn=Listbox(root, selectmode='SINGLE', bg='#FFFFFF', font=('arial', 12, 'normal'), width=0, height=0)
listBoxOn.bind('<Double-1>', lambda _: janela_nova(listBoxOn.curselection()))
listBoxOn.place(relx=0.3, rely=0.45, relwidth=0.4, relheight=0.4)
for proposta in lista_propostas:
	listBoxOn.insert(END, proposta.description)

delete_button = Button(bg='RED', fg='WHITE', height=3, text='Apagar', command=delete)
delete_button.place(relx=0.415, rely=0.875, relwidth=0.07, relheight=0.05)

edit_button = Button(bg='RED', fg='WHITE', height=3, text='Editar', command=lambda: edit(listBoxOn.curselection()))
edit_button.place(relx=0.515, rely=0.875, relwidth=0.07, relheight=0.05)

menu = Menu()
ver = Menu(menu, tearoff= 0)
ver.add_command(label="Utilizadores", command = ver_users)
ver.add_separator()
ver.add_command(label = "Exit", command = root.quit)
menu.add_cascade(label = "Ver", menu = ver)

#f = Figure(figsize=(3,2), dpi=100, facecolor= '#F0F8FF')
#ax = f.add_subplot(111)

#data = (1,2,3)

#ind = ('Favor', 'Contra', 'Abstenções') 
#width = 0.5

#rects1 = ax.bar(ind, data, width)

#canvas = FigureCanvasTkAgg(f, master=root)
#canvas.draw()
#canvas_widget = canvas.get_tk_widget()
#canvas_widget.place(relx=0.55, rely=0.25, relwidth=0.4, relheight=0.5)

#vote_count = Label(text='Votação Fechada', bg='#F0F8FF', width=100, font=('arial', 12, 'normal'))
#vote_count.place(relx=0.55, rely=0.25, relwidth=0.1, relheight=0.05)

#vote_status_label = Label(text='', bg='#F0F8FF', width=100, font=('arial', 12, 'normal'))
#vote_status_label.place(relx=0.85, rely=0.25, relwidth=0.1, relheight=0.05)

#def atualizar_votos():
#	global aberta
#	timer_votos = threading.Timer(1.0, atualizar_votos)
#	timer_votos.daemon = True
#	timer_votos.start()
#
#	cs = listBoxOn.curselection()
#	if aberta is not None and len(cs) > 0 and cs[0] == aberta:
#		try:
#			prop = lista_propostas[aberta]
#			prop = db.atualizar_votos_proposta(prop)
#			lista_propostas[aberta] = prop
#			# ax.clear()
#			# ax.bar(ind, prop.votos, width)
#			# canvas.draw()
#			vote_count.config(text="Votação Aberta\nVotos: {}/{}".format(sum(list(prop.votos)), len(lista_utilizadores)))
#		except Exception as e:
#			print("Erro ao atualizar votos: {}".format(e))
	
#atualizar_votos()

root.config(menu = menu)
root.mainloop()



