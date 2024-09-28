from bs4 import BeautifulSoup
import re
import csv

# Path to your HTML file
file_path = "/home/dell/Desktop/web-txt/GeetA.html"

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
        text = element.get_text(strip=True)  # No processing at this stage
        if re.match(r'\d+\.\d+', text):  # Check if it's a sentence ID
            if current_sentence:
                texts.append(f"{current_id} {current_sentence.strip()}")
            current_id = text
            current_sentence = ""
        else:
            current_sentence += " " + text
    
    if current_sentence:  # Add the last sentence
        texts.append(f"{current_id} {current_sentence.strip()}")
    
    return texts

# Extract elements for 'row1', 'row9', and 'row10'
sanskrit_texts = extract_formatted_text(soup.find_all(class_="row1"))
hindi_texts = extract_formatted_text(soup.find_all(class_="row9"))
english_texts = extract_formatted_text(soup.find_all(class_="row10"))

# Ensure all lists are of equal length
max_length = max(len(sanskrit_texts), len(hindi_texts), len(english_texts))
sanskrit_texts.extend([""] * (max_length - len(sanskrit_texts)))
hindi_texts.extend([""] * (max_length - len(hindi_texts)))
english_texts.extend([""] * (max_length - len(english_texts)))

# Combine all texts into rows
all_texts = list(zip(sanskrit_texts, hindi_texts, english_texts))

# Path for the output CSV file
csv_output_path = "/home/dell/Desktop/web-txt/Geeta-sent.csv"

# Save the formatted text to a CSV file
with open(csv_output_path, "w", encoding="utf-8", newline='') as file:
    writer = csv.writer(file)
    # Write the header row
    writer.writerow(["Sanskrit", "Hindi", "English"])
    # Write the rows of data
    writer.writerows(all_texts)

print(f"Initial CSV file created: {csv_output_path}")

# Step 2: Read back the CSV and replace '~' and '_' with a single space
processed_texts = []
with open(csv_output_path, "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    # Skip header row
    headers = next(reader)
    
    # Process each row
    for row in reader:
        processed_row = [col.replace('~', ' ').replace('_', ' ') for col in row]
        processed_texts.append(processed_row)

# Save the processed text back to the CSV file
with open(csv_output_path, "w", encoding="utf-8", newline='') as file:
    writer = csv.writer(file)
    # Write the header row
    writer.writerow(headers)
    # Write the processed rows
    writer.writerows(processed_texts)

print(f"Final formatted CSV with replacements saved: {csv_output_path}")
