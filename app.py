from flask import Flask, jsonify, render_template, request, session, redirect, url_for
import os
import random
import json

app = Flask(__name__)
app.secret_key = 'rastgele-bir-gizli-anahtar'  # oturum takibi için gerekli

# Görsellerin konumu ve etiket dosyası
IMAGE_FOLDER = 'static/images'
CHARACTER_FILE = 'characters.json'

# Karakter verisini yükle
with open(CHARACTER_FILE, 'r', encoding='utf-8') as f:
    character_map = json.load(f)

# Fotoğraf listesini al
image_files = list(character_map.keys())

@app.route("/", methods=["GET", "POST"])
def index():
    if "correct_character" not in session:
        # Yeni bir oyun başlat
        random_character = random.choice(list(character_map.keys()))
        session["correct_character"] = character_map[random_character]
        session["image"] = random_character
        session["lives"] = 6
        session["wrong_guesses"] = []

    message = ""

    if request.method == "POST":
        guess = request.form["guess"].strip().lower()
        correct = session["correct_character"].lower()

        if guess == correct:
            message = "Doğru!"
            random_character = random.choice(list(character_map.keys()))
            session["correct_character"] = character_map[random_character]
            session["image"] = random_character
            session["lives"] = 6
            session["wrong_guesses"] = []
        else:
            session["lives"] -= 1
            if guess not in session["wrong_guesses"]:
                session["wrong_guesses"].append(guess)
            if session["lives"] <= 0:
                message = f"Yanlış! Doğru cevap: {session['correct_character']}"
                random_character = random.choice(list(character_map.keys()))
                session["correct_character"] = character_map[random_character]
                session["image"] = random_character
                session["lives"] = 6
                session["wrong_guesses"] = []
            else:
                message = "Yanlış! Tekrar deneyin."

    return render_template(
        "index.html",
        image=session["image"],
        message=message,
        lives=session["lives"]
    )

@app.route("/characters")
def get_characters():
    unique_characters = list(set(character_map.values()))
    return jsonify(unique_characters)


if __name__ == "__main__":
    app.run(debug=True)
