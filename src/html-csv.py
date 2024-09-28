from bs4 import BeautifulSoup
import pandas as pd

# Path to your HTML file
file_path = "/home/dell/Desktop/pdf-txt/all_pages.html"

# Open and read the HTML file
with open(file_path, "r", encoding="utf-8") as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, "lxml")

# Extract elements for 'row1', 'row6', and 'row7'
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

# Create a DataFrame with columns for "Sanskrit", "Hindi", and "English"
df = pd.DataFrame({
    "संस्कृतम्": row1_texts,
    "Morphological Analysis": row3_texts,
    "शब्दविश्लेषणम्": row4_texts,
    "हिन्दी-विभक्ति:": row5_texts,
    "हिन्दी अर्ध": row6_texts,
    "English Meaning": row7_texts
})

# Path for the output CSV file
csv_output_path = "complete.csv"

# Save the DataFrame to a CSV file
df.to_csv(csv_output_path, index=False, encoding="utf-8")

print(f"Parallel corpus has been created and saved to: {csv_output_path}")
