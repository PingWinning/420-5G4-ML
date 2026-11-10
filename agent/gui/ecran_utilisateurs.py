from tkinter import ttk

import customtkinter as ctk

from theme import (
    COULEUR_BORDURE,
    COULEUR_FOND,
    COULEUR_FOOTER,
    COULEUR_PRIMAIRE,
    COULEUR_PRIMAIRE_SURVOL,
    COULEUR_SIDEBAR,
    COULEUR_TEXTE,
    COULEUR_TEXTE_PLACEHOLDER,
    COULEUR_TEXTE_SECONDAIRE,
    HAUTEUR_BOUTON,
    HAUTEUR_CHAMP,
    HAUTEUR_PIED,
    POLICE_BOUTON,
    POLICE_NORMALE,
    POLICE_PANNEAU,
    POLICE_PETITE,
    POLICE_TITRE,
    RAYON,
    STYLE_TABLEAU,
)

COLONNES = (
    ("nom", "Nom", 250, 150),
    ("id", "ID", 140, 100),
    ("livres", "Livres empruntés", 140, 120),
)


class EcranUtilisateurs(ctk.CTkFrame):
    def __init__(self, parent: ctk.CTkFrame) -> None:
        super().__init__(parent, fg_color=COULEUR_FOND, corner_radius=0)
        self._construire_pied()
        self._construire_contenu()

    def _construire_pied(self) -> None:
        pied = ctk.CTkFrame(
            self,
            height=HAUTEUR_PIED,
            fg_color=COULEUR_FOOTER,
            corner_radius=0,
        )
        pied.pack(side="bottom", fill="x")
        pied.pack_propagate(False)

        texte = ctk.CTkLabel(
            pied,
            text="0 utilisateur",
            height=HAUTEUR_PIED,
            font=POLICE_PETITE,
            text_color=COULEUR_TEXTE_SECONDAIRE,
            anchor="w",
        )
        texte.pack(side="left", padx=14)

    def _construire_contenu(self) -> None:
        contenu = ctk.CTkFrame(self, fg_color=COULEUR_FOND, corner_radius=0)
        contenu.pack(fill="both", expand=True, padx=24, pady=20)

        titre = ctk.CTkLabel(
            contenu,
            text="Liste des utilisateurs",
            height=24,
            font=POLICE_TITRE,
            text_color=COULEUR_TEXTE,
            anchor="w",
        )
        titre.pack(fill="x")

        corps = ctk.CTkFrame(contenu, fg_color="transparent")
        corps.pack(fill="both", expand=True, pady=(12, 0))
        corps.grid_columnconfigure(0, weight=1)
        corps.grid_columnconfigure(1, weight=0, minsize=280)
        corps.grid_rowconfigure(0, weight=1)

        self._construire_tableau(corps)
        self._construire_panneau(corps)

    def _construire_tableau(self, parent: ctk.CTkFrame) -> None:
        cadre_tableau = ctk.CTkFrame(
            parent,
            fg_color=COULEUR_FOND,
            corner_radius=RAYON,
            border_width=1,
            border_color=COULEUR_BORDURE,
        )
        cadre_tableau.grid(row=0, column=0, sticky="nsew", padx=(0, 20))

        self.tableau = ttk.Treeview(
            cadre_tableau,
            style=STYLE_TABLEAU,
            columns=[colonne[0] for colonne in COLONNES],
            show="headings",
            selectmode="browse",
            height=10,
        )
        self.tableau.pack(fill="both", expand=True, padx=1, pady=1)

        for cle, titre, largeur, largeur_min in COLONNES:
            self.tableau.heading(cle, text=titre, anchor="w")
            self.tableau.column(
                cle,
                width=largeur,
                minwidth=largeur_min,
                anchor="w",
                stretch=True,
            )

    def _construire_panneau(self, parent: ctk.CTkFrame) -> None:
        panneau = ctk.CTkFrame(
            parent,
            width=280,
            fg_color=COULEUR_FOND,
            corner_radius=RAYON,
            border_width=1,
            border_color=COULEUR_BORDURE,
        )
        panneau.grid(row=0, column=1, sticky="new")

        titre = ctk.CTkLabel(
            panneau,
            text="Ajouter un utilisateur",
            height=22,
            font=POLICE_PANNEAU,
            text_color=COULEUR_TEXTE,
            anchor="w",
        )
        titre.pack(fill="x", padx=16, pady=(16, 12))

        label_nom = ctk.CTkLabel(
            panneau,
            text="Nom",
            height=18,
            font=POLICE_PETITE,
            text_color=COULEUR_TEXTE_SECONDAIRE,
            anchor="w",
        )
        label_nom.pack(fill="x", padx=16, pady=(0, 4))

        champ_nom = ctk.CTkEntry(
            panneau,
            height=HAUTEUR_CHAMP,
            corner_radius=RAYON,
            border_width=1,
            border_color=COULEUR_BORDURE,
            fg_color=COULEUR_FOND,
            text_color=COULEUR_TEXTE,
            font=POLICE_NORMALE,
        )
        champ_nom.pack(fill="x", padx=16, pady=(0, 12))

        label_id = ctk.CTkLabel(
            panneau,
            text="ID utilisateur",
            height=18,
            font=POLICE_PETITE,
            text_color=COULEUR_TEXTE_SECONDAIRE,
            anchor="w",
        )
        label_id.pack(fill="x", padx=16, pady=(0, 4))

        champ_id = ctk.CTkEntry(
            panneau,
            height=HAUTEUR_CHAMP,
            corner_radius=RAYON,
            border_width=1,
            border_color=COULEUR_BORDURE,
            fg_color=COULEUR_SIDEBAR,
            text_color=COULEUR_TEXTE,
            placeholder_text="USR—",
            placeholder_text_color=COULEUR_TEXTE_PLACEHOLDER,
            font=POLICE_NORMALE,
            state="disabled",
        )
        champ_id.pack(fill="x", padx=16, pady=(0, 16))

        bouton = ctk.CTkButton(
            panneau,
            text="Ajouter",
            height=HAUTEUR_BOUTON,
            corner_radius=RAYON,
            fg_color=COULEUR_PRIMAIRE,
            hover_color=COULEUR_PRIMAIRE_SURVOL,
            text_color="#ffffff",
            font=POLICE_BOUTON,
        )
        bouton.pack(fill="x", padx=16, pady=(0, 16))
