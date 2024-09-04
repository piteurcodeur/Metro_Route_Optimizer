                    #---------------------auteur : piteurcodeur ---------------------------#

from tkinter import ttk
import tkinter as tk
from PIL import ImageTk, Image
import os
import difflib
import datetime

dico_ville_name = {
    'Paris': '',
    'Lyon': '',
    'Bordeaux': '',
    'Lille': ''
}

couleur_ligne_Paris = {
    'ligne1': 'yellow',
    'ligne2': 'blue',
    'ligne3': '#837902',
    'ligne3bis': '#6EC4E8',
    'ligne4': 'deeppink',
    'ligne5': '#e67905',
    'ligne6': '#6ECA97',
    'ligne7': '#FA9ABA',
    'ligne7b': '#FA9ABA',
    'ligne7bis': '#30f291',
    'ligne8': '#E11484',
    'ligne9': '#B4D43E',
    'ligne10': '#C9910D',
    'ligne11': '#704B1C',
    'ligne12': '#007852',
    'ligne13': '#6ECA97',
    'ligne13b': '#6ECA97',
    'ligne14': '#62259D',
    'ligneT1': '#1239ff',
    'ligneT2': '#ff1289',
    'ligneT3a': '#ff7a12',
    'ligneT3b': '#1b6b1a',
    'ligneT4': '#e1de15',
    'ligneT4b': '#e1de15',
    'ligneT5': '#5b305d',
    'ligneT6': '#ff0000',
    'ligneT7': '#5d320f',
    'ligneT8': '#9e8e31',
    'ligneT9': '#57a1e2'

}

couleur_ligne_Lille = {

    'ligne1': '#F05F40',
    'ligne2': '#0073A8',
    'ligneR': '#009246',
    'ligneT': '#E30613'
}
couleur_ligne_Lyon = {
    'ligneA': 'red',
    'ligneB': 'blue',
    'ligneC': 'yellow',
    'ligneD': 'green',
    'T1': '#3a75f3',
    'T2': '#0aa025',
    'T3': '#00f3e0',
    'T4': '#810976',
}

couleur_ligne_Bordeaux = {
    'ligneA': '#581845',
    'ligneAb': '#581845',
    'ligneB': 'red',
    'ligneBb': 'red',
    'ligneC': '#e564c5',
    'ligneCb': '#e564c5',
    'ligneD': '#85529e',
}

###


class MasterGraphe():
    def __init__(self, Ville):
        self.folder_path = str(correction(Ville, dico_ville_name))
        self.Ville = self.folder_path
        self.textes = []
        for filename in os.listdir(self.folder_path):
            if filename.endswith('.txt'):
                self.textes.append(self.folder_path+'/'+filename)
        self.graphe = {}
        self.lignes = {}
        self.correspondances = []
        self.trajet_corr = []
        self.liste_corr = []

    def createGraphe(self):
        for texte in self.textes:
            with open(texte, 'r', encoding='utf-8') as file:
                contenu = []  # contenu du fichier liste des stations
                for ligne in file:
                    curr_cont = ligne.strip().replace("’", " ")  # contenu de la ligne
                    contenu.append(curr_cont)

            texte = texte.split("/")[-1].split(".")[0]
            self.lignes[texte] = []
            # print(texte)
            # nbre de stations du fichier
            for indice_station in range(len(contenu)):

                self.lignes[texte].append(
                    contenu[indice_station][:-1] if contenu[indice_station][-1] == '&' else contenu[indice_station])

                prec = ''
                suiv = ''

                # Créer prec et suiv
                if indice_station != 0 and contenu[indice_station][-1] != '&':
                    prec = contenu[indice_station - 1][:-1] if contenu[indice_station -
                                                                       1][-1] == '&' else contenu[indice_station - 1]

                if indice_station != len(contenu)-1:
                    suiv = contenu[indice_station + 1][:-1] if contenu[indice_station +
                                                                       1][-1] == '&' else contenu[indice_station + 1]

                signe = contenu[indice_station][-1]
                curr_station = contenu[indice_station][:-
                                                       1] if '&' in contenu[indice_station] else contenu[indice_station]
                #print(prec, suiv)
                # Attribuer prec et suiv en fonction si le signe est a sens unique
                if signe == '&':
                    if curr_station in self.graphe:
                        if not(prec in self.graphe[curr_station][0]):
                            self.graphe[curr_station][0].append(prec)
                        if not(prec in self.graphe[curr_station][1]):
                            self.graphe[curr_station][1].append(suiv)

                    else:

                        self.graphe[curr_station] = [[prec], [suiv]]
                        if not(curr_station in self.correspondances):
                            self.correspondances.append(curr_station)
                else:
                    if curr_station in self.graphe:
                        if not(prec in self.graphe[curr_station][0]):
                            self.graphe[curr_station][0].append(prec)
                        if not(suiv in self.graphe[curr_station][0]):
                            self.graphe[curr_station][0].append(suiv)

                        if not(suiv in self.graphe[curr_station][1]):
                            self.graphe[curr_station][1].append(suiv)
                        if not(prec in self.graphe[curr_station][1]):
                            self.graphe[curr_station][1].append(prec)

                    else:

                        self.graphe[curr_station] = [
                            [prec, suiv], [suiv, prec]]
                        if not(curr_station in self.correspondances):
                            self.correspondances.append(curr_station)

                self.graphe[curr_station] = [[element for element in self.graphe[curr_station][0] if element != ''], [
                    element for element in self.graphe[curr_station][1] if element != '']]

    def chemin(self, graphe, start, end):
        chemin = {start: 0}
        visited = []
        queue = [(start, 0)]
        last_ligne = ''

        correspondance = None

        while queue != []:

            noeud, distance = queue.pop(0)

            if noeud == end:
                visited.append(noeud)

                return distance, visited, chemin
            if noeud in visited:
                continue
            visited.append(noeud)

            for liste_voisin in graphe[noeud]:
                for voisin in liste_voisin:
                    if voisin == []:
                        continue
                    if voisin not in visited:
                        distance, last_ligne, correspondance = self.isCorrespondance(
                            distance, noeud, voisin, last_ligne)
                        if correspondance == True and not((noeud, last_ligne) in self.liste_corr):

                            self.liste_corr.append((noeud, last_ligne))
                        queue.append((voisin, distance + 1))
                        if voisin not in chemin or chemin[voisin] > distance + 1:
                            chemin[voisin] = distance + 1

            last = noeud

        return -1, visited, chemin

    def isCorrespondance(self, distance, noeud, voisin, last_ligne):
        correspondance = False
        voisin_lignes = []  # liste des lignes contenant la station voisine
        noeud_lignes = []  # liste des lignes contenant le noeud actuel

        # recherche des lignes contenant la station voisine
        for ligne, stations in self.lignes.items():
            if voisin in stations:
                voisin_lignes.append(ligne)

        # recherche des lignes contenant le noeud actuel
        for ligne, stations in self.lignes.items():
            if noeud in stations:
                noeud_lignes.append(ligne)

        # si les deux stations sont sur la même ligne pas de correspondance
        if last_ligne == '':
            last_ligne = list(set(voisin_lignes) & set(noeud_lignes))[0]
        if not(last_ligne in voisin_lignes):
            correspondance = True
            distance += 1
            last_ligne = list(set(voisin_lignes) & set(noeud_lignes))[0]

        return distance, last_ligne, correspondance

    def find_itineraire(self, distance, visited, dic, end):
        last = end
        itineraire = [last]
        if distance != -1:
            for indice in range(distance-1, -1, -1):
                for cle in dic.keys():
                    if indice == dic[cle] and last in self.graphe[cle][1]:
                        itineraire.append(cle)
                        last = cle

                        break

            itineraire.reverse()

        # retrouver les changements de ligne
        self.liste_corr = [elem for elem in self.liste_corr if any(
            e in elem for e in itineraire)]

        last = ''
        file = []
        for i in range(0, len(itineraire)):
            if i < (len(itineraire)-1):
                L1 = [x for x in self.lignes.keys() if itineraire[i]
                      in self.lignes[x]]
                L2 = [x for x in self.lignes.keys() if itineraire[i+1]
                      in self.lignes[x]]
                if last == '':

                    Flast = list(set(L1) & set(L2))

                    if len(Flast) > 1:
                        for k in Flast:
                            if self.lignes[k].index(itineraire[i]) == (self.lignes[k].index(itineraire[i+1])+1) or self.lignes[k].index(itineraire[i]) == (self.lignes[k].index(itineraire[i+1])-1):
                                last = k
                    else:
                        last = str(Flast[0])

                    if i-1 > 0:
                        file.append([last, itineraire[i-1]])
                    else:
                        file.append([last, itineraire[i]])
                if last != '':
                    if not(last in list(set(L1) & set(L2))):
                        last = ''
            else:

                L1 = [x for x in self.lignes.keys() if itineraire[i]
                      in self.lignes[x]]
                L2 = [x for x in self.lignes.keys() if itineraire[i-1]
                      in self.lignes[x]]

                if last == '':

                    Flast = list(set(L1) & set(L2))

                    if len(Flast) > 1:
                        for k in Flast:
                            if self.lignes[k].index(itineraire[i]) == (self.lignes[k].index(itineraire[i-1])+1) or self.lignes[k].index(itineraire[i]) == (self.lignes[k].index(itineraire[i-1])-1):
                                last = k
                    else:
                        last = str(Flast[0])

                    if i-1 > 0:
                        file.append([last, itineraire[i-1]])
                    else:
                        file.append([last, itineraire[i]])
                if last != '':
                    if not(last in list(set(L1) & set(L2))):
                        last = ''

         # ligne + station ou l'on change
        return itineraire, file


def correction(cle, dictionnaire):
    if cle in dictionnaire:
        return str(cle)
    else:
        choix = difflib.get_close_matches(cle, dictionnaire.keys(), n=1)
        if choix:
            return str(choix[0])
        else:
            print("Aucune clé similaire trouvée")


# PARTIE 2 DU GUI
Ville, start, end = '', '', ''


def get_text():
    global Ville
    global start
    global end
    Ville = zone_ville.get()
    start = zone_start.get()
    end = zone_end.get()

    if Ville == '' or start == '' or end == '':
        infos.config(text="Saisie invalide", font=(
            "Helvetica", 10, 'bold'), wraplength=70)

    else:
        remove_focus()
        root.destroy()


def on_key_press(event):
    if event.keysym == 'Return':
        bouton.config(bg='blue', fg='white')
        get_text()


def on_key_release(event):
    if event.keysym == 'Return':
        bouton.config(bg='grey', fg='black')


def on_enter(e):
    bouton.config(bg='blue', fg='white')


def on_leave(e):
    bouton.config(bg='grey', fg='black')


def remove_focus(event=None):
    root.focus_set()


# Créer une fenêtre
root = tk.Tk()

# Récupérer la largeur et la hauteur de l'écran
largeur_ecran = root.winfo_screenwidth()
hauteur_ecran = root.winfo_screenheight()

# Calculer la position de la fenêtre pour qu'elle soit centrée sur l'écran
x_pos = (largeur_ecran - 400) // 2
y_pos = (hauteur_ecran - 400) // 2

root.geometry(f"400x400+{x_pos}+{y_pos}")
root.title("APP3 : MAP")

# charger image du rond case départ
rondBleu = Image.open(
    'Rond_bleu.png')
n_rondBleu = rondBleu.resize((10, 10))
imageBleu = ImageTk.PhotoImage(n_rondBleu)
# charger image arrivé icone
iconeArrivee = Image.open(
    'iconeArrivee.png')
n_iconeArrivee = iconeArrivee.resize((30, 30))
imageArrivee = ImageTk.PhotoImage(n_iconeArrivee)
# charger image fleches inversion
iconeFleche = Image.open(
    'verticalArrow.png')
n_iconeFleche = iconeFleche.resize((30, 30))
imageFleche = ImageTk.PhotoImage(n_iconeFleche)


label = tk.Label(root, text="Saisir votre itinéraire",
                 font=("Helvetica", 10), wraplength=200)
zone_ville = tk.Entry(root, bd=0, highlightbackground='black',
                      highlightcolor='black', highlightthickness=2, width=30)
zone_start = tk.Entry(root, bd=0, highlightbackground='black',
                      highlightcolor='black', highlightthickness=2, width=30)
zone_end = tk.Entry(root, bd=0, highlightbackground='black',
                    highlightcolor='black', highlightthickness=2, width=30)
bouton = tk.Button(text="🔍 rechercher", font=("Helvetica", 10, 'bold'),
                   command=get_text, highlightbackground='blue', highlightcolor='blue', bg='grey')
pointilles = tk.Label(root, text='...', wraplength=1)
inversion = tk.Label(root, image=imageFleche)
Label_ville = tk.Label(root, text='Ville')
Fimage1 = tk.Label(root, image=imageBleu, width=10)
Fimage2 = tk.Label(root, image=imageArrivee, width=10)
infos = tk.Label(root, text='')

label.grid(row=1,  column=2, padx=10, pady=10)

Label_ville.grid(row=2,  column=1, padx=10, pady=10)
zone_ville.grid(row=2,  column=2, padx=30, pady=10)

Fimage1.grid(row=3,  column=1, padx=10, pady=10)
zone_start.grid(row=3,  column=2, padx=30, pady=10)

pointilles.grid(row=4,  column=1)
inversion.grid(row=4,  column=3)

Fimage2.grid(row=5,  column=1, padx=10, pady=10)
zone_end.grid(row=5,  column=2, padx=30, pady=10)

bouton.grid(row=6,  column=2, padx=30, pady=10)

infos.grid(row=7,  column=2, padx=30, pady=0)


zone_end.bind('<KeyPress>', on_key_press)
zone_end.bind('<KeyRelease>', on_key_release)
bouton.bind('<Enter>', on_enter)
bouton.bind('<Leave>', on_leave)
bouton.bind('<Button-1>', remove_focus)
zone_ville.bind('<Return>', lambda event: zone_start.focus_set())
zone_start.bind('<Return>', lambda event: zone_end.focus_set())

# Lancer la boucle principale de la fenêtre
root.mainloop()


# BOUCLE DE PROGRAMME


Main = MasterGraphe(Ville)
Main.createGraphe()

start = str(correction(start, Main.graphe))
end = str(correction(end, Main.graphe))
distance, visited, dic = Main.chemin(Main.graphe, start, end)

itineraire, file = Main.find_itineraire(distance, visited, dic, end)

###


def get_key(dictionnaire, valeur):
    for cle, val in dictionnaire.items():
        if val == valeur:
            return cle
    return None


def get_heure(heure, minute):
    if int(minute) >= 60:
        heure = int(heure)+1
        minute = minute - 60

    if int(minute) == 0:
        minute = '00'
    if 0 < int(minute) < 10:
        minute = f'0{minute}'
    return heure, minute


# DEBUT GUI
root = tk.Tk()
root.title('APP3 : Map : ITINERAIRE')
# Récupérer la largeur et la hauteur de l'écran
largeur_ecran = root.winfo_screenwidth()
hauteur_ecran = root.winfo_screenheight()

# Calculer la position de la fenêtre pour qu'elle soit centrée sur l'écran
x_pos = (largeur_ecran - 400) // 2
y_pos = (hauteur_ecran-800) // 2

# MAIN ROOT
root.geometry(f"500x700+{x_pos}+{y_pos}")

# creer fenetre principale
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=1)

# creer un canvas
my_canvas = tk.Canvas(main_frame)
my_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

# ajouter une barre de defilement au canvas
my_scrollbar = ttk.Scrollbar(
    main_frame, orient=tk.VERTICAL, command=my_canvas.yview)
my_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


my_canvas.configure(yscrollcommand=my_scrollbar.set)
my_canvas.bind('<Configure>', lambda e: my_canvas.configure(
    scrollregion=my_canvas.bbox("all")))

# ajouter une frame au canvas
first_frame = tk.Frame(my_canvas)
first_frame.pack()
# ajout elts sur la frame
label_titre = tk.Label(first_frame, text=f'Votre trajet {itineraire[0]} - {itineraire[-1]}    {len(itineraire)+(len(file))*2-3} min', font=(
    "Arial", 15)).grid(row=0, column=0, padx=40, pady=40)

# ajout seconde frame
second_frame = tk.Frame(my_canvas)
second_frame.pack(side=tk.LEFT)
# ajout troisième frame
third_frame = tk.Frame(my_canvas)
third_frame.pack(side=tk.RIGHT)

# position de placement des frames sur le canvas
my_canvas.create_window((0, 0), window=first_frame, anchor="nw")
my_canvas.create_window((0, 100), window=second_frame, anchor="nw")
my_canvas.create_window((400, 100), window=third_frame, anchor="nw")


heure_actuelle = datetime.datetime.now()
# extraire les heures et les minutes
heure = heure_actuelle.strftime("%H")
minute = heure_actuelle.strftime("%M")
x1 = 200
y1 = 110  # 10
y2 = 140  # 40
rang = 1

c = False
for i in itineraire: #itere dans les stations de l'itineraire
    c = False
    for j in file: #itere dans les stations de changements
        if i in j:
            #print(j[0].split("_")[1])
            if Main.Ville == 'Paris':
                couleur = couleur_ligne_Paris[j[0].split("_")[1]]
                dico_de_couleur = couleur_ligne_Paris
                c = True
            if Main.Ville == 'Lille':
                couleur = couleur_ligne_Lille[j[0].split("_")[1]]
                dico_de_couleur = couleur_ligne_Lille
                c = True
            if Main.Ville == 'Bordeaux':
                couleur = couleur_ligne_Bordeaux[j[0].split("_")[1]]
                dico_de_couleur = couleur_ligne_Bordeaux
                c = True
            if Main.Ville == 'Lyon':
                couleur = couleur_ligne_Lyon[j[0].split("_")[1]]
                dico_de_couleur = couleur_ligne_Lyon
                c = True
    
    if c == True:

        my_canvas.create_line(x1, y1, x1, y2, fill=couleur, width=20)
        my_canvas.create_oval(x1-20, y1, x1+20, y1+40, fill=couleur, outline='black', width=3)
        my_canvas.create_text(x1, y1+20, text=get_key(dico_de_couleur, couleur).split("e")[1], fill='white', font=('Arial', 15))
        if i == itineraire[0]:
            minute = int(minute)+1
            heure, minute = get_heure(heure, minute)
            my_label_infos_heure = tk.Label(
                third_frame, text=f'{heure}:{minute}').grid(row=rang, column=1)
        else:
            minute = int(minute)+3
            heure, minute = get_heure(heure, minute)
            my_label_infos_heure = tk.Label(
                third_frame, text=f'{heure}:{minute}').grid(row=rang, column=1)
    if c == False:
        my_canvas.create_line(x1, y1, x1, y2, fill=couleur, width=20)

        if i == itineraire[-1]:
            my_canvas.create_oval(x1-20, y1, x1+20, y1+40,
                                  fill=couleur, outline='black', width=3)
            minute = int(minute)+1
            heure, minute = get_heure(heure, minute)
            my_label_infos_heure = tk.Label(
                third_frame, text=f'{heure}:{minute}').grid(row=rang, column=1)
        minute = int(minute)+1
        heure, minute = get_heure(heure, minute)
        my_canvas.create_oval(x1-7, y1-7+20, x1+7, y1+7+20,
                              fill='white', outline=couleur)

    my_label_station = tk.Label(second_frame, text=i).grid(row=rang, column=2)

    second_frame.grid_rowconfigure(rang, minsize=40)
    third_frame.grid_rowconfigure(rang, minsize=40)
    y1 = y2
    y2 += 40
    rang += 1


root.mainloop()
