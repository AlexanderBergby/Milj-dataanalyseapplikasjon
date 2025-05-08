import sys
import os
import tkinter as tk

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from Værdata_nå import værdata_nå
from Værdata_uke import værdata_uke
from Værdata_nå_visuell import værdata_nå_visuell
from Visualisering import visualisering
from prediktiv_analyse import prediktiv
from luftkvalitet import luftkvalitet
from interaktiv import interaktiv

def meny():
    print("Velkommen til værappen!")
    print("1 - Værdata nå for norges 5 største byer")
    print("2 - Værdata forrgje uke Trondheim")
    print("3 - Værdata nå VISUELL")
    print ("4 - Visualisering")
    print ("5 - Prediktiv") 
    print ("6 - Luftvkalitet ")
    print ("7 - Interaktiv")
    print("8 - Avslutt")

    while True:
        valg = input("Velg et alternativ: ")
        if valg == "1":
            værdata_nå()
            break
        if valg== "2":
            værdata_uke()
            break
        if valg == "3":
            værdata_nå_visuell()
            break
        if valg == "4":
            visualisering()
            break
        if valg == "5":
            prediktiv()
            break
        if valg == "6":
            luftkvalitet()
            break
        if valg == "7":
            interaktiv()
            break
        elif valg == "8":
            print("Ha en fin dag!")
            break
        else:
            print("Ugyldig valg. Prøv igjen.")

if __name__ == "__main__":
    meny()
