import re
import tkinter as tk
from tkinter import ttk


def format_code(edit_area, text):
    global previousText

    # If actually no changes have been made stop / return the function
    if edit_area.get('1.0', tk.END) == previousText:
        return

    # Remove all tags so they can be redrawn
    for tag in edit_area.tag_names():
        edit_area.tag_remove(tag, "1.0", "end")

    # Add tags where the search_re function found the pattern
    i = 0
    for pattern, color in repl:
        for start, end in search_re(pattern, edit_area.get('1.0', tk.END)):
            edit_area.tag_add(f'{i}', start, end)
            edit_area.tag_config(f'{i}', foreground=color)
            i+=1

    previousText = edit_area.get('1.0', tk.END) 

def search_re(pattern, text, groupid=0):
    matches = []

    text = text.splitlines()
    for i, line in enumerate(text):
        for match in re.finditer(pattern, line):

            matches.append(
                (f"{i + 1}.{match.start()}", f"{i + 1}.{match.end()}")
            )

    return matches


def rgb(rgb):
    return "#%02x%02x%02x" % rgb

# Define colors for the variouse types of tokens
normal = rgb((234, 234, 234))
keywords = rgb((234, 95, 95))
comments = rgb((95, 234, 165))
string = rgb((234, 162, 95))
function = rgb((95, 211, 234))
background = rgb((42, 42, 42))
code_font = 'Consolas 15'

previousText = ''

# Define a list of Regex Pattern that should be colored in a certain way
repl = [
    # Python keywords
    ['(^| )(False|None|True|and|as|assert|async|await|break|class|continue|def|del|elif|else|except|finally|for|from|global|if|import|in|is|lambda|nonlocal|not|or|pass|raise|return|try|while|with|yield)($| )', keywords],
    # Python strings
    ['".*?"', string],
    ['\'.*?\'', string],
    # Python comments
    ['#.*?$', comments],

    # C, C++, C#, and Java keywords
    ['(^| )(auto|break|case|char|const|continue|default|do|double|else|enum|explicit|export|extern|float|for|friend|goto|if|inline|int|long|namespace|register|reinterpret_cast|short|signed|sizeof|static|static_assert|static_cast|struct|switch|template|this|thread_local|throw|try|typedef|typeid|typename|union|unsigned|using|virtual|void|volatile|wchar_t|while)($| )', keywords],
    # C, C++, C#, and Java strings
    ['L?".*?"', string],  # C++ and C# raw string literals
    ['bR?".*?"', string],  # C++ binary and raw string literals
    ['br?".*?"', string],  # C++ binary and raw string literals
    ['B?".*?"', string],  # C++ binary string literals
    ['b?".*?"', string],  # C++ binary string literals
    ['R?".*?"', string],  # C++ and C# raw string literals
    ['r?".*?"', string],  # C++ and C# raw string literals
    ['u8?".*?"', string],  # C++ and C# UTF-8 string literals
    ['u?".*?"', string],  # C++ and C# Unicode string literals
    ['U?".*?"', string],  # C++ and C# wide Unicode string literals
    ['".*?"', string],
    ['\'.*?\'', string],
    # C, C++, C#, and Java single-line comments
    ['//.*?$', comments],
    # C and C++ multi-line comments
    [r'/\*.*?\*/', comments],  # Use a raw string for the pattern
]