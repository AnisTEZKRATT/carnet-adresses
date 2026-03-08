import sqlite3
from typing import Any, Dict, List, Optional

class ContactModel:
    def __init__(self, db_path: str = "contacts.db"):
        self.db_path = db_path
        self._init_db()

    def _etablir_conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._etablir_conn() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS contacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT NOT NULL,
                    prenom TEXT NOT NULL,
                    telephone TEXT,
                    email TEXT,
                    adresse TEXT
                )
                """
            )
            conn.commit()

    def get_contact_par_id(self, contact_id: int):
        with self._etablir_conn() as conn:
            ligne = conn.execute(
                """
                SELECT nom, prenom, telephone, email, adresse
                FROM contacts
                WHERE id = ?
                """,
                (contact_id,),
            ).fetchone()

        if not ligne:
            return None

        return dict(ligne)

    def ajouter_contact(
        self,
        nom: str,
        prenom: str,
        telephone: str = "",
        email: str = "",
        adresse: str = "",
    ) -> int:
        #print(telephone)
        with self._etablir_conn() as conn:
            cur = conn.execute(
                """
                INSERT INTO contacts (nom, prenom, telephone, email, adresse)
                VALUES (?, ?, ?, ?, ?)
                """,
                (nom, prenom, telephone, email, adresse),
            )
            conn.commit()
            return int(cur.lastrowid)

    def rechercher_contact(
        self,
        prenom: Optional[str] = None,
        nom: Optional[str] = None,
        telephone: Optional[str] = None,
        email: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        clauses = []
        params: List[Any] = []

        clauses = []
        params: list[Any] = []

        filtres_nom = {
            "nom": nom,
            "prenom": prenom,
        }

        name_clauses = [
            f"{col} LIKE ?"
            for col, value in filtres_nom.items()
            if value
        ]

        params.extend(
            f"%{value}%"
            for value in filtres_nom.values()
            if value
        )

        if name_clauses:
            clauses.append("(" + " AND ".join(name_clauses) + ")")

        autre_filtres = {
            "telephone": telephone,
            "email": email,
        }

        autre_clauses = [
            f"{col} LIKE ?"
            for col, value in autre_filtres.items()
            if value
        ]

        params.extend(
            f"%{value}%"
            for value in autre_filtres.values()
            if value
        )

        if autre_clauses:
            clauses.append("(" + " OR ".join(autre_clauses) + ")")

        where_sql = " AND ".join(clauses)

        query = """
            SELECT id, nom, prenom, telephone, email, adresse
            FROM contacts
        """

        if where_sql:
            query += f" WHERE {where_sql}"

        query += """
            ORDER BY nom COLLATE NOCASE ASC,
                    prenom COLLATE NOCASE ASC
        """

        with self._etablir_conn() as conn:
            rows = conn.execute(query, params).fetchall()

        return [dict(row) for row in rows]

        """

        if prenom:
            clauses.append("prenom LIKE ?")
            params.append(f"%{prenom}%")

        if nom:
            clauses.append("nom LIKE ?")
            params.append(f"%{nom}%")
        if telephone:
            clauses.append("telephone LIKE ?")
            params.append(f"%{telephone}%")
        if email:
            clauses.append("email LIKE ?")
            params.append(f"%{email}%")

        if not clauses:
            return []

        where_sql = " OR ".join(clauses)

        with self._etablir_conn() as conn:
            rows = conn.execute(
                f'''
                SELECT id, nom, prenom, telephone, email, adresse
                FROM contacts
                WHERE {where_sql}
                ORDER BY nom COLLATE NOCASE ASC, prenom COLLATE NOCASE ASC
                ''',
                params,
            ).fetchall()

        return [dict(r) for r in rows]
        
        """

    def modifier_contact(
        self,
        contact_id: int,
        nom: str,
        prenom: str,
        telephone: str = "",
        email: str = "",
        adresse: str = "",
    ) -> None:
        with self._etablir_conn() as conn:
            conn.execute(
                """
                UPDATE contacts
                SET nom = ?, prenom = ?, telephone = ?, email = ?, adresse = ?
                WHERE id = ?
                """,
                (nom, prenom, telephone, email, adresse, contact_id),
            )
            conn.commit()

    def supprimer_contact(self, contact_id: int) -> None:
        with self._etablir_conn() as conn:
            conn.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
            conn.commit()

    def afficher_tous(self) -> List[Dict[str, Any]]:
        with self._etablir_conn() as conn:
            lignes = conn.execute(
                """
                SELECT id, nom, prenom, telephone, email, adresse
                FROM contacts
                ORDER BY nom COLLATE NOCASE ASC, prenom COLLATE NOCASE ASC
                """
            ).fetchall()
        return [dict(r) for r in lignes]
