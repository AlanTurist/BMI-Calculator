import os
from typing import Optional, Tuple

from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-change-me")


def _classify_bmi(bmi: float) -> Tuple[str, str]:
    if bmi < 18.5:
        return (
            "Λιποβαρής",
            "Στόχευσε σε σταδιακή αύξηση βάρους με ποιοτική θερμιδική πρόσληψη. Αν έχεις συμπτώματα ή απότομες αλλαγές βάρους, μίλα με επαγγελματία υγείας.",
        )
    if bmi < 25:
        return (
            "Υγιές εύρος",
            "Είσαι σε φυσιολογικό εύρος. Συνέχισε με ισορροπημένη διατροφή, ύπνο και σταθερή δραστηριότητα.",
        )
    if bmi < 30:
        return (
            "Υπέρβαρος",
            "Μικρές αλλαγές (περισσότερο περπάτημα, λίγο καλύτερες μερίδες/πρωτεΐνη/ίνες) κάνουν μεγάλη διαφορά. Αν θες, μπορώ να σου προτείνω πλάνο.",
        )
    if bmi < 35:
        return (
            "Παχυσαρκία (I)",
            "Αξίζει δομημένο πλάνο διατροφής/άσκησης και έλεγχο βασικών δεικτών. Αν υπάρχουν συνοδά προβλήματα, μίλα με γιατρό.",
        )
    return (
        "Παχυσαρκία (II+)",
        "Συνιστάται ιατρική καθοδήγηση και εξατομικευμένο πλάνο. Μην το πας «ήρωας μόνος» — δεν χρειάζεται.",
    )


def _healthy_weight_range(height_m: float) -> Tuple[float, float]:
    # BMI 18.5–24.9
    min_kg = 18.5 * (height_m ** 2)
    max_kg = 24.9 * (height_m ** 2)
    return (min_kg, max_kg)


def _parse_inputs() -> Tuple[Optional[float], Optional[float], Optional[str]]:
    # Επιστρέφει (height_cm, weight_kg, error_message)
    try:
        height_cm = float((request.form.get("height") or "").strip().replace(",", "."))
        weight_kg = float((request.form.get("weight") or "").strip().replace(",", "."))
    except ValueError:
        return None, None, "Βάλε έγκυρες αριθμητικές τιμές (π.χ. 176.5 και 78.2)."

    if not (80 <= height_cm <= 230):
        return height_cm, weight_kg, "Το ύψος πρέπει να είναι μεταξύ 80 και 230 cm."
    if not (20 <= weight_kg <= 300):
        return height_cm, weight_kg, "Το βάρος πρέπει να είναι μεταξύ 20 και 300 kg."

    return height_cm, weight_kg, None


def _compute(height_cm: float, weight_kg: float) -> dict:
    h_m = height_cm / 100.0
    bmi = weight_kg / (h_m ** 2)
    category, advice = _classify_bmi(bmi)
    min_kg, max_kg = _healthy_weight_range(h_m)
    return {
        "bmi": bmi,
        "category": category,
        "advice": advice,
        "healthy_min_kg": min_kg,
        "healthy_max_kg": max_kg,
    }


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        height_cm, weight_kg, error = _parse_inputs()

        session["last_inputs"] = {
            "height": "" if height_cm is None else height_cm,
            "weight": "" if weight_kg is None else weight_kg,
        }

        if error:
            session["last_error"] = error
            session.pop("last_result", None)
            return redirect(url_for("index"))

        session["last_result"] = _compute(height_cm, weight_kg)
        session.pop("last_error", None)
        return redirect(url_for("index"))

    inputs = session.get("last_inputs") or {"height": "", "weight": ""}
    error = session.pop("last_error", None)
    result = session.get("last_result")

    return render_template("index.html", inputs=inputs, error=error, result=result)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)
