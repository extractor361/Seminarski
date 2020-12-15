from tkinter import *
import random
from datetime import datetime
from tkinter import ttk
import tkinter.messagebox
from datetime import timedelta
from PIL import ImageTk, Image
import sqlite3
from ttkthemes import themed_tk as tk
from operator import itemgetter
import re
import os


class Biblioteka:
    def __init__(self, root):
        self.root=root
        self.root.title("Gradska Biblioteka")
        self.root.geometry("1600x900")
        self.root.iconbitmap('@/root/Biblioteka/favicon.xbm')

        GlavniFrejm=Frame(self.root)
        GlavniFrejm.grid()
        self.image = Image.open("knjiga3.png")
        self.image = self.image.resize((150, 60), Image.ANTIALIAS)
        self.pic = ImageTk.PhotoImage(self.image)


        self.Slika_Dekor = Image.open("dekor1.png")
        self.Slika_Dekor=self.Slika_Dekor.resize((650, 85), Image.ANTIALIAS)
        self.Slidza = ImageTk.PhotoImage(self.Slika_Dekor)

        Broj_Rf=IntVar()
        Ime=StringVar()
        Prezime=StringVar()
        Pol=StringVar()
        Adresa=StringVar()
        Kontakt=StringVar()
        Clan_Od=StringVar()
        Knjiga_Rf=IntVar()
        Naziv_Knjige=StringVar()
        Autor_Knjige=StringVar()
        Datum_Uzimanja=StringVar()
        Vratiti_Do=StringVar()
        Dani_Pozajmice=StringVar()
        Kolicina=StringVar()
        Trazena_Knjiga=StringVar()
        Trazeni_Clan=StringVar()
        Pretrazi_Pomocu_Knjige=StringVar()
        Pretrazi_Pomocu_Clanovi=StringVar()
        Trazeni_Podatak=StringVar()


        TitlFrejm=Frame(GlavniFrejm,width=1600,bd=10,relief=RIDGE,bg='#9c3d02')
        TitlFrejm.pack(side=TOP, fill=X)

        self.Slika=Label(TitlFrejm,image=self.pic,bg ="#9c3d02")
        self.Slika.place(x=150,y=0,)
        self.Slika.image=self.pic
        self.Slikaa = Label(TitlFrejm, image=self.pic, bg="#9c3d02")
        self.Slikaa.place(x=1282, y=0, )


        self.Titl=Label(TitlFrejm,font=("arial",40,"bold"),text="Gradska Biblioteka-Baza Podataka",bg="#9c3d02",fg="white")
        self.Titl.pack(side=TOP)

        PodaciFrejm=Frame(GlavniFrejm,bd=13,width=1600,height=465,padx=20,relief=RIDGE, bg="#ffc5a1")
        PodaciFrejm.pack(side=BOTTOM,fill="x")

        PodaciFrejmLijevi=LabelFrame(PodaciFrejm,bd=3,padx=20,pady=20,relief=RIDGE, font=("arial",17,"bold"), text="Biblioteka-Unos u Glavnu Bazu Podataka",bg="#ffc5a1")
        PodaciFrejmLijevi.place(x=0,y=0,width=750,height=369)

        self.Za_Dekor=Label(PodaciFrejmLijevi,image=self.Slidza, bg="#ffc5a1")
        self.Za_Dekor.place(x=25,y=239)
        self.Za_Dekor.image=self.Slidza


        PodaciFrejmDesni=LabelFrame(PodaciFrejm,bd=3,relief=RIDGE, font=("arial",17,"bold"),width=780,height=350, text="               Dostupne knjige                              Registrovani Članovi                ",bg="#ffc5a1")
        PodaciFrejmDesni.place(x=770,y=0,width=780,height=369,)

        DetaljFrejm = Frame(GlavniFrejm, bd=13, padx=20, width=1600, height=280, bg="white")
        DetaljFrejm.pack()

        DugmadFrejm = Frame(PodaciFrejm, bd=3,padx=2, relief=RIDGE,bg="#ffc5a1")
        DugmadFrejm.place(y=363,height=75,width=750)

        DugmadFrejm1 = Frame(PodaciFrejm, bd=3, padx=20, relief=RIDGE,bg="#ffc5a1")
        DugmadFrejm1.place(y=363,x=770 ,height=75, width=390)

        DugmadFrejm2 = Frame(PodaciFrejm, bd=3, padx=20, relief=RIDGE,bg="#ffc5a1")
        DugmadFrejm2.place(y=363,x=1160, height=75, width=390)

        #Funkcije dugmadi

        def izadji():
            p=tkinter.messagebox.askyesno("Izlaz","Da li stvarno zelite da napustite program?")
            if p!=0:
                root.destroy()
        def reset():

            self.Id_entry.delete(0,END)
            self.Id_entry.insert(0,0)
            self.Ime_entry.delete(0,END)
            self.Prezime_entry.delete(0,END)
            self.Pol_entry.delete(0,END)
            self.Adresa_entry.delete(0,END)
            self.Kontakt_entry.delete(0,END)
            self.Clanstvo_entry.delete(0,END)
            self.Knjiga_Id_entry.delete(0,END)
            self.Knjiga_Ime_entry.delete(0,END)
            self.Autor_entry.delete(0,END)
            self.Datum_U_entry.delete(0,END)
            self.Datum_V_entry.delete(0,END)
            self.Dani_entry.delete(0,END)
            self.Kolicina_entry.delete(0,END)

        #definisanje baze podataka

        class Baza_Podataka:

            def konekcija(self):
                print("konekcija modul pozvan")
                konekcija=sqlite3.connect("Baza.db")
                kursor=konekcija.cursor()
                kursor.execute("CREATE VIRTUAL TABLE if not exists Knjigee USING FTS5(Broj, Naziv, Autor)")
                kursor.execute("CREATE TABLE if not exists Knjige(Broj text, Naziv text, Autor text, Kolicina text)")
                kursor.execute("create table if not exists Clanovi(Broj text, Ime text, Prezime text,Pol text, Adresa text, Kontakt text, Clanstvo text)")
                kursor.execute("create table if not exists Glavni(Broj text, Ime text, Prezime text, Adresa text, Kontakt text, Autor text,Naziv text, Datum_U text, Datum_V text)")
                konekcija.commit()
                konekcija.close()
                print("Konekcija modul zavrsen")
                #Definisanje metoda za knjige
            def Dodaj_Knjige(self,Broj,Naziv,Autor, Kolicina):
                print("Dodavanje knjiga modul pozvan")
                konekcija = sqlite3.connect("Baza.db")
                kursor = konekcija.cursor()
                query="insert into Knjige values(?,?,?,?)"
                kursor.execute(query,(Broj,Naziv,Autor,Kolicina))
                konekcija.commit()
                konekcija.close()
                print("Dodavanje knjige modul zavrsen.")

            def Prikazi_Knjige(self):
                print("Prikazivanje knjiga modul pozvan")
                konekcija = sqlite3.connect("Baza.db")
                kursor = konekcija.cursor()
                kursor.execute("select * from Knjige")
                rows=kursor.fetchall()
                konekcija.commit()
                konekcija.close()
                return rows
                print("Prikazivanje knjiga metod pozvan")

            def Prikazi_Knjigu(self,Naziv):
                print("Prikazivanje podataka knjige")
                konekcija = sqlite3.connect("Baza.db")
                kursor = konekcija.cursor()
                Query="select * from Knjige where Naziv=?"
                kursor.execute(Query,(Naziv,))
                global kurac
                kurac=[]
                kurac=kursor.fetchone()
                return kurac
                konekcija.commit()
                konekcija.close()

            def Pretraga_KnjigaN(self,Naziv=""):
                print("Prikazivanje podataka knjige")
                konekcija = sqlite3.connect("Baza.db")
                kursor = konekcija.cursor()
                query = "select * from Knjige where Naziv=?"
                kursor.execute(query,(Naziv,))
                rows=kursor.fetchall()
                konekcija.commit()
                konekcija.close()
                return rows
            def Pretraga_KnjigaA(self,Autor=""):
                print("Prikazivanje podataka knjige")
                konekcija = sqlite3.connect("Baza.db")
                kursor = konekcija.cursor()
                query = "select * from Knjige where Autor=?"
                kursor.execute(query,(Autor,))
                rows=kursor.fetchall()
                konekcija.commit()
                konekcija.close()
                return rows

            def Pretraga_KnjigaB(self,Broj=""):
                print("Prikazivanje podataka knjige")
                konekcija = sqlite3.connect("Baza.db")
                kursor = konekcija.cursor()
                query = "select from Knjige where Broj=?"
                kursor.execute(query,(Broj,))
                row=kursor.fetchone()
                konekcija.commit()
                konekcija.close()
                return row



            def Brisanje_Knjige(self,Naziv):
                print("Pozivanja modula brisanja knjige")
                konekcija = sqlite3.connect("Baza.db")
                kursor = konekcija.cursor()
                query="delete from Knjige where Naziv=?"
                kursor.execute(query,(Naziv,))
                konekcija.commit()
                konekcija.close()
            def Revidiranje_Kolicina_plus(self, Naziv=""):
                print("Pozivanja modula revidiranja kolicine")
                konekcija = sqlite3.connect("Baza.db")
                kursor = konekcija.cursor()

                kursor.execute("update Knjige set Kolicina=Kolicina+1 where Naziv=?",(Naziv,))
                konekcija.commit()
                konekcija.close()
                print("revidiranje pozvano")
            def Revidiranje_Kolicina_minus(self, Naziv=""):
                print("Pozivanja modula revidiranja kolicine")
                konekcija = sqlite3.connect("Baza.db")
                kursor = konekcija.cursor()

                kursor.execute("update Knjige set Kolicina=Kolicina-1 where Naziv=?",(Naziv,))
                konekcija.commit()
                konekcija.close()
                print("revidiranje pozvano")

            def Vracanje_Kolicine(self, Naziv, Autor):
                konekcija=sqlite3.connect("Baza.db")
                global povratak
                povratak=[]
                kursor=konekcija.cursor()
                kursor.execute("select * from Knjige where (Naziv=? and Autor=?)",(Naziv, Autor))
                povratak=kursor.fetchall()
                return povratak
                konekcija.commit()
                konekcija.close()
                print("vracanje kolicine pozvano")





            #Definisanje metoda za clanove

            def Dodaj_Clana(self,Broj,Ime,Prezime,Pol,Adresa,Kontakt,Clanstvo):
                print("Dodavanje novih clanova pozvano")
                konekcija=sqlite3.connect("Baza.db")
                kursor=konekcija.cursor()
                query="Insert into Clanovi values(?,?,?,?,?,?,?)"
                kursor.execute(query,(Broj,Ime,Prezime,Pol,Adresa,Kontakt,Clanstvo))
                konekcija.commit()
                konekcija.close()
                print("Dodavanje clanova zavrseno")
            def Prikazi_Clana(self,Broj):
                print("Prikazivanje podataka clanova")
                konekcija = sqlite3.connect("Baza.db")
                kursor = konekcija.cursor()
                Query="select * from Clanovi where Broj=?"
                kursor.execute(Query,(Broj,))
                global clann
                clann=[]
                clann=kursor.fetchone()
                return clann
                konekcija.commit()
                konekcija.close()

            def Prikazi_Clanove(self):
                print("Prikazivanje svih clanova modul pozvan")
                konekcija = sqlite3.connect("Baza.db")
                kursor = konekcija.cursor()
                kursor.execute("select * from Clanovi")
                rows=kursor.fetchall()
                konekcija.commit()
                konekcija.close()
                return rows
                print("Prikazivanje clanova metod pozvan")

            def Brisanje_Clanova(self, Broj):
                print("Metoda brisanja clan pozvan")
                konekcija=sqlite3.connect("Baza.db")
                kursor=konekcija.cursor()
                kursor.execute("delete from Clanovi where Broj=?",(Broj,))
                konekcija.commit()
                konekcija.close()

            def Pretraga_ClanovaI(self, Ime="", Prezime=""):
                print("Metoda pretrage imenom  pozvan")
                konekcija = sqlite3.connect("Baza.db")
                kursor = konekcija.cursor()
                kursor.execute("select * from Clanovi where (Ime=? and Prezime=?)", (Ime,Prezime))
                rows=kursor.fetchall()
                konekcija.commit()
                konekcija.close()
                return rows


            def Pretraga_ClanovaA(self, Adresa=""):
                print("Metoda pretrage adresom  pozvan")
                konekcija = sqlite3.connect("Baza.db")
                kursor = konekcija.cursor()
                kursor.execute("select * from Clanovi where Adresa=?", (Adresa,))
                global Adresaaa
                Adresaaa=kursor.fetchone()
                konekcija.commit()
                konekcija.close()
                return Adresaaa

            def Pretraga_ClanovaK(self, Kontakt=""):
                print("Metoda pretrage kontaktom  pozvan")
                konekcija = sqlite3.connect("Baza.db")
                kursor = konekcija.cursor()
                kursor.execute("select * from Clanovi where Kontakt=?", (Kontakt,))
                global Kontakttt
                Kontakttt=kursor.fetchone()
                konekcija.commit()

                konekcija.close()
                return Kontakttt

            def Pretraga_ClanovaID(self,Broj=""):
                print("Metoda pretrage brojem pozvana")
                konekcija = sqlite3.connect("Baza.db")
                kursor = konekcija.cursor()
                kursor.execute("select * from Clanovi where Broj=?", (Broj,))

                global ID
                ID = kursor.fetchone()
                konekcija.commit()
                konekcija.close()
                return ID


            #definisanje metoda za glavni

            def Sacuvaj_Unos(self, Broj, Ime, Prezime, Adresa, Kontakt, Autor, Naziv, Datum_U, Datum_V):
                konekcija=sqlite3.connect("Baza.db")
                kursor=konekcija.cursor()
                query="insert into Glavni values(?,?,?,?,?,?,?,?,?)"
                kursor.execute(query,(Broj, Ime, Prezime, Adresa, Kontakt, Autor, Naziv, Datum_U, Datum_V))
                konekcija.commit()
                konekcija.close()


            def Prikazi_Sve(self):
                konekcija = sqlite3.connect("Baza.db")
                kursor = konekcija.cursor()
                query = "select * from Glavni"
                kursor.execute(query)
                rows=kursor.fetchall()
                konekcija.commit()
                konekcija.close()
                return rows
            def Brisanje_Glavni(self, Broj, Naziv, Datum_U):
                print("Metoda brisanja iz glavne baze")
                konekcija = sqlite3.connect("Baza.db")
                kursor = konekcija.cursor()
                query = "delete  from Glavni where (Broj=? and Naziv=? and Datum_U=?)"
                kursor.execute(query,(Broj,Naziv, Datum_U))
                konekcija.commit()
                konekcija.close()
            def Pretraga_Glavni(self,Broj="", Ime="", Prezime="", Naziv="" ,Autor=""):
                konekcija=sqlite3.connect("Baza.db")
                kursor=konekcija.cursor()
                kursor.execute("select * from Glavni where(Broj=? or (Ime=? and Prezime=?)  or (Naziv=? and Autor=?))",(Broj,Ime, Prezime, Naziv, Autor))
                rows=kursor.fetchall()
                konekcija.commit()
                konekcija.close()
                return rows
                print("metoda pretrage pozvana")








        global baza
        baza=Baza_Podataka()
        baza.konekcija()


        #pozivanje funkcija modula

        def Sacuvaj_Unos():
            global kolicinaa
            global Naziv_Knjigee
            global xy
            kolicinaa = Kolicina.get()
            xy = int(kolicinaa) - 1
            if xy<0:
                tkinter.messagebox.showwarning("Greška","Sve zalihe ove knjige su pozajmljene.")
                return
            else:
                    baza.Sacuvaj_Unos(Broj_Rf.get(),Ime.get(),Prezime.get(),Adresa.get(),Kontakt.get(),Autor_Knjige.get(),Naziv_Knjige.get(),Datum_Uzimanja.get(),Vratiti_Do.get())
                    global s
                    s=0

                    for row in lista.get_children():
                        s+=1


                    for row in lista.get_children():
                            lista.delete(row)
                    for row in baza.Prikazi_Sve():
                            print("red iznozi",row)
                            lista.insert("", s, values=(row[0], row[1], row[2], row[3], row[4], row[6], row[5], row[7], row[8]))
                            s -= 1


            Naziv_Knjigee = Naziv_Knjige.get()
            print("naziv, kolicina",Naziv_Knjigee,xy)
            baza.Revidiranje_Kolicina_minus(Naziv_Knjigee)


        def Izabrani_Glavni(Evt):
            global Izabrani
            global Izabranii

            Izabrani=lista.focus()
            Izabranii=lista.item(Izabrani)
            baza.Vracanje_Kolicine((Izabranii['values'][5]), (Izabranii['values'][6]))
            print(povratak)
            global res
            global ress
            res=list(map(itemgetter(3),povratak))
            ress=list(map(itemgetter(1), povratak))
            print("stvari iznose",str(res[0]),str(ress[0]))

        def Brisanje_Glavni():
            baza.Brisanje_Glavni(Izabranii['values'][0],Izabranii['values'][5],Izabranii['values'][7])

            qq=int(res[0])+5
            print("sto nam treba")
            qq=str(qq)
            print(qq)
            print(ress[0])
            baza.Revidiranje_Kolicina_plus(ress[0])



            Prikazi_Sve()







        def Prikazi_Sve():
            global p
            p=0
            for row in lista.get_children():
                p+=1

            for row in lista.get_children():
                lista.delete(row)

            for row in baza.Prikazi_Sve():
                lista.insert("",p,values=(row[0],row[1],row[2],row[3],row[4],row[6],row[5],row[7],row[8]))
                p-=1







        def Pretraga_Glavni():
            g=0
            for row in lista.get_children():
                lista.delete(row)
                g+=1
            for row in baza.Pretraga_Glavni(Broj_Rf.get(),Ime.get(),Prezime.get(),Naziv_Knjige.get(),Autor_Knjige.get()):
                print(row)
                lista.insert("",g,values=(row[0],row[1],row[2],row[3],row[4],row[6],row[5],row[7],row[8]))
                g-=1
        def Dodaj_Clana():
            baza.Dodaj_Clana(Broj_Rf.get(),Ime.get(),Prezime.get(),Pol.get(),Adresa.get(),Kontakt.get(),Clan_Od.get())
            Lista_Clanova.delete(0, END)
            for row in baza.Prikazi_Clanove():
                Lista_Clanova.insert(0, str(row[0]) + ":" + row[1] + " " + row[2] + "-" + row[4])

        def Izabrani_Clan(event):
            global Novi_Clan
            global opcije
            opcije=["Muški","Ženski"]
            Novi_Clan=str(Lista_Clanova.get(Lista_Clanova.curselection()))
            Novi_Clan=re.split('-|:',Novi_Clan)
            baza.Prikazi_Clana(int(Novi_Clan[0]))
            self.Id_entry.delete(0,END)
            self.Id_entry.insert(END,clann[0])
            self.Ime_entry.delete(0, END)
            self.Ime_entry.insert(END,clann[1])
            self.Prezime_entry.delete(0, END)
            self.Prezime_entry.insert(END, clann[2])
            self.Pol_entry.delete(0, END)

            self.Pol_entry.insert(0,clann[3])

            self.Adresa_entry.delete(0, END)
            self.Adresa_entry.insert(END, clann[4])
            self.Kontakt_entry.delete(0, END)
            self.Kontakt_entry.insert(END, clann[5])
            self.Clanstvo_entry.delete(0, END)
            self.Clanstvo_entry.insert(END, clann[6])

        def Prikazi_Clanove():
            Lista_Clanova.delete(0,END)
            for row in baza.Prikazi_Clanove():
                Lista_Clanova.insert(0,str(row[0])+":"+row[1]+" "+row[2]+"-"+row[4])

        def Brisanje_Clanova():
            Lista_Clanova.delete(0,END)
            baza.Brisanje_Clanova(Novi_Clan[0])
            for row in baza.Prikazi_Clanove():
                Lista_Clanova.insert(0, str(row[0]) + "-" + row[1] + " " + row[2] + "-" + row[4])








        def dodavanje_knjiga():
                    baza.Dodaj_Knjige(Knjiga_Rf.get(), Naziv_Knjige.get(), Autor_Knjige.get(), Kolicina.get())
                    Lista_Knjiga.delete(0, END)
                    for row in baza.Prikazi_Knjige():
                        Lista_Knjiga.insert(0,row[1]+"-"+row[2])

        def prikazivanje_knjiga():
            Lista_Knjiga.delete(0,END)
            for row in baza.Prikazi_Knjige():
                Lista_Knjiga.insert(0,row[1]+"-"+row[2])





        def Izabrana_Knjiga(Evt):

            global knjiga
            knjiga = Lista_Knjiga.get(Lista_Knjiga.curselection())
            knjiga=knjiga.split("-")
            print("printanje knjige")
            print(knjiga)
            baza.Prikazi_Knjigu(knjiga[0])
            print(kurac)
            self.Knjiga_Id_entry.delete(0,END)
            self.Knjiga_Id_entry.insert(END,kurac[0])
            self.Knjiga_Ime_entry.delete(0, END)
            self.Knjiga_Ime_entry.insert(END,kurac[1])
            self.Autor_entry.delete(0, END)
            self.Autor_entry.insert(END,kurac[2])
            self.Kolicina_entry.delete(0, END)
            self.Kolicina_entry.insert(END, (kurac[3]))
            a = (datetime.date(datetime.now()))
            self.Datum_U_entry.delete(0, END)
            self.Datum_U_entry.insert(END,a)
            self.Datum_V_entry.delete(0, END)
            self.Datum_V_entry.insert(END,a+timedelta(days=30))
            self.Dani_entry.delete(0, END)
            self.Dani_entry.insert(END, "Mjesec dana")
            self.Kolicina_entry.delete(0, END)
            self.Kolicina_entry.insert(END,str(kurac[3]))

        def Brisanje_Knjige():

            baza.Brisanje_Knjige(knjiga[0])
            Lista_Knjiga.delete(0,END)
            for row in baza.Prikazi_Knjige():
                Lista_Knjiga.insert(0, row[1]+"-"+row[2])

        def Pretraga_Knjiga():
            print("pozvana pretraga")
            selektovan=Pretrazi_Pomocu_Knjige.get()

            if (selektovan=="Pretraži pomoću"):
                tkinter.messagebox.showwarning("Greška.","Niste izabrali nijedan način pretrage!")
            elif (selektovan=="Naziva"):
                Lista_Knjiga.delete(0, END)
                for row in baza.Pretraga_KnjigaN(Trazena_Knjiga.get()):
                    Lista_Knjiga.insert(END,row[1]+"-"+row[2])

            elif (selektovan=="Autora"):
                Lista_Knjiga.delete(0, END)
                for row in baza.Pretraga_KnjigaA(Trazena_Knjiga.get()):
                    Lista_Knjiga.insert(END, row[1]+"-"+row[2])




        def Pretraga_Clanova():
            print("pozvana pretraga clanova")
            selektovan=Pretrazi_Pomocu_Clanovi.get()

            if (selektovan=="Pretraži pomoću"):
                tkinter.messagebox.showwarning("Greška.","Niste izabrali nijedan način pretrage!")
            elif (selektovan=="Imena i Prezimena"):
                Lista_Clanova.delete(0, END)
                Ime_P=Trazeni_Clan.get()
                print(Ime_P)
                Ime_P=Ime_P.split(" ")
                ImeC=Ime_P[0]
                ImeP=Ime_P[1]

                for row in baza.Pretraga_ClanovaI(ImeC,ImeP):
                    print(row)
                    Lista_Clanova.insert(END,str(row[0])+":"+row[1]+" "+row[2]+"-"+row[4])

            elif (selektovan=="Kontakta"):
                Lista_Clanova.delete(0, END)
                baza.Pretraga_ClanovaK(Trazeni_Clan.get())
                print(Kontakttt)
                Lista_Clanova.insert(END,str(Kontakttt[0])+":"+Kontakttt[1]+" "+Kontakttt[2]+"-"+Kontakttt[4])
            elif (selektovan=="Adrese"):
                Lista_Clanova.delete(0, END)
                baza.Pretraga_ClanovaA(Trazeni_Clan.get())
                Lista_Clanova.insert(END,str(Adresaaa[0])+":"+Adresaaa[1]+" "+Adresaaa[2]+"-"+Adresaaa[4])
            elif (selektovan=="ID broja"):
                Lista_Clanova.delete(0, END)
                brojjj=str(Trazeni_Clan.get())
                print(brojjj)
                baza.Pretraga_ClanovaID(brojjj)

                Lista_Clanova.insert(END,str(ID[0])+":"+ID[1]+" "+ID[2]+"-"+ID[4])











        #widget
        self.Id_Lbl=Label(PodaciFrejmLijevi,text="ID član:", bd=3,font=("arial",13,"bold"), padx=2,pady=5, bg="#ffc5a1")
        self.Ime_Lbl = Label(PodaciFrejmLijevi, text="Ime:", bd=3, font=("arial", 13, "bold"), padx=2, pady=5,bg="#ffc5a1")
        self.Prezime_Lbl = Label(PodaciFrejmLijevi, text="Prezime:", bd=3, font=("arial", 13, "bold"), padx=2, pady=5,bg="#ffc5a1")
        self.Pol_Lbl = Label(PodaciFrejmLijevi, text="Pol:", bd=3, font=("arial", 13, "bold"), padx=2, pady=5,bg="#ffc5a1")
        self.Adresa_Lbl = Label(PodaciFrejmLijevi, text="Adresa:", bd=3, font=("arial", 13, "bold"), padx=2, pady=5,bg="#ffc5a1")
        self.Kontakt_Lbl = Label(PodaciFrejmLijevi, text="Kontakt:", bd=3, font=("arial", 13, "bold"), padx=2, pady=5,bg="#ffc5a1")
        self.Clanstvo_Lbl = Label(PodaciFrejmLijevi, text="Član od:", bd=3, font=("arial", 13, "bold"), padx=2, pady=5,bg="#ffc5a1")

        self.Id_Lbl.grid(row=0, column=0, sticky='W')
        self.Ime_Lbl.grid(row=1, column=0, sticky='W')
        self.Prezime_Lbl.grid(row=2, column=0, sticky='W')
        self.Pol_Lbl.grid(row=3, column=0, sticky='W')
        self.Adresa_Lbl.grid(row=4, column=0, sticky='W')
        self.Kontakt_Lbl.grid(row=5, column=0, sticky='W')
        self.Clanstvo_Lbl.grid(row=6, column=0, sticky='W')

        self.Id_entry = Entry(PodaciFrejmLijevi, font=("arial", 13, "bold"), bd=3, width=25,textvariable=Broj_Rf)
        self.Id_entry.grid(row=0, column=1)
        self.Ime_entry = Entry(PodaciFrejmLijevi, font=("arial", 13, "bold"), bd=3, width=25,textvariable=Ime)
        self.Ime_entry.grid(row=1, column=1)
        self.Prezime_entry = Entry(PodaciFrejmLijevi, font=("arial", 13, "bold"), bd=3, width=25,textvariable=Prezime)
        self.Prezime_entry.grid(row=2, column=1)
        self.Pol_entry = ttk.Combobox(PodaciFrejmLijevi, font=("arial", 13, "bold"),values=["Muški","Ženski"], width=24,textvariable=Pol)
        self.Pol_entry.current(0)
        self.Pol_entry.grid(row=3, column=1)
        self.Adresa_entry = Entry(PodaciFrejmLijevi, font=("arial", 13, "bold"), bd=3, width=25,textvariable=Adresa)
        self.Adresa_entry.grid(row=4, column=1)
        self.Kontakt_entry = Entry(PodaciFrejmLijevi, font=("arial", 13, "bold"), bd=3, width=25,textvariable=Kontakt)
        self.Kontakt_entry.grid(row=5, column=1)
        self.Clanstvo_entry = Entry(PodaciFrejmLijevi, font=("arial", 13, "bold"), bd=3, width=25,textvariable=Clan_Od)
        self.Clanstvo_entry.grid(row=6, column=1)

        self.Knjiga_Id_lbl = Label(PodaciFrejmLijevi, text="ID knjiga:", bd=3, font=("arial", 13, "bold"), padx=5, pady=5,bg="#ffc5a1")
        self.Knjiga_Ime_Lbl = Label(PodaciFrejmLijevi, text="Naziv knjige:", bd=3, font=("arial", 13, "bold"), padx=5, pady=5,bg="#ffc5a1")
        self.Autor_Lbl = Label(PodaciFrejmLijevi, text="Autor knjige:", bd=3, font=("arial", 13, "bold"), padx=5, pady=5,bg="#ffc5a1")
        self.Datum_Uzimanja_Lbl = Label(PodaciFrejmLijevi, text="Datum uzimanja:", bd=3, font=("arial", 13, "bold"), padx=5, pady=5,bg="#ffc5a1")
        self.Datum_Vracanja_lbl = Label(PodaciFrejmLijevi, text="Vratiti do:", bd=3, font=("arial", 13, "bold"), padx=5, pady=5,bg="#ffc5a1")
        self.Dani_Pozajmice_Lbl = Label(PodaciFrejmLijevi, text="Dani pozajmice:", bd=3, font=("arial", 13, "bold"), padx=5, pady=5,bg="#ffc5a1")
        self.Kazna_Lbl = Label(PodaciFrejmLijevi, text="Količina:", bd=3, font=("arial", 13, "bold"), padx=5, pady=5,bg="#ffc5a1")

        self.Knjiga_Id_lbl.grid(row=0, column=2, sticky='W')
        self.Knjiga_Ime_Lbl.grid(row=1, column=2, sticky='W')
        self.Autor_Lbl.grid(row=2, column=2, sticky='W')
        self.Datum_Uzimanja_Lbl.grid(row=3, column=2, sticky='W')
        self.Datum_Vracanja_lbl.grid(row=4, column=2, sticky='W')
        self.Dani_Pozajmice_Lbl.grid(row=5, column=2, sticky='W')
        self.Kazna_Lbl.grid(row=6, column=2, sticky='W')

        self.Knjiga_Id_entry = Entry(PodaciFrejmLijevi, font=("arial", 13, "bold"), bd=3, width=20,textvariable=Knjiga_Rf)
        self.Knjiga_Id_entry.grid(row=0, column=3)
        self.Knjiga_Ime_entry = Entry(PodaciFrejmLijevi, font=("arial", 13, "bold"), bd=3, width=20,textvariable=Naziv_Knjige)
        self.Knjiga_Ime_entry.grid(row=1, column=3)
        self.Autor_entry = Entry(PodaciFrejmLijevi, font=("arial", 13, "bold"), bd=3, width=20,textvariable=Autor_Knjige)
        self.Autor_entry.grid(row=2, column=3)
        self.Datum_U_entry = Entry(PodaciFrejmLijevi, font=("arial", 13, "bold"), bd=3, width=20,textvariable=Datum_Uzimanja)
        self.Datum_U_entry.grid(row=3, column=3)
        self.Datum_V_entry = Entry(PodaciFrejmLijevi, font=("arial", 13, "bold"), bd=3, width=20,textvariable=Vratiti_Do)
        self.Datum_V_entry.grid(row=4, column=3)
        self.Dani_entry = Entry(PodaciFrejmLijevi, font=("arial", 13, "bold"), bd=3, width=20,textvariable=Dani_Pozajmice)
        self.Dani_entry.grid(row=5, column=3)
        self.Kolicina_entry = Entry(PodaciFrejmLijevi, font=("arial", 13, "bold"), bd=3, width=20,textvariable=Kolicina)
        self.Kolicina_entry.grid(row=6, column=3)


        self.Sačuvaj_unos=Button(DugmadFrejm, text="Sačuvaj unos",font=("arial", 12, "bold"),bd=3,padx=15,pady=10, command=Sacuvaj_Unos)
        self.Sačuvaj_unos.grid(row=0,column=0,padx=10,pady=10)


        self.Obrisi = Button(DugmadFrejm, text="Brisanje", font=("arial", 12, "bold"), bd=3, padx=15,pady=10,command=Brisanje_Glavni)
        self.Obrisi.grid(row=0, column=2, padx=9,pady=7)
        self.Reset=Button(DugmadFrejm,text="Reset",bd=3,padx=15, font=("arial",12,"bold"),pady=10, command=reset)
        self.Reset.grid(row=0,column=3,padx=9,pady=10)
        self.Izadji=Button(DugmadFrejm,text="Izlaz",bd=3,padx=15, font=("arial",12,"bold"),pady=10, command=izadji)
        self.Izadji.grid(row=0,column=5,padx=9,pady=10)
        self.Prikazi = Button(DugmadFrejm, text="Prikaži sve", bd=3, padx=15, font=("arial", 12, "bold"), pady=10,command=Prikazi_Sve)
        self.Prikazi.grid(row=0, column=1, padx=9, pady=10)
        self.Prikazi = Button(DugmadFrejm, text="Pretraga", bd=3, padx=15, font=("arial", 12, "bold"), pady=10,command=Pretraga_Glavni)
        self.Prikazi.grid(row=0, column=4, padx=9, pady=10)




        # definisanje novog prozora za unos knjiga

        def open():
            Novi_Prozor = Toplevel(self.root)
            Novi_Prozor.title("Unos novih knjiga")
            Novi_Prozor.geometry("400x250")
            self.Knjigaa_Id_lbl = Label(Novi_Prozor, text="Knjiga rf..:", bd=3, font=("arial", 13, "bold"), padx=5,
                                        pady=5)
            self.Knjigaa_Ime_Lbl = Label(Novi_Prozor, text="Naziv knjige:", bd=3, font=("arial", 13, "bold"), padx=5,
                                         pady=5)
            self.Autorr_Lbl = Label(Novi_Prozor, text="Autor knjige:", bd=3, font=("arial", 13, "bold"), padx=5, pady=5)
            self.Kolicina_Lbl = Label(Novi_Prozor, text="Količina:", bd=3, font=("arial", 13, "bold"), padx=5, pady=5)

            self.Knjigaa_Id_lbl.grid(row=0, column=2, sticky='W')
            self.Knjigaa_Ime_Lbl.grid(row=1, column=2, sticky='W')
            self.Autorr_Lbl.grid(row=2, column=2, sticky='W')
            self.Kolicina_Lbl.grid(row=3,column=2, sticky="W")

            self.Knjigaa_Id_entry = Entry(Novi_Prozor, font=("arial", 13, "bold"), bd=3, width=20,textvariable=Knjiga_Rf)
            self.Knjigaa_Id_entry.grid(row=0, column=3)
            self.Knjigaa_Ime_entry = Entry(Novi_Prozor, font=("arial", 13, "bold"), bd=3, width=20,textvariable=Naziv_Knjige)
            self.Knjigaa_Ime_entry.grid(row=1, column=3)
            self.Autorr_entry = Entry(Novi_Prozor, font=("arial", 13, "bold"), bd=3, width=20, textvariable=Autor_Knjige)
            self.Autorr_entry.grid(row=2, column=3)
            self.Kolicinaa_entry=Entry(Novi_Prozor, font=("arial", 13, "bold"), bd=3, width=20, textvariable=Kolicina)
            self.Kolicinaa_entry.grid(row=3, column=3)

            self.Dodajj_Knjigu = Button(Novi_Prozor, text="Dodaj Knjigu", font=("arial", 11, "bold"), bd=3, padx=10,pady=5, command=dodavanje_knjiga)
            self.Dodajj_Knjigu.grid(row=4,column=3)

        #definisanje novog prozora za unos novih clanova

        def openn():
            Novi_Prozor2 = Toplevel(self.root)
            Novi_Prozor2.title("Unos novih clanova")
            Novi_Prozor2.geometry("400x350")
            self.Novi_Id = Label(Novi_Prozor2, text="Broj rf.:", bd=3, font=("arial", 13, "bold"), padx=5,pady=5)
            self.Novi_Ime = Label(Novi_Prozor2, text="Ime:", bd=3, font=("arial", 13, "bold"), padx=5,pady=5)
            self.Novi_Prezime = Label(Novi_Prozor2, text="Prezime:", bd=3, font=("arial", 13, "bold"), padx=5, pady=5)
            self.Novi_Pol = Label(Novi_Prozor2, text="Pol:", bd=3, font=("arial", 13, "bold"), padx=5, pady=5)
            self.Novi_Adresa = Label(Novi_Prozor2, text="Adresa:", bd=3, font=("arial", 13, "bold"), padx=5, pady=5)
            self.Novi_Kontakt = Label(Novi_Prozor2, text="Kontakt:", bd=3, font=("arial", 13, "bold"), padx=5, pady=5)
            self.Novi_Clan = Label(Novi_Prozor2, text="Clan od:", bd=3, font=("arial", 13, "bold"), padx=5, pady=5)

            self.Novi_Id.grid(row=0, column=2, sticky='W')
            self.Novi_Ime.grid(row=1, column=2, sticky='W')
            self.Novi_Prezime.grid(row=2, column=2, sticky='W')
            self.Novi_Pol.grid(row=3, column=2, sticky='W')
            self.Novi_Adresa.grid(row=4, column=2, sticky='W')
            self.Novi_Kontakt.grid(row=5, column=2, sticky='W')
            self.Novi_Clan.grid(row=6, column=2, sticky='W')


            self.Novi_Id_entry = Entry(Novi_Prozor2, font=("arial", 13, "bold"), bd=3, width=20,textvariable=Broj_Rf)
            self.Novi_Id_entry.grid(row=0, column=3)
            self.Novi_Ime_entry = Entry(Novi_Prozor2, font=("arial", 13, "bold"), bd=3, width=20,textvariable=Ime)
            self.Novi_Ime_entry.grid(row=1, column=3)
            self.Novi_Prezime_entry=Entry(Novi_Prozor2, font=("arial", 13, "bold"), bd=3, width=20,textvariable=Prezime )
            self.Novi_Prezime_entry.grid(row=2, column=3)
            self.Novi_Pol_entry = ttk.Combobox(Novi_Prozor2, font=("arial", 13, "bold"),values=["Muški","Ženski"], width=19,textvariable=Pol, state="readonly")
            self.Novi_Pol_entry.current(0)
            self.Novi_Pol_entry.grid(row=3, column=3)
            self.Novi_Adresa_entry = Entry(Novi_Prozor2, font=("arial", 13, "bold"), bd=3, width=20,textvariable=Adresa)
            self.Novi_Adresa_entry.grid(row=4, column=3)
            self.Novi_Kontakt_entry = Entry(Novi_Prozor2, font=("arial", 13, "bold"), bd=3, width=20,textvariable=Kontakt)
            self.Novi_Kontakt_entry.grid(row=5, column=3)
            self.Novi_Clan_entry = Entry(Novi_Prozor2, font=("arial", 13, "bold"), bd=3, width=20, textvariable=Clan_Od)
            self.Novi_Clan_entry.grid(row=6, column=3)
            self.Dodajj_Clana = Button(Novi_Prozor2, text="Dodaj Clana", font=("arial", 11, "bold"), bd=3, padx=20,pady=10,command=Dodaj_Clana)
            self.Dodajj_Clana.grid(row=7, column=3)

        #listaknjiga i Clanova
        Lista_Knjiga=Listbox(PodaciFrejmDesni,font=("Times New Roman",13,"bold"),bd=7,bg="#ff924d")
        Lista_Knjiga.bind('<<ListboxSelect>>',Izabrana_Knjiga)
        Lista_Knjiga.place(x=6,y=0,width=360,height=260)
        Lista_Clanova = Listbox(PodaciFrejmDesni, font=("Times New Roman", 13, "bold"), bd=7,bg="#ff924d")
        Lista_Clanova.bind('<<ListboxSelect>>',Izabrani_Clan)
        Lista_Clanova.place(x=385, y=0, width=360, height=260)
        scroll_lista=ttk.Scrollbar(PodaciFrejmDesni, orient=VERTICAL,command=Lista_Knjiga.yview)
        Lista_Knjiga.configure(yscrollcommand=scroll_lista.set)
        scroll_lista.place(x=355,y=1,height=252)
        scroll_listaH=ttk.Scrollbar(PodaciFrejmDesni,orient=HORIZONTAL,command=Lista_Knjiga.xview)
        Lista_Knjiga.configure(xscrollcommand=scroll_listaH.set)
        scroll_listaH.place(y=250,x=6,width=364)
        scroll_listaC = ttk.Scrollbar(PodaciFrejmDesni, orient=VERTICAL, command=Lista_Clanova.yview)
        Lista_Clanova.configure(yscrollcommand=scroll_listaC.set)
        scroll_listaC.place(x=737, y=1, height=250)
        scroll_listaCH=ttk.Scrollbar(PodaciFrejmDesni,orient=HORIZONTAL,command=Lista_Clanova.xview)
        Lista_Clanova.configure(xscrollcommand=scroll_listaCH)
        scroll_listaCH.place(x=386,y=251, width=366)

        for row in baza.Prikazi_Knjige():
            Lista_Knjiga.insert(0,row[1]+"-"+row[2])
        for row in baza.Prikazi_Clanove():
            Lista_Clanova.insert(0, str(row[0]) + ":" + row[1] + " " + row[2] + "-" + row[4])



        #dugmadLista
        self.Dodaj_Knjigu=Button(PodaciFrejmDesni,text="Dodaj Knjigu",font=("arial",11,"bold"),bd=3,padx=15, command=open)
        self.Dodaj_Knjigu.place(x=7,width=110, y=275)
        self.Prikazivanje_Knjiga = Button(PodaciFrejmDesni, text="Prikaži knjige", font=("arial", 11, "bold"), bd=3, padx=15, command=prikazivanje_knjiga)
        self.Prikazivanje_Knjiga.place(x=120, width=130, y=275)
        self.Brisanje_Knjige = Button(PodaciFrejmDesni, text="Obriši knjigu", font=("arial", 11, "bold"), bd=3, padx=15, command=Brisanje_Knjige)
        self.Brisanje_Knjige.place(x=253, width=110, y=275)
        self.Kombo = ttk.Combobox(DugmadFrejm1,value=["Pretraži pomoću", "Naziva", "Autora"],width=14, font=("arial",12, "bold"),textvariable=Pretrazi_Pomocu_Knjige,state="readonly")
        self.Kombo.current(0)
        self.Kombo.grid(row=0,column=0,pady=15)
        self.Pretraga=Entry(DugmadFrejm1,width=11,font=("arial",13),textvariable=Trazena_Knjiga)
        self.Pretraga.grid(row=0,column=1,pady=15,padx=3)
        self.Pretraga_Knjiga=Button(DugmadFrejm1,text="Pretraga",font=("arial",10,"bold"), command=Pretraga_Knjiga)
        self.Pretraga_Knjiga.grid(row=0,column=2,padx=7,pady=15)

        self.Dodaj_Clana = Button(PodaciFrejmDesni, text="Dodaj člana", font=("arial", 11, "bold"), bd=3, padx=15,command=openn)
        self.Dodaj_Clana.place(x=385, width=110, y=275)
        self.Prikazi_Clanove = Button(PodaciFrejmDesni, text="Prikaži članove", font=("arial", 11, "bold"), bd=3, padx=15, command=Prikazi_Clanove)
        self.Prikazi_Clanove.place(x=498, width=130, y=275)
        self.Brisanje_Clanova= Button(PodaciFrejmDesni, text="Izbriši člana", font=("arial", 11, "bold"), bd=3, padx=15, command=Brisanje_Clanova)
        self.Brisanje_Clanova.place(x=631, width=110, y=275)

        self.Kombo = ttk.Combobox(DugmadFrejm2, value=["Pretraži pomoću", "Imena i Prezimena", "Adrese","Kontakta","ID broja"], width=14,font=("arial", 12, "bold"),textvariable=Pretrazi_Pomocu_Clanovi,state="readonly")
        self.Kombo.current(0)
        self.Kombo.grid(row=0, column=0, pady=15)
        self.PretragaC = Entry(DugmadFrejm2, width=11, font=("arial", 13), textvariable=Trazeni_Clan)
        self.PretragaC.grid(row=0, column=1, pady=15, padx=3)
        self.PretragaC_Clanova = Button(DugmadFrejm2, text="Pretraga", font=("arial", 10, "bold"),command=Pretraga_Clanova)
        self.PretragaC_Clanova.grid(row=0, column=2, padx=7, pady=15)

        #za glavnu bazu

        lista=ttk.Treeview(DetaljFrejm)
        lista.place(x=-26,y=0,height=254,width=1587)
        lista.bind('<<TreeviewSelect>>',Izabrani_Glavni)





        ttk.Style().configure("Treeview", background="#ff924d", fieldbackground="#ff924d", foreground="black")
        lista["columns"]=("prva kolona","druga kolona","treca kolona","cetvrta kolona","peta kolona","sesta kolona","sedma kolona","osma kolona","deveta kolona")
        lista.column("prva kolona",width=120,anchor="n")
        lista.column("druga kolona", width=120,anchor="n")
        lista.column("treca kolona", width=167,anchor="n")
        lista.column("cetvrta kolona", width=250,anchor="n")
        lista.column("peta kolona", width=167,anchor="n")
        lista.column("sesta kolona", width=180,anchor="n")
        lista.column("sedma kolona", width=170,anchor="n")
        lista.column("osma kolona", width=130,anchor="n")
        lista.column("deveta kolona", width=130, anchor="n")

        lista.heading("prva kolona",text=" Id Broj člana")
        lista.heading("druga kolona", text="Ime")
        lista.heading("treca kolona", text="Prezime")
        lista.heading("cetvrta kolona", text="Adresa")
        lista.heading("peta kolona", text="Kontakt")
        lista.heading("sesta kolona", text="Naziv Knjige")
        lista.heading("sedma kolona", text="Autor")
        lista.heading("osma kolona", text="Datum uzimanja")
        lista.heading("deveta kolona", text="Datum vraćanja")
        lista['show'] = 'headings'

        lista_scroll=ttk.Scrollbar(DetaljFrejm,orient=VERTICAL,command=lista.yview)
        lista.configure(yscroll=lista_scroll.set)
        lista_scroll.place(x=1544,y=26,height=227)

        ll = 0

        for row in lista.get_children():
            ll += 1

        for row in lista.get_children():
            lista.delete(row)
        for row in baza.Prikazi_Sve():
            print("red iznozi", row)
            lista.insert("", ll, values=(row[0], row[1], row[2], row[3], row[4], row[6], row[5], row[7], row[8]))
            ll -= 1








if __name__=='__main__':
    root=tk.ThemedTk()
    root.set_theme("clearlooks")
    application=Biblioteka(root)
    root.mainloop()
