import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import string
nltk.download('punkt_tab')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

faqs = [
    {"question": "What are your working hours?", "answer": "We are open from 9 AM to 5 PM, Monday through Friday."},
    {"question": "How can I reset my password?", "answer": "Click on 'Forgot Password' on the login page to reset your password."},
    {"question": "Where are you located?", "answer": "We are located at 123 Main Street, Chennai."},
    {"question": "What is your name?", "answer": "My name is Pinky, your friendly chatbot!"},
    {"question": "Who created you?", "answer": "I was created by Santhosh."},
    {"question": "How do I contact support?", "answer": "You can reach support at support@example.com."},
    {"question": "Do you offer home delivery?", "answer": "Yes, we offer home delivery within city limits."},
    {"question": "What payment methods do you accept?", "answer": "We accept credit cards, debit cards, UPI, and net banking."},
    {"question": "Can I cancel my order?", "answer": "Yes, you can cancel your order within 24 hours of placement."},
    {"question": "Is my data secure?", "answer": "Yes, we use encryption and follow strict privacy policies to protect your data."}
]
+[
    {"question": "What is your return policy?", "answer": "You can return items within 7 days of delivery for a full refund."},
    {"question": "Do you support international shipping?", "answer": "Currently, we only ship within India."},
    {"question": "Can I track my order?", "answer": "Yes, use the tracking link provided in your confirmation email."},
    {"question": "Is there a mobile app?", "answer": "Yes, download our app from the Google Play Store or Apple App Store."},
    {"question": "Can I update my delivery address?", "answer": "Sure! You can update it from your profile settings before dispatch."},
    {"question": "Do you offer bulk discounts?", "answer": "Absolutely! Reach out to support@example.com for bulk orders."},
    {"question": "How do I delete my account?", "answer": "Contact support and submit a request to permanently delete your account."},
    {"question": "What if I receive a damaged product?", "answer": "No worries—we’ll replace it free of charge if you notify us within 48 hours."},
    {"question": "Are your products eco-friendly?", "answer": "Yes! Most of our packaging is recyclable, and we source sustainably."},
    {"question": "Do I need an account to place an order?", "answer": "Nope! Guest checkout is available, but creating an account helps track orders."}
]

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def preprocess(text):
    tokens = nltk.word_tokenize(text.lower())
    tokens = [word for word in tokens if word not in string.punctuation]
    tokens = [word for word in tokens if word not in stop_words]
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return " ".join(tokens)

preprocessed_questions = [preprocess(faq['question']) for faq in faqs]
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(preprocessed_questions)

def get_best_match(user_question, threshold=0.2):
    user_question_prep = preprocess(user_question)
    user_vec = vectorizer.transform([user_question_prep])
    similarities = cosine_similarity(user_vec, X).flatten()
    best_idx = similarities.argmax()
    if similarities[best_idx] < threshold:
        return "Sorry, I didn’t quite catch that. Could you please rephrase or ask something else?"
    return faqs[best_idx]['answer']

print("Pinky: Ask me something or type 'exit' to quit.")
while True:
    user_input = input("You: ")
    if user_input.lower() in ("exit", "quit"):
        print("Pinky: Goodbye! Take care 😊")
        break
    answer = get_best_match(user_input)
    print("Pinky:", answer)
