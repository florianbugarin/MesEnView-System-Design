"""
@Author: Bhupesh BISHNOI, Florian BUGARIN, Corinne LORENZO
@Project: CNRS MesEnView Computational Imaging Pipeline
@Laboratory: Institute for Research in Geroscience and Rejuvenation (RESTORE) | CNRS UMR5070 | INSERM UMR1301 |
@Laboratory: Clément Ader Institute | Federal University Toulouse Midi-Pyrénées | UMR CNRS 5312 |
@Year: 2024-2025
@License: GNU Lesser General Public License v3.0 (LGPL-3.0)
"""

import tkinter
import time
from tkinter import filedialog
from tkinter import simpledialog
import os
import matplotlib.pyplot as plt
import numpy as np
from pandas import DataFrame
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
from PIL import Image
from tkinter import ttk
plt.style.use('seaborn-white')
def SaveIm():
    answer=filedialog.asksaveasfilename(parent=master,initialdir=os.getcwd(), title= 'Select folder and name', filetypes=types)
    fig1.savefig(answer+'.png',dpi=300)
def refresh(self,self1):
    self1.clear()
def EISnum(x,y,nmax):
    numa=float(NA.get())
    pit=float(pitch.get())
    M=float(Mag.get())
    N= 2* M*y*np.tan(np.arcsin(numa))/(pit)
    N=np.trunc(N)
    FM = np.zeros(int(max(N))-int(min(N)))
    EIS = np.zeros(int(max(N))-int(min(N)))
    n=0
    s=0
    for x in range(0, nmax-1):
        con=N[x+1]-N[x]
        if con!= 0:
            n=n+1
            EIS[s]=int(min(N))+n
            FM[s]=y[x]
            s=s+1
    return EIS, FM
def res(x, y):
    pixel=float(pix.get())
    lamb=float(wav.get())
    numa=float(NA.get())
    pit=float(pitch.get())
    M=float(Mag.get())
    return 2*pixel*y/x*M+ M*lamb*10**(-3)*y*10**(3)*np.tan(np.arcsin(numa))/(pit*10**(3)*numa)
def FOV(x, y):
    pixel=float(pix.get())
    lamb=float(wav.get())
    numa=float(NA.get())
    pit=float(pitch.get())
    M=float(Mag.get())
    return pit*y/x*M
def DOF(x, y):
    pixel=float(pix.get())
    lamb=float(wav.get())
    numa=float(NA.get())
    pit=float(pitch.get())
    M=float(Mag.get())
    return M**2*pixel**2*y*10**(3)*np.tan(np.arcsin(numa))/(pit*10**(3)*numa*x/y)+M**2*lamb*10**(-3)*(2*y*10**(3)*np.tan(np.arcsin(numa))/(pit*10**(3)*numa))**(2)
def plot():
    refresh(canvas1,fig1)
    comap=Combo.get()
    nmax=100
    wa=float(fmo.get())
    wb=float(fml.get())
    xlimit=float(xaxis.get())
    mlimit=float(maxis.get())
    colm=int(col.get())
    x = np.linspace(mlimit, xlimit, nmax)
    y = np.linspace(mlimit, xlimit, nmax)
    X, Y = np.meshgrid(x, y)
    Z1 = res(X, Y)
    Z2=FOV(X,Y)
    Z3=DOF(X,Y)
    EIS, FM =EISnum(x,y,nmax)
    plt = fig1.add_subplot(131)
    limits = [ mlimit, xlimit, mlimit, xlimit]
    plt.axis(limits)
    plt.set_ylabel("MO focal length (mm)")
    plt.set_xlabel("Lens array focal length (mm)")
    plt.set_title("Lateral resolution ("+chr(956)+"m)")
    plt.set_aspect('equal', 'box')
    cont1=plt.contourf( X, Y, Z1,  colm, cmap=comap);
    fig1.colorbar(cont1,shrink=0.70)
    re=res(wb,wa)
    re="{:.2f}".format(re)
    if i.get()==1:
        plt.plot([mlimit, xlimit], [wa, wa], color = 'white', linewidth=1, linestyle='dotted')
        plt.text(wb,wa, str(re), color = 'white',fontsize=9)
    if f.get()==1:
        plt.plot([wb, wb],[mlimit, xlimit],  color = 'white', linewidth=1, linestyle='dotted')
    for x in range(int(min(EIS)-1), int(max(EIS))):
        plt.plot([xlimit, mlimit],[FM[x-int(min(EIS))], FM[x-int(min(EIS))]], color = 'white', linewidth=1, linestyle='solid')
        plt.text(round((xlimit-mlimit)*2/3+mlimit), FM[x-int(min(EIS))]+0.6/max(EIS), 'N='+str(int(EIS[x-int(min(EIS))])), color = 'white')
    clist = cont1.collections[:]
    plt2 = fig1.add_subplot(132)
    plt2.axis(limits)
    plt2.set_ylabel("MO focal length (mm)")
    plt2.set_xlabel("Lens array focal length (mm)")
    plt2.set_title("FOV (mm)")
    plt2.set_aspect('equal', 'box')
    cont2=plt2.contourf( X,  Y, Z2,  colm, cmap=comap);
    fig1.colorbar(cont2,shrink=0.70)
    field=FOV(wb,wa)
    field="{:.2f}".format(field)
    if i.get()==1:
        plt2.plot([mlimit, xlimit], [wa, wa],color = 'white', linewidth=1, linestyle='dotted')
        plt2.text(wb,wa, str(field), color = 'white',fontsize=9)
    if f.get()==1:
        plt2.plot([wb, wb],[mlimit, xlimit], color = 'white', linewidth=1, linestyle='dotted')
    plt3 = fig1.add_subplot(133)
    plt3.axis(limits)
    plt3.set_ylabel("MO focal length (mm)")
    plt3.set_xlabel("Lens array focal lentgh (mm)")
    plt3.set_title("DOF ("+chr(956)+"m)")
    plt3.set_aspect('equal', 'box')
    cont3=plt3.contourf( X,  Y, Z3,  colm, cmap=comap);
    fig1.colorbar(cont3,shrink=0.70)
    do=DOF(wb,wa)
    do="{:.0f}".format(do)
    if i.get()==1:
        plt3.plot([mlimit, xlimit], [wa, wa],color = 'white', linewidth=1, linestyle='dotted')
        plt3.text(wb,wa, str(do), color = 'white',fontsize=9)
    if f.get()==1:
        plt3.plot([wb, wb],[mlimit, xlimit], color = 'white', linewidth=1, linestyle='dotted')
    canvas1.draw()
def show_values1():
    wa=float(fmo.get())/100
def show_values2():
    wb=float(fml.get())/100
def New_page():
    popup = tkinter.Tk()
    popup.title("Focal length calculator")
    popup.geometry("200x150+700+70")
    Param = tkinter.Label(popup,text ='MO parameters:',font=('Helvetica', 8, 'bold'))
    Param.place(x=50, y=20)
    varm =tkinter.DoubleVar(value=20)
    et_m = tkinter.Label(popup,text="Magnification:")
    et_m.place(x=5, y=50, width=150)
    m = tkinter.Spinbox(popup,from_=1, to=100, increment=1, textvariable=varm)
    m.place(x=125, y=50, width=40)
    vlist = ["Olympus", "Nikon", "Zeiss","Leica"]
    Param = tkinter.Label(popup,text ='MO company:')
    Param.place(x=20, y=80)
    Combo = ttk.Combobox(popup, values = vlist,width=8)
    Combo.set("Olympus")
    Combo.place(x=105, y = 80)
    def focal():
        brand=Combo.get()
        if brand=="Nikon":
            f=200
        if brand=="Olympus":
            f=180
        if brand=="Zeiss":
            f=165
        if brand=="Leica":
            f=200
        fmo=f/float(m.get())
        et_re = tkinter.Label(popup,text="fmo="+str(fmo)+" mm")
        et_re.config(font=("Arial", 10,'bold'))
        et_re.config(fg="#0000FF")
        et_re.config(bg="yellow")
        et_re.place(x=95, y=110, width=100)
    cal = tkinter.Button(popup, text='Calculate', command=focal, height=1, width=9)
    cal.place(x=10, y=110)
    popup.update()
    popup.deiconify()
    popup.mainloop()
def exitProgram():
    master.destroy()
master = tkinter.Tk()
master.title('FLFM parameters')
master.geometry("1500x500+0+0")
fig1 = Figure(figsize = (12, 4),
                 dpi = 100)
types=[('all types', '.*'), ('text files', '.txt')]
canvas1 = FigureCanvasTkAgg(fig1,master)  
canvas1.get_tk_widget().pack(side=tkinter.RIGHT)
Param = tkinter.Label(master,text ='Fourier Light-Field microscope parameters:',font=('Helvetica', 8, 'bold'))
Param.place(x=50, y=20)
var =tkinter.DoubleVar(value=0.2)
et_NA = tkinter.Label(text="MO numerical aperture:")
et_NA.place(x=50, y=50, width=150)
NA = tkinter.Spinbox(from_=0.05, to=0.95, increment=0.05, textvariable=var)
NA.place(x=205, y=50, width=50)
var =tkinter.DoubleVar(value=1)
et_pitch = tkinter.Label(text="MLA pitch (mm):")
et_pitch.place(x=50, y=80, width=150)
pitch = tkinter.Spinbox(from_=0.1, to=3, increment=0.1, textvariable=var)
pitch.place(x=205, y=80, width=50)
var =tkinter.DoubleVar(value=1.5)
et_pix = tkinter.Label(text="Pixel size ("+chr(956)+"m):")
et_pix.place(x=50, y=110, width=150)
pix = tkinter.Spinbox(from_=0.9, to=7, increment=0.1, textvariable=var)
pix.place(x=205, y=110, width=50)
var =tkinter.DoubleVar(value=550)
et_wav = tkinter.Label(text="Wavelenght (nm):")
et_wav.place(x=50, y=140, width=150)
wav = tkinter.Spinbox(from_=400, to=700, increment=1, textvariable=var)
wav.place(x=205, y=140, width=50)
var =tkinter.DoubleVar(value=1)
et_wav = tkinter.Label(text="Relay magnification:")
et_wav.place(x=50, y=170, width=150)
Mag = tkinter.Spinbox(from_=0.1, to=10, increment=0.1, textvariable=var)
Mag.place(x=205, y=170, width=50)
plot_button = tkinter.Button(master, 
                     command = plot,
                     height = 1, 
                     width = 12,
                     text = "Plot")
plot_button.place(x=500, y=10)
Sav = tkinter.Button(master, text='Save plots', command=SaveIm, height=1, width=12)
Sav.place(x=600, y=10)
FMO = tkinter.Button(master, text='Fmo calculator', command=New_page, height=1, width=12)
FMO.place(x=700, y=10)
Exit = tkinter.Button(master, text='Exit', command=exitProgram, height=1, width=12)
Exit.place(x=800, y=10)
Param = tkinter.Label(master,text ='Plot parameters:',font=('Helvetica', 8, 'bold'))
Param.place(x=50, y=220)
var =tkinter.DoubleVar(value=12)
et_xaxis = tkinter.Label(text="Axes upper limit (mm):")
et_xaxis.place(x=50, y=250, width=150)
xaxis = tkinter.Spinbox(from_=0.1, to=20, increment=0.1, textvariable=var)
xaxis.place(x=205, y=250, width=50)
var =tkinter.DoubleVar(value=2)
et_maxis = tkinter.Label(text="Axes lower limit (mm):")
et_maxis.place(x=50, y=280, width=150)
maxis = tkinter.Spinbox(from_=0.1, to=20, increment=0.1, textvariable=var)
maxis.place(x=205, y=280, width=50)
vlist = ["jet", "hot", "plasma","hsv","gray", "inferno","tab20c"]
Param = tkinter.Label(master,text ='Choose colormap:')
Param.place(x=62, y=310)
Combo = ttk.Combobox(master, values = vlist,width=6)
Combo.set("jet")
Combo.place(x=205, y = 310)
var =tkinter.DoubleVar(value=30)
et_col = tkinter.Label(text="Colormap divisions:")
et_col.place(x=45, y=340, width=150)
col = tkinter.Spinbox(from_=1, to=200, increment=1, textvariable=var)
col.place(x=205, y=340, width=50)
var =tkinter.DoubleVar(value=3.2)
et_fmo = tkinter.Label(text="MO focal length (mm):")
et_fmo.place(x=50, y=370, width=150)
fmo = tkinter.Spinbox(from_=1, to=30, increment=0.5, textvariable=var)
fmo.place(x=205, y=370, width=50)
i = tkinter.IntVar()
c = tkinter.Checkbutton(master,variable=i)
c.place(x=32,y=368)
var =tkinter.DoubleVar(value=6)
et_fml = tkinter.Label(text="MLA focal length (mm):")
et_fml.place(x=50, y=400, width=150)
fml = tkinter.Spinbox(from_=1, to=30, increment=0.5, textvariable=var)
fml.place(x=205, y=400, width=50)
f = tkinter.IntVar()
l = tkinter.Checkbutton(master,variable=f)
l.place(x=32,y=398)
def About():
   f = open("about.txt", "r")
   filewin = tkinter.Toplevel(master)
   button = tkinter.Label(filewin, text=f.read(),justify='left')
   button.pack()
menubar= tkinter.Menu(master)
helpmenu = tkinter.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About...", command=About)
master.config(menu=menubar)
master.update()
master.deiconify()
master.mainloop()