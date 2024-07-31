from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    bmi = None
    health_message = ""
    advice = ""
    risk_percentage = 0

    if request.method == 'POST':
        try:
            # Λήψη και μετατροπή των δεδομένων από την φόρμα
            height = float(request.form['height']) / 100
            weight = float(request.form['weight'])
            
            # Υπολογισμός του BMI
            bmi = weight / (height ** 2)

            # Καθορισμός μηνυμάτων υγείας και ποσοστού κινδύνου
            if bmi < 18.5:
                health_message = "Λιποβαρής"
                advice = "Συνιστάται να αυξήσετε την πρόσληψη θερμίδων και να συμβουλευτείτε έναν διατροφολόγο."
                risk_percentage = 10
            elif 18.5 <= bmi < 25:
                health_message = "Υγιής"
                advice = "Η κατάσταση του βάρους σας είναι φυσιολογική. Συνεχίστε να διατηρείτε μια ισορροπημένη διατροφή."
                risk_percentage = 0
            elif 25 <= bmi < 30:
                health_message = "Υπερβαρής"
                advice = "Συνιστάται να μειώσετε το βάρος σας μέσω υγιεινής διατροφής και άσκησης."
                risk_percentage = 50
            elif 30 <= bmi < 35:
                health_message = "Παχύσαρκος"
                advice = "Η κατάσταση αυτή μπορεί να προκαλέσει προβλήματα υγείας. Συμβουλευτείτε έναν γιατρό για ένα πρόγραμμα απώλειας βάρους."
                risk_percentage = 75
            else:
                health_message = "Πολύ Παχύσαρκος"
                advice = "Είναι σημαντικό να αναζητήσετε ιατρική βοήθεια για να διαχειριστείτε την παχυσαρκία σας."
                risk_percentage = 90
        except ValueError as e:
            return f"Σφάλμα: {e}"

    return render_template('index.html', bmi=bmi, health_message=health_message, advice=advice, risk_percentage=risk_percentage)

if __name__ == '__main__':
    app.run(debug=True)
