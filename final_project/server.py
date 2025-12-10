"""
Flask web server for running emotion detection on user input text.
It uses the local EmotionDetection package to analyze the text.
"""
from flask import Flask, request
from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)

@app.route("/emotionDetector")
def emotion_detector_route():
    """
    Endpoint to process text for emotion detection.
    Reads 'textToAnalyze' from the request arguments, calls the
    emotion_detector, and formats the output string.
    """
    text_to_analyze = request.args.get('textToAnalyze')
    response_data = emotion_detector(text_to_analyze)

    if response_data is None:
        return "Invalid text! Please provide text to analyze."

    if response_data.get('dominant_emotion') is None:
        return "Invalid text! Please try again!."

    dominant_emotion = response_data['dominant_emotion']

    anger_score = response_data.get('anger', 0)
    disgust_score = response_data.get('disgust', 0)
    fear_score = response_data.get('fear', 0)
    joy_score = response_data.get('joy', 0)
    sadness_score = response_data.get('sadness', 0)

    output_message = (
        f"For the given statement, the system response is "
        f"'anger': {anger_score}, 'disgust': {disgust_score}, "
        f"'fear': {fear_score}, 'joy': {joy_score}, "
        f"and 'sadness': {sadness_score}. "
        f"The dominant emotion is <b>{dominant_emotion}</b>."
    )

    return output_message

@app.route("/")
def index():
    """Renders the main page with application instructions."""
    return (
        "<h1>Emotion Detection Application</h1>"
        "<p>Use the endpoint <code>/emotionDetector?textToAnalyze=&lt;your_text&gt;</code> "
        "to analyze text.</p>"
        "<p>Example: <a href='/emotionDetector?textToAnalyze=I love my life'>"
        "/emotionDetector?textToAnalyze=I love my life</a></p>"
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
