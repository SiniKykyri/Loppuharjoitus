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
ui = pygame.mixer.Sound('beep.wav')

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
        if (apinat[apinan_nimi]["thredi_lopeta"] == True): # Jos tietyn apinan thredi on pyydetty lopettamaan, niin lopetetaan se
            print("Pysäytetään apinan ääni", apinan_nimi)
            return
        if (apinat[apinan_nimi]["saarella"] == True and apinat[apinan_nimi]["kuollut"]==False): # Jos apina on saarella ja se on elossa sillä on mahdollisuus kuolla nauruun
            if random.random() < 0.01: # Arvotaan luku 0.0-1.0 ja jos se on pienempi kuin 0.01, niin apina kuolee
                print("Apina kuoli", apinan_nimi)
                with lukko:
                    play_sound(nauru) # Soitetaan nauruääni
                    maalla_kuolleet_apinat += 1 # Lisätään maalla kuolleiden apinoiden määrää
                    saaret[saaren_nimi]["apina_maara"] -= 1 # Vähennetään saaren apinoiden määrää
                    paivita_kuolleet_apinat() # Päivitetään teksti Canvasissa
                    canvas.delete(apinat[apinan_nimi]["kuva"]) # Poistetaan apinan kuva Canvasista
                    apinat[apinan_nimi]["kuollut"] = True # Merkitään apina kuolleeksi
                paivita_apinamaara(saaren_nimi) # Päivitetään apinoiden määrä Canvasissa
                return
            else:
                play_sound(apinat[apinan_nimi]["aani"]) # Soitetaan apinan ääntä, jos apina ei kuollut
                print("Soitetaan apinan ääntä", apinan_nimi , apinat[apinan_nimi]["aani"]) # Tulostetaan apinan nimi ja ääni. Ääni tulostuu pygamen takia nyt muisti paikkana, mutta sieltä kyllä näkee että kaikilla on oma ääni ja aina sama.
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
    #print("Tullaan lisäämään apina saarelle", saaren_nimi)
    apinan_nimi = 'A' + str(len(apinat) + 1) # Apinan nimi on A1, A2, A3, jne.
    # Arvotaan apinalle koordinaatit
    x = random.randint(saaret[saaren_nimi]["x"], saaret[saaren_nimi]["x"]+ 90) #Haetaan saaren koordinaatit ja arvotaan arvot niiden välistä
    y = random.randint(saaret[saaren_nimi]["y"], saaret[saaren_nimi]["y"]+ 90)
    apinan_kuva = canvas.create_oval(x, y, x + 10, y + 10, fill='brown') # Piirretään apina
    apinan_aani = apina_aanet[i_apina_aanet] # Valitaan apinalle ääni
    i_apina_aanet += 1 # Seuraava apina saa seuraavan äänen
    apinat[apinan_nimi] = {"x": x, "y": y, "kuva": apinan_kuva, "saari": saaren_nimi, "aani": apinan_aani, "saarella": True, "kuollut":False, "thredi_lopeta": False} # Tallennetaan apinan tiedot
    saaret[saaren_nimi]["apina_maara"] += 1 # Lisätään saaren apinoiden määrää
    apinat[apinan_nimi]["thredi"] = threading.Thread(target=soita_apinan_aani, args=(apinan_nimi,saaren_nimi)) # Soitetaan apinan ääni
    apinat[apinan_nimi]["thredi"].start() # Käynnistetään ääni
    
# Funktio, joka luo uuden saaren
def luo_uusi_saari():
    global i_apina_aanet
    i_apina_aanet = 0 #Nollataan apinoiden äänien lisäys indeksi, jotta voidaan aloittaa äänien jakaminen alusta.
    while True:
        # Luodaan saarelle nimi
        saaren_nimi = 'S' + str(len(saaret) + 1) # Saaren nimi on S1, S2, S3, jne.
        # Arvotaan koordinaatit johon saari luodaan
        x = random.randint(100, 800) # Jätetään vähän reunoja, että saari ei mene ruudun ulkopuolelle
        y = random.randint(100, 700)
        if tarkista_voiko_saaren_luoda(x, y): # Jos saari voidaan luoda
            tulivuori.play() # Soitetaan tulivuoriääni
            kuva = canvas.create_rectangle(x, y, x + 100, y + 100, fill='yellow')# Piirretään saari
            nimi_teksi = canvas.create_text(x + 50, y + 50, text=saaren_nimi, fill='black', font=('Arial', 15, "bold")) # Lisätään saarelle nimi
            apina_maara_teksti = f"Apinoita saarella{0}" # Teksti apinoiden määrästä
            apinoiden_maara_elementti = canvas.create_text(x + 50, y - 50, text=apina_maara_teksti, fill='black', font=('Arial', 10, "bold")) # Lisätään apinoiden määrä näkymään saaren yläpuolella
            saaret[saaren_nimi] = {"x": x, "y": y, "kuva": kuva, "apina_maara": 0, "apinat": None, "nimi_teksti":nimi_teksi, "apina_maara_teksti":apinoiden_maara_elementti,"matkailutietoinen":False,"lahetetaan_apinoita":False, "apina_maaran_tarkistus_kaynnissa":False} # Tallennetaan saaren tiedot
           
            for i in range(10): # Lisätään saarelle 10 apinaa
                lisaa_apina(saaren_nimi)
                paivita_apinamaara(saaren_nimi) # Päivitetään apinoiden määrä Canvasissa
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
    # Poistetaan saaret, niiden nimet ja apinoiden määrät
    for saaren_nimi, saari_data in saaret.items(): #Käydään läpi kaikki saaret
        canvas.delete(saari_data["kuva"]) # Poistetaan saaren kuva Canvasista
        canvas.delete(saari_data["nimi_teksti"])
        canvas.delete(saari_data["apina_maara_teksti"])

    apinat.clear() # Tyhjennetään apinat sanakirja
    saaret.clear() # Tyhjennetään saaret sanakirja
    pysaytetty = False # Muutetaan lippu takaisin, jotta saaret ja apinat voidaan luoda uudestaan
    print("Saaret ja apinat tyhjennetty")

# Funktio, joka sijoittaa apinan uimaan saaren viereen
def apina_uimaan():
    #print("Apina uimaan painettu")
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
    print("Päivitetään apinoiden määrä saarelle", saaren_nimi)
    canvas.delete(saaret[saaren_nimi]["apina_maara_teksti"]) # Poistetaan saaren oma vanha teksti
    apina_maara_uusi_teksti = f"Apinoita saarella: {saaret[saaren_nimi]['apina_maara']}" # Luodaan uusi teksti apinoiden määrästä
    apinoiden_maara_elementti = canvas.create_text(saaret[saaren_nimi]["x"] + 50, saaret[saaren_nimi]["y"] - 30, text=apina_maara_uusi_teksti, fill='black', font=('Arial', 10, "bold")) # Näytetään teksti canvasissa
    saaret[saaren_nimi]["apina_maara_teksti"] = apinoiden_maara_elementti # Päivitetään saaren tietoihin se uusi teksti

def luo_laituri(saaren_nimi):
    print("Luodaan laituri saarelle", saaren_nimi)
    saari_x = saaret[saaren_nimi]["x"] # Haetaan saaren x-koordinaatti
    saari_y = saaret[saaren_nimi]["y"] # Haetaan saaren y-koordinaatti
    saari_leveys = 100 # Saaren leveys
    saari_korkeus = 100 # Saaren korkeus
    # Halutaan luoda laituri saaren etelä,-pohjois,-itä- ja länsipuolelle
    laituri_ita_x = saari_x + saari_leveys # Itäpuolen laituri
    laituri_ita_y = saari_y + 40  # itäpuolen laituri
    laituri_lansi_x = saari_x -20  # Länsipuolen laituri
    laituri_lansi_y = saari_y + 40 # Länsipuolen laituri
    laituri_pohjoinen_x = saari_x + 40 # Pohjoispuolen laituri
    laituri_pohjoinen_y = saari_y - 20 # Pohjoispuolen laituri
    laituri_etela_x = saari_x + 40 # Eteläpuolen laituri
    laituri_etela_y = saari_y + saari_korkeus # Eteläpuolen laituri
    # Piirretään laiturit
    ita_laituri_elementti = canvas.create_rectangle(laituri_ita_x, laituri_ita_y, laituri_ita_x + 20, laituri_ita_y + 20, fill='black')
    lansi_laituri_elementti = canvas.create_rectangle(laituri_lansi_x, laituri_lansi_y, laituri_lansi_x + 20, laituri_lansi_y + 20, fill='black')
    pohjoinen_laituri_elementti = canvas.create_rectangle(laituri_pohjoinen_x, laituri_pohjoinen_y, laituri_pohjoinen_x + 20, laituri_pohjoinen_y + 20, fill='black')
    etela_laituri_elementti = canvas.create_rectangle(laituri_etela_x, laituri_etela_y, laituri_etela_x + 20, laituri_etela_y + 20, fill='black')
    # Tallennetaan laiturit saaren tietoihin
    saaret[saaren_nimi]["ita_laituri"] = ita_laituri_elementti
    saaret[saaren_nimi]["lansi_laituri"] = lansi_laituri_elementti
    saaret[saaren_nimi]["pohjoinen_laituri"] = pohjoinen_laituri_elementti
    saaret[saaren_nimi]["etela_laituri"] = etela_laituri_elementti


# Funktio, joka tarkistaa apinamäärän ja kutsuu uudestaan arvo_apina_uimaan_ilmansuunta funktiota, mikäli apinoita on tarpeeksi
def tarkista_apinamaara(saaren_nimi):
    if saaret[saaren_nimi]["apina_maaran_tarkistus_kaynnissa"] == True: #Tämä tarkistus, jotta ei aloiteta aina uutta thrediä ja tarkistusta, mikäli tarkistus on jo käynnissä
        print("Tarkistus jo käynnissä, ei aloiteta uudestaan")
        return
    
    saaret[saaren_nimi]["apina_maaran_tarkistus_kaynnissa"] = True # Muutetaan lippu,että tarkistus on käynnissä
    while saaret[saaren_nimi]["apina_maaran_tarkistus_kaynnissa"] == True: 
        print("Tarkistellaan nyt omassa thredissä apinoiden määärää" , saaren_nimi)
        if saaret[saaren_nimi]["apina_maara"] > 0:
            print("Apinoita on jälleen saarella, kutstaan uudestaan arvo_apina_uimaan_ilmansuunta funktiota", saaren_nimi)
            threading.Thread(target=arvo_apina_uimaan_ilmansuunta, args=(saaren_nimi,)).start() # Käynnistetään apinoiden lähetys uudestaan
            saaret[saaren_nimi]["apina_maaran_tarkistus_kaynnissa"] = False # Muutetaan lippu, jotta tarkistus lopetetaan
            return
        else:
            print("Odotellaan edelleen apinoita saarelle", saaren_nimi)
        
        time.sleep(1) # Odotetaan sekunti ennen kuin tarkistetaan uudestaan


def arvo_apina_uimaan_ilmansuunta(saaren_nimi):
    print("Arvotaan apina uimaan!", saaren_nimi)
    arvottavat_apinat = [n for n in apinat if apinat[n]["saari"] == saaren_nimi and apinat[n]["saarella"]==True and apinat[n]["kuollut"]==False] # Haetaan kaikki kyseisellä saarella olevat apinat, joiden tila on saarella ja ne ovat elossa.
   
    if(saaret[saaren_nimi]["apina_maara"] > 0): # Jos saarella on vielä apinoita
        arvottu_apina = random.choice(arvottavat_apinat) # Arvotaan apina
        apinat[arvottu_apina]["saarella"] = False # Muutetaan apinan tila merelle
        saaret[saaren_nimi]["apina_maara"] -= 1 # Vähennetään saaren apinoiden määrää
        paivita_apinamaara(saaren_nimi) # Päivitetään apinoiden määrä Canvasissa
        
        suunta = random.choice(["ita", "lansi", "pohjoinen", "etela"]) # Arvotaan lähteekö apina uimaan itään, länteen, pohjoiseen vai etelään
        print("Arvottu suunta", suunta)
        # Siirretään apina oikean ilmansuunnan laiturille
        if suunta == "ita":
            uimaan_x = saaret[saaren_nimi]["x"] + 100
            uimaan_y = saaret[saaren_nimi]["y"] + 40
        elif suunta == "lansi":
            uimaan_x = saaret[saaren_nimi]["x"] - 20
            uimaan_y = saaret[saaren_nimi]["y"] + 40
        elif suunta == "pohjoinen":
            uimaan_x = saaret[saaren_nimi]["x"] + 40
            uimaan_y = saaret[saaren_nimi]["y"] - 20
        elif suunta == "etela":
            uimaan_x = saaret[saaren_nimi]["x"] + 40
            uimaan_y = saaret[saaren_nimi]["y"] + 100

        canvas.coords(apinat[arvottu_apina]["kuva"], uimaan_x, uimaan_y, uimaan_x + 10, uimaan_y + 10) # Siirretään apina uimaan
        apinat[arvottu_apina]["x"] = uimaan_x # Päivitetään apinan x-koordinaatti
        apinat[arvottu_apina]["y"] = uimaan_y # Päivitetään apinan y-koordinaatti
        canvas.tag_raise(apinat[arvottu_apina]["kuva"]) # Nostetaan kuvan prioretettia, jotta se näkyy päällimmäisenä

        apinat[arvottu_apina]["thredi_lopeta"] = True # Muutetaan apinan henkilökohtainen lippu, jotta thredi lopetetaan
        apinat[arvottu_apina]["thredi"] = threading.Thread(target=liikuta_apinaa_merella, args=(arvottu_apina, suunta)) # Luodaan uusi thredi, joka liikuttaa apinaa merellä
        apinat[arvottu_apina]["thredi"].start() # Käynnistetään thredi

        threading.Timer(10, arvo_apina_uimaan_ilmansuunta, args=(saaren_nimi,)).start() # Käynnistetään uusi thredi, joka arpoo apinan uimaan 10 sekunnin välein
    else:
        print("Ei enää apinoita saarella, lopetetaan lähetys ja käynnistetään tarkistus", saaren_nimi)
        paivita_apinamaara(saaren_nimi) # Päivitetään apinoiden määrä Canvasissa
        threading.Thread(target=tarkista_apinamaara,args=(saaren_nimi,)).start() # Käynnistetään funktio, joka tarkistaa apinoiden määrän
         
# Funktio, joka liikuttaa apinaa merellä
def liikuta_apinaa_merella(apinan_nimi, suunta):
    global meressa_kuolleet_apinat
    #print("Liikutetaan apinaa merellä")
    while True: 
        if apinat[apinan_nimi]["kuollut"] == False and apinat[apinan_nimi]["saarella"]== False : # Jos apina ei ole kuollut ja se on merellä
            if random.random() < 0.01:# sillä on mahdollisuus kuolla hain syömäksi
                #print("Apina tuli hain syömäksi", apinan_nimi)
                with lukko:
                    play_sound(hai) # Soitetaan haiääni
                    meressa_kuolleet_apinat += 1 # Lisätään meressä kuolleiden apinoiden määrää
                    paivita_kuolleet_apinat() # Päivitetään teksti Canvasissa
                    canvas.delete(apinat[apinan_nimi]["kuva"])
                    apinat[apinan_nimi]["kuollut"] = True # Merkitään apina kuolleeksi
                    return
            else:
                if suunta == "ita": # Liikutetaan apinaa merellä aina 5 pikseliä kerrallaan, sen mukaan miltä laiturilta apina lähtee.
                    apinat[apinan_nimi]["x"] += 5 
                elif suunta == "lansi":
                    apinat[apinan_nimi]["x"] -= 5
                elif suunta == "pohjoinen":
                    apinat[apinan_nimi]["y"] -= 5
                elif suunta == "etela":
                    apinat[apinan_nimi]["y"] += 5
                canvas.coords(apinat[apinan_nimi]["kuva"], apinat[apinan_nimi]["x"], apinat[apinan_nimi]["y"], apinat[apinan_nimi]["x"] + 10, apinat[apinan_nimi]["y"] + 10) # Siirretään apinaa
                play_sound(ui) # Soitetaan ui ääni
                for saari_nimi, saari_data in saaret.items(): # Käydään läpi kaikki saaret
                    saari_x = saari_data["x"] # Haetaan saaren x-koordinaatti
                    saari_y = saari_data["y"] # Haetaan saaren y-koordinaatti
                    saari_koko = 100 # Saaren koko
                    if(saari_x <= apinat[apinan_nimi]["x"] <= saari_x + saari_koko and saari_y <= apinat[apinan_nimi]["y"] <= saari_y + saari_koko):
                         print("Apina ui saarelle", saari_nimi)
                         with lukko:
                            apinat[apinan_nimi]["saarella"] = True # Muutetaan apinan sijainti saarelle
                            apinat[apinan_nimi]["saari"] = saari_nimi # Muutetaan apinan saari
                            saaret[saari_nimi]["apina_maara"] += 1 # Lisätään saaren apinoiden määrää
                            saaret[saari_nimi]["matkailutietoinen"] = True # Muutetaan saari matkailutietoiseksi
                            paivita_apinamaara(saari_nimi) # Päivitetään apinoiden määrä Canvasissa
                            
                            if(saaret[saari_nimi]["lahetetaan_apinoita"]==False): #Jos saari ei vielä ole lähettänyt apinoita, niin lähetetään.
                                arvo_apina_uimaan_ilmansuunta(saari_nimi) # Käynnistetään apinoiden lähetys myös tälle saarelle
                                luo_laituri(saari_nimi) # Luodaan laituri saarelle
                                saaret[saari_nimi]["lahetetaan_apinoita"] = True # Muutetaan lippu, jotta apinoita ei lähetetä useasti
                            return # Lopetaan apinan liikuttaminen
                time.sleep(0.1) # Odotetaan sekunti ennen kuin liikutetaan uudestaan

# Funktio, joka muuttaa S1 saaren matkailutietoiseksi
def muuta_s1_matkailutietoiseksi():
    print("Muutetaan S1 saari matkailutietoiseksi")
    saaret["S1"]["matkailutietoinen"] = True # Muutetaan S1 saari matkailutietoiseksi
    luo_laituri("S1") # Luodaan laituri S1 saarelle

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
#Nappi, jolla muutta S1 saaren matkailutietoiseksi
muuta_s1_saari_matkailutietoiseksi_nappi = Button(root, text="S1 matkailutietoiseksi", command=muuta_s1_matkailutietoiseksi)
muuta_s1_saari_matkailutietoiseksi_nappi.place(x=50, y=850)
# Nappi, jolla S1 saarelta arvotaan apina uimaan
arvo_apina_uimaan_nappi = Button(root, text="Arvo 10 apina uimaan(S1)", command= lambda: threading.Thread(target=arvo_apina_uimaan_ilmansuunta, args=("S1",)).start())
arvo_apina_uimaan_nappi.place(x=200, y=850)

# Käynnistetään pääikkuna
root.mainloop()