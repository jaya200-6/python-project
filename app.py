from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = 'super_secret_key'  # Change this to a random secret key for production

# Dictionary based on the provided map image
states = {
    "Andaman & Nicobar Islands": "Port Blair",
    "Andhra Pradesh": "Amaravati",
    "Arunachal Pradesh": "Itanagar",
    "Assam": "Dispur",
    "Bihar": "Patna",
    "Chandigarh": "Chandigarh",
    "Chhattisgarh": "Raipur",
    "Dadra and Nagar Haveli & Daman & Diu": "Daman",
    "Delhi": "New Delhi",
    "Goa": "Panaji",
    "Gujarat": "Gandhinagar",
    "Haryana": "Chandigarh",
    "Himachal Pradesh": "Shimla",
    "Jammu & Kashmir": "Srinagar",
    "Jharkhand": "Ranchi",
    "Karnataka": "Bengaluru",
    "Kerala": "Thiruvananthapuram",
    "Ladakh": "Leh",
    "Lakshadweep": "Kavaratti",
    "Madhya Pradesh": "Bhopal",
    "Maharashtra": "Mumbai",
    "Manipur": "Imphal",
    "Meghalaya": "Shillong",
    "Mizoram": "Aizawl",
    "Nagaland": "Kohima",
    "Odisha": "Bhubaneswar",
    "Puducherry": "Puducherry",
    "Punjab": "Chandigarh",
    "Rajasthan": "Jaipur",
    "Sikkim": "Gangtok",
    "Tamil Nadu": "Chennai",
    "Telangana": "Hyderabad",
    "Tripura": "Agartala",
    "Uttar Pradesh": "Lucknow",
    "Uttarakhand": "Dehradun",
    "West Bengal": "Kolkata"
}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/memorize')
def memorize():
    return render_template('memorize.html', states=states)

@app.route('/guess')
def guess():
    wrong_states = random.sample(list(states.keys()), 5)
    correct_capitals = [states[state] for state in wrong_states]
    shuffled_capitals = correct_capitals[:]
    random.shuffle(shuffled_capitals)
    # Ensure no accidental correct matches
    while any(shuffled_capitals[i] == correct_capitals[i] for i in range(5)):
        random.shuffle(shuffled_capitals)
    session['wrong_states'] = wrong_states
    session['correct_capitals'] = correct_capitals
    paired = zip(wrong_states, shuffled_capitals)
    return render_template('guess.html', paired=paired)

@app.route('/result', methods=['POST'])
def result():
    wrong_states = session.get('wrong_states', [])
    correct_capitals = session.get('correct_capitals', [])
    score = 0
    correct_answers = []
    for i, state in enumerate(wrong_states):
        user_guess = request.form.get(state, '').strip().lower()
        correct = correct_capitals[i].lower()
        if user_guess == correct:
            score += 1
        correct_answers.append((state, correct_capitals[i]))
    return render_template('result.html', score=score, total=5, correct_answers=correct_answers)

if __name__ == '__main__':
    app.run(debug=True)