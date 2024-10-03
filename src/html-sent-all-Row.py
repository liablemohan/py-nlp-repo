from bs4 import BeautifulSoup
import re

# Path to your HTML file
file_path = "/home/dell/Desktop/web-txt/all_pages.html"

# Open and read the HTML file
with open(file_path, "r", encoding="utf-8") as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, "lxml")

# Function to extract and format text from elements
def extract_formatted_text(elements):
    texts = []
    current_sentence = ""
    current_id = ""
    
    for element in elements:
        text = element.get_text(strip=True)
        # Remove '_' and '~' from the text
        text = text.replace('_', ' ').replace('~', ' ')
        
        if re.match(r'\d+\.\d+\.?[A-Z]?', text):  # Check if it's a sentence ID
            if current_sentence:
                texts.append(f"{current_id} {current_sentence.strip()}")
            # Remove the alphabet from the end of the numbering
            current_id = re.sub(r'([0-9]+\.[0-9]+)\.?[A-Z]?', r'\1', text)
            current_sentence = ""
        else:
            current_sentence += " " + text
    
    if current_sentence:  # Add the last sentence
        texts.append(f"{current_id} {current_sentence.strip()}")
    
    return texts

# Extract and format elements for all rows
rows = ['row1', 'row2', 'row3', 'row4', 'row5', 'row6', 'row7']
all_texts = []

for row in rows:
    row_texts = extract_formatted_text(soup.find_all(class_=row))
    all_texts.extend(row_texts)
    all_texts.append("")  # Add a blank line between rows

# Path for the output TXT file
txt_output_path = "/home/dell/Desktop/web-txt/output/parallel_corpus_formatted.txt"

# Save the formatted text to a TXT file
with open(txt_output_path, "w", encoding="utf-8") as file:
    file.write("\n".join(all_texts))

print(f"Refined formatted parallel corpus has been created and saved to: {txt_output_path}")