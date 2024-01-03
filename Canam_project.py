#-coding utf-8
#importation des modules 
import tkinter as tk
from tkinter import messagebox
from math import pi
import pickle as p
import os.path

#definition de class
class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Projet Canam")
        self.w,self.h=self.winfo_screenwidth(),self.winfo_screenheight()
        self.geometry(f"{self.w-450}x{self.h-150}")
        self.iconbitmap("Voiture.ico")
        
        #representation de la barre de menu
        self.MenuBar()
        self.config(menu=self.menu)
        
        #zone de dessin
        self.can=tk.Canvas(self,width=self.w-850,height=self.h-300,bg="light yellow",relief="groove")
        self.can.grid(row=0,column=0,rowspan=4,pady=5,padx=10)
        self.forme=None #forme a dessiner
        self.action=None #{draw or modify}
        
        #zone d'affichage des caracteristiques
        self.frame=tk.Canvas(self,width=310,height=self.h-600,bg="cyan")
        self.frame.grid(row=0,column=1,padx=10,pady=5,rowspan=2,columnspan=2,sticky="ne")
        self.formes={}
        
        #zone d'affichage des propriétées géometrique
        
        self.frame2=tk.Frame(self,width=310,height=self.h-550,bg="dark grey")
        self.frame2.grid(row=3,column=1,rowspan=2,columnspan=2,pady=5,padx=10,sticky="se")
        
        # association-liaison d'événements <souris>  widget :
        self.can.bind("<Button-1>", self.mouseDown)
        self.bind_all("<Control-s>",lambda event:self.Titre("save"))
        self.bind_all("<Control-o>",lambda event:self.Titre("open"))
        self.bind_all("<Return>",self.submit)

        
    def MenuBar(self):
        "Creation de la barre de Menu"
        self.menu=tk.Menu(self,font="Arial 20 bold")     
        #Menu permettant de gerer la creation des formes   
        first_menu=tk.Menu(self.menu,tearoff=0,font="Arial 12 bold")
        circle=tk.Menu(first_menu)
        circle.add_command(label="Draw",command=lambda :self.print_caracterisque("circle"))
        ellipse=tk.Menu(first_menu)
        ellipse.add_command(label="Draw",command=lambda :self.print_caracterisque("ellipse"))
        rectangle=tk.Menu(first_menu)
        rectangle.add_command(label="Draw",command=lambda :self.print_caracterisque("rectangle"))
        carre=tk.Menu(first_menu)
        carre.add_command(label="Draw",command=lambda :self.print_caracterisque("carre"))
        losange=tk.Menu(first_menu)
        losange.add_command(label="Draw",command=lambda :self.print_caracterisque("losange"))
        hexagone=tk.Menu(first_menu)
        hexagone.add_command(label="Draw",command=lambda :self.print_caracterisque("hexagone"))
        #ajout des diffetents actions 
        first_menu.add_cascade(label="Circle",menu=circle)
        first_menu.add_cascade(label="Ellipse",menu=ellipse)
        first_menu.add_cascade(label="Rectangle",menu=rectangle)
        first_menu.add_cascade(label="Carre",menu=carre)
        first_menu.add_cascade(label="Losange",menu=losange)
        first_menu.add_cascade(label="Hexagone",menu=hexagone)

        first_menu.add_separator()
        
        #menu gerant le calcul geometrie des formes 
         
        second_menu=tk.Menu(self.menu,tearoff=0,font="Arial 12 bold")
        circle1=tk.Menu(second_menu)
        circle1.add_command(label="Rayon",command=lambda :self.calcul_geometrique("circle","rayon"))
        circle1.add_command(label="Périmètre",command=lambda :self.calcul_geometrique("circle","perimetre"))
        circle1.add_command(label="Aire",command=lambda :self.calcul_geometrique("circle","aire"))
        ellipse1=tk.Menu(second_menu)
        ellipse1.add_command(label="Distances focales")
        ellipse1.add_command(label="Périmètre")
        ellipse1.add_command(label="Aire")
        rectangle1=tk.Menu(second_menu)
        rectangle1.add_command(label="Longueur - Largeur",command=lambda :self.calcul_geometrique("rectangle","dimension"))
        rectangle1.add_command(label="Périmètre",command=lambda :self.calcul_geometrique("rectangle","perimetre"))
        rectangle1.add_command(label="Aire",command=lambda :self.calcul_geometrique("rectangle","aire"))
        carre1=tk.Menu(second_menu)
        carre1.add_command(label="Coté",command=lambda :self.calcul_geometrique("carre","dimension"))
        carre1.add_command(label="Périmètre",command=lambda :self.calcul_geometrique("carre","perimetre"))
        carre1.add_command(label="Aire",command=lambda :self.calcul_geometrique("carre","aire"))
        losange1=tk.Menu(second_menu)
        losange1.add_command(label="Coté")
        losange1.add_command(label="Périmètre")
        losange1.add_command(label="Aire")
        hexagone1=tk.Menu(second_menu)
        hexagone1.add_command(label="Coté")
        hexagone1.add_command(label="Périmètre")
        hexagone1.add_command(label="Aire")
        #ajout des diffetents actions 
        second_menu.add_cascade(label="Circle",menu=circle1)
        second_menu.add_cascade(label="Ellipse",menu=ellipse1)
        second_menu.add_cascade(label="Rectangle",menu=rectangle1)
        second_menu.add_cascade(label="Carre",menu=carre1)
        second_menu.add_cascade(label="Losange",menu=losange1)
        second_menu.add_cascade(label="Hexagone",menu=hexagone1)

        second_menu.add_separator()
        
        #menu gerant la sauvegarde et l'ouverture des taches 
        third_menu=tk.Menu(self.menu,tearoff=0,font="Arial 12 bold")
        third_menu.add_command(label="Save",command=lambda : self.Titre("save"))
        third_menu.add_command(label="Open",command=lambda : self.Titre("open"))
        
        third_menu.add_separator()
        
        #association des differents sous menu  au menu principale
        self.menu.add_cascade(label="~@~")
        self.menu.add_cascade(label="Fichier",menu=third_menu)
        self.menu.add_cascade(label="Insertion",menu=first_menu)
        self.menu.add_cascade(label="Calcul géométrique",menu=second_menu)


    
    #CREATION DES FORMES
    
    def build_champ(self):
        "cree les champs et masque "
        self.selObject=None
        self.origine_label=tk.Label(self.frame,text="Point d'origine",font="Comic 12 bold",bg="cyan")
        self.origine_x_label=tk.Label(self.frame,text="Abscisse origine",font="Comic 12 bold",bg="cyan")
        self.origine_y_label=tk.Label(self.frame,text="Ordonnee origine",font="Comic 12 bold",bg="cyan")
        self.origine_x=tk.Entry(self.frame,font="Arial 12 bold")
        self.origine_y=tk.Entry(self.frame,font="Arial 12 bold")
        self.origine_label.grid(row=0,column=0,columnspan=2)
        self.origine_x_label.grid(row=1,column=0,sticky="w")
        self.origine_y_label.grid(row=2,column=0,sticky="w")
        self.origine_x.grid(row=1,column=1)
        self.origine_y.grid(row=2,column=1)
        self.couleur_label=tk.Label(self.frame,text="Couleur",font="Comic 12 bold",bg="cyan")
        self.couleur=tk.Entry(self.frame,font="Arial 12 bold")
        self.couleur_label.grid(row=4,column=0,sticky="w")
        self.couleur.grid(row=4,column=1)
        self.dimension_label=tk.Label(self.frame,text="Dimension",font="Comic 12 bold",bg="cyan")
        self.dimension_label.grid(row=3,column=0,sticky="w")
        self.dimension=tk.Entry(self.frame,font="Arial 12 bold")
        self.dimension.grid(row=3,column=1)
        self.bou=tk.Button(self.frame,text="Submit",font="Time 10 bold",bg="blue",relief="groove",bd=2,command=self.submit)
        self.bou.grid(row=5,column=1)
        
        
    def print_caracterisque(self,forme):
        self.action="draw"
        self.build_champ()
        if forme =="circle":
            self.forme = "circle"
        elif forme == "rectangle":
            self.forme="rectangle"
        elif forme == "ellipse":
            self.forme = "ellipse"
        elif forme == "carre":
            self.forme = "carre"
        elif forme == "losange":
            self.forme = "losange"
        elif forme == "hexagone":
            self.forme = "hexagone"
        
    def submit(self,event=None):
        #create_oval
        if self.forme == "circle":
            #recupertion des caracteristiques
            try :
                (x,y)=(float(self.origine_x.get()),float(self.origine_y.get()))
                r=float(self.dimension.get())
            except ValueError:
                self.dimension_error()
            else:
                color=self.couleur.get()
                #dessin de la forme
                if self.action == "draw":
                    try :
                        cercle=self.can.create_oval(x-r,y-r,x+r,y+r,fill=color)
                        #enregistremennt de la forme
                        self.formes[cercle]={"type":"circle","origine":(x,y),"dimension":r,"color":color}
                    except:
                        self.color_error()
                if self.action =="modify":
                    self.can.coords(self.selObject,x-r,y-r,x+r,y+r)
                    #mise a jour des caracteristique de la forme
                    self.formes[self.selObject[0]]={"type":"circle","origine":(x,y),"dimension":r,"color":self.can.itemconfig(self.selObject,"fill")[4]}

        elif self.forme == "ellipse":
            #recupertion des caracteristiques
            try:
                 (x,y)=(float(self.origine_x.get()),float(self.origine_y.get()))
            except ValueError:
                self.dimension_error()
            else:
                dimension=self.dimension.get().split()
                try :
                    (a,b)=(float(dimension[0]),float(dimension[1]))
                except IndexError:
                    self.dimension_ellp_error()
                except ValueError:
                    self.dimension_error()
                else :
                    color=self.couleur.get()
                    #dessin de la forme
                    if self.action == "draw":
                        try :
                            ellipse=self.can.create_oval(x-a,y-b,x+a,y+b,fill=color)
                            #enregistremennt de la forme
                            self.formes[ellipse]={"type":"ellipse","origine":(x,y),"dimension":(a,b),"color":color}
                        except:
                            self.color_error() 
                    if self.action =="modify":
                        self.can.coords(self.selObject,x-a,y-b,x+a,y+b)  
                        #mise a jour des caracteristique de la forme
                        self.formes[self.selObject[0]]={"type":"ellipse","origine":(x,y),"dimension":(a,b),"color":self.can.itemconfig(self.selObject,"fill")[4]}

        #create_rectangle
        elif self.forme == "rectangle":
            #recupertion des caracteristiques
            try :
                (x,y)=(float(self.origine_x.get()),float(self.origine_y.get()))
            except ValueError:
                self.dimension_error()
            else:
                dimension=self.dimension.get().split()
                try :
                    (L,l)=(float(dimension[0]),float(dimension[1]))
                except IndexError:
                    self.dimension_rect_error()
                except ValueError:
                    self.dimension_error()
                else :
                    color=self.couleur.get()
                    #dessin de la forme
                    if self.action == "draw":
                        try :
                            rectangle=self.can.create_rectangle(x-L/2,y-l/2,x+L/2,y+l/2,fill=color)
                            #enregistremennt de la forme
                            self.formes[rectangle]={"type":"rectangle","origine":(x,y),"dimension":(L,l),"color":color}
                        except:
                            self.color_error()
                    if self.action =="modify":
                        self.can.coords(self.selObject,x-L/2,y-l/2,x+L/2,y+l/2)
                        #mise a jour des caracteristique de la forme
                        self.formes[self.selObject[0]]={"type":"rectangle","origine":(x,y),"dimension":(L,l),"color":self.can.itemconfig(self.selObject,"fill")[4]}

        elif self.forme == "carre":
            #recuperation des caracteristiques
            try :
                (x,y)=(float(self.origine_x.get()),float(self.origine_y.get()))
                c=float(self.dimension.get())
            except ValueError:
                self.dimension_error()
            else :
                    color=self.couleur.get()
                    #dessin de la forme
                    if self.action == "draw":
                        try :
                            carre=self.can.create_rectangle(x-c/2,y-c/2,x+c/2,y+c/2,fill=color)
                            #enregistremennt de la forme
                            self.formes[carre]={"type":"carre","origine":(x,y),"dimension":c,"color":color}
                        except:
                            self.color_error()
                    if self.action =="modify":
                        self.can.coords(self.selObject,x-c/2,y-c/2,x+c/2,y+c/2)
                        #mise a jour des caracteristique de la forme
                        self.formes[self.selObject[0]]={"type":"carre","origine":(x,y),"dimension":c,"color":self.can.itemconfig(self.selObject,"fill")[4]}

        #create_polygone
        elif self.forme == "losange":
            #recupertion des caracteristiques
            try:
                 (x,y)=(float(self.origine_x.get()),float(self.origine_y.get()))
            except ValueError:
                self.dimension_error()
            else:
                dimension=self.dimension.get().split()
                try :
                    (w,h)=(float(dimension[0]),float(dimension[1]))
                except IndexError:
                    self.dimension_los_error()
                except ValueError:
                    self.dimension_error()
                else :
                    color=self.couleur.get()
                    #dessin de la forme
                    if self.action == "draw":
                        try :
                            losange=self.can.create_polygon(x,y+h/2,x+w/2,y,x+w,y+h,fill=color)
                            #enregistremennt de la forme
                            self.formes[losange]={"type":"losange","origine":(x,y),"dimension":(w,h),"color":color}
                        except:
                            self.color_error() 
                    if self.action =="modify":
                        self.can.coords(self.selObject,x,y+h/2,x+w/2,y,x+w,y+h)  
                        #mise a jour des caracteristique de la forme
                        self.formes[self.selObject[0]]={"type":"losange","origine":(x,y),"dimension":(w,h),"color":self.can.itemconfig(self.selObject,"fill")[4] }
                
        elif self.forme == "hexagone":
                #recupertion des caracteristiques
            try :
                (x,y)=(float(self.origine_x.get()),float(self.origine_y.get()))
                h=float(self.dimension.get())
            except ValueError:
                self.dimension_error()
            else :
                    color=self.couleur.get()
                    #dessin de la forme
                    if self.action == "draw":
                        try :
                            hexagone=self.can.create_polygon(x,y+h*0.866,x+h,y+h*0.866,x+h*1.5,y,x+h,y-h*0.866,x,y-h*0.866,x-h/2,y,fill=color)
                            #enregistremennt de la forme
                            self.formes[hexagone]={"type":"hexagone","origine":(x,y),"dimension":h,"color":color}
                        except:
                            self.color_error()
                    if self.action =="modify":
                        self.can.coords(self.selObject,x,y+h*0.866,x+h,y+h*0.866,x+h*1.5,y,x+h,y-h*0.866,x,y-h*0.866,x-h/2,y)
                        #mise a jour des caracteristique  de la forme
                        self.formes[self.selObject[0]]={"type":"hexagone","origine":(x,y),"dimension":h,"color":self.can.itemconfig(self.selObject,"fill")[4]}
                
        if self.selObject :
              self.can.itemconfig(self.selObject, outline="black",width =1) #deselectionne l'ancienne forme
        self.action="draw"
    
    def dimension_rect_error(self):
        "Fonction permettant d'envoyer une erreur lorsque les dimensions ne sont pas bien entrées"
        messagebox.showwarning("ERREUR","ENTRER LA LONGUEUR SUIVIE DE \n LA LARGEUR SEPARRE PAR L'ESPACE!!")   
    
    def dimension_ellp_error(self):
        "Fonction permettant d'envoyer une erreur lorsque les dimensions ne sont pas bien entrées"
        messagebox.showwarning("ERREUR","ENTRER LA DISTANCE FOCAL SUIVANT LES X SUIVIE DE \n LA DISTANCE FOCAL SUIVANT LES Y SEPARRE PAR L'ESPACE !! ")  
    
    def dimension_los_error(self):
        "Fonction permettant d'envoyer une erreur lorsque les dimensions ne sont pas bien entrées"
        messagebox.showwarning("ERREUR","ENTRER LA LONGUEUR SUIVIE DE \n LA LARGEUR SEPARRE PAR L'ESPACE!!")   
        
    def dimension_error(self):
        "Fonction qui renvoie une erreur lorsque les dimensions entrées ne sont pas les nombres"
        messagebox.showerror("ERREUR","LES DIMENSIONS DOIVENT ETRE DES NOMBRES")
    
    def color_error(self):
        "Fonction qui renvoie une erreur lorsque la couleur entrer n'existe pas"
        messagebox.showerror("ERREUR","LA COULEUR DOIT ETRE EN ANGLAIS ET DOIT ETRE VALIDE!!")
        
    
    # EDITION DE LA FORME
    
    def mouseDown(self, event):
        "Opération à effectuer quand le bouton gauche de la souris est enfoncé"
        if self.selObject :
              self.can.itemconfig(self.selObject, outline="black",width =1) #deselectionne l'ancienne forme
              
        # event.x et event.y contiennent les coordonnées du clic effectué :
        self.x1, self.y1 = event.x, event.y
        # <find_closest> renvoie la référence du dessin le plus proche :
        self.selObject = self.can.find_closest(self.x1, self.y1)
        # modification de l'épaisseur du contour du dessin :
        if self.selObject:
            self.can.itemconfig(self.selObject,outline="blue",width =3)
            # <lift> fait passer le dessin à l'avant-plan :
            self.can.lift(self.selObject)
            self.action="modify"
            self.forme=self.formes[self.selObject[0]]["type"]
            tk.Label(self.frame2,text=str(self.formes[self.selObject[0]])).pack()
            # self.build_champ()
        
           
    #CALCUL GEOMETRIQUE
    def calcul_geometrique(self,forme,caract):
        objet=self.formes[self.selObject[0]]
        
        if forme=="circle":
            if objet["type"]=="circle":
                R=objet["dimension"]
            try:
                perimetre=2*pi*R
                aire=pi*R**2
            except UnboundLocalError:
                self.forme_error()
            if caract =="rayon":
                tk.Label(self.frame2,text=f"Le Rayon  du cercle selectionné est :\n     {R}",font="Time 14 bold").pack()
            elif caract =="perimetre":
                tk.Label(self.frame2,text=f"Le Périmètre  du cercle selectionné est :\n     {perimetre}",font="Time 14 bold").pack()
            elif caract =="aire":
                tk.Label(self.frame2,text=f"L'aire  du cercle selectionné est :\n     {aire}",font="Time 14 bold").pack()
        elif forme=="rectangle":
            if objet["type"]=="rectangle":
                (L,l)=(objet["dimension"][0],objet["dimension"][1])
            try:
                perimetre=L+l
                aire=L*l
            except UnboundLocalError:
                self.forme_error()
            if caract =="dimension":
                tk.Label(self.frame2,text=f"La Longueur  du rectangle selectionné est {L}\n Et la Largeur est {l}",font="Time 14 bold").pack()
            elif caract =="perimetre":
                tk.Label(self.frame2,text=f"Le Périmètre du rectangle selectionné est :\n     {perimetre}",font="Time 14 bold").pack()
            elif caract =="aire":
                tk.Label(self.frame2,text=f"L'aire du rectangle selectionné est :\n     {aire}",font="Time 14 bold").pack()
        elif forme=="carre":
            if objet["type"]=="carre":
                c=objet["dimension"]
            try:
                perimetre=4*c
                aire=c*c
            except UnboundLocalError:
                self.forme_error()
            if caract =="cote":
                tk.Label(self.frame2,text=f"Le Coté du carre selectionné est :\n     {c}",font="Time 14 bold").pack()
            elif caract =="perimetre":
                tk.Label(self.frame2,text=f"Le Périmètre  du carre selectionné est :\n     {perimetre}",font="Time 14 bold").pack()
            elif caract =="aire":
                tk.Label(self.frame2,text=f"L'aire  du carre selectionné est :\n     {aire}",font="Time 14 bold").pack()
            
    def forme_error(self):
        "Fonction qui renvoie une erreur lorsque l'utilisateur demande les calcul geometrique d'une forme non selectionne"
        messagebox.showwarning("ERREUR","VERIFIER LA FORME SELECTIONNER ET RESSAYER!!!")
        
    # STOCKAGE DES DONNEES
    def Titre(self,action):
        "Fonction permettant de recuperer le nom du fichier pour le stockage  du travail ou l'ouverture d'un travail"
        self.titre=tk.Toplevel(self,width=100,height=50,relief="groove")
        self.label=tk.Label(self.titre,text="Nom de fichier : ")
        self.entry=tk.Entry(self.titre,font="Arial 12 italic bold")
        self.label.pack(side="left")
        self.entry.pack(side="left")
        
        if action=="save":
            self.titre.bind("<Return>",self.save)
        elif action=="open":
            self.titre.bind("<Return>",self.open)

        
    def save(self,event):   
        "Fonction permettant de gerer la sauvegarde du travail dans un fichier binaire"
        #recuperation du nom de fichier
        name=self.entry.get()
        self.titre.destroy()
        
        #masque les champs liés a la récupération du nom fichier
        self.label.pack_forget()
        self.entry.pack_forget()
        
        #enregistrement
        if  os.path.exists(name+".txt"): #si un fichier portant le meme nom existe deja , on demande s'il faut remplacer le contenu
            if messagebox.askyesno("Verification","UN FICHIER AYANT CE NOM EXISTE DEJA!!!\n VOULEZ-VOUS REMPLACER LE CONTENU??"): #si l'utilisateur dire oui
                with open(name+".txt","wb") as file:
                    mon_pickle=p.Pickler(file)
                    mon_pickle.dump(self.formes)
            else:
                self.Titre("save")
                
        else:
            with open(name+".txt","wb") as file:
                    mon_pickle=p.Pickler(file)
                    mon_pickle.dump(self.formes)
        
    def open(self,event):
        "Fonction permettant de gerer l'ouverture des fichiers"
        self.build_champ()
        self.couleur_label.grid_forget()
        self.couleur.grid_forget()
        #recuperation du nom de fichier
        name=self.entry.get()
        self.titre.destroy()
        
        #masque les champs liés a la récupération du nom fichier
        self.label.pack_forget()
        self.entry.pack_forget()
        
        #ouverture
        self.formes={}
        try :
            with open(name+".txt","rb") as file:
                mon_depickle=p.Unpickler(file)
                self.formes=mon_depickle.load()
        except FileNotFoundError:
            self.FileNotFoundError()
        else:
            self.can.delete(all)
            self.restitution()
            
    def restitution(self):
        "charge sur l'ecran le fichier ouvert"

        for key in self.formes.keys():
            (x,y)=self.formes[key]["origine"]
            color=self.formes[key]["color"]
            #create_oval
            if self.formes[key]["type"] == "circle":
                r=self.formes[key]["dimension"]
                self.can.create_oval(x-r,y-r,x+r,y+r,fill=color)
            elif self.formes[key]["type"] == "ellipse":
                (a,b)=self.formes[key]["dimension"]
                ellipse=self.can.create_oval(x-a,y-b,x+a,y+b,fill=color)
            #create_rectangle
            elif self.formes[key]["type"] == "rectangle":
                (L,l)=self.formes[key]["dimension"]
                self.can.create_rectangle(x-L/2,y-l/2,x+L/2,y+l/2,fill=color)
               
            elif self.formes[key]["type"] == "carre":
                c=self.formes[key]["dimension"]
                self.can.create_rectangle(x-c/2,y-c/2,x+c/2,y+c/2,fill=color)
              
            #create_polygone
            elif self.formes[key]["type"] == "losange":
                (w,h)=self.formes[key]["dimension"]
                self.can.create_polygon(x,y+h/2,x+w/2,y,x+w,y+h,fill=color)
                
            elif self.formes[key]["type"] == "hexagone":
                h=self.formes[key]["dimension"]
                self.can.create_polygon(x,y+h*0.866,x+h,y+h*0.866,x+h*1.5,y,x+h,y-h*0.866,x,y-h*0.866,x-h/2,y,fill=color)
            
        
    def FileNotFoundError(self):
        "Fonction qui renvoie une erreur lorsque le fichier que l'utilisateur demande à ouvrir n'existe pas "  
        messagebox.showerror("ERREUR","CE FICHIER N'EXISTE PAS")
        
 
#programme principal
if __name__=="__main__":
    myapp=App()
    myapp.mainloop()