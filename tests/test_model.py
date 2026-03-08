import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model import ContactModel

test_contacts = [
    {"nom": "Sahraoui", "prenom": "Aris", "telephone": "", "email": "aris.sahraoui@fgei.ummto.dz", "adresse": "Makouda, Cite 200 logs"},
    {"nom": "Doe", "prenom": "John", "telephone": "0534123456", "email": "john.doe@example.com", "adresse": "123 Rue de Paris, Alger"},
    {"nom": "Smith", "prenom": "Jane", "telephone": "+213661234567", "email": "jane.smith@example.com", "adresse": "45 Avenue Didouche Mourad, Alger"},
    {"nom": "Mansouri", "prenom": "Ali", "telephone": "0555123456", "email": "ali.mansouri@example.com", "adresse": "78 Boulevard Krim Belkacem, Tizi Ouzou"},
    {"nom": "Benali", "prenom": "Sofia", "telephone": "+213540123456", "email": "sofia.benali@example.com", "adresse": "12 Rue Didouche, Oran"},
    {"nom": "Cherif", "prenom": "Karim", "telephone": "", "email": "karim.cherif@example.com", "adresse": "7 Place des Martyrs, Constantine"},

    {"nom": "AitAhmed", "prenom": "Yacine", "telephone": "0778123456", "email": "yacine.a@example.com", "adresse": "Rue des Frères Oukil, Tizi Ouzou"},
    {"nom": "Boumediene", "prenom": "Nadia", "telephone": "0667123987", "email": "nadia.b@example.com", "adresse": "Hai El Badr, Annaba"},
    {"nom": "Khelifi", "prenom": "Omar", "telephone": "+213698765432", "email": "omar.k@example.com", "adresse": "Cité 500 Logements, Blida"},
    {"nom": "Rahmani", "prenom": "Lina", "telephone": "0541122334", "email": "lina.rahmani@example.com", "adresse": "Rue Emir Abdelkader, Bejaia"},
    {"nom": "Zerrouki", "prenom": "Hichem", "telephone": "0560456789", "email": "hichem.z@example.com", "adresse": "Centre-ville, Bouira"},

    {"nom": "Bensaid", "prenom": "Amel", "telephone": "", "email": "amel.bensaid@example.com", "adresse": "Cité Universitaire, Alger"},
    {"nom": "Toumi", "prenom": "Reda", "telephone": "0654321987", "email": "", "adresse": "Rue de la Gare, Setif"},
    {"nom": "Hamdi", "prenom": "Salim", "telephone": "0777001122", "email": "salim.hamdi@example.com", "adresse": "Quartier El Menzah, Alger"},
    {"nom": "Boukhalfa", "prenom": "Imene", "telephone": "+213550334455", "email": "imene.b@example.com", "adresse": "Hai Essalem, Batna"},
    {"nom": "Saidi", "prenom": "Nour", "telephone": "0522003344", "email": "nour.saidi@example.com", "adresse": "Rue Larbi Ben M'hidi, Skikda"},

    {"nom": "Meziani", "prenom": "Farid", "telephone": "0678456123", "email": "farid.m@example.com", "adresse": "Centre-ville, Medea"},
    {"nom": "Abdelkader", "prenom": "Rania", "telephone": "0549988776", "email": "rania.abk@example.com", "adresse": "Rue 1er Novembre, Mostaganem"},
    {"nom": "OuldAli", "prenom": "Mohamed", "telephone": "+213662345678", "email": "m.ouldali@example.com", "adresse": "Cité Ennasr, Ouargla"},
    {"nom": "Yahiaoui", "prenom": "Samir", "telephone": "0556677889", "email": "", "adresse": "Zone industrielle, Relizane"},
    {"nom": "Haddad", "prenom": "Asma", "telephone": "0533445566", "email": "asma.haddad@example.com", "adresse": "Rue de l'Indépendance, Jijel"},

    {"nom": "Lakhdar", "prenom": "Bilal", "telephone": "0789123456", "email": "bilal.l@example.com", "adresse": "Hai El Nour, Ghardaia"},
    {"nom": "Guettaf", "prenom": "Sara", "telephone": "", "email": "sara.g@example.com", "adresse": "Centre-ville, El Oued"},
    {"nom": "Mokhtar", "prenom": "Anis", "telephone": "0666012345", "email": "anis.m@example.com", "adresse": "Rue Ahmed Zabana, Oran"},
    {"nom": "Boudjemaa", "prenom": "Yasmine", "telephone": "+213558889900", "email": "yasmine.b@example.com", "adresse": "Cité 1000 Logements, Sidi Bel Abbès"},
    {"nom": "Kerrouche", "prenom": "Adel", "telephone": "0543210987", "email": "adel.k@example.com", "adresse": "Rue des Palmiers, Chlef"}
]


class TestContactModel(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.model = ContactModel(db_path="contacts.db")

        for contact in cls.model.afficher_tous():
            cls.model.supprimer_contact(contact["id"])

    def test_ajouter_contacts(self):
        for c in test_contacts:
            self.model.ajouter_contact(
                nom=c["nom"],
                prenom=c["prenom"],
                telephone=c.get("telephone", ""),
                email=c.get("email", ""),
                adresse=c.get("adresse", "")
            )

        tout_contacts = self.model.afficher_tous()
        self.assertEqual(len(tout_contacts), len(test_contacts))

        noms_db = {(c["nom"], c["prenom"]) for c in tout_contacts}
        noms_attendus = {(c["nom"], c["prenom"]) for c in test_contacts}
        self.assertSetEqual(noms_db, noms_attendus)


if __name__ == "__main__":
    unittest.main()
