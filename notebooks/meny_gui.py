import tkinter as tk
import sys
import os
from PIL import Image, ImageTk
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from verdatavisuell_na import værdata_nå_visuell
from Verdata_uke import værdata_uke
from Visualisering import visualisering
from prediktiv_analyse import prediktiv
from luftkvalitet import luftkvalitet
from interaktiv import interaktiv

def start_gui():
    root = tk.Tk()
    root.title("Værapp - Hovedmeny")
    root.geometry("600x600")
    root.resizable(False, False)

    #Bakgrunn
    image_path = "docs/bakgrunn3.jpg"
    bakgrunn = Image.open(image_path).resize((600, 600))
    bg_image = ImageTk.PhotoImage(bakgrunn)
    tk.Label(root, image=bg_image).place(x=0, y=0, relwidth=1, relheight=1)

    tk.Label(root, text="Velkommen til værappen!", font=("Helvetica", 20, "bold"), bg="white").pack(pady=20)

    menyvalg = [
        ("1 - Værdata nå", lambda: værdata_nå_visuell(root)),
        ("2 - Værdata uke", værdata_uke),
        ("3 - Visualisering", visualisering),
        ("4 - Prediktiv analyse", prediktiv),
        ("5 - Luftkvalitet", luftkvalitet),
        ("6 - Interaktiv visning", interaktiv)
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
