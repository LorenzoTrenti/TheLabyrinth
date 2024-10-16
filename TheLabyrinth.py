import pygame as pg
import random

pg.init()

ROWS = 25
COLS = 40
DIM_MURI = 20

FPS = 30

DISTANZA_DA_TITOLO = 160
DISTANZA_DA_LATO = 55
SPAZIO_FRA_I_MURI = 2
WIDTH = COLS*DIM_MURI+100
HEIGHT = DISTANZA_DA_TITOLO+(ROWS*DIM_MURI)+100

MURO = '#'
SENTIERO = ' '
VUOTO = '/'
START = 'S'
FINISH = 'F'
VISUALIZZATO = 'V'
AMPIEZZA_VISIVA = 2
PERCENTUALE_PER_MURI = 45

SCREEN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Labirinth")
Clock = pg.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
AZZURRO = (0, 255, 255)

FONT1 = pg.font.SysFont('Comic Sans MS', 80, bold=True)
FONT2 = pg.font.SysFont('Comic Sans MS', 50, bold=True)
FONT3 = pg.font.SysFont('Comic Sans MS', 40, bold=True)
FONT4 = pg.font.SysFont('Comic Sans MS', 30, bold=True)

def controllo(tabella, rows, cols):
    for i in range(1, rows-1, 1):
        for j in range(1, cols-1, 1):
            if tabella[i-1][j-1]==SENTIERO and tabella[i][j-1]==SENTIERO and tabella[i-1][j]==SENTIERO:
                tabella[i][j]=MURO
            elif tabella[i-1][j+1]==SENTIERO and tabella[i-1][j]==SENTIERO and tabella[i][j+1]==SENTIERO:
                tabella[i][j]=MURO
            elif tabella[i][j+1]==SENTIERO and tabella[i+1][j+1]==SENTIERO and tabella[i+1][j]==SENTIERO:
                tabella[i][j]=MURO
            elif tabella[i+1][j]==SENTIERO and tabella[i+1][j-1]==SENTIERO and tabella[i][j-1]==SENTIERO:
                tabella[i][j]=MURO

def scelta_direzione(prec, x, y, tabella, alternative):
    val_disponibili = []
    lista = [True, True, True, True]

    for i in range(4):
        if i+1==prec:
            val_disponibili.append(False)
        else:
            val_disponibili.append(True)
    valido=True
    direzione=-1
    while valido:
        flag = False
        all_numbers = True 
        while all_numbers:
            all_numbers=False
            val = random.randint(1, 4)
            lista[val-1]=False
            for i in range(4):
                if lista[i]==True:
                    all_numbers=True
            if val_disponibili[val-1]==True:
                flag = True
                break
        if flag:
            if val==1:
                if tabella[x-1][y]!=VUOTO:
                    val_disponibili[0]=False
                    if alternative==True and tabella[x-1][y]==SENTIERO:
                        return val
                else:
                    direzione=val
                    break
            elif val==2:
                if tabella[x][y+1]!=VUOTO:
                    val_disponibili[1]=False
                    if alternative==True and tabella[x][y+1]==SENTIERO:
                        return val
                else:
                    direzione=val
                    break
            elif val==3:
                if tabella[x+1][y]!=VUOTO:
                    val_disponibili[2]=False
                    if alternative==True and tabella[x+1][y]==SENTIERO:
                        return val
                else:
                    direzione=val
                    break
            elif val==4:
                if tabella[x][y-1]!=VUOTO:
                    val_disponibili[3]=False
                    if alternative==True and tabella[x][y-1]==SENTIERO:
                        return val
                else:
                    direzione=val
                    break
        else:
            break
    return direzione

def scava(tabella, i, j, rows, cols):
    labirinto=tabella
    trovata_uscita=False
    prec = 0
    bloccato = False
    x=i
    y=j
    while not trovata_uscita and not bloccato:
        direzione = scelta_direzione(prec, x, y, labirinto, True)
        if direzione!=-1:
            if direzione==1:
                x-=1
            elif direzione==2:
                y+=1
            elif direzione==3:
                x+=1
            elif direzione==4:
                y-=1
            
            if labirinto[x][y]==SENTIERO:
                trovata_uscita=True
            else:
                labirinto[x][y]=SENTIERO
            controllo(labirinto, rows, cols)
            if direzione==1 or direzione==2:
                prec=direzione+2
            else:
                prec=direzione-2
        else:
            bloccato=True

    if bloccato:
        labirinto=scava(tabella, i, j, rows, cols)

    return labirinto
            
def labirinto3(labirinto, rows, cols):
    for i in range(1, rows-1, 1):
        for j in range(1, cols-1, 1):
            flag=True
            for k in range(-1, 2, 1):
                for h in range(-1, 2, 1):
                    if i!=k or j!=h:
                        if labirinto[i+k][j+h]!=VUOTO and labirinto[i+k][j+h]!=MURO:
                            flag=False
            if flag:
                labirinto=scava(labirinto, i, j, rows, cols)
                
    return labirinto

def crea_labirinto(rows, cols):
    global partenza, arrivo

    tabella = []

    SCREEN.fill(BLACK)
    loading = FONT2.render("Loading...", True, WHITE)
    rectLoading = loading.get_rect()
    rectLoading.center = (WIDTH/2, HEIGHT/2)
    SCREEN.blit(loading, rectLoading)
    aggiorna()
    partenza = random.randint(1, rows-2)
    arrivo = random.randint(1, rows-2)
    for i in range(rows):
        riga = []
        for j in range(cols):
            if i==partenza and j==0:
                riga.append(START)
            elif i==arrivo and j==cols-1:
                riga.append(FINISH)
            elif(i==0 or j==0 or i==rows-1 or j==cols-1):
                riga.append(MURO)
            else:
                riga.append(VUOTO)
        tabella.append(riga)
    prec = 4
    x = partenza
    y = 0
    uscita=False
    bloccato=False
    while(uscita==False and bloccato==False):
        if tabella[arrivo][cols-2]!=SENTIERO:
            direzione = scelta_direzione(prec, x, y, tabella, False)
            if direzione!=-1:
                if direzione==1:
                    x-=1
                elif direzione==2:
                    y+=1
                elif direzione==3:
                    x+=1
                elif direzione==4:
                    y-=1
                tabella[x][y]=SENTIERO
                controllo(tabella, rows, cols)
                if direzione==1 or direzione==2:
                    prec=direzione+2
                else:
                    prec=direzione-2
            else:
                bloccato=True	
        else:
            uscita=True
    if bloccato==True:
        tabella=crea_labirinto(rows, cols)
    else:
        # Creazioni muri restanti
        for i in range(1, rows-1, 1):
            for j in range(1, cols-1, 1):
                if tabella[i][j]==VUOTO:
                    num=random.randint(1, 100)
                    if num<=PERCENTUALE_PER_MURI:
                        tabella[i][j]=MURO    # Percentuale mura
                    else:
                        tabella[i][j]=SENTIERO

    return tabella

def aggiorna():
    pg.display.flip()
    Clock.tick(FPS)

def inizializza():
    global labirinto, tabella_visiva
    global x, y
    global arrivo
    global omino, wall

    labirinto = crea_labirinto(ROWS, COLS)
    tabella_visiva = []
    for i in range(ROWS):
        n=[]
        for j in range(COLS):
            n.append(VUOTO)
        tabella_visiva.append(n)
    # Inizializzazione MURI e OMINO
    wall = pg.Rect(0, 0, DIM_MURI - SPAZIO_FRA_I_MURI, DIM_MURI - SPAZIO_FRA_I_MURI)
    omino = pg.Rect(0, 0, DIM_MURI - SPAZIO_FRA_I_MURI, DIM_MURI - SPAZIO_FRA_I_MURI)
    x = partenza
    y = 0

def menu_iniziale():
    SCREEN.fill(BLACK)
    titolo = FONT1.render("THE LABYRINTH", True, WHITE)
    rectTitle = titolo.get_rect()
    rectTitle.center=(WIDTH/2, HEIGHT/8)
    SCREEN.blit(titolo, rectTitle)
    modalita = FONT3.render("Press the difficulty:", True, WHITE)
    rectModalita = modalita.get_rect()
    rectModalita.center = (WIDTH/2, HEIGHT/3)
    SCREEN.blit(modalita, rectModalita)
    easy = FONT3.render("1) Easy", True, WHITE)
    rectEasy = easy.get_rect()
    rectEasy.center = (WIDTH/2, rectModalita.center[1]+70)
    SCREEN.blit(easy, rectEasy)
    medium = FONT3.render("2) Medium", True, WHITE)
    rectMedium = medium.get_rect()
    rectMedium.center = (WIDTH/2, rectEasy.center[1]+50)
    SCREEN.blit(medium, rectMedium)
    hard = FONT3.render("3) Hard", True, WHITE)
    rectHard = hard.get_rect()
    rectHard.center = (WIDTH/2, rectMedium.center[1]+50)
    SCREEN.blit(hard, rectHard)
    veryHard = FONT3.render("4) Very hard", True, WHITE)
    rectVeryHard = veryHard.get_rect()
    rectVeryHard.center = (WIDTH/2, rectHard.center[1]+50)
    SCREEN.blit(veryHard, rectVeryHard)

flag=0
inizializza()

while True:
    menu_iniziale()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_1:
                flag=1
            if event.key == pg.K_2:
                flag=2
            if event.key == pg.K_3:
                flag=3
            if event.key == pg.K_4:
                flag=4
    aggiorna()
    while flag!=0:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            # Scelta direzione WASD o frecce
            if event.type == pg.KEYDOWN:
                if (event.key==pg.K_UP or event.key==pg.K_w) and x-1>=0 and labirinto[x-1][y]==SENTIERO:
                    x-=1
                if (event.key==pg.K_DOWN or event.key==pg.K_s) and x+1<ROWS and labirinto[x+1][y]==SENTIERO:
                    x+=1
                if (event.key==pg.K_RIGHT or event.key==pg.K_d) and y+1<COLS and (labirinto[x][y+1]==SENTIERO or labirinto[x][y+1]==FINISH):
                    y+=1
                if (event.key==pg.K_LEFT or event.key==pg.K_a) and y-1>=0 and (labirinto[x][y-1]==SENTIERO):
                    y-=1
                if event.key==pg.K_0:
                    inizializza()
                    flag=0
                if event.type == pg.QUIT:
                    exit()
        SCREEN.fill(BLACK)
        # Titolo
        titolo = FONT1.render("THE LABYRINTH", True, WHITE)
        rectTitle = titolo.get_rect()
        rectTitle.center=(WIDTH/2, HEIGHT/8)
        SCREEN.blit(titolo, rectTitle)
        back = FONT4.render("0) Back to menu", True, WHITE)
        rectBack = back.get_rect()
        rectBack.center = (WIDTH-DISTANZA_DA_LATO-rectBack[2]/2, DISTANZA_DA_TITOLO+(ROWS*DIM_MURI)+10)
        SCREEN.blit(back, rectBack)
        instructions = FONT4.render("To move use ARROWS or WASD", True, WHITE)
        rectInstructions = instructions.get_rect()
        rectInstructions.center = (DISTANZA_DA_LATO+rectInstructions[2]/2, DISTANZA_DA_TITOLO+(ROWS*DIM_MURI)+10)
        SCREEN.blit(instructions, rectInstructions)

        # Stampa labirinto
        if flag==1:
            for i in range(ROWS):
                for j in range(COLS):
                    if i==x and j==y:
                        omino.center = (DISTANZA_DA_LATO+(j*DIM_MURI), DISTANZA_DA_TITOLO+(i*DIM_MURI))
                        pg.draw.rect(SCREEN, GREEN, omino)
                    else:
                        if labirinto[i][j]==MURO:
                            wall.center = (DISTANZA_DA_LATO+(j*DIM_MURI), DISTANZA_DA_TITOLO+(i*DIM_MURI))
                            pg.draw.rect(SCREEN, WHITE, wall)
                        elif labirinto[i][j]==START:
                            wall.center = (DISTANZA_DA_LATO+(j*DIM_MURI), DISTANZA_DA_TITOLO+(i*DIM_MURI))
                            pg.draw.rect(SCREEN, BLUE, wall)
                        elif labirinto[i][j]==FINISH:
                            wall.center = (DISTANZA_DA_LATO+(j*DIM_MURI), DISTANZA_DA_TITOLO+(i*DIM_MURI))
                            pg.draw.rect(SCREEN, RED, wall)
        elif flag==2 or flag==3:
            if flag==3:
                for i in range(ROWS):
                    for j in range(COLS):
                        tabella_visiva[i][j]=VUOTO
            for i in range(-AMPIEZZA_VISIVA, AMPIEZZA_VISIVA+1, 1):
                for j in range(-AMPIEZZA_VISIVA, AMPIEZZA_VISIVA+1, 1):
                    if x+i>=0 and x+i<ROWS and y+j>=0 and y+j<COLS:
                        if i!=0 or j!=0:
                            tabella_visiva[x+i][y+j]=VISUALIZZATO
            for i in range(ROWS):
                for j in range(COLS):
                    if i==0 or i==ROWS-1 or j==0 or j==COLS-1:
                        wall.center = (DISTANZA_DA_LATO+(j*DIM_MURI), DISTANZA_DA_TITOLO+(i*DIM_MURI))
                        pg.draw.rect(SCREEN, WHITE, wall)
                    if i==x and j==y:
                        omino.center = (DISTANZA_DA_LATO+(j*DIM_MURI), DISTANZA_DA_TITOLO+(i*DIM_MURI))
                        pg.draw.rect(SCREEN, GREEN, omino)
                    elif tabella_visiva[i][j]==VISUALIZZATO:
                        if labirinto[i][j]==MURO:
                            wall.center = (DISTANZA_DA_LATO+(j*DIM_MURI), DISTANZA_DA_TITOLO+(i*DIM_MURI))
                            pg.draw.rect(SCREEN, WHITE, wall)
                        elif labirinto[i][j]==START:
                            wall.center = (DISTANZA_DA_LATO+(j*DIM_MURI), DISTANZA_DA_TITOLO+(i*DIM_MURI))
                            pg.draw.rect(SCREEN, BLUE, wall)
                        elif labirinto[i][j]==FINISH:
                            wall.center = (DISTANZA_DA_LATO+(j*DIM_MURI), DISTANZA_DA_TITOLO+(i*DIM_MURI))
                            pg.draw.rect(SCREEN, RED, wall)
        elif flag==4:
            for i in range(-AMPIEZZA_VISIVA, AMPIEZZA_VISIVA+1, 1):
                for j in range(-AMPIEZZA_VISIVA, AMPIEZZA_VISIVA+1, 1):
                    if x+i>=0 and x+i<ROWS and y+j>=0 and y+j<COLS:
                        if i==0 and j==0:
                            omino.center = ((WIDTH/2)+(j*DIM_MURI), (HEIGHT/2)+(i*DIM_MURI))
                            pg.draw.rect(SCREEN, GREEN, omino)
                        else:
                            if labirinto[x+i][y+j]==MURO:
                                wall.center = ((WIDTH/2)+(j*DIM_MURI), (HEIGHT/2)+(i*DIM_MURI))
                                pg.draw.rect(SCREEN, WHITE, wall)
                            elif labirinto[x+i][y+j]==START:
                                wall.center = ((WIDTH/2)+(j*DIM_MURI), (HEIGHT/2)+(i*DIM_MURI))
                                pg.draw.rect(SCREEN, BLUE, wall)
                            elif labirinto[x+i][y+j]==FINISH:
                                wall.center = ((WIDTH/2)+(j*DIM_MURI), (HEIGHT/2)+(i*DIM_MURI))
                                pg.draw.rect(SCREEN, RED, wall)
        if x==arrivo and y==COLS-1:
            win = FONT2.render("Congratulations, YOU ESCAPED!!!", True, AZZURRO)
            rectWin = win.get_rect()
            rectWin.center = (WIDTH/2, HEIGHT-50)
            SCREEN.blit(win, rectWin)
            aggiorna()
            ricominciamo = False
            while not ricominciamo:
                for event in pg.event.get():
                    if event.type==pg.KEYDOWN:
                        if event.key == pg.K_0 or event.key == pg.K_SPACE:
                            inizializza()
                            ricominciamo = True
                            flag=0
                    if event.type == pg.QUIT:
                        exit()
        aggiorna()