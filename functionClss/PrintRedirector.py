import tkinter as tk

class PrintRedirector:
    def __init__(self, text_widget):
        self.text_space = text_widget
    def write(self, text):
        self.text_space.insert(tk.END, text)