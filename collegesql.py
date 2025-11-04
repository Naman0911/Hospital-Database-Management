import streamlit as st
import mysql.connector
import pandas as pd

# MySQL Connection
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="NamanUp@091105",
        database="HospitalDB",
        auth_plugin='mysql_native_password' 
    )

# Function to execute queries
def execute_query(query, values=None, fetch=False):
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    if values:
        cursor.execute(query, values)
    else:
        cursor.execute(query)
    if fetch:
        result = cursor.fetchall()
        conn.close()
        return result
    else:
        conn.commit()
        conn.close()

# Function to display patients
def manage_patients():
    st.subheader("Manage Patients")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0, max_value=120, step=1)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    contact = st.text_input("Contact")
    address = st.text_area("Address")

    if st.button("Add Patient"):
        execute_query("INSERT INTO Patient (Name, Age, Gender, Contact, Address) VALUES (%s, %s, %s, %s, %s)", 
                      (name, age, gender, contact, address))
        st.success("Patient Added Successfully!")

    patients = execute_query("SELECT * FROM Patient", fetch=True)
    df = pd.DataFrame(patients)
    st.dataframe(df)

# Function to display doctors
def manage_doctors():
    st.subheader("Manage Doctors")
    name = st.text_input("Doctor Name")
    specialization = st.text_input("Specialization")
    contact = st.text_input("Contact")

    if st.button("Add Doctor"):
        execute_query("INSERT INTO Doctor (Name, Specialization, Contact) VALUES (%s, %s, %s)", 
                      (name, specialization, contact))
        st.success("Doctor Added Successfully!")

    doctors = execute_query("SELECT * FROM Doctor", fetch=True)
    df = pd.DataFrame(doctors)
    st.dataframe(df)

# Function to manage appointments
def manage_appointments():
    st.subheader("Manage Appointments")
    patients = execute_query("SELECT PatientID, Name FROM Patient", fetch=True)
    doctors = execute_query("SELECT DoctorID, Name FROM Doctor", fetch=True)

    patient_dict = {p["Name"]: p["PatientID"] for p in patients}
    doctor_dict = {d["Name"]: d["DoctorID"] for d in doctors}

    patient = st.selectbox("Select Patient", list(patient_dict.keys()))
    doctor = st.selectbox("Select Doctor", list(doctor_dict.keys()))
    date = st.date_input("Appointment Date")
    time = st.time_input("Appointment Time")
    status = st.selectbox("Status", ["Scheduled", "Completed", "Cancelled"])

    if st.button("Book Appointment"):
        execute_query("INSERT INTO Appointment (PatientID, DoctorID, Date, Time, Status) VALUES (%s, %s, %s, %s, %s)", 
                      (patient_dict[patient], doctor_dict[doctor], date, time, status))
        st.success("Appointment Scheduled Successfully!")

    appointments = execute_query("SELECT * FROM Appointment", fetch=True)
    df = pd.DataFrame(appointments)
    st.dataframe(df)

# Function to manage bills
def manage_bills():
    st.subheader("Manage Bills")
    patients = execute_query("SELECT PatientID, Name FROM Patient", fetch=True)
    patient_dict = {p["Name"]: p["PatientID"] for p in patients}

    patient = st.selectbox("Select Patient", list(patient_dict.keys()))
    amount = st.number_input("Amount", min_value=0.0, step=0.01)
    date = st.date_input("Billing Date")

    if st.button("Generate Bill"):
        execute_query("INSERT INTO Bill (PatientID, Amount, Date) VALUES (%s, %s, %s)", 
                      (patient_dict[patient], amount, date))
        st.success("Bill Generated Successfully!")

    bills = execute_query("SELECT * FROM Bill", fetch=True)
    df = pd.DataFrame(bills)
    st.dataframe(df)

# Function to manage medicines
def manage_medicines():
    st.subheader("Manage Medicines")
    name = st.text_input("Medicine Name")
    price = st.number_input("Price", min_value=0.0, step=0.01)
    stock = st.number_input("Stock", min_value=0, step=1)

    if st.button("Add Medicine"):
        execute_query("INSERT INTO Medicine (Name, Price, Stock) VALUES (%s, %s, %s)", 
                      (name, price, stock))
        st.success("Medicine Added Successfully!")

    medicines = execute_query("SELECT * FROM Medicine", fetch=True)
    df = pd.DataFrame(medicines)
    st.dataframe(df)

# Function to manage prescriptions
def manage_prescriptions():
    st.subheader("Manage Prescriptions")
    patients = execute_query("SELECT PatientID, Name FROM Patient", fetch=True)
    doctors = execute_query("SELECT DoctorID, Name FROM Doctor", fetch=True)
    medicines = execute_query("SELECT MedicineID, Name FROM Medicine", fetch=True)

    patient_dict = {p["Name"]: p["PatientID"] for p in patients}
    doctor_dict = {d["Name"]: d["DoctorID"] for d in doctors}
    medicine_dict = {m["Name"]: m["MedicineID"] for m in medicines}

    patient = st.selectbox("Select Patient", list(patient_dict.keys()))
    doctor = st.selectbox("Select Doctor", list(doctor_dict.keys()))
    medicine = st.selectbox("Select Medicine", list(medicine_dict.keys()))
    dosage = st.text_input("Dosage")
    instructions = st.text_area("Instructions")

    if st.button("Add Prescription"):
        execute_query("INSERT INTO Prescription (PatientID, DoctorID, MedicineID, Dosage, Instructions) VALUES (%s, %s, %s, %s, %s)", 
                      (patient_dict[patient], doctor_dict[doctor], medicine_dict[medicine], dosage, instructions))
        st.success("Prescription Added Successfully!")

# Streamlit Navigation
st.sidebar.title("Hospital Management")
menu = st.sidebar.radio("Menu", ["Patients", "Doctors", "Appointments", "Bills", "Medicines", "Prescriptions"])

if menu == "Patients":
    manage_patients()
elif menu == "Doctors":
    manage_doctors()
elif menu == "Appointments":
    manage_appointments()
elif menu == "Bills":
    manage_bills()
elif menu == "Medicines":
    manage_medicines()
elif menu == "Prescriptions":
    manage_prescriptions()
    
    #python -m streamlit run frontend.py