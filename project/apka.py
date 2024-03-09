import tkinter as tk
import subprocess
import sys
from random import randint
from PIL import Image, ImageTk



def loguj():
    print("Akcja logowania")
    try:
        if wersja_aplikacji == "Biometria + Twilio":
        	root.withdraw()
        	process = subprocess.run([sys.executable, 'main.py'], stdin=subprocess.PIPE, check=True)
        elif wersja_aplikacji == "Biometria + GoogleAuth":
        	root.withdraw()
        	process = subprocess.run([sys.executable, 'main2.py'], stdin=subprocess.PIPE, check=True)
     #   subprocess.run([sys.executable, 'main.py'], stdin=subprocess.PIPE, check=True)
        #process.communicate()  # Czekanie na zakończenie procesu drugiego skryptu
    except Exception as e:
        print(f"Wystąpił błąd: {e}")
    #finally:
        #print("klops")
        #process.terminate()  # Zabicie procesu pierwszego skryptu, niezależnie od wyniku drugiego skryptu



#Popen
    root.deiconify()
    
wersja_aplikacji = "Biometria + Twilio"


def opcje():
    global wersja_aplikacji
    option_window = tk.Tk()
    option_window.title("Opcje")
    option_window.geometry("400x400")

    option_list = ["Biometria + Twilio", "Biometria + GoogleAuth"]
    value_inside = tk.StringVar(option_window)
    value_inside.set("Rodzaj autoryzacji")
    question_menu = tk.OptionMenu(option_window, value_inside, *option_list)
    question_menu.pack()

    def print_answers():
        global wersja_aplikacji
        wersja_aplikacji = value_inside.get()
        label_wersja['text'] = wersja_aplikacji
        option_window.destroy()
        return None

    submit_button = tk.Button(option_window, text='Zatwierdź', command=print_answers)
    submit_button.pack()

    option_window.mainloop()
    

def wyjdz():
    root.destroy()

#print(wersja_aplikacji)

# Tworzenie głównego okna
root = tk.Tk()
root.title("STAH App")
root.geometry("500x500")

label_wersja = tk.Label(root, text="Wersja autoryzacji: " + wersja_aplikacji)
label_wersja.place(x=75, y=150)
    
# Dodawanie przycisków
button_loguj = tk.Button(root, text="Loguj", activebackground="#C1CDCD", command=loguj, width=40, height=5)
button_loguj.place(x=75, y=200)
#button_loguj.pack(pady=20)

button_opcje = tk.Button(root, text="Opcje", command=opcje, width=40, height=5)
button_opcje.place(x=75, y=300)

obraz = Image.open("StahApps4.jpg")
obraz_tk = ImageTk.PhotoImage(obraz)
label_obraz = tk.Label(root, image=obraz_tk)
label_obraz.place(x=37, y=20)

#button_opcje.pack(pady=20)

button_wyjdz = tk.Button(root, text="Wyjdź", command=wyjdz, width=40, height=5)
button_wyjdz.place(x=75, y=400)
#button_wyjdz.pack(pady=20)

# Uruchamianie głównej pętli programu
def update():
   root.after(1000, update) # run itself again after 1000 ms

# run first time

update()

root.mainloop()
