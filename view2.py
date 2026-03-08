import logging
import tkinter as tk
from tkinter import font
from tkinter import messagebox

import ttkbootstrap as tb

logger = logging.getLogger(__name__)
if not logger.handlers:
    _handler = logging.StreamHandler()
    _handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s"))
    logger.addHandler(_handler)
logger.setLevel(logging.INFO)
logger.propagate = False


class CarnetAdressesView:
    def __init__(self):
        try:
            from ctypes import windll

            windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass

        self.root = tb.Window(themename="flatly")
        self.root.title("Carnet d’adresses")
        self.root.geometry("1080x900")
        self.root.minsize(1080, 900)

        font_par_df = font.nametofont("TkDefaultFont")
        font_par_df.configure(family="Segoe UI", size=10)


        import sys

        self._icon = tk.PhotoImage(file="./icons/user2.png")
        self.root.iconphoto(True, self._icon)

        if sys.platform.startswith("win"):
            self.root.iconbitmap("./icons/user2.ico")


        self.icon_add = tk.PhotoImage(file="icons/add2.png")
        self.icon_effacer = tk.PhotoImage(file="./icons/effacer.png")
        self.icon_rechercher = tk.PhotoImage(file="./icons/rechercher.png")
        self.icon_modifier = tk.PhotoImage(file="./icons/modify.png")
        self.icon_afficher_tout = tk.PhotoImage(file="./icons/affichertout.png")
        self.icon_quitter = tk.PhotoImage(file="./icons/quit.png")
        self.icon_supprimer = tk.PhotoImage(file="./icons/delete.png")

        self._construire_menu()
        self._construire_form()
        self._construire_actions()
        self._construire_list()
        self._construire_status_bar()

        logger.info("Vue ttkbootstrap initialisée")

    def _construire_menu(self) -> None:
        menubar = tk.Menu(self.root)

        self.menu_fichier = tk.Menu(menubar, tearoff=0)
        self.menu_fichier.add_command(label="Exporter CSV")
        self.menu_fichier.add_separator()
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
            "Développée pour le projet IHM",
        )

    def _construire_form(self) -> None:
        frame_form = tb.Labelframe(self.root, text="Informations du contact", padding=10)
        frame_form.pack(padx=10, pady=10, anchor="center")

        tb.Label(frame_form, text="Nom").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.entry_nom = tb.Entry(frame_form, width=30)
        self.entry_nom.grid(row=0, column=1, padx=5, pady=5)

        tb.Label(frame_form, text="Prénom").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.entry_prenom = tb.Entry(frame_form, width=30)
        self.entry_prenom.grid(row=0, column=3, padx=5, pady=5)

        tb.Label(frame_form, text="Téléphone").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.entry_tel = tb.Entry(frame_form, width=30)
        self.entry_tel.grid(row=1, column=1, padx=5, pady=(5, 0))

        tb.Label(frame_form, text="Email").grid(row=1, column=2, sticky="w", padx=5, pady=5)
        self.entry_email = tb.Entry(frame_form, width=30)
        self.entry_email.grid(row=1, column=3, padx=5, pady=5)

        tb.Label(
            frame_form,
            text="Ex: 0534…, +21364…, 21364…",
            font=("Segoe UI", 8),
            foreground="#666666",
        ).grid(row=2, column=1, sticky="w", padx=5, pady=(0, 5))

        tb.Label(frame_form, text="Adresse").grid(row=3, column=0, sticky="nw", padx=5, pady=(12, 5))

        self.text_adresse = tk.Text(frame_form, height=3, width=67, wrap="word")
        self.text_adresse.grid(row=3, column=1, columnspan=3, padx=5, pady=(12, 5), sticky="w")

        scroll_adresse = tb.Scrollbar(frame_form, orient="vertical", command=self.text_adresse.yview)
        scroll_adresse.grid(row=3, column=4, sticky="ns", padx=(0, 5), pady=(12, 5))
        self.text_adresse.configure(yscrollcommand=scroll_adresse.set)

        self.btn_effacer = tb.Button(
            frame_form,
            text="Effacer",
            image=self.icon_effacer,
            compound="left",
            bootstyle="secondary",
        )
        self.btn_effacer.grid(row=4, column=0, columnspan=4, pady=10)

    def _construire_actions(self) -> None:
        frame_actions = tb.Frame(self.root, padding=10)
        frame_actions.pack(fill="x", padx=10, pady=5)

        self.btn_ajouter = tb.Button(
            frame_actions, text="Ajouter", image=self.icon_add, compound="left", bootstyle="success"
        )
        self.btn_ajouter.pack(side="left", padx=5)

        self.btn_rechercher = tb.Button(
            frame_actions,
            text="Rechercher",
            image=self.icon_rechercher,
            compound="left",
            bootstyle="info",
        )
        self.btn_rechercher.pack(side="left", padx=5)

        self.btn_modifier = tb.Button(
            frame_actions,
            text="Modifier",
            image=self.icon_modifier,
            compound="left",
            bootstyle="warning",
        )
        self.btn_modifier.pack(side="left", padx=5)

        self.btn_supprimer = tb.Button(
            frame_actions,
            text="Supprimer",
            image=self.icon_supprimer,
            compound="left",
            bootstyle="danger",
        )
        self.btn_supprimer.pack(side="left", padx=5)

        self.btn_afficher_tous = tb.Button(
            frame_actions,
            text="Afficher tous",
            image=self.icon_afficher_tout,
            compound="left",
            bootstyle="primary",
        )
        self.btn_afficher_tous.pack(side="left", padx=5)

        self.btn_quitter = tb.Button(
            frame_actions, text="Quitter", image=self.icon_quitter, compound="left", bootstyle="secondary"
        )
        self.btn_quitter.pack(side="right", padx=5)

    def _construire_status_bar(self) -> None:
        frame_status = tb.Frame(self.root, padding=(10, 5))
        frame_status.pack(fill="x", side="bottom")

        self.lbl_status = tb.Label(
            frame_status,
            text="Contacts Affiche : 0",
            anchor="w",
        )
        self.lbl_status.pack(side="left")

        self._theme_var = tk.StringVar(value=self.root.style.theme_use())

        theme_frame = tb.Frame(frame_status)
        theme_frame.pack(side="right")

        tb.Label(theme_frame, text="Thème").pack(side="left", padx=(0, 6))

        theme_names = list(self.root.style.theme_names())
        self.cmb_theme = tb.Combobox(
            theme_frame,
            values=theme_names,
            textvariable=self._theme_var,
            state="readonly",
            width=18,
        )
        self.cmb_theme.pack(side="left")
        self.cmb_theme.bind("<<ComboboxSelected>>", self._on_theme_selected)


    def _on_theme_selected(self, event=None) -> None:
        theme = self._theme_var.get()
        try:
            logger.info("Changement de thème: %s", theme)
            self.root.style.theme_use(theme)
        except Exception:
            logger.exception("Échec du changement de thème")

    def mettre_a_jour_total_contacts(self, est_recherche: bool = False) -> None:
        total = len(self.tree.get_children())

        if est_recherche:
            self.lbl_status.config(text=f"Résultats de la recherche: {total}")
        else:    
            self.lbl_status.config(text=f"Contacts Affiche : {total}")

    def _construire_list(self) -> None:
        frame_list = tb.Frame(self.root)
        frame_list.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("nom", "prenom", "telephone", "email", "adresse")

        style = tb.Style()
        style.configure("Treeview", rowheight=32, font=(None, 10))
        style.configure("Treeview.Heading", font=(None, 10, "bold"))

        self.tree = tb.Treeview(frame_list, columns=columns, show="headings")
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

        scrollbar = tb.Scrollbar(frame_list, orient="vertical", command=self.tree.yview)
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
        self.effacer_inputs()

        nom = contact.get("nom", "")
        prenom = contact.get("prenom", "")
        telephone = str(contact.get("telephone", ""))
        email = contact.get("email", "")
        adresse = str(contact.get("adresse", ""))

        self.entry_nom.insert(0, nom)
        self.entry_prenom.insert(0, prenom)
        self.entry_email.insert(0, email)
        self.text_adresse.insert("1.0", adresse)

        if telephone:
            self.entry_tel.delete(0, tk.END)
            self.entry_tel.insert(0, telephone)

    def afficher_liste(self, liste_contacts):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for c in liste_contacts:
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
