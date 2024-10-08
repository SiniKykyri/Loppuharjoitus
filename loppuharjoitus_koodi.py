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

# Lippu thredien pysäyttämiseen
pysaytetty = False

# Funktio joka soittaa apinan ääntä
def soita_apinan_aani(apinan_nimi):
    while not pysaytetty: # Jos ääntelyä ei ole pyydetty pysäyttämään, niin soitetaan ääntä
        print("Soitetaan apinan ääntä", apinan_nimi , apinat[apinan_nimi]["aani"]) # Tulostetaan apinan nimi ja ääni. Ääni tulostuu pygamen takia nyt muisti paikkana, mutta sieltä kyllä näkee että kaikilla on oma ääni ja aina sama.
        play_sound(apinat[apinan_nimi]["aani"])
        time.sleep(2)
        stop_sound(apinat[apinan_nimi]["aani"])
        time.sleep(10) # Soitetaan ääni 10 sekunnin välein
    print("Pysäytetään apinan ääni", apinan_nimi) # Jos ääntely on pyydetty pysäyttämään, niin tulostetaan apinan nimi ja pysäytetään ääni
          
# Funktio, joka tarkistaa saaren sijainnin
def tarkista_voiko_saaren_luoda(x, y):
    for saaren_nimi,saari_data in saaret.items(): # Käydään läpi kaikki saaret
        sx = saari_data["x"] # Haetaan saaren x-koordinaatti
        sy = saari_data["y"] # Haetaan saaren y-koordinaatti
        if abs(sx-x) < 150 and abs(sy-y) < 150: # Tarkistetaan, että onko uusi saari liian lähellä vanhaa saarta
            return False # Jos on, palautetaan False
    return True # Jos ei ole, palautetaan True

#Luodaan globaali muuttuja i
i_apina_aanet = 0
# Funktio, joka lisää apinan saarelle
def lisaa_apina(saaren_nimi):
    global i_apina_aanet
    print("Tullaan lisäämään apina saarelle", saaren_nimi)
    apinan_nimi = 'A' + str(len(apinat) + 1) # Apinan nimi on A1, A2, A3, jne.
    # Arvotaan apinalle koordinaatit
    x = random.randint(saaret[saaren_nimi]["x"], saaret[saaren_nimi]["x"]+ 90) #Haetaan saaren koordinaatit ja arvotaan arvot niiden välistä
    y = random.randint(saaret[saaren_nimi]["y"], saaret[saaren_nimi]["y"]+ 90)
    apinan_kuva = canvas.create_oval(x, y, x + 10, y + 10, fill='brown') # Piirretään apina
    apinan_aani = apina_aanet[i_apina_aanet] # Valitaan apinalle ääni
    i_apina_aanet += 1 # Seuraava apina saa seuraavan äänen
    apinat[apinan_nimi] = {"x": x, "y": y, "kuva": apinan_kuva, "saari": saaren_nimi, "aani": apinan_aani} # Tallennetaan apinan tiedot
    apinat[apinan_nimi]["thredi"] = threading.Thread(target=soita_apinan_aani, args=(apinan_nimi,)) # Soitetaan apinan ääni
    apinat[apinan_nimi]["thredi"].start() # Käynnistetään ääni
    

# Funktio, joka luo uuden saaren
def luo_uusi_saari():
    global i_apina_aanet
    i_apina_aanet = 0 #Nollataan apinoiden äänien lisäys indeksi, jotta voidaan aloittaa äänien jakaminen alusta.
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
            tulivuori.play() # Soitetaan tulivuoriääni
            for i in range(10):
                lisaa_apina(saaren_nimi)
            break
        else:
            print("Saari liian lähellä toista saarta, arvotaan uusi sijainti")

# Funktio, joka tyhjentää meren saarista ja apinoista
def tyhjenna():
    print("Tyhjennetään saaret ja apinat")
    global pysaytetty
    pysaytetty = True # Muutetaan lippu, jotta thredit pysäytetään

    for apinan_nimi, apina_data in apinat.items(): # Käydään läpi kaikki apinat
        apina_data["thredi"].join() # Odotetaan thredin loppumista
        canvas.delete(apina_data["kuva"]) # Poistetaan apinan kuva Canvasista
    # Poistetaan saaret
    for saaren_nimi, saari_data in saaret.items(): #Käydään läpi kaikki saaret
        canvas.delete(saari_data["kuva"]) # Poistetaan saaren kuva Canvasista

    apinat.clear() # Tyhjennetään apinat sanakirja
    saaret.clear() # Tyhjennetään saaret sanakirja
    pysaytetty = False # Muutetaan lippu takaisin, jotta saaret ja apinat voidaan luoda uudestaan
    print("Saaret ja apinat tyhjennetty")

# Nappi, joka luo uuden saaren
tulivuorenpurkaus_nappi = Button(root, text='Tulivuorenpurkaus', command=luo_uusi_saari)
tulivuorenpurkaus_nappi.place(x=50, y=800)
# Nappi, jolla voi tyhjentää meren saarista ja apinoista
tyhjenna_nappi = Button(root, text='Tyhjennä', command=tyhjenna)
tyhjenna_nappi.place(x=200, y=800)
# ---------------- APINASAARISTON ESIHISTORIA PÄÄTTYY (5 PISTETTÄ) ----------------


# Käynnistetään pääikkuna
root.mainloop()