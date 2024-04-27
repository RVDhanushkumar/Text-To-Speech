import tkinter as tk
from tkinter import ttk, messagebox
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
            messagebox.showerror("Error", "Invalid voice ID")

    def save_to_file(self, text, voice_id, rate, volume, filename="output.wav"):
        try:
            self.speak(text, voice_id, rate, volume)
            self.engine.save_to_file(text, filename)
            self.engine.runAndWait()
            messagebox.showinfo("Success", f"Audio saved as {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save audio: {str(e)}")

class TextToSpeechApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text-to-Speech Application")
        self.create_widgets()

    def create_widgets(self):
        self.tts_engine = TextToSpeechEngine()

        # Text Input
        self.text_label = ttk.Label(self.root, text="Enter text:")
        self.text_label.grid(row=0, column=0, padx=10, pady=10)
        self.text_entry = tk.Text(self.root, width=50, height=10)
        self.text_entry.grid(row=0, column=1, padx=10, pady=10)

        # Voice Selection
        self.voice_label = ttk.Label(self.root, text="Select voice:")
        self.voice_label.grid(row=1, column=0, padx=10, pady=10)
        self.voices = self.tts_engine.get_supported_voices()
        self.voice_names = [voice.name for voice in self.voices]
        self.voice_combo = ttk.Combobox(self.root, values=self.voice_names, width=45)
        self.voice_combo.grid(row=1, column=1, padx=10, pady=10)
        self.voice_combo.current(0)

        # Speech Parameters
        self.rate_label = ttk.Label(self.root, text="Rate:")
        self.rate_label.grid(row=2, column=0, padx=10, pady=10)
        self.rate_slider = ttk.Scale(self.root, from_=50, to=200, orient=tk.HORIZONTAL)
        self.rate_slider.grid(row=2, column=1, padx=10, pady=10)
        self.rate_slider.set(150)

        self.volume_label = ttk.Label(self.root, text="Volume:")
        self.volume_label.grid(row=3, column=0, padx=10, pady=10)
        self.volume_slider = ttk.Scale(self.root, from_=0, to=100, orient=tk.HORIZONTAL)
        self.volume_slider.grid(row=3, column=1, padx=10, pady=10)
        self.volume_slider.set(100)

        # Playback Controls
        self.play_button = ttk.Button(self.root, text="Play", command=self.play_text)
        self.play_button.grid(row=4, column=0, padx=10, pady=10)

        self.save_button = ttk.Button(self.root, text="Save Audio", command=self.save_audio)
        self.save_button.grid(row=4, column=1, padx=10, pady=10)

        self.exit_button = ttk.Button(self.root, text="Exit", command=self.root.quit)
        self.exit_button.grid(row=4, column=2, padx=10, pady=10)

    def play_text(self):
        text = self.text_entry.get("1.0", tk.END)
        if text.strip():
            voice_id = self.voice_names.index(self.voice_combo.get())
            rate = self.rate_slider.get()
            volume = self.volume_slider.get()
            self.tts_engine.speak(text, voice_id, rate, volume)
        else:
            messagebox.showerror("Error", "Please enter text to play.")

    def save_audio(self):
        text = self.text_entry.get("1.0", tk.END)
        if text.strip():
            voice_id = self.voice_names.index(self.voice_combo.get())
            rate = self.rate_slider.get()
            volume = self.volume_slider.get()
            self.tts_engine.save_to_file(text, voice_id, rate, volume)
        else:
            messagebox.showerror("Error", "Please enter text to save.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TextToSpeechApp(root)
    root.mainloop()