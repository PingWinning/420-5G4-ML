import customtkinter as ctk


def main() -> None:
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("Test CustomTkinter")
    app.geometry("480x320")

    label = ctk.CTkLabel(app, text="Fenêtre de test CustomTkinter")
    label.pack(expand=True)

    app.mainloop()


if __name__ == "__main__":
    main()
