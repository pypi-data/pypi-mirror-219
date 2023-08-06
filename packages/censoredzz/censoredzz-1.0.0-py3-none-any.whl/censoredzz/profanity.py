import re
import os
import pickle
from sklearn.feature_extraction.text import CountVectorizer

def has_profanity(sentence):
    # Load the machine learning model
    model_path = os.path.join(os.path.dirname(__file__), 'models', 'rf_model.pkl')
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    # Load the vocabulary used for training
    vocabulary_path = os.path.join(os.path.dirname(__file__), 'models', 'vocabulary.pkl')
    with open(vocabulary_path, 'rb') as f:
        vocabulary = pickle.load(f)
    # Extract features
    vectorizer = CountVectorizer(vocabulary=vocabulary)
    
    # Split sentence into individual words
    sentence_tokens = sentence.split()

    
    for token in sentence_tokens:
        #lowercase
        preprocessed_token = token.lower()  # Perform any necessary preprocessing steps
        token_features = vectorizer.transform([preprocessed_token])
        # Predict the class
        if model.predict(token_features)[0] ==1:
            return True
    return False
