import json
import random
import unicodedata

def normalize_text(text: str) -> str:
    text = text.strip().lower()
    nfkd_form = unicodedata.normalize('NFKD', text)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

def check_answer(user_input: str, country_data: dict) -> bool:
    clean_user = normalize_text(user_input)
    if not clean_user:
        return False

    clean_official = normalize_text(country_data["name"])
    if clean_user == clean_official:
        return True

    for alias in country_data.get("aliases", []):
        if clean_user == normalize_text(alias):
            return True

    return False

class QuizGame:
    def __init__(self, json_path: str, time_limit: int = 60):
        with open(json_path, "r", encoding="utf-8") as f:
            self.countries = json.load(f)
        self.time_limit = time_limit  # Temps en secondes (ex: 60s)
        self.score = 0
        self.streak = 0
        self.total_answered = 0
        self.current_country = None
        self.remaining_countries = []
        self.reset_game()

    def reset_game(self):
        self.score = 0
        self.streak = 0
        self.total_answered = 0
        self.remaining_countries = self.countries.copy()
        random.shuffle(self.remaining_countries)

    def next_question(self):
        # Si la liste de pays est épuisée, on la re-mélange pour continuer sans s'arrêter
        if not self.remaining_countries:
            self.remaining_countries = self.countries.copy()
            random.shuffle(self.remaining_countries)
            
        self.current_country = self.remaining_countries.pop()
        return self.current_country

    def submit_answer(self, user_input: str) -> tuple[bool, str]:
        is_correct = check_answer(user_input, self.current_country)
        official_name = self.current_country["name"]
        self.total_answered += 1
        
        if is_correct:
            self.score += 1
            self.streak += 1
        else:
            self.streak = 0
            
        return is_correct, official_name