import speech_recognition as sr
import RPi.GPIO as GPIO
import time

# Setup GPIO for the light
LIGHT_PIN = 18  # Replace with your GPIO pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(LIGHT_PIN, GPIO.OUT)

def ledon():
    GPIO.output(LIGHT_PIN, GPIO.HIGH)
    print("Light ON")
    time.sleep(0.5)  # Debounce time

def ledoff():
    GPIO.output(LIGHT_PIN, GPIO.LOW)
    print("Light OFF")
    time.sleep(0.5)  # Debounce time

def listencommand():
    # Initialize the recognizer
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    try:
        with microphone as source:
            print("Adjusting for background noise... Please wait.")
            recognizer.adjust_for_ambient_noise(source)
            print("Listening for command...")
            audio = recognizer.listen(source)

            # Recognize speech using Google Speech Recognition
            command = recognizer.recognize_google(audio).lower()
            print(f"Command received: {command}")

            return command
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
    except sr.RequestError:
        print("Could not request results from the speech recognition service.")
    return ""

def process_command(command):
    print(f"Processing command: {command}")
    if "light on" in command:
        print("Recognized command: Light ON")
        ledon()
    elif "light off" in command:
        print("Recognized command: Light OFF")
        ledoff()
    else:
        print("Command not recognized. Please say 'light on' or 'light off'.")

if __name__ == "__main__":
    try:
        while True:
            command = listencommand()
            if command:
                process_command(command)
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting program.")
    finally:
        GPIO.cleanup()
