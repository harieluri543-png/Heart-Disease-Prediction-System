❤️ Heart Disease Prediction System

A web-based Heart Disease Prediction System developed using Python, Flask, Machine Learning, HTML, CSS and SQLite. The application predicts whether a person is at risk of heart disease based on medical information entered by the user.


📌 Features

Heart Disease Prediction using Machine Learning
Prediction Confidence Score
Personalized Health Recommendations
Prediction History
Responsive User Interface
SQLite Database Integration
PDF Report Generation

🛠️ Technologies Used :

Frontend :
HTML5
CSS3

Backend  :
Python
Flask

Machine Learning :
Scikit-learn
Pandas
NumPy
Joblib
Database
SQLite

📂 Project Structure
Heart-Disease-Prediction-System/
│
├── datase/
│
├──model/
│   └── heart_model.pkl
│
├── static/
│   ├── css/
│   └── images/
│   
├── screenshots
│
├── templates/
│   ├── index.html
│   ├── about.html
│   ├── home.html
│   ├── database.py
│   ├── result.html
│   └── history.html
│
│
├── heart.db
├── Heart_Disease_Report.pdf
├── app.py
├── requirements.txt
├── README.md
└── train_model.py


⚙️ Installation :

1. Clone the Repository
git clone https://github.com/YOUR_USERNAME/Heart-Disease-Prediction-System.git

2. Open the Project Folder
cd Heart-Disease-Prediction-System

3. Create a Virtual Environment (Optional)
python -m venv venv

Activate it:

Windows

venv\Scripts\activate

4. Install Dependencies
pip install -r requirements.txt

5. Run the Application
python app.py

Open your browser and visit:

http://127.0.0.1:5000/

🧠 Machine Learning Model :

The model is trained using the Heart Disease dataset and predicts the likelihood of heart disease based on patient health parameters.

Input Features:

Age
Sex
Chest Pain Type
Resting Blood Pressure
Cholesterol
Fasting Blood Sugar
Resting ECG
Maximum Heart Rate
Exercise Induced Angina
ST Depression (Oldpeak)
Slope
Number of Major Vessels (CA)
Thalassemia

📊 Prediction Output

The system displays:

Heart Disease Risk (Yes/No)
Prediction Confidence
Health Recommendations

## 📸 Screenshots

### Home Page
![Home Page](screenshots/home.png)
(https://heart-disease-prediction-system-210s.onrender.com/)

### Prediction Page
![Prediction Page](screenshots/prediction.png)
(https://heart-disease-prediction-system-210s.onrender.com/prediction)

### Result Page
![Result Page](screenshots/result.png)
![Result Page](screenshots/result1.png)
![Result Page](screenshots/result2.png)

### History Page
![History Page](screenshots/history.png)
(https://heart-disease-prediction-system-210s.onrender.com/history)

### About Page
![History Page](screenshots/about.png)
(https://heart-disease-prediction-system-210s.onrender.com/about)

🚀 Future Improvements :

User Registration and Login
Secure Password Storage
Email Notifications
Cloud Database Support
Multiple Disease Prediction
User Profile Management


## 🌐 Live Demo

https://heart-disease-prediction-system-210s.onrender.com


📄 License

This project is intended for educational purposes.

👨‍💻 Author

Hari Eluri

GitHub: https://github.com/harieluri543


🔗 Live Demo(prediction page):
https://heart-disease-prediction-system-210s.onrender.com/prediction