import streamlit as st
import pandas as pd
from joblib import load


pipeline = load('kmeans_pipeline_women.joblib')

# Define the label mappings
LABELS = {
    0: "aging",
    1: "cardiovascular",
    2: "healthy",
    3: "dysglycemia",
    4: "adiposity"
}

st.title("KMeans Health Predictor")
st.write("""
Use this app to predict your health category based on certain metrics!
""")


input_option = st.sidebar.radio("Choose input type", ["Manual", "CSV Upload"])

if input_option == "Manual":
    age = st.sidebar.slider("Age", 10, 100, 25, 1)
    waist = st.sidebar.slider("Waist Measurement (in cm)", 50, 150, 80, 1)
    sbp = st.sidebar.slider("Systolic Blood Pressure (SBP)", 90, 200, 120, 1)
    dbp = st.sidebar.slider("Diastolic Blood Pressure (DBP)", 60, 140, 80, 1)
    tc = st.sidebar.slider("Total Cholesterol (TC) in mg/dL", 100, 300, 200, 1)
    fglu = st.sidebar.slider("Fasting Glucose (FGLU) in mg/dL", 70, 140, 90, 1)

    if st.sidebar.button("Predict"):

        input_data = pd.DataFrame([[age, waist, sbp, dbp, tc, fglu]],
                                  columns=['age', 'waist', 'sbp', 'dbp', 'tc', 'fglu'])


        prediction = pipeline.predict(input_data)[0]


        st.subheader(f"Prediction: **{LABELS[prediction]}**")
        st.write("""
        This is a prediction based on KMeans clustering. Always consult with a healthcare professional for a comprehensive assessment.
        """)

elif input_option == "CSV Upload":
    st.sidebar.header("User Requirements")
    email = st.sidebar.text_input("Email")
    country = st.sidebar.text_input("Country")
    institution = st.sidebar.text_input("Institution or Company")
    degree = st.sidebar.text_input("Degree")


    if email and country and institution and degree:

        user_info = pd.DataFrame([[email, country, institution, degree]],
                                 columns=['email', 'country', 'institution', 'degree'])
        user_info.to_csv('user_stats.csv', mode='a', header=False, index=False)

        uploaded_file = st.sidebar.file_uploader("Now, upload your CSV file", type=["csv"])

        if uploaded_file:
            df_uploaded = pd.read_csv(uploaded_file)
            if all(col in df_uploaded.columns for col in ['age', 'waist', 'sbp', 'dbp', 'tc', 'fglu']):
                predictions = pipeline.predict(df_uploaded[['age', 'waist', 'sbp', 'dbp', 'tc', 'fglu']])
                df_uploaded['prediction'] = [LABELS[pred] for pred in predictions]

                st.write(df_uploaded)


                import base64

                def get_csv_download_link(df, filename="predictions.csv"):
                    csv = df.to_csv(index=False)
                    b64 = base64.b64encode(csv.encode()).decode()
                    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download CSV with Predictions</a>'
                    return href

                st.markdown(get_csv_download_link(df_uploaded), unsafe_allow_html=True)

            else:
                st.write("Error: The uploaded CSV does not have the required columns.")
    else:
        st.sidebar.write("Please fill in all the required fields to proceed.")
