## Programa para estoque em lojas

## Bibliotecas
import tkinter
from tkinter import messagebox
from tkinter.simpledialog import askinteger, askstring
from tkinter.ttk import Treeview
import customtkinter
from tkinter import *
from customtkinter import *
import mysql.connector

## OBS - Todas as conexões com o banco de dados estão desconfiguradas, portanto, é necessario colocar a conexão com o mesmo, como o "HOST,USER,PASSWORD,DATABASE".

##DB
conect = mysql.connector.connect(host="HOST DO SEU DB",user='USUARIO',passwd='SENHA',db='DATABASE')

## Window config
root = Tk()
root.title("Controle")
root.configure(background="#F2E3D5")
root.geometry("650x350")

## Functions
#Função para facilitar a conexão ao DATABASE
def conectar():
    conect = mysql.connector.connect(host="HOST DO SEU DB",user='USUARIO',passwd='SENHA',db='DATABASE')
    cursor = conect.cursor()
    cursor.execute(f'select count(*) from produtos;')
    quantidade = cursor.fetchone()
    quantidade = quantidade[0]
    cont = 0
    while cont < quantidade:
        cursor.execute(f'select codigo from produtos;')
        cod = cursor.fetchall()
        cursor.execute(f'select nomeprod from produtos;')
        prod1 = cursor.fetchall()
        cursor.execute(f'select quantidade from produtos;')
        quanti = cursor.fetchall()
        lista.insert("",tkinter.END,text=cod[cont],values=(prod1[cont],quanti[cont]))
        cont +=1

#Função para editar um produto
def editar():
    conect = mysql.connector.connect(host="HOST DO SEU DB",user='USUARIO',passwd='SENHA',db='DATABASE')
    cursor = conect.cursor()
    oq = askstring("EDITAR","O que deseja alterar?\n-CODIGO\n-NOME\n-QUANTIDADE")
    oq = oq.lower()
    if oq == "codigo":
        cdat = askstring("Codigo","Qual o antigo código?")
        cursor.execute(f'select nomeprod from produtos where codigo = {cdat};')
        prod = cursor.fetchone()
        cd = askstring("CODIGO","Qual o novo código?")
        cd = int(cd)
        prod = prod[0]
        cursor.execute(f'update produtos set codigo = {cd} where nomeprod = "{prod}";')
        conect.commit()
        messagebox.showinfo("TROCA",f'O codigo = {cdat} foi alterado para = {cd}')
        lista.delete(*lista.get_children())
        conectar()
    elif oq == "nome":
        nmat = askstring("NOME","Qual o antigo nome?")
        cursor.execute(f'select codigo from produtos where nomeprod = "{nmat}";')
        cod = cursor.fetchone()
        cod = cod[0]
        nm = askstring("NEW","Digite o novo nome")
        cursor.execute(f'update produtos set nomeprod = "{nm}" where codigo = {cod};')
        conect.commit()
        messagebox.showinfo("TROCA",f'O nome = {nmat} foi alterado para = {nm}')
        lista.delete(*lista.get_children())
        conectar()
    elif oq == "quantidade":
        qtat = askinteger("QUANTIDADE","Qual o produto para ser alterada a quantidade?\nOBS: Digitar o codigo do produto")
        cursor.execute(f'select quantidade from produtos where codigo = {qtat}')
        qu = cursor.fetchone()
        qu = qu[0]
        qtnv = askinteger("QUANTIDADE","Digite qual vai ser a nova quantidade")
        cursor.execute(f'update produtos set quantidade = {qtnv} where codigo = {qtat};')
        conect.commit()
        messagebox.showinfo("TROCA",f'A quantidade que era = {qu}\nPassou a ser = {qtnv}')
        lista.delete(*lista.get_children())
        conectar()

#Função para remover um produto
def remove():
    prod = askstring("REMOVER","Digite qual produto deseja remover, colocar o código apenas")
    messagebox.showwarning("REMOÇÃO",f"Você removeu o item  de código {prod}")
    conect = mysql.connector.connect(host="HOST DO SEU DB",user='USUARIO',passwd='SENHA',db='DATABASE')
    cursor = conect.cursor()
    cursor.execute(f'delete from produtos where codigo = {prod};')
    conect.commit()
    lista.delete(*lista.get_children())
    conectar()
    
    
#Função para adicionar um produto   
def add():
    prod = askstring("PRODUTO","Digite qual o produto, seguido de seu código, colocando ' - ' para separar")
    hifen = prod.find("-")
    tudo = prod.replace(" ","")
    tudo = prod.replace("-","")
    codigo = tudo[hifen:]
    produto = tudo[:hifen]
    qut = askinteger("Quantidade","Qual a quantidade do produto?")
    ## Adicionar o produto no database
    conect = mysql.connector.connect(host="HOST DO SEU DB",user='USUARIO',passwd='SENHA',db='DATABASE')
    cursor = conect.cursor()
    cursor.execute(f'insert into produtos values("{codigo}","{produto}","{qut}");')
    conect.commit()
    lista.insert("",tkinter.END,text=codigo,values=produto)
    lista.delete(*lista.get_children())
    conectar()
    



##NULL LAYOUT
null = Label(root, text="   ", bg="#F2E3D5")
null6 = Label(root, text="   ", bg="#F2E3D5")
null1 = Label(root, text="   ", bg="#F2E3D5")
null2 = Label(root, text="   ", bg="#F2E3D5")
null3 = Label(root, text="   ", bg="#F2E3D5")
null4 = Label(root, text="Gestão de estoque", fg="Black",bg="#F2E3D5",font=("Franklin Gothic Demi",20))
null.grid(column=1,row=0)
null1.grid(column=3,row=0)
null2.grid(column=2,row=2)
null3.grid(column=2,row=4)
null6.grid(column=2,row=6,rowspan=2)
null4.grid(column=2,row=0,columnspan=4)


## Window layout
prods = CTkFrame(master=root,
                 fg_color="White",
                 width=450,
                 height=450)
prods.grid(column=4,row=1,rowspan=6,columnspan=2)
columns1 = ("Codigo","Quantidade")
lista = Treeview(prods,columns=columns1,padding=5,takefocus=True)
lista.grid(sticky=N)
lista.heading('#0', text="Codigo")
lista.heading('Codigo',text="Nome")
lista.heading('Quantidade',text="X")
lista.column('Quantidade',width=50)
lista.column('#0',width=150)
conectar()


addprod = CTkButton(master=root,
                    text="Add Product",
                    text_color="Green",
                    fg_color="#F2E3D5",
                    text_font=("Franklin Gothic Demi",15),
                    height=75,
                    width=150,
                    command=add)
addprod.grid(column=2,row=1)

removeprod = CTkButton(master=root,
                       text="Remove Product",
                       text_color="Red",
                       fg_color="#F2E3D5",
                       text_font=("Franklin Gothic Demi",15),
                        height=75,
                        width=150,
                        command=remove)
removeprod.grid(column=2,row=3)

edit = CTkButton(master=root,
                text="EDIT Product",
                text_color="Black",
                fg_color="#F2E3D5",
                text_font=("Franklin Gothic Demi",15),
                height=75,
                width=150,
                command=editar)
edit.grid(column=2,row=5)

## LOOOOP Window
root.mainloop()