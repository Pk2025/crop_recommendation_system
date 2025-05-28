from flask import Flask, request, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import numpy as np
import pickle
import os

# Create Flask app
app = Flask(__name__)
app.secret_key = 'mysecretkey123'

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:parth2025@localhost/crop'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Load trained model and scalers
model = pickle.load(open('model.pkl', 'rb'))
sc = pickle.load(open('standscaler.pkl', 'rb'))
ms = pickle.load(open('minmaxscaler.pkl', 'rb'))

# List of crops
crops = [
    "Rice", "Maize", "Jute", "Cotton", "Coconut", "Papaya",
    "Orange", "Apple", "Muskmelon", "Watermelon", "Grapes",
    "Mango", "Banana", "Pomegranate", "Lentil", "Blackgram",
    "Mungbean", "Mothbeans", "Pigeonpeas", "Kidneybeans",
    "Chickpea", "Coffee"
]

# Define User model for SQLite
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

# Create the database and tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('signup'))
    return render_template("index.html")

@app.route("/contact")
def contact():
    if 'username' not in session:
        return redirect(url_for('signup'))
    return render_template("contact.html")

@app.route("/about")
def about():
    if 'username' not in session:
        return redirect(url_for('signup'))
    return render_template("about.html")

@app.route("/predict", methods=['POST'])
def predict():
    if 'username' not in session:
        return redirect(url_for('signup'))
    
    try:
        N = float(request.form['Nitrogen'])
        P = float(request.form['Phosphorus'])
        K = float(request.form['Potassium'])
        temp = float(request.form['Temperature'])
        humidity = float(request.form['Humidity'])
        ph = float(request.form['pH'])
        rainfall = float(request.form['Rainfall'])

        feature_list = [N, P, K, temp, humidity, ph, rainfall]
        single_pred = np.array(feature_list).reshape(1, -1)

        scaled_features = ms.transform(single_pred)
        final_features = sc.transform(scaled_features)

        prediction = model.predict(final_features)[0]

        crop_dict = {
            1: "Rice", 2: "Maize", 3: "Jute", 4: "Cotton", 5: "Coconut", 6: "Papaya",
            7: "Orange", 8: "Apple", 9: "Muskmelon", 10: "Watermelon", 11: "Grapes",
            12: "Mango", 13: "Banana", 14: "Pomegranate", 15: "Lentil", 16: "Blackgram",
            17: "Mungbean", 18: "Mothbeans", 19: "Pigeonpeas", 20: "Kidneybeans",
            21: "Chickpea", 22: "Coffee"
        }

        crop = crop_dict.get(prediction, "Unknown Crop")
        session['last_crop'] = crop
        crop_image = crop.lower() + ".jpg"

        return render_template('result.html', crop=crop, crop_image=crop_image)

    except Exception as e:
        return render_template('index.html', result=f"Error: {str(e)}")

@app.route('/result')
def result():
    if 'username' not in session:
        return redirect(url_for('signup'))

    crop = session.get('last_crop', None)
    crop_image = crop.lower() + ".jpg" if crop else "default.jpg"
    return render_template('result.html', crop=crop, crop_image=crop_image)

@app.route('/description')
def description():
    crops = [
        {"name": "rice", "conditions": "Hot and humid climate with plenty of water.", "benefits": "Staple food rich in carbohydrates."},
        {"name": "maize", "conditions": "Warm climate with moderate rainfall.", "benefits": "Used for food, feed, and industrial products."},
        {"name": "chickpea", "conditions": "Cool, dry climate with good sunlight.", "benefits": "High in protein and fiber."},
        {"name": "kidneybeans", "conditions": "Warm days and cool nights.", "benefits": "Good for heart and rich in protein."},
        {"name": "pigeonpeas", "conditions": "Semi-arid climate, well-drained soil.", "benefits": "Rich in protein and fiber."},
        {"name": "mothbeans", "conditions": "Hot and arid conditions.", "benefits": "Excellent drought resistance."},
        {"name": "mungbean", "conditions": "Hot, dry regions.", "benefits": "Easily digestible protein."},
        {"name": "blackgram", "conditions": "Warm and humid conditions.", "benefits": "Promotes bone health."},
        {"name": "lentil", "conditions": "Cool and dry climate.", "benefits": "Rich in iron and folate."},
        {"name": "pomegranate", "conditions": "Hot and dry climate.", "benefits": "Antioxidant rich and boosts immunity."},
        {"name": "banana", "conditions": "Tropical humid climate.", "benefits": "High in potassium and energy."},
        {"name": "mango", "conditions": "Tropical and subtropical climate.", "benefits": "Rich in Vitamin A and C."},
        {"name": "grapes", "conditions": "Moderate temperature with dry soil.", "benefits": "Rich in antioxidants."},
        {"name": "watermelon", "conditions": "Warm climate, sandy loam soil.", "benefits": "Hydrating and low in calories."},
        {"name": "muskmelon", "conditions": "Warm, sunny climate.", "benefits": "Good for digestion and hydration."},
        {"name": "apple", "conditions": "Cold climate, well-drained soil.", "benefits": "Boosts heart and gut health."},
        {"name": "orange", "conditions": "Subtropical climate.", "benefits": "Rich in Vitamin C."},
        {"name": "papaya", "conditions": "Tropical climate with warm weather.", "benefits": "Improves digestion and eye health."},
        {"name": "coconut", "conditions": "Humid coastal regions.", "benefits": "Good source of healthy fats."},
        {"name": "cotton", "conditions": "Warm climate, light soil.", "benefits": "Used in textiles and oils."},
        {"name": "jute", "conditions": "Warm, humid climate.", "benefits": "Eco-friendly fiber crop."},
        {"name": "coffee", "conditions": "Cool tropical climate.", "benefits": "Rich in antioxidants and energy boosting."}
    ]
    return render_template('description.html', crops=crops)

@app.route('/search', methods=['GET'])
def search_crops():
    if 'username' not in session:
        return redirect(url_for('signup'))

    query = request.args.get('search')
    if query:
        results = [crop for crop in crops if query.lower() in crop.lower()]
    else:
        results = []
    return render_template('index.html', search_results=results)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(name=username).first()
        if user and user.check_password(password):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Invalid username or password")

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'username' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if User.query.filter_by(name=username).first():
            return render_template('signup.html', error="Username already exists")
        if User.query.filter_by(email=email).first():
            return render_template('signup.html', error="Email already exists")

        new_user = User(name=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        session['username'] = username
        return redirect(url_for('index'))

    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('last_crop', None)
    return redirect(url_for('signup'))

if __name__ == "__main__":
    app.run(debug=True)

'''
Activation code
# Use in terminal, not in code:
# 1. Set-ExecutionPolicy Unrestricted -Scope Process
# 2. .venv\Scripts\Activate.ps1
# 3. python app.py
'''