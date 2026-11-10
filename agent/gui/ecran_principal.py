from tkinter import ttk

import customtkinter as ctk

from dialogue_ajout_livre import DialogueAjoutLivre
from dialogue_emprunt_livre import DialogueEmpruntLivre
from theme import (
    COULEUR_BORDURE,
    COULEUR_FOND,
    COULEUR_PRIMAIRE,
    COULEUR_PRIMAIRE_SURVOL,
    COULEUR_SURVOL,
    COULEUR_TEXTE,
    COULEUR_TEXTE_MENU,
    COULEUR_TEXTE_PLACEHOLDER,
    COULEUR_TEXTE_SECONDAIRE,
    HAUTEUR_BOUTON,
    HAUTEUR_CHAMP,
    POLICE_BOUTON,
    POLICE_BOUTON_SECONDAIRE,
    POLICE_NORMALE,
    POLICE_PETITE,
    RAYON,
    STYLE_TABLEAU,
)

COLONNES = (
    ("titre", "Titre", 210, 120),
    ("auteur", "Auteur", 210, 120),
    ("isbn", "ISBN", 150, 110),
    ("statut", "Statut", 100, 90),
    ("emprunteur", "Emprunteur", 100, 90),
)


class EcranPrincipal(ctk.CTkFrame):
    def __init__(self, parent: ctk.CTkFrame) -> None:
        super().__init__(parent, fg_color=COULEUR_FOND, corner_radius=0)
        self._construire_filtres()
        self._construire_tableau()
        self._construire_actions()

    def _construire_filtres(self) -> None:
        filtres = ctk.CTkFrame(self, fg_color="transparent")
        filtres.pack(fill="x", padx=24, pady=(20, 12))
        filtres.grid_columnconfigure(0, weight=1)
        filtres.grid_columnconfigure(1, weight=0)
        filtres.grid_columnconfigure(2, weight=0)

        label_rechercher = ctk.CTkLabel(
            filtres,
            text="Rechercher",
            height=18,
            font=POLICE_PETITE,
            text_color=COULEUR_TEXTE_SECONDAIRE,
            anchor="w",
        )
        label_rechercher.grid(row=0, column=0, sticky="w", padx=(0, 12), pady=(0, 4))

        champ_recherche = ctk.CTkEntry(
            filtres,
            height=HAUTEUR_CHAMP,
            corner_radius=RAYON,
            border_width=1,
            border_color=COULEUR_BORDURE,
            fg_color=COULEUR_FOND,
            text_color=COULEUR_TEXTE,
            placeholder_text="Titre ou auteur…",
            placeholder_text_color=COULEUR_TEXTE_PLACEHOLDER,
            font=POLICE_NORMALE,
        )
        champ_recherche.grid(row=1, column=0, sticky="ew", padx=(0, 12))

        label_par = ctk.CTkLabel(
            filtres,
            text="Par",
            height=18,
            font=POLICE_PETITE,
            text_color=COULEUR_TEXTE_SECONDAIRE,
            anchor="w",
        )
        label_par.grid(row=0, column=1, sticky="w", padx=(0, 12), pady=(0, 4))

        choix_tri = ctk.CTkComboBox(
            filtres,
            values=["Titre", "Auteur", "ISBN"],
            width=140,
            height=HAUTEUR_CHAMP,
            corner_radius=RAYON,
            border_width=1,
            border_color=COULEUR_BORDURE,
            fg_color=COULEUR_FOND,
            button_color=COULEUR_FOND,
            button_hover_color=COULEUR_SURVOL,
            text_color=COULEUR_TEXTE,
            dropdown_fg_color=COULEUR_FOND,
            dropdown_hover_color=COULEUR_SURVOL,
            dropdown_text_color=COULEUR_TEXTE,
            font=POLICE_NORMALE,
            dropdown_font=POLICE_NORMALE,
            state="readonly",
        )
        choix_tri.set("Titre")
        choix_tri.grid(row=1, column=1, sticky="w", padx=(0, 12))

        disponibles = ctk.CTkCheckBox(
            filtres,
            text="Disponibles seulement",
            font=POLICE_NORMALE,
            text_color=COULEUR_TEXTE_MENU,
            fg_color=COULEUR_PRIMAIRE,
            hover_color=COULEUR_PRIMAIRE_SURVOL,
            border_color=COULEUR_BORDURE,
            checkbox_width=14,
            checkbox_height=14,
            corner_radius=3,
        )
        disponibles.grid(row=1, column=2, sticky="w")

    def _construire_tableau(self) -> None:
        cadre_tableau = ctk.CTkFrame(
            self,
            fg_color=COULEUR_FOND,
            corner_radius=RAYON,
            border_width=1,
            border_color=COULEUR_BORDURE,
        )
        cadre_tableau.pack(fill="both", expand=True, padx=24)

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

    def _construire_actions(self) -> None:
        actions = ctk.CTkFrame(self, fg_color="transparent")
        actions.pack(fill="x", padx=24, pady=(16, 20))

        bouton_ajouter = self._bouton_primaire(
            actions,
            "Ajouter un livre",
            150,
            commande=self._ouvrir_dialogue_ajout,
        )
        bouton_ajouter.pack(side="left")

        for texte, largeur, commande in (
            ("Supprimer", 100, None),
            ("Emprunter", 100, self._ouvrir_dialogue_emprunt),
            ("Retourner", 100, None),
        ):
            bouton = self._bouton_secondaire(
                actions,
                texte,
                largeur,
                commande,
            )
            bouton.pack(side="left", padx=(10, 0))

        bouton_copie = self._bouton_secondaire(actions, "Créer une copie", 140)
        bouton_copie.pack(side="right")

        bouton_sauvegarder = self._bouton_secondaire(actions, "Sauvegarder", 130)
        bouton_sauvegarder.pack(side="right", padx=(0, 10))

    def _ouvrir_dialogue_ajout(self) -> None:
        dialogue = DialogueAjoutLivre(self.winfo_toplevel())
        self.wait_window(dialogue)

    def _ouvrir_dialogue_emprunt(self) -> None:
        dialogue = DialogueEmpruntLivre(self.winfo_toplevel())
        self.wait_window(dialogue)

    def _bouton_primaire(
        self,
        parent: ctk.CTkFrame,
        texte: str,
        largeur: int,
        commande=None,
    ) -> ctk.CTkButton:
        return ctk.CTkButton(
            parent,
            text=texte,
            command=commande,
            width=largeur,
            height=HAUTEUR_BOUTON,
            corner_radius=RAYON,
            fg_color=COULEUR_PRIMAIRE,
            hover_color=COULEUR_PRIMAIRE_SURVOL,
            text_color="#ffffff",
            font=POLICE_BOUTON,
        )

    def _bouton_secondaire(
        self,
        parent: ctk.CTkFrame,
        texte: str,
        largeur: int,
        commande=None,
    ) -> ctk.CTkButton:
        return ctk.CTkButton(
            parent,
            text=texte,
            command=commande,
            width=largeur,
            height=HAUTEUR_BOUTON,
            corner_radius=RAYON,
            fg_color=COULEUR_FOND,
            hover_color=COULEUR_SURVOL,
            border_width=1,
            border_color=COULEUR_BORDURE,
            text_color=COULEUR_TEXTE,
            font=POLICE_BOUTON_SECONDAIRE,
        )
