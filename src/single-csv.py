from bs4 import BeautifulSoup
import pandas as pd
import os
import re

# Path to your HTML file
file_path = "/home/dell/Desktop/web-txt/all_pages.html"

# Directory to save the individual CSV files
output_directory = "/home/dell/Desktop/web-txt/output_sents-rama"

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Open and read the HTML file
with open(file_path, "r", encoding="utf-8") as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, "lxml")

# Extract elements for 'row1', 'row3', 'row4', 'row5', 'row6', and 'row7'
row1_elements = soup.find_all(class_="row1")
row3_elements = soup.find_all(class_="row3")
row4_elements = soup.find_all(class_="row4")
row5_elements = soup.find_all(class_="row5")
row6_elements = soup.find_all(class_="row6")
row7_elements = soup.find_all(class_="row7")

# Extract text content of these elements
row1_texts = [element.get_text(strip=True) for element in row1_elements]
row3_texts = [element.get_text(strip=True) for element in row3_elements]
row4_texts = [element.get_text(strip=True) for element in row4_elements]
row5_texts = [element.get_text(strip=True) for element in row5_elements]
row6_texts = [element.get_text(strip=True) for element in row6_elements]
row7_texts = [element.get_text(strip=True) for element in row7_elements]

# Adjust lists to have the same length by padding with empty strings
max_length = max(len(row1_texts), len(row3_texts), len(row4_texts), len(row5_texts), len(row6_texts), len(row7_texts))
row1_texts.extend([''] * (max_length - len(row1_texts)))
row3_texts.extend([''] * (max_length - len(row3_texts)))
row4_texts.extend([''] * (max_length - len(row4_texts)))
row5_texts.extend([''] * (max_length - len(row5_texts)))
row6_texts.extend([''] * (max_length - len(row6_texts)))
row7_texts.extend([''] * (max_length - len(row7_texts)))

# Regular expression to match the index pattern like '2.1.A'
index_pattern = re.compile(r'^\d+\.\d+\.[A-Z]$')

# Variables to accumulate data for each group
current_group_data = {
    "संस्कृतम्": [],
    "Morphological Analysis": [],
    "शब्दविश्लेषणम्": [],
    "हिन्दी-विभक्ति:": [],
    "हिन्दी अर्ध": [],
    "English Meaning": []
}
current_group_index = None
file_count = 0

# Loop through each entry and group data by index
for i in range(max_length):
    current_index = row1_texts[i]

    # Debugging: Print the current_index being checked
    print(f"Processing index: {current_index}")

    # Check if the current text matches the index pattern
    if index_pattern.match(current_index):
        print(f"Matched index: {current_index}")  # Debugging statement
        
        # Save the current group to a CSV if it's not the first group
        if current_group_index is not None:
            df_sentence = pd.DataFrame(current_group_data)
            sentence_filename = f"sentence_{current_group_index}.csv"
            sentence_output_path = os.path.join(output_directory, sentence_filename)
            df_sentence.to_csv(sentence_output_path, index=False, encoding="utf-8")
            file_count += 1
            print(f"Saved: {sentence_filename}")

        # Start a new group
        current_group_index = current_index
        current_group_data = {
            "संस्कृतम्": [],
            "Morphological Analysis": [],
            "शब्दविश्लेषणम्": [],
            "हिन्दी-विभक्ति:": [],
            "हिन्दी अर्ध": [],
            "English Meaning": []
        }
    
    # Append the current row to the current group data
    current_group_data["संस्कृतम्"].append(row1_texts[i])
    current_group_data["Morphological Analysis"].append(row3_texts[i])
    current_group_data["शब्दविश्लेषणम्"].append(row4_texts[i])
    current_group_data["हिन्दी-विभक्ति:"].append(row5_texts[i])
    current_group_data["हिन्दी अर्ध"].append(row6_texts[i])
    current_group_data["English Meaning"].append(row7_texts[i])

# Save the last group
if current_group_index is not None:
    df_sentence = pd.DataFrame(current_group_data)
    sentence_filename = f"sentence_{current_group_index}.csv"
    sentence_output_path = os.path.join(output_directory, sentence_filename)
    df_sentence.to_csv(sentence_output_path, index=False, encoding="utf-8")
    file_count += 1
    print(f"Saved: {sentence_filename}")

print(f"A total of {file_count} CSV files have been created and saved in: {output_directory}")
