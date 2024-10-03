from bs4 import BeautifulSoup
import pandas as pd
import os
import re  # Regular expressions for parsing the index

# Path to your HTML file
file_path = "/home/dell/Desktop/pdf-txt/GeetA.html"

# Open and read the HTML file
with open(file_path, "r", encoding="utf-8") as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, "lxml")

# The classes for each row from 'row1' to 'row13'
row_classes = [f"row{i}" for i in range(1, 14)]
columns = [
    "Index", "Sanskrit", "Without Sandhi", "Multiple Morphology", "Morph in Context", 
    "Samaasa Structural Analysis", "Samaasa Vigraha", "Kaaraka Relation", "Category",
    "Hindi Meaning", "English Meaning", "Derivational Meaning", "Sandhi Rules", "Meter: Guru-Laghu"
]

# Extract text content for each row class and store them in a dictionary
row_data = {}
max_length = 0

for row_class in row_classes:
    elements = soup.find_all(class_=row_class)
    # Extract text content, replacing '~' and '_' with a single space
    text_list = [element.get_text(strip=True).replace('~', ' ').replace('_', ' ') for element in elements]
    row_data[row_class] = text_list
    # Update the maximum length for padding later
    max_length = max(max_length, len(text_list))

# Pad the lists to ensure all have the same length
for key in row_data:
    row_data[key].extend([''] * (max_length - len(row_data[key])))

# Prepare the final DataFrame with index extraction and cleaning
data = []
for i in range(max_length):
    row = []
    # Extract index and text from the Sanskrit column
    if row_data['row1'][i]:  # Assuming row1 contains the Sanskrit text with index
        match = re.match(r'([0-9]+\.[0-9]+\.[A-Z])(.*)', row_data['row1'][i])
        if match:
            index = match.group(1)  # Extracted index
            text = match.group(2).strip()  # Remaining text after the index
        else:
            index = ''
            text = row_data['row1'][i]

        row.append(index)  # Add index to the row
    else:
        row.append('')  # Empty index if no text

    # Clean other columns from indexing (remove anything matching the pattern)
    row.append(text)  # Add cleaned Sanskrit text
    for j in range(2, 14):  # From row2 to row13
        cleaned_text = re.sub(r'[0-9]+\.[0-9]+\.[A-Z].*', '', row_data[f'row{j}'][i]).strip()
        row.append(cleaned_text)

    data.append(row)  # Append the cleaned row to data

# Create a DataFrame using the extracted and cleaned data
df = pd.DataFrame(data, columns=columns)

# Path for the output CSV file
csv_output_path = "/home/dell/Desktop/pdf-txt/geeta-complete.csv"

# Save the DataFrame to a CSV file
df.to_csv(csv_output_path, index=False, encoding="utf-8")

print(f"Parallel corpus has been created and saved to: {csv_output_path}")
