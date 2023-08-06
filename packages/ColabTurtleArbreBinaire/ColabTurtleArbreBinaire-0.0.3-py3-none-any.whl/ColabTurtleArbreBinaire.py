"""Ce module permet de représenter un arbre binaire et de visualiser son
parcours à l'aide du module ColabTurtlePlus (un module dérivé de Turtle pour
Google Colab). Il faut préalablement installer le module ColabTurtlePlus en
exécutant la commande shell suivante dans une cellule :

!pip install ColabTurtlePlus

Dans ce module, un arbre binaire est représenté en Python à l'aide d'une liste
de la façon suivante :
    [] représente l'arbre vide ;
    [v, sag, sad] représente un arbre non vide avec :
        v : la valeur de sa racine ;
        sag : son sous-arbre de gauche ;
        sad : son sous-arbre de droite.

Les deux fonctions principales du module sont :
    dessiner(a, dessiner_vide=True)
        qui permet de dessiner un arbre a avec ou sans ses arbres vides.
    dessiner_parcours(a, parcours='préfixe', dessiner_vide=True)
        qui permet de dessiner un arbre a et animer son parcours en 'largeur' ou
        en profondeur 'préfixe', 'infixe', 'suffixe' (ou 'postfixe').

Exemples d'utilisations :

arb0 = [
    30,
        [9,
            [2,
                [5, [], []],
                [90, [], []]
            ],
            [13,
                [25, [], []],
                []
            ]
        ],
        [5,
            [54, [], []],
            [15, [], []]
        ]
]
dessiner(arb0)
dessiner(arb0, dessiner_vide=False)
dessin_parcours(arb0, parcours='préfixe')
dessin_parcours(arb0, parcours='suffixe', dessiner_vide=False)

arb1 = [
    'Albatros',
        ['Baleine',
            ['Cachalot',
                ['Dauphin', [], []],
                ['Éléphant', [], []]
            ],
            ['Faucon',
                ['Gazelle', [], []],
                []
            ]
        ],
        ['Héron',
            ['Iguane', [], []],
            ['Jaguar', [], []]
        ]
]

dessiner(arb1)
dessiner(arb1, dessiner_vide=False)
dessin_parcours(arb1, parcours='infixe')
dessin_parcours(arb1, parcours='postfixe', dessiner_vide=False)
"""

import ColabTurtlePlus.Turtle as t
from math import sqrt
from time import sleep
from copy import deepcopy

VIT_DESSIN = 0 # par défaut 0 (dessin instantané), de 1 à 13 pour une vitesse de
               # tracé variable : 1 (la plus lente) ) 13 (la plus rapide)
VIT_PARCOURS = 5 # par défaut 5, de 1 à 13
FACT_ECHELLE = 40  # par défaut 40 : l'unité d'affichage vaut 40 pixels
                   # les centre des noeuds sont espacés verticalement de deux
                   # unités et au minimum de deux unités horizontalement
# Choisir des fontes prise en charge nativement par le navigateur
# (safe-web font):
#    - Arial (sans-serif)
#    - Verdana (sans-serif)
#    - Tahoma (sans-serif)
#    - Trebuchet MS (sans-serif)
#    - Times New Roman (serif)
#    - Georgia (serif) (inadaptée)
#    - Garamond (serif)
#    - Courier New (monospace)
#    - Brush Script MT (cursive)
# Fonte pour les valeurs numériques entre 1 et 99 ou les chaînes à un ou deux
# caractère(s). Par défaut 'Garamond'.
FONT_SERIF = 'Garamond'
# Fonte pour les chaînes ou nombres d'au moins trois caractères. Par défaut
# 'Courier New'.
FONT_MONO = 'Courier New'

def arbre_valide(a):
    """Indique si a est un arbre binaire valide selon les conventions donnés en 
    début de module."""
    if a == []:
        return True
    elif isinstance(a, list) and len(a) == 3:
            return arbre_valide(a[1]) and arbre_valide(a[2])
    else:
        return False


def arbre_recherche_valide(a):
    """Indique si a est un arbre binaire de recherche."""
    assert arbre_valide(a), "arbre d'entrée invalide !"
    if a == []:
        return True
    elif a[1] != [] and a[1][0] > a[0] or a[2] != [] and a[2][0] < a[0]:
        return False
    else:
        return arbre_valide(a[1]) and arbre_valide(a[2])

################################################################################
# Interface d'une file pour l'algorithme de parcours en largeur                #
################################################################################

def creer_file_vide():
    return []


def file_est_vide(file):
    return file == []


def enfiler(file, e):
    file.append(e)


def defiler(file: list):
    assert not file_est_vide(file), 'défiler impossible : file vide !'
    tete = file.pop(0)
    return tete


def hauteur(a):
    """Prend en entrée un arbre binaire et renvoie sa hauteur (par convention
    l'arbre vide a pour hauteur 0)."""
    if a == []:
        return 0
    else:
        return 1 + max(hauteur(a[1]), hauteur(a[2]))


def liste_noeuds(a):
    """Prend en entrée un arbre binaire et renvoie dans une liste les valeurs
    de ses noeuds parcourus dans l'ordre infixe."""
    tab = []
    def liste_noeuds_rec(a):
        if a != []:
            tab.append(a[0])
            liste_noeuds_rec(a[1])
            liste_noeuds_rec(a[2])
    liste_noeuds_rec(a)
    return tab


def longueur_max_element(a):
    """Prend en entrée un arbre binaire et renvoie la taille maximum (le nombre
    de caractères maximum) des valeurs de ses noeuds supposées être des nombres
    ou des chaînes de carctères."""
    maxi = 0
    for e in liste_noeuds(a):
        if len(str(e)) > maxi:
            maxi = len(str(e))
    return maxi


def initialisation_affichage(h, longueur_max):
    """Prend en entrée la hauteur d'un arbre binaire et le nombre maximum en
    de caractères des valeurs de ses noeuds. Initialise le cadre d'affichage de
    ColabTurtlePlus en le dimensionnant de manière adaptée, initialise les
    paramètres de la tortue"""
    t.clearscreen()
    t.hideturtle()
    if longueur_max <= 2:
        t.setup(FACT_ECHELLE*max(2**h, 1), FACT_ECHELLE*max(2*h, 1))
    else:
        t.setup(round(FACT_ECHELLE*2**(h - 1)*max(longueur_max/3 + 0.25, 2)),
                FACT_ECHELLE*max(2*h, 1))
    t.pensize(2)
    t.shape('turtle')
    t.turtlesize()
    t.animationOff()


def dessin_arete(sous_arbre, x, y, xf, yf, vers_haut=False, couleur="black",
                 parcours=False, chaine_longue=False, dessiner_vide=True):
    """Dessine une arête entre la racine de a de coordonnées (x, y) et un noeud
    fils de coordonnées (xf, yf). Ne doit pas être appelé avant un appel de la
    fonction initialisation_affichage."""
    if sous_arbre != [] or dessiner_vide:
        x_depart = x * FACT_ECHELLE
        y_depart = y * FACT_ECHELLE
        x_dest = xf * FACT_ECHELLE
        y_dest = yf * FACT_ECHELLE
        dx = x_dest - x_depart
        dy = y_dest - y_depart
        coef = 1
        if chaine_longue:
            r = 0.3/abs(dy) * sqrt(dx**2 + dy**2)
            r_dest = r
            r_depart = r
        else:
            r_dest = 0.5
            r_depart = 0.5
        if sous_arbre == []:
            r_dest = 0.125
        ratio_depart = r_depart*FACT_ECHELLE/sqrt(dx**2 + dy**2)
        ratio_dest = r_dest*FACT_ECHELLE/sqrt(dx**2 + dy**2)
        if vers_haut:
            ratio_depart, ratio_dest = ratio_dest, ratio_depart
            x_dest, x_depart = x_depart, x_dest
            y_dest, y_depart = y_depart, y_dest
            coef = -1
        if parcours:
            t.speed(VIT_PARCOURS)
            t.penup()
            t.color(couleur, couleur)
            t.showturtle()
            t.face(t.towards(x_dest, y_dest))
            t.goto(x_depart + coef*ratio_depart*dx,
                   y_depart + coef*ratio_depart*dy)
        else:
            t.speed(VIT_DESSIN)
            t.hideturtle()
        t.pendown()
        t.jumpto(x_depart + coef*ratio_depart*dx,
                 y_depart + coef*ratio_depart*dy)
        t.face(t.towards(x_dest, y_dest))
        t.goto(x_dest - coef*ratio_dest*dx, y_dest - coef*ratio_dest*dy)
        if parcours:
            t.speed(VIT_PARCOURS)
            t.penup()
            t.showturtle()
            t.goto(x_dest, y_dest)


def coordonnees_fils(a, x, y, prof, haut, gauche, longueur_max):
    """Calcul les coordonnées du noeud fils de gauche (si gauche=True) ou du
    noeud fils de droite (si gauche=False) de la racine de l'arbre a de position
    (x, y)."""
    if gauche:
        i = 1
        coef = -1
    else:
        i = 2
        coef = 1
    if a[i] == []:
        xf = x + coef*0.25
        yf = y - 0.75
    else:
        if longueur_max <= 2:
            decallage = 2**(haut - prof - 2)
        else:
            decallage = 2**(haut - prof - 2)*max(longueur_max/6 + 0.125, 1)
        xf = x + coef*decallage
        yf = y - 2
    return xf, yf


def dessin_noeud(val, x, y, couleur=("black", "white"), parcours=False,
                 chaine_longue=False):
    """Dessine un noeud de valeur val centré au point (x, y). Ne doit pas être
    appelé avant un appel de la fonction initialisation_affichage."""
    angle_arrivee = t.heading()
    t.speed(VIT_DESSIN)
    t.color(couleur[0], couleur[1])
    t.hideturtle()
    t.pendown()
    t.face(0)
    x *= FACT_ECHELLE
    y *= FACT_ECHELLE
    r = FACT_ECHELLE//2
    if not chaine_longue:
        t.jumpto(x, y - r)
        t.begin_fill()
        t.circle(r)
        t.end_fill()
        fonte = FONT_SERIF
        t.jumpto(x, y - r/3)
    else:
        fonte = FONT_MONO
        t.jumpto(x, y - r/4)
    # choisir une fonte prise en charge nativement en HTML
    t.write(val, move=False, align='center', font=(fonte, r, 'normal'))
    t.jumpto(x, y)
    if parcours:
        t.showturtle()
    t.face(angle_arrivee)


def dessin_arbre_vide(x, y, couleur="black", parcours=False,
                      dessiner_vide=True):
    """Dessine un arbre vide à la position (x, y). Ne doit pas être
    appelé avant un appel de la fonction initialisation_affichage."""
    if dessiner_vide:
        angle_arrivee = t.heading()
        t.speed(VIT_DESSIN)
        t.color(couleur, couleur)
        t.hideturtle()
        t.pendown()
        t.face(0)
        x *= FACT_ECHELLE
        y *= FACT_ECHELLE
        r = FACT_ECHELLE * 0.125
        t.jumpto(x, y - r)
        t.begin_fill()
        t.circle(r)
        t.end_fill()
        t.jumpto(x, y)
        if parcours:
            t.showturtle()
        t.face(angle_arrivee)
        t.done()


def dessiner(a, dessiner_vide=True, etendre=False, val=None):
    """Prend en entrée un arbre binaire et affiche sa représentation graphique.
    Le paramètre booléen dessiner_vide par (défaut égal à True) précise si l'on
    souhaite que la représentation graphique affiche les arbres vides. Le
    paramètre booléen etendre permet d'indiquer si l'on souhaite que l'affichage
    de l'arbre soit étendue en vue d'une insertion (pour les arbres binaires
    de recherche uniquement) de la valeur val."""
    assert arbre_valide(a), "abre non valide !"
    h = hauteur(a)
    if etendre: # pour les insertions augmentant la hauteur de l'arbre
        h += 1
    if val == None:
        lmax = longueur_max_element(a)
    else:
        lmax = max(longueur_max_element(a), len(str(val)))
    initialisation_affichage(h, lmax)
    if lmax >= 3:
        chaine = True
    else:
        chaine = False
    # définition de la fonction encapsulée récursive
    def dessiner_rec(a, x, y, prof=0, chaine_longue=chaine):
        if a == []:
            dessin_arbre_vide(x, y, dessiner_vide=dessiner_vide)
        else:
            # dessin de la racine de l'arbre courant
            dessin_noeud(a[0], x, y, chaine_longue=chaine_longue)
            # dessin du sous-arbre gauche
            xg, yg = coordonnees_fils(a, x, y, prof, h, gauche=True,
                                      longueur_max=lmax)
            dessin_arete(a[1], x, y, xg, yg, chaine_longue=chaine_longue,
                         dessiner_vide=dessiner_vide)
            dessiner_rec(a[1], xg, yg, prof + 1)
            # dessin du sous-arbre droit
            xd, yd = coordonnees_fils(a, x, y, prof, h, gauche=False,
                                      longueur_max=lmax)
            dessin_arete(a[2], x, y, xd, yd, chaine_longue=chaine_longue,
                         dessiner_vide=dessiner_vide)
            dessiner_rec(a[2], xd, yd, prof + 1)
    # appel de la fonction récursive encapsulée
    dessiner_rec(a, 0, max(h - 1, 0))
    t.done()


def dessiner_parcours(a, parcours='préfixe', dessiner_vide=True):
    """Prend en entrée un arbre binaire, le représente puis génère une animation
    de parcours en profondeur. Le paramètre parcours (str) permet d'indiquer le
    type de parcours souhaité :
        - 'largeur': parcours en largeur.
            Un affichage permet de suivre au fur et à mesure la file utilisée
            pour cet algorithme de parcours ainsi que la liste des noeuds
            visités.
        - en profondeur :
            - 'préfixe'
            - 'infixe'
            - 'suffixe' (ou 'postfixe')
    Le paramètre booléen dessiner_vide (par défaut True) précise si l'on
    souhaite que l'affichage et le parcours présentent les arbres vides.
    """
    assert arbre_valide(a), "abre non valide !"
    dessiner(a, dessiner_vide=dessiner_vide)
    h = hauteur(a)
    lmax = longueur_max_element(a)
    if lmax >= 3:
        chaine_longue = True
    else:
        chaine_longue = False
    t.penup()
    t.goto(0, max(h - 1, 0))
    if parcours == 'largeur' and a != []:
        f = creer_file_vide()
        f_affichage = creer_file_vide()
        visites = []
        prof = 0
        x = 0
        y = max(h - 1, 0)
        print('File :', '⬅' + str(f_affichage) + '⬅', '\t\tNoeuds visités :',
              visites)
        enfiler(f, (a, prof, x, y))
        enfiler(f_affichage, a[0])
        print('File :', '⬅' + str(f_affichage) + '⬅', '\t\tNoeuds visités :',
              visites)
        while not file_est_vide(f):
            a_courant, prof, x, y = defiler(f)
            visites.append(defiler(f_affichage))
            print('File :', '⬅' + str(f_affichage) + '⬅',
                  '\t\tNoeuds visités :', visites)
            # dessin de la racine de l'arbre courant
            couleur = ('green', 'lightgray')
            dessin_noeud(a_courant[0], x, y, couleur=couleur,
                            chaine_longue=chaine_longue, parcours=True)
            t.color('green', 'green')
            t.update()
            sleep(1)
            #t.update()
            # dessin des sous-arbres gauche et droit
            couleur = ('red', 'white')
            for i in (1, 2):
                booleens = [True, False]
                xf, yf = coordonnees_fils(a_courant, x, y, prof, h,
                                          longueur_max=lmax,
                                          gauche=booleens[i - 1])
                dessin_arete(a_courant[i], x, y, xf, yf, couleur='red',
                            parcours=True, chaine_longue=chaine_longue,
                            dessiner_vide=dessiner_vide)
                if a_courant[i] == []:
                    dessin_arbre_vide(xf, yf, couleur="black", parcours=True,
                                      dessiner_vide=dessiner_vide)
                else :
                    enfiler(f, (a_courant[i], prof + 1, xf, yf))
                    enfiler(f_affichage, a_courant[i][0])
                    print('File :', '⬅' + str(f_affichage) + '⬅',
                          '\t\tNoeuds visités :', visites)
                    dessin_noeud(a_courant[i][0], xf, yf, couleur=couleur,
                                chaine_longue=chaine_longue, parcours=True)
                dessin_arete(a_courant[i], x, y, xf, yf, couleur='green',
                            parcours=True, chaine_longue=chaine_longue,
                            dessiner_vide=dessiner_vide, vers_haut=True)
    else:
        # définition de la fonction encapsulée récursive
        def dessiner_parcours_rec(a, x, y, prof=0, chaine_longue=chaine_longue):
            if a == []:
                dessin_arbre_vide(x, y, couleur='green',
                                  dessiner_vide=dessiner_vide)
            else:
                if parcours == 'préfixe':
                    couleur = ('green', 'lightgray')
                else:
                    couleur = ('red', 'white')
                # dessin de la racine de l'arbre courant
                dessin_noeud(a[0], x, y, couleur=couleur,
                             chaine_longue=chaine_longue, parcours=True)
                # dessin du sous-arbre gauche
                xg, yg = coordonnees_fils(a, x, y, prof, h, longueur_max=lmax,
                                          gauche=True)
                dessin_arete(a[1], x, y, xg, yg, couleur='red', parcours=True,
                             chaine_longue=chaine_longue,
                             dessiner_vide=dessiner_vide)
                dessiner_parcours_rec(a[1], xg, yg, prof + 1,
                                      chaine_longue=chaine_longue)
                dessin_arete(a[1], x, y, xg, yg, couleur='green',
                             vers_haut=True, parcours=True,
                             chaine_longue=chaine_longue,
                             dessiner_vide=dessiner_vide)
                if parcours == 'infixe':
                    couleur = ('green', 'lightgray')
                    # dessin de la racine de l'arbre courant
                    dessin_noeud(a[0], x, y, couleur=couleur,
                                 chaine_longue=chaine_longue, parcours=True)
                # dessin du sous-arbre droit
                xd, yd = coordonnees_fils(a, x, y, prof, h, longueur_max=lmax,
                                          gauche=False)
                dessin_arete(a[2], x, y, xd, yd, couleur='red', parcours=True,
                             chaine_longue=chaine_longue,
                             dessiner_vide=dessiner_vide)
                dessiner_parcours_rec(a[2], xd, yd, prof + 1,
                                      chaine_longue=chaine_longue)
                dessin_arete(a[2], x, y, xd, yd, couleur='green',
                             vers_haut=True, parcours=True,
                             chaine_longue=chaine_longue,
                             dessiner_vide=dessiner_vide)
                if parcours == 'suffixe' or parcours == 'postfixe':
                    couleur = ('green', 'lightgray')
                    # dessin de la racine de l'arbre courant
                    dessin_noeud(a[0], x, y, couleur=couleur,
                                 chaine_longue=chaine_longue, parcours=True)
        # appel de la fonction récursive encapsulée
        dessiner_parcours_rec(a, 0, max(h - 1, 0), chaine_longue=chaine_longue)
    t.hideturtle()
    t.done()


def dessiner_insertion(a, val, dessiner_vide=True):
    """Prend en entrée un arbre binaire de recherche, le représente puis
    génère une animation de l'insertion de val dans cet arbre. Le paramètre
    booléen dessiner_vide (par défaut True) précise si l'on souhaite que
    l'affichage et l'insertion présentent les arbres vides.
    """
    assert arbre_recherche_valide(a), "a doit être un arbre de recherche !"
    def inserer(a2, val):
        if a2 == []:
            a2.append(val)
            a2.append([])
            a2.append([])
        elif val < a2[0]:
            inserer(a2[1], val)
        else:
            inserer(a2[2], val)
    a_apres_insertion = deepcopy(a) # copie de l'arbre a
    inserer(a_apres_insertion, val)
    h = hauteur(a)
    h_apres_insertion = hauteur(a_apres_insertion)
    if h_apres_insertion > h:
        etendre = True
    else:
        etendre = False
    dessiner(a, dessiner_vide=dessiner_vide, etendre=etendre, val=val)
    lmax = longueur_max_element(a_apres_insertion)
    if lmax >= 3:
        chaine_longue = True
    else:
        chaine_longue = False
    t.penup()
    t.goto(0, max(h - 1, 0))
    # définition de la fonction encapsulée récursive
    def dessiner_insertion_rec(a, a_apres_insertion, x, y, prof=0,
                               chaine_longue=chaine_longue,
                               dessiner_vide=dessiner_vide):
        if a == []:
            dessin_noeud(val, x, y, couleur=('green', 'lightgreen'),
                         chaine_longue=chaine_longue, parcours=True)
            if dessiner_vide:
                # dessin du sous-arbre vide de gauche
                xg, yg = coordonnees_fils(a_apres_insertion, x, y, prof,
                                          h_apres_insertion, longueur_max=lmax,
                                          gauche=True)
                dessin_arete(a_apres_insertion[1], x, y, xg, yg,
                             couleur='green',
                             parcours=False,
                             chaine_longue=chaine_longue,
                             dessiner_vide=dessiner_vide)
                dessin_arbre_vide(xg, yg, couleur='green')
                # dessin du sous-arbre vide de droite
                xd, yd = coordonnees_fils(a_apres_insertion, x, y, prof,
                                          h_apres_insertion, longueur_max=lmax,
                                          gauche=False)
                dessin_arete(a_apres_insertion[2], x, y, xd, yd,
                             couleur='green',
                             parcours=False,
                             chaine_longue=chaine_longue,
                             dessiner_vide=dessiner_vide)
                dessin_arbre_vide(xd, yd, couleur='green')
        else:
            # dessin de la racine de l'arbre courant
            dessin_noeud(a_apres_insertion[0], x, y,
                         couleur=('green', 'lightgray'),
                         chaine_longue=chaine_longue, parcours=True)
            # dessin de la racine du sous-arbre de gauche
            if val < a[0]:
                xg, yg = coordonnees_fils(a_apres_insertion, x, y, prof,
                                          h_apres_insertion,
                                          longueur_max=lmax, gauche=True)
                if a[1] == [] and dessiner_vide:
                    xvg, yvg = coordonnees_fils(a, x, y, prof,
                                                h_apres_insertion,
                                                longueur_max=lmax, gauche=True)
                    dessin_arbre_vide(xvg, yvg, couleur="white", parcours=False,
                                      dessiner_vide=True)
                    dessin_arete(a[1], x, y, xvg, yvg, couleur='white',
                                 parcours=False, chaine_longue=chaine_longue,
                                 dessiner_vide=dessiner_vide)
                    dessin_noeud(a[0], x, y, couleur=('green', 'lightgray'),
                                 chaine_longue=chaine_longue, parcours=False)
                dessin_arete(a_apres_insertion[1], x, y, xg, yg,
                             couleur='green', parcours=True,
                             chaine_longue=chaine_longue,
                             dessiner_vide=dessiner_vide)
                dessiner_insertion_rec(a[1], a_apres_insertion[1], xg, yg,
                                       prof + 1, chaine_longue=chaine_longue,
                                       dessiner_vide=dessiner_vide)
            # dessin de la racine du sous-arbre de gauche
            else:
                xd, yd = coordonnees_fils(a_apres_insertion, x, y, prof,
                                          h_apres_insertion,
                                          longueur_max=lmax, gauche=False)
                if a[2] == [] and dessiner_vide:
                    xvd, yvd = coordonnees_fils(a, x, y, prof,
                                                h_apres_insertion,
                                                longueur_max=lmax, gauche=False)
                    dessin_arbre_vide(xvd, yvd, couleur="white", parcours=False,
                                      dessiner_vide=True)
                    dessin_arete(a[2], x, y, xvd, yvd,
                                 couleur='white',
                                 parcours=False, chaine_longue=chaine_longue,
                                 dessiner_vide=dessiner_vide)
                    dessin_noeud(a[0], x, y,
                                 couleur=('green', 'lightgray'),
                                 chaine_longue=chaine_longue, parcours=False)
                dessin_arete(a_apres_insertion[2], x, y, xd, yd,
                             couleur='green', parcours=True,
                             chaine_longue=chaine_longue,
                             dessiner_vide=dessiner_vide)
                dessiner_insertion_rec(a[2], a_apres_insertion[2], xd, yd,
                                       prof + 1, chaine_longue=chaine_longue,
                                       dessiner_vide=dessiner_vide)
    # appel de la fonction récursive encapsulée
    dessiner_insertion_rec(a, a_apres_insertion, 0,
                           max(h_apres_insertion - 1, 0),
                           chaine_longue=chaine_longue,
                           dessiner_vide=dessiner_vide)
    t.hideturtle()
    t.done()


def dessiner_recherche(a, val, dessiner_vide=True, arbre_bin_recherche=False,
                       parcours='préfixe'):
    """Prend en entrée un arbre binaire, le représente puis génère une animation
    de la recherche de val dans cet arbre. Le paramètre booléen dessiner_vide
    (par défaut True) précise si l'on souhaite que l'affichage et la recherche
    présentent les arbres vides. Le paramètre booléen arbre_bin_recherche
    précise si la recherche a lieu dans un arbre binaire de recherche. Pour les
    arbre binaires quelconques, le paramètre parcours permet de préciser le type
    de parcours utilisé pour la recherche :
        - 'largeur': parcours en largeur
        - en profondeur :
            - 'préfixe'
            - 'infixe'
            - 'suffixe' (ou 'postfixe')
    """
    if arbre_bin_recherche:
        assert arbre_recherche_valide(a), "a doit être un arbre de recherche !"
        h = hauteur(a)
        dessiner(a, dessiner_vide=dessiner_vide)
        lmax = longueur_max_element(a)
        if lmax >= 3:
            chaine_longue = True
        else:
            chaine_longue = False
        t.penup()
        t.goto(0, max(h - 1, 0))
        # définition de la fonction encapsulée récursive
        def dessiner_recherche_rec(a, x, y, prof=0, chaine_longue=chaine_longue,
                                   dessiner_vide=dessiner_vide):
            if a == []:
                dessin_arbre_vide(x, y, couleur='red', parcours=True,
                                  dessiner_vide=dessiner_vide)
            else:
                # dessin de la racine de l'arbre courant
                if val == a[0]:
                    dessin_noeud(a[0], x, y, couleur=('green', 'lightgreen'),
                                 chaine_longue=chaine_longue, parcours=True)
                # dessin de la racine du sous-arbre de gauche
                elif val < a[0] and a[1] != []:
                    dessin_noeud(a[0], x, y, couleur=('green', 'lightgray'),
                             chaine_longue=chaine_longue, parcours=True)
                    xg, yg = coordonnees_fils(a, x, y, prof, h,
                                              longueur_max=lmax, gauche=True)
                    dessin_arete(a[1], x, y, xg, yg, couleur='green',
                                 parcours=True,
                                 chaine_longue=chaine_longue,
                                 dessiner_vide=dessiner_vide)
                    dessiner_recherche_rec(a[1], xg, yg, prof + 1,
                                           chaine_longue=chaine_longue,
                                           dessiner_vide=dessiner_vide)
                elif val < a[0] and a[1] == []:
                    dessin_noeud(a[0], x, y, couleur=('red', 'white'),
                             chaine_longue=chaine_longue, parcours=True)
                    xg, yg = coordonnees_fils(a, x, y, prof, h,
                                              longueur_max=lmax, gauche=True)
                    dessin_arete(a[1], x, y, xg, yg, couleur='red',
                                 parcours=True,
                                 chaine_longue=chaine_longue,
                                 dessiner_vide=dessiner_vide)
                    dessiner_recherche_rec(a[1], xg, yg, prof + 1,
                                           chaine_longue=chaine_longue,
                                           dessiner_vide=dessiner_vide)
                # dessin de la racine du sous-arbre de droite
                elif val > a[0] and a[2] != []:
                    dessin_noeud(a[0], x, y, couleur=('green', 'lightgray'),
                             chaine_longue=chaine_longue, parcours=True)
                    xd, yd = coordonnees_fils(a, x, y, prof, h,
                                              longueur_max=lmax, gauche=False)
                    dessin_arete(a[2], x, y, xd, yd, couleur='green',
                                 parcours=True,
                                 chaine_longue=chaine_longue,
                                 dessiner_vide=dessiner_vide)
                    dessiner_recherche_rec(a[2], xd, yd, prof + 1,
                                           chaine_longue=chaine_longue,
                                           dessiner_vide=dessiner_vide)
                else: # val > a[0] and a[2] == []:
                    dessin_noeud(a[0], x, y, couleur=('red', 'white'),
                             chaine_longue=chaine_longue, parcours=True)
                    xd, yd = coordonnees_fils(a, x, y, prof, h,
                                              longueur_max=lmax, gauche=False)
                    dessin_arete(a[2], x, y, xd, yd, couleur='red',
                                 parcours=True,
                                 chaine_longue=chaine_longue,
                                 dessiner_vide=dessiner_vide)
                    dessiner_recherche_rec(a[2], xd, yd, prof + 1,
                                           chaine_longue=chaine_longue,
                                           dessiner_vide=dessiner_vide)
        # appel de la fonction récursive encapsulée
        dessiner_recherche_rec(a, 0, max(h - 1, 0), chaine_longue=chaine_longue,
                               dessiner_vide=dessiner_vide)
        t.hideturtle()
        t.done()
    else: # arbre binaire classique (non de recherche)
        assert arbre_valide(a), "abre non valide !"
        dessiner(a, dessiner_vide=dessiner_vide)
        h = hauteur(a)
        lmax = longueur_max_element(a)
        if lmax >= 3:
            chaine_longue = True
        else:
            chaine_longue = False
        t.penup()
        t.goto(0, max(h - 1, 0))
        if parcours == 'largeur' and a != []:
            f = creer_file_vide()
            f_affichage = creer_file_vide()
            visites = []
            prof = 0
            x = 0
            y = max(h - 1, 0)
            print('File :', '⬅' + str(f_affichage) + '⬅',
                  '\t\tNoeuds visités :', visites)
            enfiler(f, (a, prof, x, y))
            enfiler(f_affichage, a[0])
            print('File :', '⬅' + str(f_affichage) + '⬅',
                  '\t\tNoeuds visités :', visites)
            trouvee = False
            while not file_est_vide(f) and not trouvee:
                a_courant, prof, x, y = defiler(f)
                visites.append(defiler(f_affichage))
                print('File :', '⬅' + str(f_affichage) + '⬅',
                    '\t\tNoeuds visités :', visites)
                if a_courant[0] == val:
                    couleur = ('green', 'lightgreen')
                    # dessin de la racine de l'arbre courant
                    dessin_noeud(a_courant[0], x, y, couleur=couleur,
                                chaine_longue=chaine_longue, parcours=True)
                    trouvee = True
                else:
                    couleur = ('green', 'lightgray')
                    # dessin de la racine de l'arbre courant
                    dessin_noeud(a_courant[0], x, y, couleur=couleur,
                                    chaine_longue=chaine_longue, parcours=True)
                    t.color('green', 'green')
                    t.update()
                    sleep(1)
                    #t.update()
                    # dessin des sous-arbres gauche et droit
                    couleur = ('red', 'white')
                    for i in (1, 2):
                        booleens = [True, False]
                        xf, yf = coordonnees_fils(a_courant, x, y, prof, h,
                                                longueur_max=lmax,
                                                gauche=booleens[i - 1])
                        dessin_arete(a_courant[i], x, y, xf, yf, couleur='red',
                                    parcours=True, chaine_longue=chaine_longue,
                                    dessiner_vide=dessiner_vide)
                        if a_courant[i] == []:
                            dessin_arbre_vide(xf, yf, couleur="black",
                                              parcours=True,
                                              dessiner_vide=dessiner_vide)
                        else:
                            enfiler(f, (a_courant[i], prof + 1, xf, yf))
                            enfiler(f_affichage, a_courant[i][0])
                            print('File :', '⬅' + str(f_affichage) + '⬅',
                                '\t\tNoeuds visités :', visites)
                            dessin_noeud(a_courant[i][0], xf, yf,
                                         couleur=couleur,
                                         chaine_longue=chaine_longue,
                                         parcours=True)
                        dessin_arete(a_courant[i], x, y, xf, yf,
                                     couleur='green',
                                     parcours=True, chaine_longue=chaine_longue,
                                     dessiner_vide=dessiner_vide,
                                     vers_haut=True)
        else: # parcours en profondeur
            # définition de la fonction encapsulée récursive
            def dessiner_parcours_rec(a, x, y, prof=0,
                                      chaine_longue=chaine_longue):
                if a == []:
                    dessin_arbre_vide(x, y, couleur='green',
                                    dessiner_vide=dessiner_vide)
                elif a[0] == val and parcours == 'préfixe':
                    dessin_noeud(a[0], x, y, couleur=('green', 'lightgreen'),
                                chaine_longue=chaine_longue, parcours=True)
                else:
                    if parcours == 'préfixe':
                        couleur = ('green', 'lightgray')
                    else:
                        couleur = ('red', 'white')
                    # dessin de la racine de l'arbre courant
                    dessin_noeud(a[0], x, y, couleur=couleur,
                                chaine_longue=chaine_longue, parcours=True)
                    # dessin du sous-arbre gauche
                    xg, yg = coordonnees_fils(a, x, y, prof, h,
                                              longueur_max=lmax,
                                              gauche=True)
                    dessin_arete(a[1], x, y, xg, yg, couleur='red',
                                 parcours=True,
                                 chaine_longue=chaine_longue,
                                 dessiner_vide=dessiner_vide)
                    dessiner_parcours_rec(a[1], xg, yg, prof + 1,
                                        chaine_longue=chaine_longue)
                    dessin_arete(a[1], x, y, xg, yg, couleur='green',
                                vers_haut=True, parcours=True,
                                chaine_longue=chaine_longue,
                                dessiner_vide=dessiner_vide)
                    if a[0] == val and parcours == 'infixe':
                        dessin_noeud(a[0], x, y,
                                     couleur=('green', 'lightgreen'),
                                     chaine_longue=chaine_longue, parcours=True)
                    else:
                        if parcours == 'infixe':
                            couleur = ('green', 'lightgray')
                            # dessin de la racine de l'arbre courant
                            dessin_noeud(a[0], x, y, couleur=couleur,
                                         chaine_longue=chaine_longue,
                                         parcours=True)
                        # dessin du sous-arbre droit
                        xd, yd = coordonnees_fils(a, x, y, prof, h,
                                                  longueur_max=lmax,
                                                  gauche=False)
                        dessin_arete(a[2], x, y, xd, yd, couleur='red',
                                     parcours=True,
                                     chaine_longue=chaine_longue,
                                     dessiner_vide=dessiner_vide)
                        dessiner_parcours_rec(a[2], xd, yd, prof + 1,
                                            chaine_longue=chaine_longue)
                        dessin_arete(a[2], x, y, xd, yd, couleur='green',
                                    vers_haut=True, parcours=True,
                                    chaine_longue=chaine_longue,
                                    dessiner_vide=dessiner_vide)
                        if a[0] == val and parcours == 'suffixe':
                            dessin_noeud(a[0], x, y,
                                         couleur=('green', 'lightgreen'),
                                         chaine_longue=chaine_longue,
                                         parcours=True)
                        else:
                            if parcours == 'suffixe' or parcours == 'postfixe':
                                couleur = ('green', 'lightgray')
                                # dessin de la racine de l'arbre courant
                                dessin_noeud(a[0], x, y, couleur=couleur,
                                             chaine_longue=chaine_longue,
                                             parcours=True)
            # appel de la fonction récursive encapsulée
            dessiner_parcours_rec(a, 0, max(h - 1, 0),
                                  chaine_longue=chaine_longue)
        t.hideturtle()
        t.done()