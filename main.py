import pygame as pg
import time

pg.init()

sirina=800
visina=400

velicina_prozora = (sirina, visina)
prozor = pg.display.set_mode(velicina_prozora)

pg.display.set_caption("Svemirski lovac")

kraj_igre = False

pozadina = pg.image.load("slike/pozadina.jpg").convert()

prozor.blit(pozadina, [0, 0])
lovac = pg.image.load("slike/spaceship.png")
buba = pg.image.load("slike/termite.png")
metak = pg.image.load("slike/bullet.png")
eksplozija = pg.image.load("slike/explosion.png")
lovac = pg.transform.scale(lovac,(60,60))
buba = pg.transform.scale(buba,(60,60))
buba = pg.transform.rotate(buba,180)
metak = pg.transform.scale(metak,(20,20))
eksplozija = pg.transform.scale(eksplozija,(60,60))
nivo = 1

razmak_izmedju_buba = 65
pomeraj_buba = 5
pocetni_broj_buba = 10
trenutno_buba = 10
lovac_x = 350
lovac_y = 320
bube_x = 50
bube_y = 50
niz_buba = []

metak_aktivan = False
metak_x = 0
metak_y = 0

eksplozija_aktivna = False
eksplozija_x = 0
eksplozija_y = 0
for i in range(pocetni_broj_buba):
    niz_buba.append(1)
def poredjaj_bube(a,b):
    x = a
    y = b
    for i in range(pocetni_broj_buba):
        if niz_buba[i] == 1:
            prozor.blit(buba,(x,y))
        x = x+razmak_izmedju_buba
def crtaj_scenu():
    prozor.blit(pozadina, [0, 0])
    prozor.blit(lovac, (lovac_x, lovac_y))
    if(metak_aktivan == True):
        prozor.blit(metak,(metak_x,metak_y))
    if(eksplozija_aktivna == True):
        prozor.blit(eksplozija,(eksplozija_x,eksplozija_y))
    poredjaj_bube(bube_x, bube_y)

def crtaj_kraj(poruka):
    prozor.fill(pg.Color("white"))
    font = pg.font.SysFont("Arial", 60)
    #poruka = "Kraj igre!"
    tekst = font.render(poruka, True, pg.Color("black"))
    (sirina_teksta, visina_teksta) = (tekst.get_width(), tekst.get_height())
    (x, y) = ((sirina - sirina_teksta) / 2, (visina - visina_teksta) / 2)
    prozor.blit(tekst, (x, y))
    pg.display.update()

def crtaj():
    if not kraj_igre:
        crtaj_scenu()
    else:
        crtaj_kraj()
def aktiviraj_eksploziju(x,y):
    global eksplozija_aktivna,eksplozija_x,eksplozija_y
    eksplozija_aktivna = True
    eksplozija_x = x
    eksplozija_y = y
def proveri_pogodak():
    global metak_aktivan
    global niz_buba
    v = bube_x
    for i in range(pocetni_broj_buba):
        if niz_buba[i]==1:
            c = metak_x - v -20
            if(c<0):
                c = c * (-1)
            if(c <= 10):
                if(metak_y <= bube_y):
                    niz_buba[i] = 0
                    metak_aktivan = False
                    aktiviraj_eksploziju(metak_x-20,metak_y-10)
        v = v + razmak_izmedju_buba
            #print("Bube x: %d",v)
    #print("Metak x: %d",metak_x)
sat = pg.time.Clock()
prozor.blit(pozadina, [0, 0])
prozor.blit(lovac, (lovac_x, lovac_y))
poredjaj_bube(50, 50)

def novi_nivo(broj_buba):
    global pocetni_broj_buba
    global niz_buba
    pocetni_broj_buba = broj_buba
    for i in range(pocetni_broj_buba):
        niz_buba.append(1)
    poredjaj_bube(50,100)

def novi_frejm():
    global kraj_igre
    global metak_aktivan
    global eksplozija_aktivna
    global nivo
    if(metak_y<0):
        metak_aktivan = False
    if (metak_aktivan == True):
        proveri_pogodak()
    if(brojac%5==0 and eksplozija_aktivna == True):
        eksplozija_aktivna = False
    if(bube_y+20 >= lovac_y):
        #bube su pojele lovca
        kraj_igre = True
        crtaj_kraj("Izgubili ste! Kraj igre!")
    c = 0
    for i in range(pocetni_broj_buba):
        if(niz_buba[i]==1):
            c = 1
            break
    if(c==0):
        #kraj_igre = True
        if nivo == 2:
            kraj_igre = True
            crtaj_kraj("Pobeda! Kraj igre!")
        else:
            nivo = 2


def obradi_dogadjaj(dogadjaj):
    global lovac_x
    global metak_aktivan, metak_x, metak_y

    keys = pg.key.get_pressed()
    if(keys[pg.K_RIGHT]):
        lovac_x = lovac_x + 10
    if(keys[pg.K_LEFT]):
        lovac_x = lovac_x - 10
    if dogadjaj.type == pg.KEYDOWN:
        if dogadjaj.key == pg.K_UP or dogadjaj.key == pg.K_SPACE:
            if(metak_aktivan == False):
                metak_aktivan = True
                metak_x = lovac_x+20
                metak_y = lovac_y

def promeni_bube(x):
    global bube_y
    bube_y = bube_y + x
def pomeri_metak():
    global metak_y
    metak_y = metak_y - 20
brojac = 0
print("Nivo: ",nivo)
while nivo == 1 and not kraj_igre:
    if(brojac%100 == 0):
        promeni_bube(pomeraj_buba) #pomeri poziciju gde ce biti bude u sledecem crtanju
    if(brojac%5==0 and metak_aktivan == True):
        pomeri_metak()
    crtaj()
    pg.display.update()
    for dogadjaj in pg.event.get():
        if dogadjaj.type == pg.QUIT:
            pg.quit()
        else:
            obradi_dogadjaj(dogadjaj)
    sat.tick(200)
    brojac = brojac + 1
    novi_frejm()

#nivo 2
if not kraj_igre:
    crtaj_kraj("Nivo 2")
    time.sleep(2)
    pozadina = pg.image.load("slike/pozadina2.jpg").convert()
    pocetni_broj_buba = 7
    razmak_izmedju_buba = 100
    niz_buba.clear()
    for i in range(pocetni_broj_buba):
        niz_buba.append(1)
    crtaj_scenu()
    bube_y = 50
    bube_x = 50
    poredjaj_bube(50, 100)
    print("Nivo: ",nivo)
    brojac = 0
while nivo == 2 and not kraj_igre:
    if(brojac%50 == 0):
        promeni_bube(pomeraj_buba) #pomeri poziciju gde ce biti bude u sledecem crtanju
    if(brojac%5==0 and metak_aktivan == True):
        pomeri_metak()
    crtaj()
    pg.display.update()
    for dogadjaj in pg.event.get():
        if dogadjaj.type == pg.QUIT:
            pg.quit()
        else:
            obradi_dogadjaj(dogadjaj)
    sat.tick(200)
    brojac = brojac + 1
    novi_frejm()

print("Kraj")
while kraj_igre:
    for dogadjaj in pg.event.get():
        if dogadjaj.type == pg.QUIT:
            pg.quit()