import re
from typing import Any, Dict, Optional


class CarnetAdressesController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.view.btn_ajouter.config(command=self.ajouter_contact)
        self.view.btn_rechercher.config(command=self.rechercher_contact)
        self.view.btn_modifier.config(command=self.modifier_contact)
        self.view.btn_supprimer.config(command=self.supprimer_contact)
        self.view.btn_afficher_tous.config(command=self.afficher_tous)
        self.view.btn_effacer.config(command=self.effac)
        self.view.btn_quitter.config(command=self.quitter_application)


        self.view.tree.bind("<Double-1>", self._tree_double_click)
        #self.view.tree.bind("<<TreeviewSelect>>", self._tree_select)

        # Les raccourcis

        self.view.menu_fichier.entryconfig("Exporter CSV", command=self.exporter_tout_vers_csv)
        
        self.view.menu_fichier.entryconfig("Quitter", command=self.quitter_application)

        self.view.menu_edition.entryconfig("Modifier", command=self.modifier_contact)
        self.view.menu_edition.entryconfig("Supprimer", command=self.supprimer_contact)

        self.view.menu_edition.entryconfig("Rechercher", command=self.rechercher_contact)
        self.view.menu_edition.entryconfig("Ajouter", command=self.ajouter_contact)

        self.view.menu_affichage.entryconfig("Afficher tous", command=self.afficher_tous)


        self.view.bind_raccourcie("<Control-q>", lambda e: self.quitter_application())
        self.view.bind_raccourcie("<Control-n>", lambda e: self.ajouter_contact())
        self.view.bind_raccourcie("<Control-f>", lambda e: self.rechercher_contact())
        self.view.bind_raccourcie("<Control-m>", lambda e: self.modifier_contact())
        self.view.bind_raccourcie("<Delete>",   lambda e: self.supprimer_contact())
        self.view.bind_raccourcie("<Control-a>", lambda e: self.afficher_tous())


        self.afficher_tous()

        self.view.root.protocol("WM_DELETE_WINDOW", self.quitter_application)



    # pour teste les expression reguliare: https://regex101.com/

    def effac(self):
        self.view.effacer_inputs()
        self.view.tree.selection_remove(self.view.tree.selection())


    def _email_valide(self, email: str) -> bool:
        if not email:
            return True
        return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email))

    def _telephone_valide(self, telephone) -> bool:
        #print(telephone)
        # https://regex101.com/r/Wb3FRQ/1
        if not telephone:
            return True
        return bool(re.match(r"^(?:$|0[0-9]{8}|\+?[0-9]{7,15})$", telephone))

    def _valider_tout(self, data: Dict[str, Any]) -> bool:
        if not data.get("nom"):
            self.view.message_erreur("Erreur", "Le nom est obligatoire.")
            return False
        if not data.get("prenom"):
            self.view.message_erreur("Erreur", "Le prénom est obligatoire.")
            return False
        if not self._email_valide(data.get("email", "")):
            self.view.message_erreur("Erreur", "Email invalide.")
            return False
        
        if not self._telephone_valide(data.get("telephone", "")):
            self.view.message_erreur("Erreur", "Téléphone invalide.")
            return False
        
        return True
        
    def quitter_application(self) -> None:
        if self.view.message_confirmation(
            "Quitter",
            "Voulez-vous vraiment quitter l’application ?"
        ):
            self.view.root.quit()

    def verfie_deja_exist(self, data: Dict[str, Any]) -> bool:
        pass

    def exporter_tout_vers_csv(self) -> None:
        from tkinter import filedialog
        import csv
        import os

        contacts = self.model.afficher_tous()

        if not contacts:
            self.view.message_erreur("Erreur", "Aucun contact à exporter.")
            return

        fichier = filedialog.asksaveasfilename(
            title="Exporter les contacts",
            initialdir=os.getcwd(),  # dossier actuel de l'application
            defaultextension=".csv",
            filetypes=[("Fichier CSV", "*.csv")],
        )

        if not fichier:
            return

        try:
            with open(fichier, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f, delimiter=";")

                # en-têtes (sans ID)
                writer.writerow(["Nom", "Prénom", "Téléphone", "Email", "Adresse"])

                for c in contacts:
                    writer.writerow([
                        c["nom"],
                        c["prenom"],
                        c.get("telephone", ""),
                        c.get("email", ""),
                        c.get("adresse", ""),
                    ])

            self.view.message_info("Succès", "Contacts exportés avec succès.")

        except Exception as e:
            self.view.message_erreur("Erreur", f"Échec de l’export : {e}")


    def ajouter_contact(self) -> None:
        data = self.view.get_inputs()
        if not self._valider_tout(data):
            return

        self.model.ajouter_contact(
            data["nom"],
            data["prenom"],
            data.get("telephone", ""),
            data.get("email", ""),
            data.get("adresse", ""),
        )
        self.view.message_info("Succès", "Contact ajouté.")
        self.view.effacer_inputs()
        self.afficher_tous()

    def rechercher_contact(self) -> None:
        data = self.view.get_inputs()

        nom = data.get("nom") or None
        prenom = data.get("prenom") or None

        telephone = None if not (phone := data.get("telephone", "").strip()) else phone
        email = data.get("email") or None
        if not (nom or prenom or telephone or email):
            self.view.message_erreur(
                "Erreur",
                "Saisissez un critère (Nom, Prénom, Téléphone ou/et Email) pour rechercher.",
            )
            return

        resultats = self.model.rechercher_contact(nom=nom, prenom=prenom, telephone=telephone, email=email)
        self.view.afficher_liste(resultats)
        self.view.mettre_a_jour_total_contacts(est_recherche=True)

    def modifier_contact(self) -> None:
        contact_id = self.view.get_contact_id_selectione() # avoir juste le ID
        if contact_id is None:
            self.view.message_erreur("Erreur", "Sélectionnez un contact à modifier.")
            return

        data = self.view.get_inputs()
        if not self._valider_tout(data):
            return # arrête la fonction

        self.model.modifier_contact(
            contact_id,
            data["nom"],
            data["prenom"],
            data.get("telephone", ""),
            data.get("email", ""),
            data.get("adresse", ""),
        )
        self.view.message_info("Succès", "Contact modifié.")
        self.view.effacer_inputs()
        self.afficher_tous()

    def supprimer_contact(self) -> None:
        contact_id = self.view.get_contact_id_selectione()
        if contact_id is None:
            self.view.message_erreur("Erreur", "Sélectionnez un contact à supprimer.")
            return

        if not self.view.message_confirmation("Confirmation", "Supprimer ce contact ?"):
            return

        self.model.supprimer_contact(contact_id)
        self.view.message_info("Succès", "Contact supprimé.")
        self.view.effacer_inputs()
        self.afficher_tous()

    def afficher_tous(self) -> None:
        contacts = self.model.afficher_tous()
        self.view.afficher_liste(contacts)
        self.view.effacer_inputs()

    def _tree_select(self, event) -> None:
        self._charger_selectione_dans_form()

    def _tree_double_click(self, event) -> None:
        self._charger_selectione_dans_form()

    def _charger_selectione_dans_form(self) -> None:
        # ..?
        contact_id = self.view.get_contact_id_selectione()
        if contact_id is None:
            return

        contact = self.model.get_contact_par_id(contact_id)

        if not contact:
            return

        self.view.set_inputs(
            {
                "nom": contact["nom"],
                "prenom": contact["prenom"],
                "telephone": contact["telephone"],
                "email": contact["email"],
                "adresse": contact["adresse"],
            }
        )