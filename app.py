from flask import Flask, render_template, request

app = Flask(__name__)

def calculate_bmi(weight, height):
    height_m = height / 100
    bmi = weight / (height_m ** 2)
    
    # Determine health status and advice
    if bmi < 18.5:
        health_message = "Λιποβαρής"
        advice = "Αναθεώρησε τη διατροφή σου και συμβουλεύσου έναν ειδικό."
        risk_percentage = (bmi / 18.5) * 100  # Scale risk percentage
    elif 18.5 <= bmi < 25:
        health_message = "Υγιής"
        advice = "Συνέχισε τη σωστή διατροφή και άσκηση."
        risk_percentage = 0
    elif 25 <= bmi < 30:
        health_message = "Υπερβαρής"
        advice = "Εργάσου για να μειώσεις το βάρος σου με υγιεινή διατροφή και άσκηση."
        risk_percentage = ((bmi - 25) / 5) * 100  # Scale risk percentage
    elif 30 <= bmi < 35:
        health_message = "Παχύσαρκος"
        advice = "Συμβουλεύσου έναν ειδικό για να αναπτύξεις ένα σχέδιο απώλειας βάρους."
        risk_percentage = ((bmi - 30) / 5) * 100  # Scale risk percentage
    else:
        health_message = "Πολύ Παχύσαρκος"
        advice = "Αναγκαία η ιατρική παρακολούθηση για να διαχειριστείς την κατάσταση."
        risk_percentage = 100

    return bmi, health_message, advice, risk_percentage

@app.route('/', methods=['GET', 'POST'])
def index():
    bmi = None
    health_message = ""
    advice = ""
    risk_percentage = 0
    
    if request.method == 'POST':
        height = float(request.form['height'])
        weight = float(request.form['weight'])
        bmi, health_message, advice, risk_percentage = calculate_bmi(weight, height)
    
    return render_template('index.html', bmi=bmi, health_message=health_message, advice=advice, risk_percentage=risk_percentage)

if __name__ == '__main__':
    app.run(debug=True)
