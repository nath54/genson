#coding:utf-8
import pygame,wave,math,binascii,time,random,os
from pygame.locals import *

do=[32.703, 65.406, 130.81, 261.63, 523.25, 1046.5, 2093, 4186 ,8372,16744]
do_d=[34.648, 69.296, 138.59, 277.18, 554.37, 1108.7, 2217.5, 4434.9, 8869.8, 17740.0]
re=[36.708, 73.416, 146.83, 293.66, 587.33, 1174.7, 2349.3, 4698.6, 9397.3, 18795]
re_d=[38.891, 77.782, 155.56, 311.13, 622.25, 1244.5, 2489.0, 4978.0, 9956.1, 19912.0]
mi=[41.203, 82.407, 164.81, 329.63, 659.26, 1318.5, 2637.0, 5274.0, 10548.0, 21096.0]
fa=[43.654, 87.307, 174.61, 349.23, 698.46, 1396.9, 2793.8, 5587.7, 11175.0, 22351.0]
fa_d=[46.249, 92.499, 185., 369.99, 739.99, 1480., 2960., 5919.9, 11840., 23680.]
sol=[48.999, 97.999, 196., 392., 783.99, 1568., 3136., 6271.9, 12544., 25088.]
sol_d=[51.913, 103.83, 207.65, 415.3, 830.61, 1661.2, 3322.4, 6644.9, 13290., 26580.]
la=[55., 110., 220., 440., 880., 1760., 3520., 7040., 14080., 28160.]
la_d=[58.27, 116.54, 233.08, 466.16, 932.33, 1864.7, 3729.3, 7458.6, 14917., 29834]
si=[61.735, 123.47, 246.94, 493.88, 987.77, 1975.5, 3951.1, 7902.1, 15804., 31609.]


notest=["do","do#","re","re#","mi","fa","fa#","sol","sol#","la","la#","si"]
nts=        [do ,do_d,re ,mi ,fa ,fa_d,sol,sol_d,la ,la_d,si ]
keysnotes=  [K_e,K_d ,K_r,K_t,K_y,K_h ,K_u,K_j  ,K_i,K_k ,K_o]
tkeysnotes= ["e","d" ,"r","t","y","h" ,"u","j"  ,"i","k" ,"o"]
dirm="musiques/"

tex,tey=1000,500

pygame.init()
fenetre=pygame.display.set_mode([tex,tey])
font=pygame.font.SysFont("Serif",10)

if not dirm[:-1] in os.listdir("./"): os.mkdir(dirm)

def a(duree,notes,nom):
    NomFichier = nom
    Monson = wave.open(NomFichier,'w') # instanciation de l'objet Monson
    nbCanal = 2    # stéreo
    nbOctet = 1    # taille d'un échantillon : 1 octet = 8 bits
    fech = 4000   # fréquence d'échantillonnage
    nbEchantillon = int(duree*fech)
    parametres = (nbCanal,nbOctet,fech,nbEchantillon,'NONE','not compressed')# tuple
    Monson.setparams(parametres)    # création de l'en-tête (44 octets)
    # niveau max dans l'onde positive : +1 -> 255 (0xFF)
    # niveau max dans l'onde négative : -1 ->   0 (0x00)
    # niveau sonore nul :                0 -> 127.5 (0x80 en valeur arrondi)
    for nn in range(0,len(notes)-1):
        amplitudeG = 127.5*notes[nn][2]
        amplitudeD = 127.5*notes[nn][3]
        for i in range(0,int(nbEchantillon/(len(notes)-1))):
            # canal gauche
            # 127.5 + 0.5 pour arrondir à l'entier le plus proche
            valG = wave.struct.pack('B',int(128.0 + amplitudeG*math.sin(2.0*math.pi*notes[nn][0]*i/fech)))
            # canal droit
            valD = wave.struct.pack('B',int(128.0 + amplitudeD*math.sin(2.0*math.pi*notes[nn][1]*i/fech)))
            Monson.writeframes(valG + valD) # écriture frame
    
    Monson.close()
    Fichier = open(NomFichier,'rb')
    data = Fichier.read()
    tailleFichier = len(data)
    print('\nTaille du fichier',NomFichier, ':', tailleFichier,'octets')
    print("Lecture du contenu de l'en-tête (44 octets) :")
    print(binascii.hexlify(data[0:44]))
    print("Nombre d'octets de données :",tailleFichier - 44)
    Fichier.close()
    # lecture audio (sortie vers la carte son)
    import winsound
    winsound.PlaySound(nom,winsound.SND_FILENAME)


def gal():
    encour=True
    while encour:
        nom=str(random.randint(0,999999999))+".wav"
        notes=[]
        n=[random.randint(0,len(nts)-1),random.randint(0,len(nts[0])-1),random.randint(0,len(nts)-1),random.randint(0,len(nts[0])-1)]
        for x in range(random.randint(10,100)):
            notes.append([nts[n[0]][n[1]],nts[n[2]][n[3]],float(random.randint(30,100))/100.0,float(random.randint(30,100))/100.0])
            n[0]+=random.randint(-1,1)
            n[1]+=random.randint(-1,1)
            n[2]+=random.randint(-1,1)
            n[3]+=random.randint(-1,1)
            if n[0]<0: n[0]=0
            if n[0]>len(nts)-1: n[0]=len(nts)-1
            if n[1]<0: n[1]=0
            if n[1]>len(nts[0])-1: n[1]=len(nts[0])-1
            if n[2]<0: n[2]=0
            if n[2]>len(nts)-1: n[2]=len(nts)-1
            if n[3]<0: n[3]=0
            if n[3]>len(nts[0])-1: n[3]=len(nts[0])-1
        fenetre.fill((0,0,0))
        tfg,tfd,tng,tnd="","","",""
        for n in notes: tfg,tfd,tng,tnd=tfg+" "+str(n[0]),tfd+" "+str(n[1]),tng+" "+str(n[2]),tnd+" "+str(n[3])
        duree=float(random.randint(50,250)/300)*float(len(notes))
        fenetre.blit(font.render("frequence gauche = "+tfg,20,(255,255,255)),[20,50])
        fenetre.blit(font.render("frequence droite = "+tfd,20,(255,255,255)),[20,100])
        fenetre.blit(font.render("niveau gauche = "+tng,20,(255,255,255)),[20,150])
        fenetre.blit(font.render("niveau droit = "+tnd,20,(255,255,255)),[20,200])
        fenetre.blit(font.render("duree = "+str(duree)+" sec",20,(255,255,255)),[20,250])
        pygame.display.update()
        a(duree,notes,nom)
        for event in pygame.event.get():
            if event.type==QUIT: encour=False
            elif event.type==KEYDOWN and event.key==K_q: encour=False

def aff_norm(notess,octsel):
    fenetre.fill((0,0,0))
    bts=[]
    for x in range(20): bts.append(None)
    txt=""
    for n in notess:
        txt+=" "+n
    fenetre.blit(font.render(txt,20,(255,255,255)),[10,10])
    xx,yy,b=10,75,5
    tx,ty=50,150
    for n in nts:
        bts[b]=pygame.draw.rect(fenetre,(200,200,200),(xx,yy,tx,ty),0)
        fenetre.blit(font.render(notest[nts.index(n)]+str(octsel+1),20,(0,0,0)),[xx+5,yy+5])
        fenetre.blit(font.render(str(n[octsel]),20,(0,0,0)),[xx+1,yy+35])
        fenetre.blit(font.render(tkeysnotes[nts.index(n)],20,(0,0,0)),[xx+1,yy+55])
        b+=1
        xx+=tx+5
    bts[0]=pygame.draw.rect(fenetre,(50,150,20),(450,400,100,50),0)
    fenetre.blit(font.render("play",20,(0,0,0)),[455,405])
    bts[1]=pygame.draw.rect(fenetre,(50,150,20),(xx,yy+ty+25,100,50),0)
    fenetre.blit(font.render("<--",20,(0,0,0)),[xx+5,yy+ty+30])
    bts[2]=pygame.draw.rect(fenetre,(255,255,255),(xx,yy,tx,ty),0)
    bts[3]=pygame.draw.rect(fenetre,(50,150,20),(50,300,80,50),0)
    fenetre.blit(font.render("octave-",20,(0,0,0)),[55,305])
    bts[4]=pygame.draw.rect(fenetre,(50,150,20),(170,300,80,50),0)
    fenetre.blit(font.render("octave+",20,(0,0,0)),[175,305])
    pygame.display.update()
    return bts
        

def gnorm():
    encour=True
    tn=0.3
    octsel=0
    notess=[]
    notesf=[]
    while encour:
        bts=aff_norm(notess,octsel)
        for event in pygame.event.get():
            if event.type==QUIT: exit()
            elif event.type==KEYDOWN:
                if event.key==K_ESCAPE: encour=False
                for k in keysnotes:
                    if event.key==k:
                       notess.append(str(notest[keysnotes.index(k)]+str(octsel+1)))
                       notesf.append([nts[keysnotes.index(k)][octsel],nts[keysnotes.index(k)][octsel],1,1])
                       
            elif event.type==MOUSEBUTTONUP:
                pos=pygame.mouse.get_pos()
                for b in bts:
                    if b!=None and b.collidepoint(pos):
                        di=bts.index(b)
                        if di==0:
                            duree=len(notesf)*tn
                            nom=dirm+str(len(os.listdir(dirm)))+".wav"
                            a(duree,notesf,nom)
                        elif di==1:
                            if notess!=[]:
                                del(notess[len(notess)-1])
                                del(notesf[len(notesf)-1])
                        elif di==2:
                            notess.append("_")
                            notesf.append([0,0,0,0])
                        elif di==3:
                            if octsel>0: octsel-=1
                        elif di==4:
                            if octsel<len(nts[0])-1: octsel+=1
                        elif di>=5 and di<=5+len(nts):
                            notess.append(notest[di-5]+str(octsel))
                            notesf.append([nts[di-5][octsel],nts[di-5][octsel],1,1])
                
gnorm()
    
