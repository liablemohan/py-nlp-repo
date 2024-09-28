from bs4 import BeautifulSoup
import pandas as pd

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
    "Sanskrit", "Without Sandhi", "Multipule Morphology", "Morph in Context", 
    "Samaasa structural analysis", "Samaasa vigraha", "Kaaraka relation", "Category",
    "Hindi Meaning", "English Meaning", "Derivational Meaning", "Sandhi rules", "Meter: Guru-Laghu"
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

# Create a DataFrame using the extracted and padded data
df = pd.DataFrame({columns[i]: row_data[f"row{i+1}"] for i in range(13)})

# Path for the output CSV file
csv_output_path = "/home/dell/Desktop/pdf-txt/geeta-complete.csv"

# Save the DataFrame to a CSV file
df.to_csv(csv_output_path, index=False, encoding="utf-8")

print(f"Parallel corpus has been created and saved to: {csv_output_path}")
