import tkinter as tk
import sys
import os
from PIL import Image, ImageTk
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from rensing import rens_tempdata
from verdatavisuell_na import værdata_nå_visuell
from Verdata_uke import værdata_uke
from Visualisering import visualisering
from prediktiv_analyse import prediktiv
from luftkvalitet import luftkvalitet
from interaktiv import interaktiv
from verdata_10_aar import vis_temperaturgraf

#Renser data før meny visning.
fil_inn = "data/csv/Temp_data_Theim_14_25.csv"
fil_ut = "data/csv/renset_tempdata_Theim.csv"
#Sjekker om filen eksisterer
if not os.path.exists(fil_ut):
    rens_tempdata(fil_inn, fil_ut)
else:
    print(f"Filen '{fil_ut}' eksisterer allerede. Ingen rensing nødvendig.")

#For å komibinere en meny til verdata_uke og visualisering
def åpne_væranalysemeny():
    vindu = tk.Toplevel()
    vindu.title("Værdata for Trondheim - forrgje uke")
    vindu.geometry("400x300")
    vindu.resizable(False, False)

    tk.Label(vindu, text="Velg format:", font=("Helvetica", 14, "bold")).pack(pady=20)

    tk.Button(vindu, text="Værdata tekstbasert", width=40, height=2, command=værdata_uke).pack(pady=10)
    tk.Button(vindu, text="Figur med temperaturutvikling og statistikk", width=40, height=2, command=visualisering).pack(pady=10)

    tk.Button(vindu, text="Lukk", command=vindu.destroy).pack(pady=30)

#Start appen
def start_gui():
    root = tk.Tk()
    root.title("Værappen - Vær så god")
    root.geometry("600x600")
    root.resizable(False, False)

    #Bakgrunn
    image_path = "resources/bakgrunn3.jpg"
    bakgrunn = Image.open(image_path).resize((600, 600))
    bg_image = ImageTk.PhotoImage(bakgrunn)
    tk.Label(root, image=bg_image).place(x=0, y=0, relwidth=1, relheight=1)

    tk.Label(root, text="Velkommen til værappen!", font=("Helvetica", 20, "bold"), bg="white").pack(pady=20)

    menyvalg = [
        ("1 - Værmelding - Norske byer", lambda: værdata_nå_visuell(root)),
        ("2 - Værdata for Trondheim", åpne_væranalysemeny),
        ("3 - Prediktiv analyse", prediktiv),
        ("4 - Luftkvalitet", luftkvalitet),
        ("5 - Interaktiv visning", interaktiv), 
        ("6 - Temperatur siste 10 årene", vis_temperaturgraf)
    ]

    for tekst, funksjon in menyvalg:
        tk.Button(root, text=tekst, width=35, height=2, command=funksjon).pack(pady=5)

    #Avslutt-knapp
    exit_btn = tk.Label(
        root,
        text="Avslutt",
        bg="red",
        fg="white",
        width=20,
        height=2,
        font=("Helvetica", 12, "bold"),
        relief="raised",
        cursor="hand2"
    )
    exit_btn.pack(pady=30)
    exit_btn.bind("<Button-1>", lambda e: root.destroy())

    root.bg_image = bg_image  #Hindre garbage collection
    root.mainloop()

#For testing
if __name__ == "__main__":
    start_gui()
