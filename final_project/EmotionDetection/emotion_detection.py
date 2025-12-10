import requests
import json

def emotion_detector(text_to_analyze):
    """
    Analyzes the emotion in a given text using the Watson NLP Emotion Predict service.

    Args:
        text_to_analyze (str): The text content to be analyzed for emotions.

    Returns:
        dict: A dictionary containing the predicted emotions and their scores,
              with an added 'dominant_emotion' key, or None if the analysis fails.
    """
    URL = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    HEADERS = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    input_json = { "raw_document": { "text": text_to_analyze } }

    try:
        response = requests.post(URL, headers=HEADERS, json=input_json)

        if response.status_code == 200:
            formatted_response = response.json()
            emotion_aggregated = formatted_response['emotionPredictions'][0]['emotion']
            dominant_emotion = max(emotion_aggregated, key=emotion_aggregated.get)
            emotion_aggregated['dominant_emotion'] = dominant_emotion
            
            return emotion_aggregated
        
        elif response.status_code == 400:
            return None

        else:
            print(f"Error: Request failed with status code {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {e}")
        return None