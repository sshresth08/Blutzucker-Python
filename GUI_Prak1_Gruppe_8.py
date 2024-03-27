##########################################################
#Gruppe Nr.: 08
#Wolf Mika, Matrikel Nr:11161432
#Shrestha Sudin, Matrikel Nr:11147459
#Baier Dominik, Matrikel Nr: 11160516
# 
#
#Dokumentiert Blutzucker Werte von Patienten,
#damit der Hausartz verschiedene Werde einfach und effizient auswerten kann.
# 
#
#Bibliothek: tkinter, ttk, sqlite3, datetime
#Compiler Version: Python 3.12.0
#05.12.2023 Version 0.1
##########################################################

import tkinter
from tkinter import ttk
import sqlite3
from tkinter import *
from datetime import datetime

unterfenster_geöffnet = False #Variable um zu prüfen ob schon ein Unterfenster geöffnet wurde
einheit = "mmol/l" #Variable für die Blutzucker-Einheit
con = sqlite3.connect("blutzuckerDaten.db") #Verbindung zur lokalen Datenbank
cur = con.cursor() #Objekt für Datenbank

cur.execute('''
            CREATE TABLE IF NOT EXISTS blut_zucker_daten (
                name TEXT,
                vorname TEXT,
                geburtstag TEXT,
                datum TIMESTAMP,
                blut_zucker_wert_mg REAL,
                blut_zucker_wert_mmol REAL,
                mahlzeitenGroesse REAL,
                medikation TEXT,
                information TEXT
            )
        ''')
con.commit() #Datenbank erstellen

#Daten in Datenbank einfügen
def einfuegen_daten(name, vorname, geburtstag, datum, blutzuckermg, blutzuckermmol, mahlzeitenGroesse, medikation, information):
    cur.execute('''
            INSERT INTO blut_zucker_daten (name, vorname, geburtstag, datum, blut_zucker_wert_mg, blut_zucker_wert_mmol, mahlzeitenGroesse, medikation, information)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            name,
            vorname,
            geburtstag,
            datum,
            blutzuckermg,
            blutzuckermmol,
            mahlzeitenGroesse,
            medikation,
            information
        ))
    con.commit()        
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
root = tkinter.Tk() # Konstruktor fürs Fensterobjekt

root.geometry("1550x900") #Fenstergröße ▪ registrieren Widgets bei dem zugrundeliegenden Fenstermanager ▪ ordnen Widgets auf dem Bildschirm an ▪ Managen die Darstellung der Widgets auf dem Bildschirm
root.title("Blutzucker") #Titel für Fenster

def maßfestlegen(): #Funktion für Unterfenster der Blutzucker-Einheit
    global unterfenster_geöffnet
    global einheit

    if not unterfenster_geöffnet: #Mehrere Unterfenster vom Menu nicht erlaubt
        unterfenster_geöffnet = True
        unterfenster = Toplevel(root) #Unterfenster mit Vater root

        def on_close(): #Falls Fenster geschlossen wird, globale Variable ändern
            global unterfenster_geöffnet 
            unterfenster_geöffnet = False
            unterfenster.destroy()
        unterfenster.protocol("WM_DELETE_WINDOW", on_close) #on_close() ausführen, wenn Unterfenster geschlossen wird

        def updateDefaultSelection(): #Einheit ändern
            global einheit
            if (selection.get() == 1): einheit = "mmol/l" #selection = radiobutton
            else: einheit = "mg/dl"
            blutwertL.config(text = "Blutwert in [" + einheit + "]") #Text updaten bei Änderung der Blutwert-Einheit

        selection = IntVar() #Variable für Selektor
        selection.set(1) #Default Einheit = mmol/l


        #Radiobuttons für Unterfenster erstellen
        label = Label(unterfenster, text="Maßeinheit festlegen:") 
        label.pack() #Anstatt die genaue Position eines Widgets zu deklarieren, deklariert die pack()Methode die Position von Widgets im Verhältnis zueinander
        radio1 = Radiobutton(unterfenster, text="Millimol pro Liter (mmol/l)", variable=selection, value=1, command=updateDefaultSelection)
        radio1.pack()
        radio2 = Radiobutton(unterfenster, text="Milligramm pro Deziliter (mg/dl)", variable=selection, value=2, command=updateDefaultSelection)
        radio2.pack()
        #-----------------------------------------------------------------------------------------------------------------------------------------


menu = Menu(root) #Menu im Fenster
root.config(menu=menu) #Menu dem root Objekt hinzufügen

dateimenu = Menu(menu, tearoff=0) #Dateimenu ohne gestrichelte Linie
dateimenu.add_command(label="Beenden", command=quit) #Command Beenden -> schließt Fenster
menu.add_cascade(label="Datei", menu=dateimenu) #Fügt Datei Menu in der oberen Leiste hinzu

menu.add_command(label="Maßeinheit festlegen", command=maßfestlegen) #Maßeinheiten festlegen -> Ruft maßfestlegen() Funktion auf


#----Textfelder Patientendaten Frame---

frame = tkinter.Frame(root) #Objekt für die Gitteranordnung der Textfelder. Python Tkinter Frame Widget wird verwendet, um die Gruppe der Widgets zu organisieren
frame.columnconfigure(0, weight=1) #Gitteranordnung für Daten
frame.columnconfigure(1, weight=1) #Weight=1 -> Reihe wächst wenn genug Platz ist
frame.columnconfigure(2, weight=1)
frame.columnconfigure(3, weight=1)

#-- Textfelder Patientendaten----

nameL = tkinter.Label(frame, text="Name")
nameL.grid(row=0, column=0, sticky="WE")  #Label in das Grid reinmachen. Beim Layout-Manager grid kann man das Attribut sticky unter Angabe der Himmelsrichtungen verwenden, um die Inhalte anzupinnen
nameTB = tkinter.Text(frame, height=1)    #Textbox
nameTB.grid(row=1, column=0, sticky="WE")  # Textfeld in das Grid hinzufügen, sticky="WE" -> Feld "klebt" in der West-Ost Ecke

vornameL = tkinter.Label(frame, text="Vorname")
vornameL.grid(row=0, column=1, sticky="WE")
vornameTB = tkinter.Text(frame, height=1)
vornameTB.grid(row=1, column=1, sticky="WE")

geburtstagL = tkinter.Label(frame, text="Geburtstag")
geburtstagL.grid(row=2, column=0, sticky="WE")
geburtstagTB = tkinter.Text(frame, height=1)
geburtstagTB.grid(row=4, column=0, sticky="WE")

frame.pack()   #Frame sichbar machen

leerzeile2 = tkinter.Label(root, text="")    #Abstand zwischen den patientendaten frame und Listbox
leerzeile2.pack()


#----Textfelder Blutdaten Frame---
frame2 = tkinter.Frame(root)   #Objekt für die Gitteranordnung der Textfelder
frame2.columnconfigure(0, weight=1)   #Spaltenazahl definieren
frame2.columnconfigure(1, weight=1)
frame2.columnconfigure(2, weight=1)
frame2.columnconfigure(3, weight=1)

#-- Textfelder Blutdaten----

blutwertL = tkinter.Label(frame2, text="Blutwert in [" + einheit + "]")   #Text basierend auf eigestellter Eiheit (Nur für default Wert)
blutwertL.grid(row=0, column=0, sticky="WE")
blutwertTB = tkinter.Text(frame2, height=1)
blutwertTB.grid(row=1, column=0, sticky="WE") 

mahlzeitL = tkinter.Label(frame2, text="Mahlzeitgröße in [KE/BE]")
mahlzeitL.grid(row=0, column=1, sticky="WE")
mahlzeitTB = tkinter.Text(frame2, height=1)
mahlzeitTB.grid(row=1, column=1, sticky="WE") 

medikationL = tkinter.Label(frame2, text="Medikation")
medikationL.grid(row=2, column=0, sticky="WE")
medikationTB = tkinter.Text(frame2, height=1)
medikationTB.grid(row=3, column=0, sticky="WE")

infosL = tkinter.Label(frame2, text="Informationen zu Sport, Alkohol, Krankheiten...")
infosL.grid(row=2, column=1, sticky="WE")
infosTB = tkinter.Text(frame2, height=1)
infosTB.grid(row=3, column=1, sticky="WE")

frame2.pack()

#----------Einfügen knopf-------------------


#Werte in die Datenbank einfügen
def einfuegen():
    name = nameTB.get(1.0, "end-1c") #Daten aus Textfeldern lesen
    vorname = vornameTB.get(1.0, "end-1c") #(1.0, "end-1c") -> Von Anfang bis Ende des Strings
    geburtstag = geburtstagTB.get(1.0, "end-1c")
    datum = datetime.now() #Datum an dem die Werte hinzugefügt wurden
    blutwert = blutwertTB.get(1.0, "end-1c")
    mahlzeitenGroesse = mahlzeitTB.get(1.0, "end-1c")
    medikation = medikationTB.get(1.0, "end-1c")
    information = infosTB.get(1.0, "end-1c")

    if(name=="" or vorname=="" or geburtstag=="" or datum=="" or blutwert=="" or mahlzeitenGroesse==""): return #Testen ob Parameter leer gelassen wurden

    blutzuckermg = -1 #Werte initialisieren
    blutzuckermmol = -1

    #Umrechnen der Einheit, basierend auf des eingestellten Wertes
    if(einheit == "mmol/l"):
        blutzuckermmol = blutwert
        blutzuckermg = int(blutzuckermmol)*18.0182
        print("test")
    
    if(einheit == "mg/dl"):
        blutzuckermg = blutwert
        blutzuckermmol = int(blutzuckermg) * 0.0555
        print("test2")
    #----------------------------------------------------------------
    
    #Falls alles ausgefüllt worden ist, Daten in die Datenbank einfügen
    einfuegen_daten(name, vorname, geburtstag, datum, blutzuckermg, blutzuckermmol, mahlzeitenGroesse, medikation, information)


#Daten aus der Datenbank in dem Fenster anzeigen
def anzeigen():
    tree.delete(*tree.get_children()) #Vorherige Daten löschen

    #Daten mit dem Vor- und Nachnamen des Patienten ausgeben. (Nur falls das Datum nicht länger als 31 Tage her ist)
    name = nameTB.get(1.0, "end-1c")
    vorname = vornameTB.get(1.0, "end-1c")
    sql_query = "SELECT * FROM blut_zucker_daten WHERE name=? AND vorname=? AND (datum - ?) <= 31"

    #Für jeden Datensatz in dem Ergebnis, eine Spalte mit den jeweiligen Werten dem Tree hinzufügen
    for row in cur.execute(sql_query, (name, vorname, datetime.today())):
        blutzuckermg = row[4] #Spalte des Blutzucker-Werte in mg/dl

        #Hintergrundfarbe des Spalten dem Blutzuckerwert anpassen
        if(blutzuckermg < 70): colorTag = "red"
        else: 
            if ((blutzuckermg > 90) and blutzuckermg < 125): colorTag = "green"
            else: 
                if(blutzuckermg > 160): colorTag = "yellow"
        #--------------------------------------------------------

        tree.insert("", "end", values=row, tags=(colorTag)) #Tree Daten und Color-Tag hinzufügen


einfuegenButton = tkinter.Button(root, name="einfügen", command=einfuegen, text="Einfügen",width=50,bg="#FF5162") #Einfüge-Knopf
einfuegenButton.pack()

anzeigenButton = tkinter.Button(root, name="anzeigen", command=anzeigen, text="Auswerten",width=50,bg="#8FFF89") #Auswerten-Knopf
anzeigenButton.pack()

leerzeile = tkinter.Label(root, text="") #Abstand zwischen den Patientendaten frame und Listbox 
leerzeile.pack()

#Tree zum Anzeigen der Daten
tree = ttk.Treeview(root, columns=("Name", "Vorname", "Geburtstag", "Datum", "mg/dl", "mmol/l", "Mahlzeitengröße", "Medikation", "Information"), height=200) #Spalten definieren
tree.column("#0", width=0, stretch="no") #Leere Zeile "löschen"
tree.heading("Name", text="Name")   #Spaltennamen
tree.heading("Vorname", text="Vorname")
tree.heading("Geburtstag", text="Geburtstag")
tree.heading("Datum", text="Datum")
tree.heading("mg/dl", text="mg/dl")
tree.heading("mmol/l", text="mmol/l")
tree.heading("Mahlzeitengröße", text= "Mahlzeitengröße")
tree.heading("Medikation", text="Medikation")
tree.heading("Information", text="Information")
tree.pack()

#Hintergrundfarben mit Tags definieren
tree.tag_configure('red', background='red')
tree.tag_configure('yellow', background='yellow')
tree.tag_configure('green', background='green')

root.mainloop() #Programm läuft immer weiter (Fenster schließt sich nicht)