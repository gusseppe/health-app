# KMeans Health Predictor

The KMeans Health Predictor is a Streamlit app that predicts health categories based on certain metrics. The app utilizes a KMeans clustering model to classify the data into one of the five categories: aging, cardiovascular, healthy, dysglycemia, and adiposity.

Demo: https://health-app-predictor.streamlit.app/

## Features

- **Manual Input**: Users can input individual data points manually using sliders and receive predictions in real-time.
- **CSV Upload**: Users can upload a CSV file with multiple data points to receive batch predictions. The app also captures user information such as email, country, institution, and degree for statistics.
- **Downloadable Results**: Users can download the CSV file with predictions appended as a new column.

## Usage

1. Clone this repository and navigate to the project directory.
2. Install the required libraries with `pip install -r requirements.txt`.
3. Run the Streamlit app with `streamlit run app.py`.
4. Access the app in your web browser at `http://localhost:8501`.

### Input Format for CSV Upload

The CSV file should have the following columns:
- `age`: Age of the individual.
- `waist`: Waist measurement in centimeters.
- `sbp`: Systolic blood pressure.
- `dbp`: Diastolic blood pressure.
- `tc`: Total cholesterol in mg/dL.
- `fglu`: Fasting glucose in mg/dL.

Each row in the CSV file should represent a set of data points for which you want to get a prediction.

Example CSV format:

| age | waist | sbp | dbp | tc  | fglu |
|-----|-------|-----|-----|-----|------|
| 25  | 80    | 120 | 80  | 200 | 90   |
| 30  | 85    | 110 | 75  | 195 | 92   |
| 28  | 82    | 115 | 79  | 198 | 91   |

