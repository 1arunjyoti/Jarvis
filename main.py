import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI

recognizer = sr.Recognizer()
engine = pyttsx3.init()

newsapi = "882fa2ed46774d169b0d441ba188864a"

def speak(text):
    engine.say(text)
    engine.runAndWait()

#needs a paid openai account to use the api
def aiProcess(command):
    #client = OpenAI(api_key="",)

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a virtual assistant, skilled in genaral tasks."},
            {"role": "user", "content": "what is coding"}
        ]
    )
    return completion.choices[0].message.content

def processCommand(c):
    if 'open google' in c.lower():
        webbrowser.open("https://google.com")
    elif 'open youtube' in c.lower():
        webbrowser.open("https://youtube.com")
    elif 'open facebook' in c.lower():
        webbrowser.open("https://facebook.com")
    elif 'open instagram' in c.lower():
        webbrowser.open("https://instagram.com")
    elif c.lower().startwith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music(song)
        webbrowser.open(link)

    elif "news" in c.lower():
        r = requests.get("https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")

        if r.status_code == 200:
            data = r.json()
            articles = data.get("articles", [])
            for article in articles:
                speak(article["title"])

    else:
        #let openai handle the rest
        output = aiProcess(c)
        speak(output)

    
if __name__ == "__main__":
    speak("Initializing Jarvis...")

    while(True):
        # obtain audio from the microphone
        #listen for the wake word
        r = sr.Recognizer()
        
        # recognize speech 
        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...!")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)
            word = r.recognize_google(audio)
            if(word.lower() == "jarvis"):
                speak("Ya")
                with sr.Microphone() as source:
                    print("Listening...!")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)
            #print(command)
        
        #except sr.UnknownValueError:
        #    print("Sphinx could not understand audio")
        #except sr.RequestError as e:
        #    print("Sphinx error; {0}".format(e))

        except Exception as e:
            print("Error: {0}".format(e))
        