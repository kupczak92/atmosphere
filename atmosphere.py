from cProfile import label
import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np


from setuptools import Command

#tworzenie okienka
window = tk.Tk()

window.title("Predominance Area Diagram")
window.geometry('347x335+347+335')

temperatura_podaj = tk.Label(text="Temperature ["+u'\u00B0'+"C]:")
temperatura_podaj.pack()

entry = tk.Entry()
entry.pack()

#określenie stałych globalnych
stala_PbS = 0
stala_PbO = 0
stala_ZnO = 0
stala_ZnS = 0
stala_FeO = 0
stala_Fe3O4 = 0
stala_Fe2O3 = 0
stala_FeS = 0
stala_Cu2O = 0
stala_MnO = 0
stala_MnS = 0
#stala_CuO = 0
stala_Cu2S = 0
PbO_Pb = 0
ZnO_Zn = 0
FeO_Fe = 0
FeO_Fe3O4 = 0
Fe3O4_Fe2O3 = 0
Cu2O_Cu = 0
MnO_Mn = 0
#CuO_Cu20 = 0
PbS_Pb = 0
ZnS_Zn = 0
FeS_Fe = 0
Cu2S_Cu = 0
MnS_Mn = 0
lista_logO = [-12,-11,-10,-9,-8,-7,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5]
lista_logPb = []
lista_logZn =[]
lista_logFe = []
lista_logCu = []
lista_logMn = []
lista_logSPb = []
lista_logSZn = []
lista_logSFe = []
lista_logSCu2 = []
lista_logSMn = []
stala_PbO_PbS = 0
stala_ZnO_ZnS = 0
stala_FeO_FeS = 0
stala_Cu2O_Cu2S = 0
stala_MnO_MnS = 0

#okienka zaznaczenia
Pb = tk.IntVar() # zmienna przechowująca dane typu int, która zostanie przypisana do kontrolki
checkbutton = tk.Checkbutton(window, text="Pb", variable=Pb, \
                         onvalue=1, offvalue=0).place(x=0, y=115)
Zn = tk.IntVar() 
checkbutton = tk.Checkbutton(window, text="Zn", variable=Zn, \
                         onvalue=1, offvalue=0).place(x=50, y=115)
Cu = tk.IntVar() 
checkbutton = tk.Checkbutton(window, text="Cu", variable=Cu, \
                         onvalue=1, offvalue=0).place(x=100, y=115)
Mn = tk.IntVar() 
checkbutton = tk.Checkbutton(window, text="Mn", variable=Mn, \
                         onvalue=1, offvalue=0).place(x=250, y=115)

# CuO Rozpada się w temperaturacvh 800-100 C - nie ma sensu uwzględniać w obliczeniach
# #CuO = tk.IntVar() 
#checkbutton = tk.Checkbutton(window, text="Cu" + u'\u2082' + "O/CuO", variable=CuO, \
 #                        onvalue=1, offvalue=0).place(x=160, y=135)
Fe = tk.IntVar() 
checkbutton = tk.Checkbutton(window, text="Fe/FeO(FeS)", variable=Fe, \
                         onvalue=1, offvalue=0).place(x=150, y=115)
Fe3O4 = tk.IntVar() 
checkbutton = tk.Checkbutton(window, text="Fe" + u'\u2083' + "O" + u'\u2084' + '/FeO', variable=Fe3O4, \
                         onvalue=1, offvalue=0).place(x=150, y=135)
Fe2O3 = tk.IntVar() 
checkbutton = tk.Checkbutton(window, text='Fe' + u'\u2083' + "O" + u'\u2084' + "Fe" + u'\u2082' + 'O' + u'\u2083', variable=Fe2O3, \
                         onvalue=1, offvalue=0).place(x=150, y=155)

#obliczanie lotności po kliknięciu w calculate
def obliczenia(event):
    temperatura = int(entry.get())
    temp = (float(((temperatura+273)-1000)/100)+1) #konwersja temperatury z K na C (dodatkowo funkcja opisująca zależność temperatury od stałej K była przygotowana dla zakresu 1000-2000 K dlatego takie obliczenia)
    #obliczanie stałych K (jako logK) na podstawie wykresów zrobionych w excelu
    global stala_PbS
    stala_PbS = float(0.00007  * (temp ** 4) - 0.0041 * (temp ** 3) + 0.0892 * (temp ** 2) -1.0184 * temp + 4.8541)
    global stala_PbO
    #stala_PbO = float(-0.00004 * (temp ** 5) +0.0015 * (temp **4) -0.0248 * (temp ** 3) +0.2309 * (temp ** 2) -1.5774 *temp +7.6008)
    stala_PbO = float(-0.0034 * (temp ** 3) + 0.0995 * (temp ** 2) -1.2438 * temp + 7.3472)
    round(stala_PbO, 2)
    global stala_ZnO
    stala_ZnO = float(-0.0006* (temp ** 4) +0.013 * (temp ** 3) -0.0309 * (temp ** 2) -1.6452 * temp + 14.622)
    global stala_ZnS
    stala_ZnS = float(-0.0007 * (temp **4) +0.016 * (temp ** 3) - 0.0823 * (temp ** 2) -1.061 * temp + 9.8726)
    global stala_FeO
    stala_FeO = float(-0.0032 * (temp ** 3) + 0.1064 * (temp ** 2) -1.5484 * temp + 12.245)
    global stala_Fe3O4
    stala_Fe3O4 = float(-0.0123 * (temp ** 3) + 0.4145 * (temp ** 2) -6.1716 * temp + 47.069)
    global stala_Fe2O3
    stala_Fe2O3 = float(-0.0137 * (temp ** 3) + 0.3712 * (temp ** 2) -4.8172 * temp + 33.735)
    global stala_FeS
    stala_FeS = float(-0.0026 * (temp ** 3) + 0.0775 * (temp ** 2) -0.9698 * temp + 6.0041)
    global stala_Cu2O
    stala_Cu2O = float(-0.0016 * (temp ** 3) + 0.0642 * (temp ** 2) -0.9699 * temp + 5.8996)
    #global stala_CuO
    #stala_CuO = float(0.0041 * (temp ** 3) - 0.1277 * (temp ** 2) + 1.7558 * temp - 12.571)
    global stala_Cu2S
    stala_Cu2S = float(0.0214 * (temp ** 2) - 0.5995 * temp + 5.6538)
    global stala_MnO
    stala_MnO = float(-0.0045 * (temp ** 3) + 0.1453 * (temp ** 2) -2.1723 * temp + 18.289)
    global stala_MnS
    stala_MnS = float(-0.0028 * (temp ** 3) + 0.098 * (temp ** 2) -1.5415 * temp + 12.529)
    #od tej pory obliczana jest lotność O2 dla równowagi pomiędzy fazami metalicznymi a tlenkami
    global PbO_Pb
    PbO_Pb = -2* stala_PbO
    PbO_Pb = round(PbO_Pb, 2)
    global ZnO_Zn
    ZnO_Zn = -2* stala_ZnO
    ZnO_Zn = round(ZnO_Zn, 2)
    global MnO_Mn
    MnO_Mn = -2 * stala_MnO
    MnO_Mn = round(MnO_Mn,2)
    #żelazo
    global FeO_Fe
    FeO_Fe = -2* stala_FeO
    FeO_Fe = round(FeO_Fe, 2)
    global FeO_Fe3O4
    FeO_Fe3O4 = -6 * ((1/3 * stala_Fe3O4) -  stala_FeO)
    FeO_Fe3O4 = round(FeO_Fe3O4, 2)
    global Fe3O4_Fe2O3
    Fe3O4_Fe2O3 = - 12 * ((1/2 * stala_Fe2O3) - (1/3 * stala_Fe3O4))
    Fe3O4_Fe2O3 = round(Fe3O4_Fe2O3, 2)
    #miedź
    global Cu2O_Cu
    Cu2O_Cu = stala_Cu2O/2 * -4
    Cu2O_Cu = round(Cu2O_Cu,2)
    #global CuO_Cu20
    #CuO_Cu20 = -4 * (stala_CuO - (1/2 * stala_Cu2O))
    #CuO_Cu20 = round(CuO_Cu20, 2)
    #obliczanie lotności S2 pomiędzy fazami siarczkowymi a metalicznymi
    global PbS_Pb
    PbS_Pb = -2* stala_PbS
    PbS_Pb = round(PbS_Pb, 2)
    global ZnS_Zn
    ZnS_Zn = -2* stala_ZnS
    ZnS_Zn = round(ZnS_Zn, 2)
    global MnS_Mn
    MnS_Mn = -2 * stala_MnS
    MnS_Mn = round(MnS_Mn,2)
    global FeS_Fe
    FeS_Fe = -2* stala_FeS
    FeS_Fe = round(FeS_Fe, 2)
    global Cu2S_Cu
    Cu2S_Cu = stala_Cu2S/2 * -4
    Cu2S_Cu = round(Cu2S_Cu, 2)
    stala_PbO_PbS = float(stala_PbS - stala_PbO)
    global stala_ZnO_ZnS
    stala_ZnO_ZnS = float(stala_ZnS - stala_ZnO)
    global stala_FeO_FeS
    stala_FeO_FeS = float(stala_FeS - stala_FeO)
    global stala_Cu2O_Cu2S
    stala_Cu2O_Cu2S = float(stala_Cu2S - stala_Cu2O)
    global stala_MnO_MnS
    stala_MnO_MnS = float(stala_MnS - stala_MnO)
    # określanie lotności pomiędzy fazami siarczkowymi a tlenkowymi
    global lista_logPb
    lista_logPb = [PbS_Pb, PbS_Pb + 1, PbS_Pb + 2, PbS_Pb + 3, PbS_Pb + 4]

    global lista_logSPb
    lista_logSPb = [x + (2*stala_PbO_PbS) for x in lista_logPb]

    global lista_logZn
    lista_logZn = [ZnS_Zn, ZnS_Zn + 1, ZnS_Zn + 2, ZnS_Zn + 3, ZnS_Zn + 4]
    global lista_logSZn
    lista_logSZn = [x + (2*stala_ZnO_ZnS) for x in lista_logZn]

    global lista_logMn
    lista_logMn = [MnS_Mn, MnS_Mn + 1, MnS_Mn + 2, MnS_Mn + 3, MnS_Mn + 4]

    global lista_logSMn
    lista_logSMn = [x + (2 * stala_MnO_MnS) for x in lista_logMn]

    global lista_logFe
    lista_logFe = [FeS_Fe, FeS_Fe + 1, FeS_Fe + 2, FeS_Fe + 3, FeS_Fe + 4]
    global lista_logSFe
    lista_logSFe = [x + (2*stala_FeO_FeS) for x in lista_logFe]
    global lista_logCu
    lista_logCu = [Cu2S_Cu, Cu2S_Cu + 1, Cu2S_Cu + 2, Cu2S_Cu + 3, Cu2S_Cu + 4]
    global lista_logSCu2
    lista_logSCu2 = [x + (2*stala_Cu2O_Cu2S) for x in lista_logCu]
    
    #wprowadzenie wartości w okienku aplikacji
    label_Pb2 = tk.Label(text= PbO_Pb).place(x=115, y=180)
    label_Pb4 = tk.Label(text = PbS_Pb).place(x=315, y=180)

    label_Zn2 = tk.Label(text = ZnO_Zn).place(x=115, y=200)
    label_Zn4 = tk.Label(text = ZnS_Zn).place(x=315, y=200)

    label_Mn2 = tk.Label(text = MnO_Mn).place(x=120, y=300)
    label_Mn4 = tk.Label(text = MnS_Mn).place(x=315, y=260)

    label_Fe2 = tk.Label(text = FeO_Fe).place(x=115, y=220)
    label_Fe4 = tk.Label(text = FeS_Fe).place(x=315, y=220)
    label_Fe6 = tk.Label(text = FeO_Fe3O4).place(x=130, y=260)
    label_Fe8 = tk.Label(text = Fe3O4_Fe2O3).place(x=130, y=280)

    label_Cu2 = tk.Label(text = Cu2O_Cu).place(x=115, y=240)
    #label_Cu6 = tk.Label(text = CuO_Cu20).place(x=130, y=300)
    label_Cu4 = tk.Label(text = Cu2S_Cu).place(x=315, y=240)

#funkcja tworząca wykres po kliknięciu w przycisk "plot"

def plotting(event):
    if Pb.get() == 1:
        plt.hlines(y = PbO_Pb, xmin = PbS_Pb -5, xmax = PbS_Pb, color = 'r', linestyle = '-', label='PbO/Pb')
    if Zn.get() == 1:
        plt.hlines(y = ZnO_Zn, xmin = ZnS_Zn -5, xmax = ZnS_Zn, color = 'g', linestyle = '-', label='ZnO/Zn')
    if Fe.get() == 1:
        plt.hlines(y = FeO_Fe, xmin = FeS_Fe -5, xmax = FeS_Fe, color = 'y', linestyle = '-', label="FeO/Fe")
    if Fe3O4.get() == 1:
        plt.hlines(y = FeO_Fe3O4, xmin = FeS_Fe -5, xmax = FeS_Fe + 5, color = '#EEFF00', linestyle = '-', label='FeO/Fe' + u'\u2083' + 'O' + u'\u2084' + '')
    if Fe2O3.get() == 1:
        plt.hlines(y = Fe3O4_Fe2O3, xmin = FeS_Fe -5, xmax = FeS_Fe + 5, color = '#C8FF00', linestyle = '-', label='Fe' + u'\u2083' + 'O' + u'\u2084' + '/Fe' + u'\u2082' + 'O' + u'\u2083' + '')
    if Cu.get() == 1:
        plt.hlines(y = Cu2O_Cu, xmin = Cu2S_Cu -5, xmax = Cu2S_Cu, color = 'b', linestyle = '-', label="Cu" + u'\u2082' + "O/Cu")
    if Mn.get() == 1:
        plt.hlines(y = MnO_Mn, xmin = MnS_Mn -5, xmax = MnS_Mn, color = '#68217A', linestyle = '-', label='MnO/Mn')
    #if CuO.get() == 1:
        #plt.hlines(y = CuO_Cu20, xmin = Cu2S_Cu -5, xmax = Cu2S_Cu, color = 'b', linestyle = '-', label="Cu" + u'\u2082' + "O/CuO")
    # specifying vertical line type
    if Pb.get() == 1:
        plt.vlines(x = PbS_Pb, ymin =  PbO_Pb - 8, ymax = PbO_Pb, color = 'r', linestyle = '--', label = 'PbS/Pb')
    if Zn.get() == 1:
        plt.vlines(x = ZnS_Zn, ymin = ZnO_Zn - 8, ymax = ZnO_Zn, color = 'g', linestyle = '--', label = 'ZnS/Zn')
    if Fe.get() == 1:
        plt.vlines(x = FeS_Fe, ymin= FeO_Fe - 8, ymax = FeO_Fe, color = 'y', linestyle = '--', label = 'FeS/Fe')
    if Cu.get() == 1:
        plt.vlines(x = Cu2S_Cu, ymin = Cu2O_Cu - 8, ymax = Cu2O_Cu, color = 'b', linestyle = '--', label = 'Cu' + u'\u2082' + 'S/Cu')
    if Mn.get() == 1:
        plt.vlines(x = MnS_Mn, ymin = MnO_Mn - 8, ymax = MnO_Mn, color = '#68217A', linestyle = '--', label = 'MnS/Mn')
    #linia MeO/MeS
    if Pb.get() == 1:
        plt.plot(lista_logPb, lista_logSPb, color = 'r', linestyle = ':', label = 'PbO/PbS')
    if Zn.get() == 1:
        plt.plot(lista_logZn, lista_logSZn, color = 'g', linestyle = ':', label = 'ZnO/ZnS')
    if Fe.get() == 1:
        plt.plot(lista_logFe, lista_logSFe, color = 'y', linestyle = ':', label = 'FeO/FeS')
    if Cu.get() == 1:
        plt.plot(lista_logCu, lista_logSCu2, color = 'b', linestyle = ':', label = 'Cu' + u'\u2082' + 'O/Cu' + u'\u2082' + 'S')
    
    if Mn.get() == 1:
        plt.plot(lista_logMn, lista_logSMn, color = '#68217A', linestyle = ':', label = 'MnO/MnS')

    plt.legend(loc=4)  

    plt.xlabel('logP S' + u'\u2082')
    plt.ylabel('logP O' + u'\u2082')
    
    # rendering the plot
    plt.show()

button = tk.Button(text="Calculate")
button.bind("<Button-1>", obliczenia)

button.pack()

button2 = tk.Button(text="Plot PAD")
button2.bind("<Button-1>", plotting)


button2.pack()

#tekst który będzie cały czas widoczny w okienku aplikacji
label_oblicz = tk.Label(text = "mark phases before plotting").place(x=0, y=95)

label_Pb1 = tk.Label(text = 'logP O' + u'\u2082' + ' for Pb/PbO:').place(x=0, y=180)
label_Pb3 = tk.Label(text = 'logP S' + u'\u2082' + ' for Pb/PbS:').place(x=200, y=180)

label_Zn1 = tk.Label(text = 'logP O' + u'\u2082' + ' for Zn/ZnO:').place(x=0, y=200)
label_Zn3 = tk.Label(text = 'logP S' + u'\u2082' + ' for Zn/ZnS:').place(x=200, y=200)

label_Mn1 = tk.Label(text = 'logP O' + u'\u2082' + ' for Mn/MnO:').place(x=0, y=300)
label_Mn3 = tk.Label(text = 'logP S' + u'\u2082' + ' for Mn/MnS:').place(x=200, y=260)

label_Fe1 = tk.Label(text = 'logP O' + u'\u2082' + ' for Fe/FeO:').place(x=0, y=220)
label_Fe5 = tk.Label(text = 'logP O' + u'\u2082' + ' for FeO/Fe' + u'\u2083' + 'O' + u'\u2084' + ':').place(x=0, y=260)
label_Fe7 = tk.Label(text = 'logP O' + u'\u2082' + ' for Fe' + u'\u2083' + 'O' + u'\u2084' + '/Fe' + u'\u2082' + 'O' + u'\u2083' + ':').place(x=0, y=280)
label_Fe3 = tk.Label(text = 'logP S' + u'\u2082' + ' for Fe/FeS:').place(x=200, y=220)

label_Cu1 = tk.Label(text = 'logP O' + u'\u2082' + ' for Cu/CuO:').place(x=0, y=240)
#label_Cu5 = tk.Label(text = 'logP O' + u'\u2082' + ' for Cu:' + u'\u2082' + 'O/CuO:').place(x=0, y=300)
label_Cu3 = tk.Label(text = 'logP S' + u'\u2082' + ' for Cu/CuS:').place(x=200, y=240)

                         
name = entry.get()
name
entry.delete(0)

window.mainloop() 