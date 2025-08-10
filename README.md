 Crop Recommendation System
A Machine Learning project that recommends the most suitable crop to grow based on soil, climate, and environmental conditions.
This system uses historical agricultural data and ML algorithms to help farmers and agricultural planners make informed decisions.

 Features
Crop Prediction: Suggests the best crop for given soil & climate data.

User Input: Takes parameters such as:

Nitrogen (N)

Phosphorus (P)

Potassium (K)

Temperature

Humidity

pH level

Rainfall

Machine Learning Model: Uses classification algorithms to predict the crop.

Data Visualization: Graphs and charts to understand data distribution.

Web/App Interface : Google URL

 Tech Stack
Programming Language: Python 🐍

Libraries:

pandas — Data handling

numpy — Numerical computation

matplotlib / seaborn — Data visualization

scikit-learn — Machine Learning

Model: Random Forest / Decision Tree / SVM 

Dataset: Public agricultural dataset (On Kaggle )

Project Structure
Crop-Recommendation-System/
│-- dataset/
│   └── crop_data.csv
│-- notebooks/
│   └── model_training.ipynb
│-- app.py              
│-- model.pkl           
│-- requirements.txt    
│-- README.md

Installation & Usage
1]Clone the repository
git clone https://github.com/your-username/crop_recommendation_system.git
cd crop_recommendation_system

2] Install dependencies
pip install -r requirements.txt

3] Run the application
python app.py

4] Open in browser
http://127.0.0.1:5000






