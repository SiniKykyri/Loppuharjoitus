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
nauru = pygame.mixer.Sound('nauru.wav')
hai = pygame.mixer.Sound('hai.wav')

# Funktio äänen soittamiselle
def play_sound(sound):
    sound.stop()
    sound.play()
# Funktio äänen pysäyttämiselle
def stop_sound(sound):
    sound.stop()  
# Alustetaan pääikkuna
root = Tk()
canvas = Canvas(root, width=900, height=900, bg='Blue')
canvas.pack()

# Määritellään sanakirja, johon tiedot saarista tallennetaan
saaret = {} 

# Määritellään sanakirja apinat, johon tallenetaan apinoiden tiedot
apinat = {}
apina_aanet = [apina1, apina2, apina3, apina4, apina5, apina6, apina7, apina8, apina9, apina10]

# Määritellään muuttuja, johon tallennetaan maalla kuoleet apinat
maalla_kuolleet_apinat = 0
#Määritellään muuttuja, johon tallennetaan meressä kuoleet apinat
meressa_kuolleet_apinat = 0

# Lippu thredien pysäyttämiseen
pysaytetty = False
# Lukko thredeille
lukko = threading.Lock() # APINOIDEN ELÄMÄÄ - NAURU LYHENTÄÄ IKÄÄ (10 PISTETTÄ)

# Funktio joka soittaa apinan ääntä. Tähän on lisätty myös riski, että apina kuolee nauruun.
def soita_apinan_aani(apinan_nimi, saaren_nimi):
    global maalla_kuolleet_apinat, meressa_kuolleet_apinat
    while not pysaytetty: # Jos ääntelyä ei ole pyydetty pysäyttämään, niin soitetaan ääntä
        if (apinat[apinan_nimi]["saarella"] == True and apinat[apinan_nimi]["kuollut"]==False): # Jos apina on saarella ja se on elossa sillä on mahdollisuus kuolla nauruun
            if random.random() < 0.01: # Arvotaan luku 0.0-1.0 ja jos se on pienempi kuin 0.01, niin apina kuolee
                print("Apina kuoli", apinan_nimi)
                with lukko:
                    play_sound(nauru) # Soitetaan nauruääni
                    maalla_kuolleet_apinat += 1 # Lisätään maalla kuolleiden apinoiden määrää
                    saaret[saaren_nimi]["apina_maara"] -= 1 # Vähennetään saaren apinoiden määrää
                    paivita_apinamaara(saaren_nimi) # Päivitetään apinoiden määrä Canvasissa
                    paivita_kuolleet_apinat() # Päivitetään teksti Canvasissa
                    canvas.delete(apinat[apinan_nimi]["kuva"]) # Poistetaan apinan kuva Canvasista
                    apinat[apinan_nimi]["kuollut"] = True # Merkitään apina kuolleeksi
                    return
            else:
                play_sound(apinat[apinan_nimi]["aani"]) # Soitetaan apinan ääntä, jos apina ei kuollut
                print("Soitetaan apinan ääntä", apinan_nimi , apinat[apinan_nimi]["aani"]) # Tulostetaan apinan nimi ja ääni. Ääni tulostuu pygamen takia nyt muisti paikkana, mutta sieltä kyllä näkee että kaikilla on oma ääni ja aina sama.
                play_sound(apinat[apinan_nimi]["aani"])
                time.sleep(2)
                stop_sound(apinat[apinan_nimi]["aani"])
                time.sleep(10) # Soitetaan ääni 10 sekunnin välein
        elif(apinat[apinan_nimi]["saarella"] == False and apinat[apinan_nimi]["kuollut"]== False): # Jos apina ei ole saarella, eli se on meressä ja jos apina ei ole kuollut
            if random.random() < 0.01:
                print("Apina tuli hain syömäksi", apinan_nimi)
                with lukko:
                    play_sound(hai) # Soitetaan haiääni
                    meressa_kuolleet_apinat += 1 # Lisätään meressä kuolleiden apinoiden määrää
                    paivita_kuolleet_apinat() # Päivitetään teksti Canvasissa
                    canvas.delete(apinat[apinan_nimi]["kuva"])
                    apinat[apinan_nimi]["kuollut"] = True # Merkitään apina kuolleeksi
            else:
                time.sleep(1) # Odotellaan sekuntti ennen kuin katsotaan tuleeko syödyksi

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
    apinat[apinan_nimi] = {"x": x, "y": y, "kuva": apinan_kuva, "saari": saaren_nimi, "aani": apinan_aani, "saarella": True, "kuollut":False} # Tallennetaan apinan tiedot
    saaret[saaren_nimi]["apina_maara"] += 1 # Lisätään saaren apinoiden määrää
    apinat[apinan_nimi]["thredi"] = threading.Thread(target=soita_apinan_aani, args=(apinan_nimi,saaren_nimi)) # Soitetaan apinan ääni
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
            nimi_teksi = canvas.create_text(x + 50, y + 50, text=saaren_nimi, fill='black', font=('Arial', 15, "bold")) # Lisätään saarelle nimi
            apina_maara_teksti = f"Apinoita saarella{0}" # Teksti apinoiden määrästä
            apinoiden_maara_elementti = canvas.create_text(x + 50, y - 50, text=apina_maara_teksti, fill='black', font=('Arial', 10, "bold"), tag="apina_maara") # Lisätään apinoiden määrä
            saaret[saaren_nimi] = {"x": x, "y": y, "kuva": kuva, "apina_maara": 0, "apinat": None, "nimi_teksti":nimi_teksi, "apina_maara_teksti":apinoiden_maara_elementti} # Tallennetaan saaren tiedot
            tulivuori.play() # Soitetaan tulivuoriääni
            for i in range(10):
                lisaa_apina(saaren_nimi)
                paivita_apinamaara(saaren_nimi)
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

# Funktio, joka sijoittaa apinan uimaan saaren viereen
def apina_uimaan():
    print("Apina uimaan painettu")
    saarella_olevat_apinat = [n for n in apinat if apinat[n]["saarella"] == True and apinat[n]["kuollut"]==False] # Haetaan kaikki saarella olevat apinat, jotka ovat elossa
    if not saarella_olevat_apinat: # Jos saarella ei ole enää apinoita
        print("Ei enää apinoita saarella")
        return
    apinan_nimi = random.choice(saarella_olevat_apinat) # Valitaan satunnainen apina
    apina_data = apinat[apinan_nimi] # Haetaan apinan tiedot
    apina_data["saarella"] = False # Muutetaan apinan sijainti meressä olevaksi
    saaret[apina_data["saari"]]["apina_maara"] -= 1 # Vähennetään saaren apinoiden määrää
    paivita_apinamaara(apina_data["saari"]) # Päivitetään apinoiden määrä Canvasissa
    saari_x = saaret[apina_data["saari"]]["x"] # Haetaan saaren jolla apina on x-koordinaatti
    saari_y = saaret[apina_data["saari"]]["y"] # Haetaan saaren jolla apina on y-koordinaatti
    saari_leveys = 100 # Saaren leveys
    saari_korkeus = 100 # Saaren korkeus
    meri_x = saari_x + saari_leveys + 10 # Kohta johon apina tulee uimaan
    meri_y =  saari_y + random.randint(0,saari_korkeus) # Kohta johon apina tulee uimaan
    canvas.coords(apina_data["kuva"], meri_x, meri_y, meri_x + 10, meri_y + 10) # Siirretään apina merelle

#Funktio, joka näyttää kuolleet apinat canvasissa
def paivita_kuolleet_apinat():
    canvas.delete("kuolleet_apinat") # Poistetaan vanhat kuolleet apinat teksti
    kuolleet_apinat = f"Kuolleet apinat: Maalla {maalla_kuolleet_apinat}, Meressä {meressa_kuolleet_apinat}" # Luodaan teksti kuolleista apinoista
    teksti = canvas.create_text(500, 850, text=kuolleet_apinat, fill='white', font=('Arial', 15), tag="kuolleet_apinat") # Näytetään teksti canvasissa
# Funktio, joka päivittää saaren reaaliaikaisen apinamäärän
def paivita_apinamaara(saaren_nimi):
    canvas.delete(saaret[saaren_nimi]["apina_maara_teksti"]) # Poistetaan saaren oma vanha teksti
    apina_maara_uusi_teksti = f"Apinoita saarella: {saaret[saaren_nimi]['apina_maara']}" # Luodaan uusi teksti apinoiden määrästä
    apinoiden_maara_elementti = canvas.create_text(saaret[saaren_nimi]["x"] + 50, saaret[saaren_nimi]["y"] - 30, text=apina_maara_uusi_teksti, fill='black', font=('Arial', 10, "bold"), tag="apina_maara") # Näytetään teksti canvasissa
    saaret[saaren_nimi]["apina_maara_teksti"] = apinoiden_maara_elementti # Päivitetään saaren tietoihin se uusi teksti

# Nappi, joka luo uuden saaren
tulivuorenpurkaus_nappi = Button(root, text='Tulivuorenpurkaus', command=luo_uusi_saari)
tulivuorenpurkaus_nappi.place(x=50, y=800)
# Nappi, jolla voi tyhjentää meren saarista ja apinoista
tyhjenna_nappi = Button(root, text='Tyhjennä', command=tyhjenna)
tyhjenna_nappi.place(x=200, y=800)
# Debug nappi, jolla voi tulostaa apinoiden tiedot
debug_nappi = Button(root, text='Tulosta apinat', command=lambda: print(apinat))
debug_nappi.place(x=300, y=800)
# Nappi jolla apinan saa uimaan oman saaren viereen
apina_uimaan_nappi = Button(root, text='Laita apina uimaan', command=apina_uimaan)
apina_uimaan_nappi.place(x=430, y=800)
#Debuggaus nappi
saarella_olevat_apinat_nappi = Button(root, text='Saarella olevat apinat', command=lambda: print([n for n in apinat if apinat[n]["saarella"] == True and apinat[n]["kuollut"]==False]))
saarella_olevat_apinat_nappi.place(x=600, y=800)

# Käynnistetään pääikkuna
root.mainloop()