from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import joblib
import os

app = Flask(__name__)
CORS(app)  # Enable CORS

base_dir = os.path.dirname(__file__)
model_path = os.path.join(base_dir, "spam_filter_model.pkl")
vectorizer_path = os.path.join(base_dir, "tfidf_vectorizer.pkl")

model = joblib.load(open(model_path, "rb"))
vectorizer = joblib.load(open(vectorizer_path, "rb"))

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        text = data.get("message")
        if not text:
            return jsonify({"error": "No message provided"}), 400

        vectorized_text = vectorizer.transform([text])
        prediction = model.predict(vectorized_text)[0]

        return jsonify({"prediction": "spam" if prediction == 1 else "ham"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
