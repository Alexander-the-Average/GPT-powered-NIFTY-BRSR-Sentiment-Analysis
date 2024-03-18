import webbrowser
import pyautogui
import time
import pyperclip
from docx import Document

# URL of the webpage you want to open
url = "https://chat.openai.com"

# Open the webpage in the default web browser
webbrowser.open(url)

# Wait for the webpage to load (check for a specific element, adjust as needed)
while not pyautogui.locateOnScreen("webpage_loaded.png"):
    time.sleep(1)

# Path to the Word file
docx_file_path = r"C:\IIM Project\test file\WordFiles\SBIBRSR.docx"

# Function to read the specified number of characters from the Word file
def read_characters_from_docx_file(file_path, num_characters):
    try:
        doc = Document(file_path)
        text = ''
        for paragraph in doc.paragraphs:
            text += paragraph.text
            if len(text) >= num_characters:
                break
        return text
    except Exception as e:
        print(f"Error reading Word file: {str(e)}")
        return None

# Read and paste the text from the Word file in chunks of 4000 characters
chunk_size = 4000
remaining_text = read_characters_from_docx_file(docx_file_path, chunk_size)

while remaining_text:
    # Define the text to paste (including the sentence)
    text_to_paste = remaining_text[:chunk_size]
    remaining_text = remaining_text[chunk_size:]

    # Copy the text to the clipboard
    pyperclip.copy(text_to_paste)

    # Simulate pressing Ctrl+V to paste the text
    pyautogui.hotkey('ctrl', 'v')

    # Simulate pressing Enter
    pyautogui.press('enter')

    # Wait for 4 seconds for the page to load (adjust as needed)
    time.sleep(4)

# Close the browser (optional)
# webbrowser.close()
