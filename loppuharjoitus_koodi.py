import pygame
import random
import threading
import time
from tkinter import Tk, Canvas, Button 

# ----- ALUSTETAAN YLEISIÄ JUTTUJA -----
# Alustetaan pygame
pygame.mixer.init()
# Tuodaan ääni tiedostot
tulivuori = pygame.mixer.Sound('tulivuori.wav')
apina1 = pygame.mixer.Sound('400.wav')
apina2 = pygame.mixer.Sound('500.mp3')
apina3 = pygame.mixer.Sound('800.wav')
apina4 = pygame.mixer.Sound('900.mp3')
apina5 = pygame.mixer.Sound('1000.wav')
apina6 = pygame.mixer.Sound('1200.mp3')
apina7 = pygame.mixer.Sound('1400.mp3')
apina8 = pygame.mixer.Sound('1600.mp3')
apina9 = pygame.mixer.Sound('1800.mp3')
apina10 = pygame.mixer.Sound('1900.mp3')

# Funktio äänen soittamiselle
def play_sound(sound):
    sound.stop()
    sound.play()

def stop_sound(sound):
    sound.stop()  
# Alustetaan pääikkuna
root = Tk()
canvas = Canvas(root, width=900, height=900, bg='Blue')
canvas.pack()
# ---------------------------------------

# ---------------- APINASAARISTON ESIHISTORIA (5 PISTETTÄ) -----------------------
# Määritellään sanakirja, johon tiedot saarista tallennetaan
saaret = {} 
#Sanakirjassa on siis:
# - Saaren_nimi
# - Saaren_koordinaatit
# - Saaren_kuva
# - Saaren_apina_maara
# - Tieto saaren apinoiden ID:stä

# Määritellään sanakirja apinat, johon tallenetaan apinoiden tiedot
apinat = {}
apina_aanet = [apina1, apina2, apina3, apina4, apina5, apina6, apina7, apina8, apina9, apina10]

# Funktio joka soittaa apinan ääntä
def soita_apinan_aani(apina_nimi):
    while True:
        print("Soitetaan apinan ääntä", apina_nimi)
        play_sound(apinat[apina_nimi]["aani"])
        time.sleep(2)
        stop_sound(apinat[apina_nimi]["aani"])
        time.sleep(10) # Soitetaan ääni 10 sekunnin välein
          
# Funktio, joka tarkistaa saaren sijainnin
def tarkista_voiko_saaren_luoda(x, y):
    for saaren_nimi,saari_data in saaret.items(): # Käydään läpi kaikki saaret
        sx = saari_data["x"] # Haetaan saaren x-koordinaatti
        sy = saari_data["y"] # Haetaan saaren y-koordinaatti
        if abs(sx-x) < 150 and abs(sy-y) < 150: # Tarkistetaan, että onko uusi saari liian lähellä vanhaa saarta
            return False # Jos on, palautetaan False
    return True # Jos ei ole, palautetaan True

# Funktio, joka lisää apinan saarelle
def lisaa_apina(saaren_nimi):
    i = 0
    print("Tullaan lisäämään apina saarelle", saaren_nimi)
    apinan_nimi = 'A' + str(len(apinat) + 1) # Apinan nimi on A1, A2, A3, jne.
    # Arvotaan apinalle koordinaatit
    x = random.randint(saaret[saaren_nimi]["x"], saaret[saaren_nimi]["x"]+ 90) #Haetaan saaren koordinaatit ja arvotaan arvot niiden välistä
    y = random.randint(saaret[saaren_nimi]["y"], saaret[saaren_nimi]["y"]+ 90)
    apinan_kuva = canvas.create_oval(x, y, x + 10, y + 10, fill='brown') # Piirretään apina
    apinan_aani = apina_aanet[i] # Valitaan apinalle ääni
    i += 1 # Seuraava apina saa seuraavan äänen
    apinat[apinan_nimi] = {"x": x, "y": y, "kuva": apinan_kuva, "saari": saaren_nimi, "aani": apinan_aani} # Tallennetaan apinan tiedot
    apina_aani_thread = threading.Thread(target=soita_apinan_aani, args=(apinan_nimi,)) # Soitetaan apinan ääni
    apina_aani_thread.start() # Käynnistetään ääni
    

# Funktio, joka luo uuden saaren
def luo_uusi_saari():
    while True:
        print("Tulivuorenpurkaus nappia painettu")
        # Luodaan saarelle nimi
        saaren_nimi = 'S' + str(len(saaret) + 1) # Saaren nimi on S1, S2, S3, jne.
        # Arvotaan koordinaatit johon saari luodaan
        x = random.randint(100, 800) # Jätetään vähän reunoja, että saari ei mene ruudun ulkopuolelle
        y = random.randint(100, 700)
        if tarkista_voiko_saaren_luoda(x, y): # Jos saari voidaan luoda
            kuva = canvas.create_rectangle(x, y, x + 100, y + 100, fill='yellow')# Piirretään saari
            saaret[saaren_nimi] = {"x": x, "y": y, "kuva": kuva, "apina_maara": 0, "apinat": None} # Tallennetaan saaren tiedot
            #tulivuori.play() # Soitetaan tulivuoriääni
            for i in range(10):
                #apina_thread = threading.Thread(target=lisaa_apina, args=(saaren_nimi,)) # Lisätään apina saarelle
                #apina_thread.start()
                lisaa_apina(saaren_nimi)
            break
        else:
            print("Saari liian lähellä toista saarta, arvotaan uusi sijainti")

# Nappi, joka luo uuden saaren
tulivuorenpurkaus_nappi = Button(root, text='Tulivuorenpurkaus', command=luo_uusi_saari)
tulivuorenpurkaus_nappi.place(x=50, y=800)
# ---------------- APINASAARISTON ESIHISTORIA PÄÄTTYY (5 PISTETTÄ) ----------------


# Käynnistetään pääikkuna
root.mainloop()