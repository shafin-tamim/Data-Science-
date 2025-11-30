import speech_recognition as sr 
import pyttsx3 
import logging 
import os 
import datetime 
import wikipedia 
import webbrowser 
import random 
import subprocess 
import google.generativeai as genai 
from dotenv import load_dotenv


# Configure logging
LOG_DIR = "logs"
LOG_FILE_NAME = "application.log"

os.makedirs(LOG_DIR, exist_ok=True)

log_path = os.path.join(LOG_DIR, LOG_FILE_NAME)

logging.basicConfig(
    filename= log_path,
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
    )

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in environment variables")
genai.configure(api_key=api_key)
logging.info("Environment variables loaded successfully.")  


# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
engine.setProperty('rate', 170)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Select the first voice


def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        logging.info("Listening for command...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        logging.info("Recognizing command...")
        query = r.recognize_google(audio, language='en-in')
        logging.info(f"Command recognized: {query}")
    
    except Exception as e:
        logging.info(e)
        print("Say that again please...")
        return "None"

    return query


def wish_me():
    """Greet the user based on the time of day."""
    hour = (datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    
    speak("I am Jarvis. How may I assist you today?")


def gemini_model_response(user_input):
    GEMINI_API_KEY = api_key
    genai.configure(api_key=GEMINI_API_KEY) 
    model = genai.GenerativeModel("gemini-2.5-flash") 
    prompt = f"Your name is JARVIS, You act like JARVIS. Answar the provided question in short, Question: {user_input}"
    response = model.generate_content(prompt)
    result = response.text

    return result

wish_me()

while True:
    query = take_command().lower()
    if "your name" in query:
        speak("My name is Jarvis")
        logging.info("User asked for assistant's name.")

    elif "time" in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"Sir the time is {strTime}")
        logging.info("User asked for current time.")

    

    elif "how are you" in query:
        speak("I am functioning at full capacity sir!")
        logging.info("User asked about assistant's well-being.")

        
    elif "who made you" in query:
        speak("I was created by Shafin sir, a brilliant mind!")
        logging.info("User asked about assistant's creator.")

        
    elif "thank you" in query:
        speak("It's my pleasure sir. Always happy to help.")
        logging.info("User expressed gratitude.")

        
    elif "open google" in query:
        speak("ok sir. please type here what do you want to read")
        webbrowser.open("google.com")
        logging.info("User requested to open Google.")

        
 
    elif "open calculator" in query or "calculator" in query:
        speak("Opening calculator")
        subprocess.Popen("calc.exe")
        logging.info("User requested to open Calculator.")

        

    elif "open notepad" in query:
        speak("Opening Notepad")
        subprocess.Popen("notepad.exe")
        logging.info("User requested to open Notepad.")

        
    # Calendar
    elif "open calendar" in query or "calendar" in query:
        speak("Opening Windows Calendar")
        webbrowser.open("https://calendar.google.com")
        logging.info("User requested to open Calendar.")

        
  
    elif "youtube" in query:
        speak("Opening YouTube for you.")
        query = query.replace("youtube", "")
        webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
        logging.info("User requested to search on YouTube.")

        
    elif "open facebook" in query:
        speak("ok sir. opening facebook")
        webbrowser.open("facebook.com")
        logging.info("User requested to open Facebook.")

        
    elif "open github" in query:
        speak("ok sir. opening github")
        webbrowser.open("github.com")
        logging.info("User requested to open GitHub.")


    elif "open linkedin" in query:
        speak("ok sir. opening linkedin")
        webbrowser.open("linkedin.com")
        logging.info("User requested to open GitHub.")
   

    elif "joke" in query:
        jokes = [
                "Why don't programmers like nature? Too many bugs.",
                "I told my computer I needed a break. It said no problem, it will go to sleep.",
                "Why do Java developers wear glasses? Because they don't C sharp."
            ]
        speak(random.choice(jokes))
        logging.info("User requested a joke.")

        
    elif "wikipedia" in query:
        speak("Searching Wikipedia...")
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        speak(results)
        logging.info("User requested information from Wikipedia.")


    elif "exit" in query or "quit" in query or "stop" in query:
            speak("Goodbye sir! Have a great day.")
            logging.info("User requested to exit the application.")
            exit()


    else:
        response = gemini_model_response(query)
        speak(response)
        logging.info("User asked for others question")

        

