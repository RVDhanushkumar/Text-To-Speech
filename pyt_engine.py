import pyttsx3

class TextToSpeechEngine:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.current_text = None

    def get_supported_voices(self):
        return self.engine.getProperty('voices')

    def speak(self, text, voice_id, rate, volume):
        self.engine.setProperty("rate", rate)
        self.engine.setProperty("volume", volume / 100)
        voices = self.get_supported_voices()
        if voice_id < len(voices):
            voice = voices[voice_id]
            self.engine.setProperty("voice", voice.id)
            self.current_text = text
            self.engine.say(text)
            self.engine.runAndWait()
        else:
            print("Invalid voice ID")

    def stop(self):
        self.engine.stop()

    def save_to_file(self, text, voice_id, rate, volume, filename="output.wav"):
        self.speak(text, voice_id, rate, volume)
        self.engine.save_to_file(self.current_text, filename)
        self.engine.runAndWait()