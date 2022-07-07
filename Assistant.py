from cmath import e
from gtts import gTTS 
import speech_recognition as sr
import playsound
import os
import wolframalpha
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
num = 1
driver = 0
def assistant_speaks(output):
    global num
  
    num += 1
    print("PerSon : ", output)
  
    toSpeak = gTTS(text = output, lang ='en', slow = False)
    # saving the audio file given by google text to speech
    file = str(num)+".mp3 "
    toSpeak.save(file)
      
    
    playsound.playsound(file, True) 
    os.remove(file)
  
  
def get_audio():
  
    rObject = sr.Recognizer()
    audio = ''
  
    with sr.Microphone() as source:
        print("Speak...")
          
        # recording the audio using speech recognition
        audio = rObject.listen(source, phrase_time_limit = 5) 
    print("Stop.") # limit 5 secs
  
    try:
  
        text = rObject.recognize_google(audio, language ='en-US')
        print("You : ", text)
        return text
  
    except:
  
        assistant_speaks("Could not understand your audio, PLease try again !")
        return 0
  
  
def process_text(input):
	try:
		if 'search' in input or 'play' in input:
			
			search_web(input)
			return

		elif "who are you" in input or "define yourself" in input:
			speak = '''Hello, I am Your personal Assistant.
			You can command me to perform
			various tasks such as calculating sums or opening applications etcetra'''
			assistant_speaks(speak)
			return

		elif "who made you" in input or "created you" in input:
			speak = "I have been created by Harshitha."
			assistant_speaks(speak)
			return


		elif "calculate" in input.lower():
			
			
			app_id = "U8U95H-GRUAR3GQVE"
			client = wolframalpha.Client(app_id)

			indx = input.lower().split().index('calculate')
			query = input.split()[indx + 1:]
			res = client.query(' '.join(query))
			answer = next(res.results).text
			assistant_speaks("The answer is " + answer)
			return

		elif 'open' in input:
			
			
			open_application(input.lower())
			return

		else:
			while True:
				assistant_speaks("I can search the web for you, Do you want to continue?")
				ans = get_audio()
				if 'yes' in str(ans) or 'yeah' in str(ans) or 'ok' in str(ans):
					search_web(input)
				elif 'no' in str(ans):
					return
				else:
					assistant_speaks("I don't understand")
    
	except Exception as e:
		# print(e)
		assistant_speaks("I don't understand, I can search the web for you, Do you want to continue?")
		ans = get_audio()
		if 'yes' in str(ans) or 'yeah' in str(ans):
			search_web(input)

def search_web(input):
	global driver
	driver = webdriver.Chrome(executable_path="./chromedriver.exe")
	driver.implicitly_wait(1)
	driver.maximize_window()
	

	if 'youtube' in input.lower():

		assistant_speaks("Opening in youtube")
		indx = input.lower().split().index('youtube')
		query = input.split()[indx + 1:]
		print(query)
		driver.get("https://www.youtube.com/results?search_query=" + '+'.join(query))

		return

	elif 'wikipedia' in input.lower():

		assistant_speaks("Opening Wikipedia")
		indx = input.lower().split().index('wikipedia')
		query = input.split()[indx + 1:]
		driver.get("https://en.wikipedia.org/wiki/" + '_'.join(query))
		return

	else:

		if 'google' in input:

			indx = input.lower().split().index('google')
			query = input.split()[indx + 1:]
			driver.get("https://www.google.com/search?q=" + '+'.join(query))

		elif 'search' in input:

			indx = input.lower().split().index('google')
			query = input.split()[indx + 1:]
			driver.get("https://www.google.com/search?q=" + '+'.join(query))

		else:

			driver.get("https://www.google.com/search?q=" + '+'.join(input.split()))

		return


# function used to open application
# present inside the system.
def open_application(input):

	if "chrome" in input:
		assistant_speaks("Google Chrome")
		os.startfile('C:\Program Files\Google\Chrome\Application\chrome.exe')
		return

	elif "firefox" in input or "mozilla" in input:
		assistant_speaks("Opening Mozilla Firefox")
		os.startfile('C:\Program Files\Mozilla Firefox\\firefox.exe')
		return

	elif "word" in input:
		assistant_speaks("Opening Microsoft Word")
		os.startfile("C:\Program Files\Microsoft Office\\root\Office16\WINWORD.EXE")
		return

	elif "excel" in input:
		assistant_speaks("Opening Microsoft Excel")
		os.startfile('C:\Program Files\Microsoft Office\\root\Office16\EXCEL.EXE')
		return

	else:

		assistant_speaks("Application not available")
		return

# Driver Code
if __name__ == "__main__":
	assistant_speaks("What's your name?")
	name ='Human'
	name = get_audio()
	assistant_speaks("Hello, " + name + '.')

	while(1):

		assistant_speaks("What can i do for you?")
		text = get_audio()

		if text == 0:
			continue
		text = text.lower()


		if "exit" in str(text) or "bye" in str(text) or "sleep" in str(text):
			assistant_speaks("Ok bye, "+ name+'.')
			break

		# calling process text to process the query
		process_text(text)

