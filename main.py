import streamlit as st
import pandas as pd
from joblib import load

LABELS_MEN = {
    0: "dysglycemia",
    1: "aging",
    2: "cardiovascular",
    3: "adiposity",
    4: "healthy",
}

LABELS_WOMEN = {
    0: "aging",
    1: "cardiovascular",
    2: "healthy",
    3: "dysglycemia",
    4: "adiposity",
}

st.title("KMeans Obesity Phenotyping")
st.write("""
Use this app to predict your obesity phenotype based on selected cardiometabolic risk factors!
""")

model_option = st.sidebar.radio("Choose gender model", ["Women", "Men"])
if model_option == "Women":
    pipeline = load('kmeans_pipeline_women.joblib')
    LABELS = LABELS_WOMEN
else:
    pipeline = load('kmeans_pipeline_men.joblib')
    LABELS = LABELS_MEN

input_option = st.sidebar.radio("Choose input type", ["Manual", "CSV Upload"])

if input_option == "Manual":
    age = st.sidebar.slider("Age", 20, 85, 25, 1)
    waist = st.sidebar.slider("Waist Measurement (in cm)", 30, 300, 80, 1)
    sbp = st.sidebar.slider("Systolic Blood Pressure (SBP)", 70, 270, 120, 1)
    dbp = st.sidebar.slider("Diastolic Blood Pressure (DBP)", 30, 150, 80, 1)
    tc = st.sidebar.slider("Total Cholesterol (TC) in mg/dL", 67, 773, 200, 1)
    fglu = st.sidebar.slider("Fasting Glucose (FGLU) in mg/dL", 36, 540, 90, 1)

    if st.sidebar.button("Predict"):
        input_data = pd.DataFrame([[age, waist, sbp, dbp, tc, fglu]],
                                  columns=['age', 'waist', 'sbp', 'dbp', 'tc', 'fglu'])
        prediction = pipeline.predict(input_data)[0]
        st.subheader(f"Prediction: **{LABELS[prediction]}**")
        st.write("""
        This is a prediction based on KMeans clustering. **This is not clinical advice. Always seek professional health care and advice, and discuss any medical information you find online with your doctor.**
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
                df_uploaded = df_uploaded[(df_uploaded['age'].between(20, 85)) &
                                          (df_uploaded['waist'].between(30, 300)) &
                                          (df_uploaded['sbp'].between(70, 270)) &
                                          (df_uploaded['dbp'].between(30, 150)) &
                                          (df_uploaded['tc'].between(67, 773)) &
                                          (df_uploaded['fglu'].between(36, 540))]
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
