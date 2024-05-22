import tkinter as tk
from tkinter import ttk
import threading
import re
import tokenizer

from mlx_lm import load, generate

class ChatBot:
    def __init__(self, master):
        self.master = master
        self.master.title("ChatBot")
        self.master.configure(bg='#2c3e50')

        # Create main frame
        main_frame = ttk.Frame(self.master, padding="10 10 10 10")
        main_frame.pack(expand=True, fill=tk.BOTH)

        # Create text area with scrollbar
        self.text_area_frame = ttk.Frame(main_frame)
        self.text_area_frame.pack(expand=True, fill=tk.BOTH)

        self.text_area = tk.Text(self.text_area_frame, height=20, width=50, wrap=tk.WORD, state=tk.DISABLED, bg='#ecf0f1', fg='#2c3e50', font=('Arial', 12))
        self.text_area.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5, pady=5)

        self.scrollbar = ttk.Scrollbar(self.text_area_frame, command=self.text_area.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_area['yscrollcommand'] = self.scrollbar.set

        # Create entry field and submit button frame
        entry_frame = ttk.Frame(main_frame)
        entry_frame.pack(fill=tk.X, pady=10)

        # Create a multiline text field
        self.entry_field = tk.Text(entry_frame, height=5, width=50, font=('Arial', 12))
        self.entry_field.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        # Create a scrollbar for the text field
        scrollbar = ttk.Scrollbar(entry_frame, orient=tk.VERTICAL, command=self.entry_field.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.entry_field.configure(yscrollcommand=scrollbar.set)

        self.submit_button = ttk.Button(entry_frame, text="Submit", command=self.send_command)
        self.submit_button.pack(side=tk.RIGHT, padx=5)

        # Load model
        self.model, self.tokenizer = load("mlx-community/codegemma-1.1-7b-it-8bit")

    def format_code_blocks(self, text):
        # Regular expression pattern
        pattern = r"```"

        # Iterate over the matches
        formatted_fragments = []
        fragments = re.split(pattern, text)
        for i, fragment in enumerate(fragments):
            if i % 2 == 0:
                # This fragment is regular text
                formatted_fragments.append(fragment)
                self.text_area.insert(tk.END, fragment)
            else:
                # This fragment is a code block, so format it
                self.text_area.insert(tk.END, fragment)
                formatted_code = f'```\n{fragment}\n```'
                formatted_fragments.append(formatted_code)
                tokenizer.format_code(self.text_area, fragment)
        return formatted_fragments        

    def send_command(self):
        self.entry_field.config(state='disabled')
        self.submit_button.config(state='disabled')

        command = self.entry_field.get('1.0', 'end-1c')
        self.text_area.config(state=tk.NORMAL)
        self.text_area.insert(tk.END, f"You: {command}\n")
        self.text_area.config(state=tk.DISABLED)

        def run_command():
            response = generate(self.model, self.tokenizer, prompt=f"{command}", verbose=True, max_tokens=1500)

            self.text_area.config(state=tk.NORMAL)
            # Test the function
            formatted_fragments = self.format_code_blocks(response)

            self.entry_field.config(state='normal')
            self.submit_button.config(state='normal')

            self.text_area.insert(tk.END, "\n")

        thread = threading.Thread(target=run_command)
        thread.start()

root = tk.Tk()
style = ttk.Style(root)
style.theme_use('clam')  # You can change this to 'default', 'classic', 'alt', or 'clam' depending on what looks best

my_bot = ChatBot(root)
root.mainloop()
