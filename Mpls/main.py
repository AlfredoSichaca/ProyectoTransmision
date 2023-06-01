from __future__ import division

import math
import time
from threading import Thread
from tkinter import END, LEFT, RIGHT, Button, Entry, Label, Listbox, Menu, Toplevel, messagebox, Tk, Canvas, BOTH, YES
from tkinter.filedialog import *
from tkinter.ttk import Combobox

from PIL import Image, ImageTk

from Ventana import *

#ventana principal
Ventana = Tk()
Ventana.state("zoomed")
Ventana.title("MPLS")
canvas = Canvas(Ventana, width=1200, height=650, bg="#b3b1b1", cursor="tcross")#taget
canvas.pack(fill=BOTH, expand=YES)
ancho = 40
li = []



# Crear Grafo
g = grafo()
l = []
img = Image.open('enviando.png')
msj = ImageTk.PhotoImage(img)


# Informacion del vertice
def click(event):
    for vert in g.listav:
        if event.x > vert.x and event.x < vert.x + ancho and event.y > vert.y and event.y < vert.y + ancho:
            info = Toplevel()
            info.title("Informacion del Punto")
            l1 = Label(info, text="Nombre:").grid(row=0, column=0)
            l2 = Label(info, text=vert.nombre).grid(row=0, column=1)
           
# Agregar vertice al mapa
def dobleclick(event):
    # Ingresar Vertice
    ingreso = Toplevel()
    ingreso.title("Agregar Punto")
    tnombre = Label(ingreso, text="Ingrese Nombre del vertice:")
    tnombre.grid(row=0, column=0)
    nombre = Entry(ingreso)
    nombre.grid(row=0, column=1)
    ttipo = Label(ingreso, text="Tipo del vertice:")
    ttipo.grid(row=1, column=0)
    opciones = ["LER", "LSR"]
    tipov = Combobox(ingreso, values=opciones, state="readonly")
    tipov.grid(row=1, column=1)
    agregar = Button(ingreso, text="Agregar",
                     command=lambda: agregarv(event.x, event.y,nombre.get(), tipov.get(), ingreso))
    agregar.grid(row=3, columnspan=2)

def agregarv(x, y, nombre,tipo, ingreso):

    vtemp = vertice(nombre, x, y, tipo)
    g.agregarVertice(vtemp)
    ingreso.destroy()
    actualizar()
    

def agregarA(frm, to, distancia, x1, y1, x2, y2):
    atemp = arista(frm, to, distancia, x1, y1, x2, y2)
    g.agregarArista(atemp)
    print(atemp.distancia)
    actualizar()

# Relacionar vertices
def clickrelacion():
    vrelacion = Toplevel()
    vrelacion.title("Agregar Ruta")
    opciones1 = Listbox(vrelacion, exportselection=0)
    opciones2 = Listbox(vrelacion, exportselection=0)
    for v in g.listav:
        opciones1.insert(END, v.nombre)
        opciones2.insert(END, v.nombre)
    opciones1.pack(side=LEFT)
    opciones2.pack(side=LEFT)
   
    relacionar2 = Button(vrelacion, text="Relacionar",
                         command=lambda: relacion(opciones1.get(opciones1.curselection()),
                                                  opciones2.get(opciones2.curselection()), vrelacion))
    relacionar2.pack()

def relacion(nv1, nv2, vrelacion):
    if (nv1 == nv2):
        vrelacion.destroy()
        messagebox.showinfo("Denegado", "No puede seleccionar el mismo punto de interes")
    else:

        for v in g.listav:
            if (nv1 == v.nombre):
                a = v
                for v in g.listav:
                    if (nv2 == v.nombre):
                        b = v
                        a.vecino(b)
                        d = distancias(a, b)
                        agregarA(a, b, d, a.x, a.y, b.x, b.y)
                        vrelacion.destroy()
        actualizar()

# Eliminar Vertices
def clickeliminarv():
    veliminar = Toplevel()
    veliminar.title("Eliminar Punto")
    t1 = Label(veliminar, text="Nombre punto de interes")
    t1.pack()
    opciones = Listbox(veliminar, exportselection=0)
    for v in g.listav:
        opciones.insert(END, v.nombre)
    opciones.pack()
    nombrev = Entry(veliminar)
    nombrev.pack()
    eliminar2 = Button(veliminar, text="Elimina desde listas",
                       command=lambda: eliminarv(opciones.get(opciones.curselection()), veliminar))
    eliminar2.pack()

def eliminarv(nombrev, veliminar):
    try:
        for v in g.listav:
            if (nombrev == v.nombre):
                a = v
            for i in v.la:
                if (nombrev == i.nombre):
                    b = i
                    v.la.remove(b)
        g.listav.remove(a)
        c = 0
        indice = []
        for a in g.listaA:
            if nombrev == a.frm.nombre or nombrev == a.to.nombre:
                c += 1
                indice.append(g.listaA.index(a))
        for i in reversed(indice):  
            del g.listaA[i]
        veliminar.destroy()
        actualizar()
    except:
        veliminar.destroy()
        messagebox.showerror("ERROR", "El punto no se encuentra")

# Eliminar Aristas
def clickeliminara():
    veliminara = Toplevel()
    veliminara.title("Eliminar Ruta")
    desde = Listbox(veliminara, exportselection=0)
    hasta = Listbox(veliminara, exportselection=0)
    for v in g.listav:
        desde.insert(END, v.nombre)
        hasta.insert(END, v.nombre)
    desde.pack(side=LEFT)
    hasta.pack(side=LEFT)
    
    eliminar2 = Button(veliminara, text="Eliminar",
                       command=lambda: eliminara(desde.get(desde.curselection()), hasta.get(hasta.curselection()),
                                                 veliminara))
    eliminar2.pack()

def eliminara(desde, hasta, veliminara):
    try:
        for v in g.listav:
            if (desde == v.nombre):
                a = v
                for i in a.la:
                    if (hasta == i.nombre):
                        b = i
                        a.la.remove(b)
        for ar in g.listaA:
            if (desde == ar.frm.nombre and hasta == ar.to.nombre):
                temp = ar
                g.listaA.remove(temp)
        veliminara.destroy()
        actualizar()
    except:
        print("No elimina ruta")

# Calcular Distancias
def distancias(a, b):
    distancia = math.sqrt(math.pow(b.x - a.x, 2) + math.pow(b.y - a.y, 2))
    return int(distancia)

def clickdijkstra():
    vdijkstra = Toplevel()
    vdijkstra.title("Añadir Etiquetas")
    t1 = Label(vdijkstra, text="Nombre del punto")
    t1.pack()
    opciones = Listbox(vdijkstra, exportselection=0)
    for v in g.listav:
        opciones.insert(END, v.nombre)
    opciones.pack()
    eliminar = Button(vdijkstra, text="Añadir etiqueta",
                      command=lambda: dijkstra(opciones.get(opciones.curselection()), vdijkstra))
    actualizar()
    eliminar.pack()

def dijkstra(inicio, vdijkstra):
    for i in g.listav:
        if inicio == i.nombre:
            indice = i
    listad, listap = g.dijkstra(indice)
    if (len(indice.la) == 0):
        messagebox.showinfo("Dijkstra", "El punto seleccionado no tiene rutas")
    else:
        resaltarcaminos(listap, li, indice)
        vdijkstra.destroy()
        mostrardijkstra = Toplevel()
        mostrardijkstra.title("Distancias")
        t1 = Label(mostrardijkstra, text="Suma de las etiquetas desde %s : " % (inicio.upper()), font="Verdana 10 bold")
        t1.pack()
        for i in range(len(g.listav)):
            if (listap[i] != None):
                dista = str(listad[i])    
                hastaa = g.listav[i].nombre
                hastaa = hastaa.upper()
                dista = dista[0:6]
                t2 = Label(mostrardijkstra, text=" hasta " + hastaa + " es: " + dista)
                t2.pack()


def dibujaxp(ruta,li):
    num=ancho/2
    for aris in li:
        canvas.delete(aris)
    del li[:]
    for i in range(len(ruta)):
        if(i!=(len(ruta)-1)):
            if (ruta[i].x >= ruta[i+1].x and ruta[i].y > ruta[i+1].y):
                    a = canvas.create_line(ruta[i].x + num, ruta[i].y, ruta[i+1].x + ancho, ruta[i+1].y + num,
                                           width=3, fill="#02F5A0", arrow="last", smooth=True)
                    li.append(a)
            if (ruta[i].x > ruta[i+1].x and ruta[i].y < ruta[i+1].y):
                a = canvas.create_line(ruta[i].x + num, ruta[i].y + ancho, ruta[i+1].x + ancho,
                                       ruta[i+1].y + num, width=3, fill="#02F5A0", arrow="last", smooth=True)
                li.append(a)
            if (ruta[i].x <= ruta[i+1].x and ruta[i].y > ruta[i+1].y):
                a = canvas.create_line(ruta[i].x + num, ruta[i].y, ruta[i+1].x, ruta[i+1].y + num, width=3,
                                       fill="#02F5A0", arrow="last", smooth=True)
                li.append(a)
            if (ruta[i].x < ruta[+1].x and ruta[i].y < ruta[i+1].y):
                a = canvas.create_line(ruta[i].x + num, ruta[i].y + ancho, ruta[i+1].x, ruta[i+1].y + num,
                                       width=3, fill="#02F5A0", arrow="last", smooth=True)
                li.append(a)
        else:
            if (ruta[i-1].x >= ruta[i].x and ruta[i-1].y > ruta[i].y):
                    a = canvas.create_line(ruta[i-1].x + num, ruta[i-1].y, ruta[i].x + ancho, ruta[i].y + num,
                                           width=3, fill="#02F5A0", arrow="last", smooth=True)
                    li.append(a)
            if (ruta[i-1].x > ruta[i].x and ruta[i-1].y < ruta[i].y):
                a = canvas.create_line(ruta[i-1].x + num, ruta[i-1].y + ancho, ruta[i].x + ancho,
                                       ruta[i].y + num, width=3, fill="#02F5A0", arrow="last", smooth=True)
                li.append(a)
            if (ruta[i-1].x <= ruta[i].x and ruta[i-1].y > ruta[i].y):
                a = canvas.create_line(ruta[i-1].x + num, ruta[i-1].y, ruta[i].x, ruta[i].y + num, width=3,
                                       fill="#02F5A0", arrow="last", smooth=True)
                li.append(a)
            if (ruta[i-1].x < ruta[i].x and ruta[i-1].y < ruta[i].y):
                a = canvas.create_line(ruta[i-1].x + num, ruta[i-1].y + ancho, ruta[i].x, ruta[i].y + num,
                                       width=3, fill="#02F5A0", arrow="last", smooth=True)
                li.append(a)


# Resaltar Caminos del Dijkstra
def resaltarcaminos(listap, li, inicio):
    for aris in li:
        canvas.delete(aris)
    del li[:]
    h1 = Thread(target=resaltar, args=(listap, li, inicio))
    h1.start()

def resaltar(listap, li, inicio):
    num = ancho / 2
    for i in range(len(g.listav)):
        if listap[i] != None and listap[i].nombre == inicio.nombre:
            time.sleep(0.5)
            if (listap[i].x >= g.listav[i].x and listap[i].y > g.listav[i].y):
                a = canvas.create_line(listap[i].x + num, listap[i].y, g.listav[i].x + ancho, g.listav[i].y + num,
                                       width=3, fill="#02F5A0", arrow="last", smooth=True)
                li.append(a)
            if (listap[i].x > g.listav[i].x and listap[i].y < g.listav[i].y):
                a = canvas.create_line(listap[i].x + num, listap[i].y + ancho, g.listav[i].x + ancho,
                                       g.listav[i].y + num, width=3, fill="#02F5A0", arrow="last", smooth=True)
                li.append(a)
            if (listap[i].x <= g.listav[i].x and listap[i].y > g.listav[i].y):
                a = canvas.create_line(listap[i].x + num, listap[i].y, g.listav[i].x, g.listav[i].y + num, width=3,
                                       fill="#02F5A0", arrow="last", smooth=True)
                li.append(a)
            if (listap[i].x < g.listav[i].x and listap[i].y < g.listav[i].y):
                a = canvas.create_line(listap[i].x + num, listap[i].y + ancho, g.listav[i].x, g.listav[i].y + num,
                                       width=3, fill="#02F5A0", arrow="last", smooth=True)
                li.append(a)
            resaltar(listap, li, g.listav[i])

# Camino
def clickcamino():
 
    vcamino = Toplevel()
    vcamino.title("Mostrar Ruta")
    desde = Listbox(vcamino, exportselection=0)
    hasta = Listbox(vcamino, exportselection=0)
    for v in g.listav:
        desde.insert(END, v.nombre)
        hasta.insert(END, v.nombre)
    desde.grid(row=1, column=0)
    hasta.grid(row=1, column=1)
    t1 = Label(vcamino, text="Desde")
    t1.grid(row=0, column=0)
    t2 = Label(vcamino, text="Hasta")
    t2.grid(row=0, column=1)
    caminob = Button(vcamino, text="Camino",
                     command=lambda: camino(desde.get(desde.curselection()), hasta.get(hasta.curselection()), vcamino))
    caminob.grid(row=1, column=2)

def camino(desde, hasta, vcamino):
    try:
        for v in g.listav:
            if desde == v.nombre:
                ld, lp = g.dijkstra(v)
        lc = []
        for i in range(len(g.listav)):
            if lp[i] != None:
                if hasta == g.listav[i].nombre:
                    lc.append(g.listav[i])
                    lc.append(lp[i])
                    lc = rec(lp[i], lc, lp)
                    print(g.dijkstra)
       # lp[i].x, lp[i].y, g.listav[i].x, g.listav[i].y
        vcamino.destroy()
        mostrarcamino(list(reversed(lc)), li)
        hmc = Thread(target=mostrarcamino, args=(list(reversed(lc)), li))
        hmc.start()
        hm = Thread(target=movimiento, args=(list(reversed(lc)), msj))
        hm.start()
    except:
        messagebox.showerror("ERROR","Camino no encontrado")

def rec(vdestino, lc, lp):
    for i in range(len(g.listav)):
        if vdestino == g.listav[i]:
            if lp[i] != None:
                lc.append(lp[i])
                rec(lp[i], lc, lp)
    return lc

def mostrarcamino(lc, li):
    num = ancho / 2
    for aris in li:
        canvas.delete(aris)
    del li[:]
    for i, j in zip(lc, lc[1:]):
        time.sleep(0.5)
        if i.x >= j.x and i.y > j.y:
            a = canvas.create_line(i.x + num, i.y, j.x + ancho, j.y + num, width=3, fill="#02F5A0", arrow="last",smooth=True)
            li.append(a)
        if (i.x > j.x and i.y < j.y):
            a = canvas.create_line(i.x + num, i.y + ancho, j.x + ancho, j.y + num, width=3, fill="#02F5A0",arrow="last", smooth=True)
            li.append(a)
        if (i.x <= j.x and i.y > j.y):
            a = canvas.create_line(i.x + num, i.y, j.x, j.y + num, width=3, fill="#02F5A0", arrow="last",smooth=True)
            li.append(a)
        if (i.x < j.x and i.y < j.y):
            a = canvas.create_line(i.x + num, i.y + ancho, j.x, j.y + num, width=3, fill="#02F5A0", arrow="last",smooth=True)
            li.append(a)

def movimiento(lc, msj):
    if(len(lc)!=0):
        num = ancho / 2
        canvas.delete("obj")
        canvas.create_image(lc[0].x + num, lc[0].y + num, image=msj, tag="obj")
        aumento = 2
        tiempo=0.05

        for i, j in zip(lc, lc[1:]):
            cords = canvas.coords("obj")
            h1 = Thread(args=(cords[0],cords[1],lc))
            h1.start()
            time.sleep(tiempo)
            if i.x >= j.x and i.y > j.y:
                m = (j.y - i.y) / (j.x - i.x)
                for x in range(i.x, j.x, -aumento):
                    pos = canvas.coords("obj")
                    if pos[0] > j.x+num:
                        canvas.move("obj", -aumento, -aumento * m)
                        canvas.update()
                        time.sleep(tiempo)
                    else:
                        break
            if i.x > j.x and i.y < j.y:
                m = (j.y - i.y) / (j.x - i.x)
                for x in range(i.x, j.x, -aumento):
                    pos = canvas.coords("obj")
                    if pos[0] > j.x+num:
                        canvas.move("obj", -aumento, -aumento * m)
                        canvas.update()
                        time.sleep(tiempo)
                    else:
                        break
            if i.x <= j.x and i.y > j.y:
                m = (j.y - i.y) / (j.x - i.x)
                for x in range(i.x, j.x, aumento):
                    pos = canvas.coords("obj")
                    if pos[0] < j.x+num:
                        canvas.move("obj", aumento, aumento * m)
                        canvas.update()
                        time.sleep(tiempo)
                    else:
                        break
            if i.x < j.x and i.y < j.y:
                m = (j.y - i.y) / (j.x - i.x)
                for x in range(i.x, j.x, aumento):
                    pos = canvas.coords("obj")
                    if pos[0] < j.x+num:
                        canvas.move("obj", aumento, aumento * m)
                        canvas.update()
                        time.sleep(tiempo)
                    else:
                        break
    else:
        messagebox.showerror("ERROR","No se puede calcular la ruta")




def listaprev(previo, listap, listica):
    for i in range(len(g.listav)):
        if g.listav[i] == previo:
            if listap[i] != None:
                listica.append(listap[i])
                listaprev(listap[i], listap, listica)
    return listica

def mostrarprofundidad():
    l = []
    l = g.profundidad(g.listav[0], l)
    for vert in l:
        print(vert.nombre)

menubar = Menu(Ventana)

menubar.add_command(label="Relacionar", command=clickrelacion)
menubar.add_separator()
menubar.add_command(label="Eliminar Punto", command=clickeliminarv)
menubar.add_separator()
menubar.add_command(label="Eliminar Camino", command=clickeliminara)
menubar.add_separator()
menubar.add_command(label="Mostrar Ruta", command=clickcamino)
menubar.add_separator()
menubar.add_command(label="Añadir Etiqueta", command=clickdijkstra)
menubar.add_separator()

Ventana.config(menu=menubar)
canvas.bind("<Double-1>", dobleclick)
canvas.bind("<Button-1>", click)

def actualizar():
    num = ancho / 2
    canvas.delete("all")
    q=0
    for i in range(len(g.listav)):
        if(g.listav[i].tipo=="LER"):
         canvas.create_oval(g.listav[i].x, g.listav[i].y, g.listav[i].x + ancho, g.listav[i].y + ancho, fill="#f25627", width=0)
         canvas.create_oval(g.listav[i].x+5, g.listav[i].y+5, g.listav[i].x + ancho-5, g.listav[i].y + ancho-5, fill="#f25627", activefill="#024959", width=0)
        else:
             canvas.create_oval(g.listav[i].x, g.listav[i].y, g.listav[i].x + ancho, g.listav[i].y + ancho, fill="#5cd695", width=0)
             canvas.create_oval(g.listav[i].x+5, g.listav[i].y+5, g.listav[i].x + ancho-5, g.listav[i].y + ancho-5, fill="#5cd695", activefill="#024959", width=0)
    for i in range(len(g.listaA)):
        if g.listaA[i].x1 >= g.listaA[i].x2 and g.listaA[i].y1 > g.listaA[i].y2:
            canvas.create_line(g.listaA[i].x1 + num, g.listaA[i].y1, g.listaA[i].x2 + ancho, g.listaA[i].y2 + num,
                               width=3, fill="white", arrow="last", smooth=True)
        if g.listaA[i].x1 > g.listaA[i].x2 and g.listaA[i].y1 < g.listaA[i].y2:
            canvas.create_line(g.listaA[i].x1 + num, g.listaA[i].y1 + ancho, g.listaA[i].x2 + ancho,
                               g.listaA[i].y2 + num, width=3, fill="white", arrow="last", smooth=True)
        if g.listaA[i].x1 <= g.listaA[i].x2 and g.listaA[i].y1 > g.listaA[i].y2:
            canvas.create_line(g.listaA[i].x1 + num, g.listaA[i].y1, g.listaA[i].x2, g.listaA[i].y2 + num, width=3,
                               fill="white", arrow="last", smooth=True)
        if g.listaA[i].x1 < g.listaA[i].x2 and g.listaA[i].y1 < g.listaA[i].y2:
            canvas.create_line(g.listaA[i].x1 + num, g.listaA[i].y1 + ancho, g.listaA[i].x2, g.listaA[i].y2 + num,
                               width=3, fill="white", arrow="last", smooth=True)

    for i in range(len(g.listaA)):

        if g.listaA[i].x1 >= g.listaA[i].x2 and g.listaA[i].y1 > g.listaA[i].y2:
            tx1 = ((g.listaA[i].x1 + num) + (g.listaA[i].x2 + ancho)) / 2
            ty1 = (g.listaA[i].y1 + (g.listaA[i].y2 - num)) / 2
            canvas.create_text(tx1, ty1 + num, text=str(g.listaA[i].distancia) )
        if g.listaA[i].x1 > g.listaA[i].x2 and g.listaA[i].y1 < g.listaA[i].y2:
            tx1 = ((g.listaA[i].x1 + num) + (g.listaA[i].x2 + ancho)) / 2
            ty1 = ((g.listaA[i].y1 - ancho) + (g.listaA[i].y2 + num)) / 2
            canvas.create_text(tx1, ty1 + ancho, text=str(g.listaA[i].distancia))
        if g.listaA[i].x1 <= g.listaA[i].x2 and g.listaA[i].y1 > g.listaA[i].y2:
            tx1 = ((g.listaA[i].x1 + num) + g.listaA[i].x2) / 2
            ty1 = (g.listaA[i].y1 + (g.listaA[i].y2 - num)) / 2
            canvas.create_text(tx1, ty1 + num, text=str(g.listaA[i].distancia))
        if g.listaA[i].x1 < g.listaA[i].x2 and g.listaA[i].y1 < g.listaA[i].y2:
            tx1 = (g.listaA[i].x1 + (num + g.listaA[i].x2)) / 2
            ty1 = ((g.listaA[i].y1 - ancho) + (g.listaA[i].y2 + num)) / 2
            canvas.create_text(tx1, ty1 + ancho, text=str(g.listaA[i].distancia) )

    for i in range(len(g.listav)):
        nombre = str(g.listav[i].nombre)
        if len(nombre) > 5:
            nombre = nombre[0:4] + ".."
        canvas.create_text(g.listav[i].x + num, g.listav[i].y + num, text=nombre, fill="white", font="bold")

Ventana.mainloop()
