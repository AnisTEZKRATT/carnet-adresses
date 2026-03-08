import tkinter as tk
from tkinter import font
from tkinter import messagebox
from tkinter import ttk

class CarnetAdressesView:
    def __init__(self):
        try:
            from ctypes import windll

            windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass

        self.root = tk.Tk()
        self.root.title("Carnet d’adresses")
        self.root.geometry("1200x900")
        self.root.minsize(1200, 900)

        font_par_df = font.nametofont("TkDefaultFont")
        font_par_df.configure(family="Segoe UI", size=10)

        
        self._icon = tk.PhotoImage(file="./icons/user2.png")
        self.root.iconphoto(True, self._icon)

        self.icon_add = tk.PhotoImage(file="icons/add2.png")
        self.icon_effacer = tk.PhotoImage(file="./icons/effacer.png")
        self.icon_rechercher = tk.PhotoImage(file="./icons/rechercher.png")
        self.icon_modifier = tk.PhotoImage(file="./icons/modify.png")
        self.icon_afficher_tout = tk.PhotoImage(file="./icons/affichertout.png")
        self.icon_quitter = tk.PhotoImage(file="./icons/quit.png")
        self.icon_supprimer = tk.PhotoImage(file="./icons/delete.png")

        #self.root.bind("<Control-q>", lambda event: self.root.quit())
        #self.root.bind("<Control-Q>", lambda event: self.root.quit())

        self._construire_menu()
        self._construire_form()
        self._construire_actions()
        self._construire_list()
        self._construire_status_bar()

    def _construire_menu(self) -> None:
        menubar = tk.Menu(self.root)

        self.menu_fichier = tk.Menu(menubar, tearoff=0)
        #self.menu_fichier.add_command(label="Quitter")

        self.menu_fichier.add_command(label="Exporter CSV")

        self.menu_fichier.add_command(label="Quitter", accelerator="Ctrl+Q")

        menubar.add_cascade(label="Fichier", menu=self.menu_fichier)

        self.menu_edition = tk.Menu(menubar, tearoff=0)
        self.menu_edition.add_command(label="Ajouter", accelerator="Ctrl+N")

        self.menu_edition.add_command(label="Modifier", accelerator="Ctrl+M")

        self.menu_edition.add_command(label="Rechercher", accelerator="Ctrl+F")
        
        self.menu_edition.add_command(label="Supprimer", accelerator="Delete")

        menubar.add_cascade(label="Édition", menu=self.menu_edition)

        self.menu_affichage = tk.Menu(menubar, tearoff=0)
        self.menu_affichage.add_command(label="Afficher tous", accelerator="Ctrl+A")
        menubar.add_cascade(label="Affichage", menu=self.menu_affichage)

        self.menu_aide = tk.Menu(menubar, tearoff=0)
        self.menu_aide.add_command(label="À propos", command=self.afficher_a_propos)
        self.menu_aide.add_command(label="Code Source", command=self.ouvrir_gh)

        menubar.add_cascade(label="Aide", menu=self.menu_aide)

        self.root.config(menu=menubar)


    def ouvrir_gh(self):
        import webbrowser
        webbrowser.open("https://github.com/AnisTEZKRATT/carnet-adresses")

    def afficher_a_propos(self):
        messagebox.showinfo(
            "À propos",
            "Carnet d'adresses v1.0\n\n"
            "Application de gestion de contacts\n"
            "Développée pour le projet IHM"
        )

    def _construire_form(self) -> None:
        frame_form = ttk.LabelFrame(self.root, text="Informations du contact", padding=10)
        frame_form.pack(padx=10, pady=10, anchor="center")

        # Ligne 0
        ttk.Label(frame_form, text="Nom *").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.entry_nom = ttk.Entry(frame_form, width=30)
        self.entry_nom.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_form, text="Prénom *").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.entry_prenom = ttk.Entry(frame_form, width=30)
        self.entry_prenom.grid(row=0, column=3, padx=5, pady=5)

        # Ligne 1
        ttk.Label(frame_form, text="Téléphone").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.entry_tel = ttk.Entry(frame_form, width=30)
        self.entry_tel.grid(row=1, column=1, padx=5, pady=(5, 0))

        ttk.Label(frame_form, text="Email").grid(row=1, column=2, sticky="w", padx=5, pady=5)
        self.entry_email = ttk.Entry(frame_form, width=30)
        self.entry_email.grid(row=1, column=3, padx=5, pady=5)

        # Ligne 2
        ttk.Label(
            frame_form,
            text="Ex: 0534…, +21364…, 21364…",
            font=("Segoe UI", 8),
            foreground="#666666"
        ).grid(row=2, column=1, sticky="w", padx=5, pady=(0, 5))

        # Ligne 3
        ttk.Label(frame_form, text="Adresse").grid(
            row=3, column=0, sticky="nw", padx=5, pady=(12, 5)
        )

        self.text_adresse = tk.Text(frame_form, height=3, width=58, wrap="word")
        self.text_adresse.grid(
            row=3, column=1, columnspan=3, padx=5, pady=(12, 5), sticky="w"
        )

        scroll_adresse = ttk.Scrollbar(frame_form, orient="vertical", command=self.text_adresse.yview)
        scroll_adresse.grid(row=3, column=4, sticky="ns", padx=(0, 5), pady=(12, 5))
        self.text_adresse.configure(yscrollcommand=scroll_adresse.set)

        # Ligne 4 (Btn)
        self.btn_effacer = ttk.Button(
            frame_form,
            text="Effacer",
            image=self.icon_effacer,
            compound="left"
        )
        self.btn_effacer.grid(row=4, column=0, columnspan=4, pady=10)


    def _construire_actions(self) -> None:
        frame_actions = ttk.Frame(self.root, padding=10)
        frame_actions.pack(fill="x", padx=10, pady=5)

        self.btn_ajouter = ttk.Button(frame_actions, text="Ajouter", image=self.icon_add, compound="left")
        self.btn_ajouter.pack(side="left", padx=5)

        self.btn_rechercher = ttk.Button(frame_actions, text="Rechercher", image=self.icon_rechercher, compound="left")
        self.btn_rechercher.pack(side="left", padx=5)

        self.btn_modifier = ttk.Button(frame_actions, text="Modifier", image=self.icon_modifier, compound="left")
        self.btn_modifier.pack(side="left", padx=5)

        self.btn_supprimer = ttk.Button(frame_actions, text="Supprimer", image=self.icon_supprimer, compound="left")
        self.btn_supprimer.pack(side="left", padx=5)

        self.btn_afficher_tous = ttk.Button(frame_actions, text="Afficher tous", image=self.icon_afficher_tout, compound="left")
        self.btn_afficher_tous.pack(side="left", padx=5)

        self.btn_quitter = ttk.Button(frame_actions, text="Quitter", image=self.icon_quitter, compound="left")
        self.btn_quitter.pack(side="right", padx=5)
        
    def _construire_status_bar(self) -> None:
        frame_status = ttk.Frame(self.root, padding=(10, 5))
        frame_status.pack(fill="x", side="bottom")

        self.lbl_status = ttk.Label(
            frame_status,
            text="Contacts Affiche : 0",
            anchor="w"
        )
        self.lbl_status.pack(side="left")


    def mettre_a_jour_total_contacts(self, est_recherche: bool = False) -> None:
        total = len(self.tree.get_children())

        if est_recherche:
            self.lbl_status.config(text=f"Résultats de la recherche: {total}")
        else:    
            self.lbl_status.config(text=f"Contacts Affiche : {total}")


    def _construire_list(self) -> None:
        frame_list = ttk.Frame(self.root)
        frame_list.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("nom", "prenom", "telephone", "email", "adresse")

        style = ttk.Style()
        style.configure("Treeview", rowheight=32, font=(None, 10))
        style.configure("Treeview.Heading", font=(None, 10, "bold"))


        self.tree = ttk.Treeview(frame_list, columns=columns, show="headings")
        self.tree.heading("nom", text="Nom")
        self.tree.heading("prenom", text="Prénom")
        self.tree.heading("telephone", text="Téléphone")
        self.tree.heading("email", text="Email")
        self.tree.heading("adresse", text="Adresse")

        self.tree.column("nom", width=120)
        self.tree.column("prenom", width=120)
        self.tree.column("telephone", width=140)
        self.tree.column("email", width=220)
        self.tree.column("adresse", width=250)

        scrollbar = ttk.Scrollbar(frame_list, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def get_inputs(self):
        return {
            "nom": self.entry_nom.get().strip(),
            "prenom": self.entry_prenom.get().strip(),
            "telephone": self.entry_tel.get().strip(),
            "email": self.entry_email.get().strip(),
            "adresse": self.text_adresse.get("1.0", "end").strip(),
        }

    def effacer_inputs(self) -> None:
        self.entry_nom.delete(0, tk.END)
        self.entry_prenom.delete(0, tk.END)
        self.entry_tel.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.text_adresse.delete("1.0", "end")


    def set_inputs(self, contact):
        """Remplit les champs du formulaire avec les données du contact"""
        self.effacer_inputs()
        
        # Récupère les valeurs ou des chaînes vides si non définies
        nom = contact.get("nom", "")
        prenom = contact.get("prenom", "")
        telephone = str(contact.get("telephone", ""))
        email = contact.get("email", "")
        adresse = str(contact.get("adresse", ""))

        # Met à jour les champs
        self.entry_nom.insert(0, nom)
        self.entry_prenom.insert(0, prenom)
        self.entry_email.insert(0, email)
        self.text_adresse.insert("1.0", adresse)
        
        # Gestion spéciale pour téléphone
        if telephone:
            self.entry_tel.delete(0, tk.END)
            self.entry_tel.insert(0, telephone)
            self.entry_tel.config(foreground="black")

    def afficher_liste(self, liste_contacts):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for c in liste_contacts:
            #print(c.get("telephone", ""))
            contact_id = c.get("id")
            self.tree.insert(
                "",
                "end",
                iid=str(contact_id),
                values=(
                    c.get("nom", ""),
                    c.get("prenom", ""),
                    str(c.get("telephone", "")),
                    c.get("email", ""),
                    c.get("adresse", ""),
                ),
            )

        self.mettre_a_jour_total_contacts()

    def bind_raccourcie(self, sequence: str, callback) -> None:
        self.root.bind(sequence, callback)

    def get_contact_id_selectione(self):
        sel = self.tree.selection()
        if not sel:
            return None
        try:
            return int(sel[0])
        except Exception:
            return None

    def message_info(self, titre: str, message: str) -> None:
        messagebox.showinfo(titre, message)

    def message_erreur(self, titre: str, message: str) -> None:
        messagebox.showerror(titre, message)

    def message_confirmation(self, titre: str, message: str) -> bool:
        return bool(messagebox.askyesno(titre, message))
