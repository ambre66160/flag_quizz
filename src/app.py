import customtkinter as ctk
from PIL import Image
from src.logic import QuizGame

# Palette Option 3 : Vert Sauge / Naturel
COLOR_BG = "#8A9A86"          # Vert Sauge / Olive clair (Fond principal)
COLOR_CARD = "#F4F6F0"        # Blanc cassé / Crème doux (Carte centrale)
COLOR_TEXT = "#1C2E20"        # Vert forêt très foncé (Textes)
COLOR_PRIMARY = "#3A5A40"     # Vert olive profond (Boutons)
COLOR_PRIMARY_HOVER = "#2D4732"
COLOR_INPUT_BORDER = "#A3B19B"# Vert sauge adouci
COLOR_SUCCESS = "#588157"     # Vert feuillage (Victoire)
COLOR_WARNING = "#D4A373"     # Terracotta / Cuivre doux (Passer)

ctk.set_appearance_mode("light")

class FlagQuizApp(ctk.CTk):
    def __init__(self, duration_seconds: int = 60):
        super().__init__()

        self.title("🌿 Quiz Drapeau 🌿")
        self.geometry("520x670")
        self.configure(fg_color=COLOR_BG)
        self.resizable(False, False)

        self.duration = duration_seconds
        self.time_left = self.duration
        self.timer_job = None

        self.game = QuizGame("data/countries.json", time_limit=self.duration)
        
        self.setup_ui()
        self.start_game()

    def setup_ui(self):
        # Header (Chrono, Score, Série)
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=20, pady=(15, 5))

        self.timer_label = ctk.CTkLabel(
            self.header_frame, 
            text=f"⏱️ {self.time_left}s", 
            font=("Poppins", 16, "bold"),
            text_color="#F4F6F0"
        )
        self.timer_label.pack(side="left")

        self.streak_label = ctk.CTkLabel(
            self.header_frame, 
            text="Série: 🔥 0", 
            font=("Poppins", 16, "bold"),
            text_color="#F4F6F0"
        )
        self.streak_label.pack(side="right")

        self.score_label = ctk.CTkLabel(
            self.header_frame, 
            text="Score: 0", 
            font=("Poppins", 16, "bold"),
            text_color="#F4F6F0"
        )
        self.score_label.pack(side="right", padx=20)

        # Carte centrale unique (disposition verticale)
        self.card = ctk.CTkFrame(self, fg_color=COLOR_CARD, corner_radius=20)
        self.card.pack(fill="both", expand=True, padx=20, pady=15)

        # Question / Titre
        self.question_label = ctk.CTkLabel(
            self.card, 
            text="Quel est ce pays ?", 
            font=("Poppins", 20, "bold"),
            text_color=COLOR_TEXT
        )
        self.question_label.pack(pady=(20, 10))

        # Drapeau au-dessus du champ de texte
        self.flag_label = ctk.CTkLabel(self.card, text="")
        self.flag_label.pack(pady=10)

        # Champ de saisie
        self.entry = ctk.CTkEntry(
            self.card,
            placeholder_text="Entrez le nom du pays...",
            width=320,
            height=45,
            corner_radius=12,
            border_color=COLOR_INPUT_BORDER,
            border_width=2,
            font=("Poppins", 14),
            text_color=COLOR_TEXT
        )
        self.entry.pack(pady=10)
        self.entry.bind("<Return>", lambda event: self.validate())

        # Feedback
        self.feedback_label = ctk.CTkLabel(
            self.card, 
            text="", 
            font=("Poppins", 13, "bold"),
            text_color=COLOR_TEXT
        )
        self.feedback_label.pack(pady=5)

        # Bouton Valider
        self.btn_validate = ctk.CTkButton(
            self.card,
            text="VALIDER",
            fg_color=COLOR_PRIMARY,
            hover_color=COLOR_PRIMARY_HOVER,
            text_color="#FFFFFF",
            font=("Poppins", 14, "bold"),
            height=45,
            width=320,
            corner_radius=12,
            command=self.validate
        )
        self.btn_validate.pack(pady=5)

        # Bouton Passer
        self.btn_skip = ctk.CTkButton(
            self.card,
            text="Je ne sais pas ",
            fg_color="transparent",
            text_color=COLOR_WARNING,
            hover_color="#E9ECE0",
            font=("Poppins", 12),
            command=self.skip
        )
        self.btn_skip.pack(pady=(5, 15))

    def start_game(self):
        self.game.reset_game()
        self.time_left = self.duration
        self.update_timer()
        self.load_next_question()

    def update_timer(self):
        self.timer_label.configure(text=f"⏱️ {self.time_left}s")

        if self.time_left <= 10:
            self.timer_label.configure(text_color="#BC4749")
        else:
            self.timer_label.configure(text_color="#F4F6F0")

        if self.time_left > 0:
            self.time_left -= 1
            self.timer_job = self.after(1000, self.update_timer)
        else:
            self.end_game()

    def load_next_question(self):
        self.entry.delete(0, "end")
        self.entry.configure(border_color=COLOR_INPUT_BORDER)
        self.feedback_label.configure(text="")

        country = self.game.next_question()

        try:
            img = Image.open(country["flag"])
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(270, 180))
            self.flag_label.configure(image=ctk_img)
        except Exception:
            self.flag_label.configure(text="[ Image introuvable ]", image=None)

    def validate(self):
        if self.time_left <= 0:
            return

        user_input = self.entry.get()
        if not user_input.strip():
            return

        is_correct, official_name = self.game.submit_answer(user_input)
        
        self.score_label.configure(text=f"Score: {self.game.score}")
        self.streak_label.configure(text=f"Série: 🔥 {self.game.streak}")

        if is_correct:
            self.entry.configure(border_color=COLOR_SUCCESS)
            self.feedback_label.configure(text="Bravo ! ✨", text_color=COLOR_SUCCESS)
            self.after(500, self.load_next_question)
        else:
            self.entry.configure(border_color="#BC4749")
            self.feedback_label.configure(
                text=f"Dommage ! C'était : {official_name}", 
                text_color="#BC4749"
            )
            self.after(1000, self.load_next_question)

    def skip(self):
        if self.time_left <= 0:
            return

        country = self.game.current_country
        self.game.streak = 0
        self.game.total_answered += 1
        self.streak_label.configure(text="Série: 🔥 0")
        self.feedback_label.configure(
            text=f"Réponse : {country['name']}", 
            text_color=COLOR_WARNING
        )
        self.after(800, self.load_next_question)

    def end_game(self):
        if self.timer_job:
            self.after_cancel(self.timer_job)

        self.card.pack_forget()
        
        self.end_frame = ctk.CTkFrame(self, fg_color=COLOR_CARD, corner_radius=20)
        self.end_frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(
            self.end_frame, 
            text="Temps écoulé ! ⏳", 
            font=("Poppins", 24, "bold"),
            text_color=COLOR_PRIMARY
        ).pack(pady=(40, 15))

        ctk.CTkLabel(
            self.end_frame, 
            text=f"Score final : {self.game.score} / {self.game.total_answered}", 
            font=("Poppins", 18, "bold"),
            text_color=COLOR_TEXT
        ).pack(pady=5)

        accuracy = int((self.game.score / self.game.total_answered * 100)) if self.game.total_answered > 0 else 0
        ctk.CTkLabel(
            self.end_frame, 
            text=f"Précision : {accuracy}%", 
            font=("Poppins", 15),
            text_color=COLOR_TEXT
        ).pack(pady=5)

        ctk.CTkButton(
            self.end_frame,
            text="REJOUER",
            fg_color=COLOR_PRIMARY,
            hover_color=COLOR_PRIMARY_HOVER,
            text_color="#FFFFFF",
            font=("Poppins", 14, "bold"),
            height=45,
            width=200,
            corner_radius=12,
            command=self.restart
        ).pack(pady=25)

    def restart(self):
        self.end_frame.pack_forget()
        self.card.pack(fill="both", expand=True, padx=20, pady=15)
        self.start_game()