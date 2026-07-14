from flask import Flask, render_template, request
import joblib
import numpy as np
#pdf
from flask import send_file
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.units import inch
from datetime import datetime
import os
#sql database connectivity
import sqlite3
from flask import redirect

# Create the application
app = Flask(__name__)

model = joblib.load("model/heart_model.pkl")

#Create a home route
@app.route("/")
def home():
    return render_template("home.html")
# Create a prediction route
@app.route("/prediction")
def predict_page():
    return render_template("index.html")
# Create a about route
@app.route("/about")
def about():
    return render_template("about.html")

#Create a history page
@app.route("/history")
def history():

    conn = sqlite3.connect("heart.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM history ORDER BY id DESC")
    records = cursor.fetchall()

    conn.close()

    return render_template("history.html", records=records)
#Delete the history page
@app.route("/delete/<int:id>")
def delete(id):

    conn = sqlite3.connect("heart.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM history WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect("/history")

#Delete entire history with one click
@app.route("/clear_history")
def clear_history():

    conn = sqlite3.connect("heart.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM history")

    conn.commit()
    conn.close()

    return redirect("/history")

# Create a prediction route
@app.route("/predict", methods=["POST"])
def predict():

    age = float(request.form["age"])
    sex = float(request.form["sex"])
    cp = float(request.form["cp"])
    trestbps = float(request.form["trestbps"])
    chol = float(request.form["chol"])
    fbs = float(request.form["fbs"])
    restecg = float(request.form["restecg"])
    thalach = float(request.form["thalach"])
    exang = float(request.form["exang"])
    oldpeak = float(request.form["oldpeak"])
    slope = float(request.form["slope"])
    ca = float(request.form["ca"])
    thal = float(request.form["thal"])

    # Server-side validation
    if age < 1 or age > 120:
        return "Invalid Age"

    if trestbps < 80 or trestbps > 250:
        return "Invalid Resting Blood Pressure"

    if chol < 100 or chol > 600:
        return "Invalid Serum Cholesterol"

    if thalach < 60 or thalach > 220:
        return "Invalid Maximum Heart Rate"

    if oldpeak < 0 or oldpeak > 6.2:
        return "Invalid Oldpeak Value"

    cp_map = {
    "0": "Typical Angina",
    "1": "Atypical Angina",
    "2": "Non-Anginal Pain",
    "3": "Asymptomatic"
   }

    restecg_map = {
    "0": "Normal",
    "1": "ST-T Wave Abnormality",
    "2": "Left Ventricular Hypertrophy"
    }

    slope_map = {
    "0": "Upsloping",
    "1": "Flat",
    "2": "Downsloping"
   }

    thal_map = {
    "0": "Normal",
    "1": "Fixed Defect",
    "2": "Reversible Defect",
    "3": "Unknown"
   }

    
   
    data = np.array([[
       age,
       sex,
       cp,
       trestbps,
       chol,
       fbs,
       restecg,
       thalach,
       exang,
       oldpeak,
       slope,
       ca,
       thal
   ]])
    prediction = model.predict(data)
    probability = model.predict_proba(data)
    print("\nInput Values:")
    print(data)

    print("Prediction:", prediction[0])

    print("Probability:", probability)
    print(probability)
    high_risk = round(probability[0][1] * 100, 2)
    low_risk = round(probability[0][0] * 100, 2)
    confidence = max(high_risk, low_risk)

    if prediction[0] == 1:
        result = "❤️ High Risk of Heart Disease"
        color = "danger"
        recommendations = [
        "✅ Consult a cardiologist immediately.",
        "🩺 Monitor blood pressure regularly.",
        "🥗 Follow a heart-healthy diet.",
        "🏃 Exercise as advised by your doctor.",
        "🚭 Avoid smoking and alcohol.",
        "💊 Take prescribed medications on time.",
        "🍷 Limit or avoid alcohol consumption.",
        "🚨 Do not ignore chest pain or discomfort.",
        "📅 Schedule follow-up appointments regularly."
        ]
        
    else:
        result = "💚 Low Risk of Heart Disease"
        color = "safe"
        recommendations = [
        "⚖️ Maintain a healthy lifestyle.",
        "🏃 Exercise at least 30 minutes daily.",
        "🥗 Eat fruits and vegetables regularly.",
        "📅 Have regular health checkups.",
        "🩺 Continue monitoring your health.",
        "❤️ Manage stress through relaxation or meditation.",
        "💧 Drink enough water."
        ]
        global report_data

    report_data = {
        "age": age,
        "sex": "Male" if sex == 1 else "Female",

        "cp": cp_map[request.form["cp"]],
        "trestbps": trestbps,
        "chol": chol,
        "fbs": "Greater than 120 mg/dL" if fbs == 1 else "120 mg/dL or Less",
        "restecg": restecg_map[request.form["restecg"]],
        "thalach": thalach,
        "exang": "Yes" if exang == 1 else "No",
        "oldpeak": oldpeak,
        "slope": slope_map[request.form["slope"]],
        "ca": ca,
        "thal": thal_map[request.form["thal"]],

        "result": result,
        "confidence": confidence,
        "recommendations": recommendations,

        "date": datetime.now().strftime("%d-%m-%Y"),
        "time": datetime.now().strftime("%I:%M %p")
    }
    conn = sqlite3.connect("heart.db")

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO history
    (age, gender, prediction, confidence, date, time)
    VALUES (?, ?, ?, ?, ?, ?)
    """,
    (
    int(age),
    "Male" if sex == 1 else "Female",
    result,
    confidence,
    report_data["date"],
    report_data["time"]
    ))

    conn.commit()
    conn.close()


    return render_template(
        "result.html",
        result=result,
        color=color,
        confidence=confidence,
        recommendations=recommendations,
        patient=report_data,
        high_risk=high_risk,
        low_risk=low_risk
        ) 
@app.route("/download")
def download():

    pdf_file = "Heart_Disease_Report.pdf"

    doc = SimpleDocTemplate(pdf_file)
# Generate the id for the pdf    
    report_id = "HDP-" + datetime.now().strftime("%Y%m%d%H%M%S")

    styles = getSampleStyleSheet()
    style = styles["Heading1"]
    style.alignment = TA_CENTER

    elements = []

    # Title
    # Adds a subtitle
    elements.append(Paragraph("Heart Disease Prediction Report", style))

    elements.append(
    Paragraph(
        "<b>Generated by Heart Disease Prediction System. Machine Learning Based Clinical Decision Support</b>",
        styles["Heading3"]
        )
    )

    elements.append(Paragraph("<br/><br/>", styles["Normal"]))
    
# Patient Details
    data = [
    ["Parameter", "Value"],

    ["Age", str(report_data["age"]) + " Years"],
    ["Gender", report_data["sex"]],
    ["Chest Pain Type", report_data["cp"]],
    ["Resting Blood Pressure", str(report_data["trestbps"]) + " mmHg"],
    ["Serum Cholesterol", str(report_data["chol"]) + " mg/dL"],
    ["Fasting Blood Sugar", report_data["fbs"]],
    ["Resting ECG", report_data["restecg"]],
    ["Maximum Heart Rate", str(report_data["thalach"]) + " bpm"],
    ["Exercise Induced Angina", report_data["exang"]],
    ["Oldpeak", str(report_data["oldpeak"])],
    ["Slope", report_data["slope"]],
    ["Major Vessels", str(report_data["ca"])],
    ["Thalassemia", report_data["thal"]],
    ["Prediction", report_data["result"]],
    ["Confidence", str(report_data["confidence"]) + "%"],
    ["Model Used", "Random Forest Classifier"],
    ["Report Date", report_data["date"]],
    ["Report Time", report_data["time"]],
    ["Report ID", report_id]
]

    table = Table(data, colWidths=[220, 220])

    table.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),colors.red),
        ('TEXTCOLOR',(0,0),(-1,0),colors.white),

        ('GRID',(0,0),(-1,-1),1,colors.black),

        ('BACKGROUND',(0,1),(0,-1),colors.lightgrey),

        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),

        ('BOTTOMPADDING',(0,0),(-1,0),10),

        ('ALIGN',(0,0),(-1,-1),'CENTER')
    ]))

    elements.append(table)
    elements.append(Paragraph("<br/><br/>", styles["Normal"]))

    # Recommendations
    elements.append(Paragraph("<b>Recommendations</b>", styles["Heading2"]))

    for item in report_data["recommendations"]:
        elements.append(Paragraph("• " + item, styles["Normal"]))

    elements.append(Paragraph("<br/>", styles["Normal"]))

    # Disclaimer
    elements.append(
    Paragraph(
        "<b>Disclaimer:</b><br/>"
        "This report has been generated using a Machine Learning model for educational purposes only."
        "<br/>It should not be used as a substitute for professional medical diagnosis or treatment."
        "<br/>Please consult a qualified healthcare professional.",
        styles["Normal"]
        )
    )

    elements.append(
    Paragraph(
        "<b>Heart Disease Prediction System</b><br/><br/>"
        "<b>Developed by Hari Eluri</b><br/>"
        "B.Tech CSE (AI & ML)<br/>"
        "Uttaranchal University",
        styles["Normal"]
        )
    )
    doc.build(elements)

    return send_file(pdf_file, as_attachment=True)


# Run the server
if __name__ == "__main__":
    app.run(debug=True)
