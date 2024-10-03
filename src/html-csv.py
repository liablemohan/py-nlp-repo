# for content processing of extracted html content of Sankshepa ramayana from Sansaadhanii.scl for all rows into csv 

from bs4 import BeautifulSoup
import pandas as pd
import os
import re  # Regular expressions for parsing the index

# Path to your HTML file
file_path = "/home/dell/Desktop/web-txt/Geeta.html"

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

# Create a DataFrame with separate columns for index and text
data = []
for i in range(max_length):
    # Extract index and text from the row1_texts (assumed to be formatted like "2.1.Atext")
    if row1_texts[i]:  # Ensure there's text to process
        match = re.match(r'([0-9]+\.[0-9]+\.[A-Z])(.*)', row1_texts[i])
        if match:
            index = match.group(1)  # Extracted index
            text = match.group(2).strip()  # Remaining text after the index
        else:
            index = ''
            text = row1_texts[i]

    else:
        index = ''
        text = ''

    # Clean other texts from indexing (remove anything matching the pattern)
    row3_cleaned = re.sub(r'[0-9]+\.[0-9]+\.[A-Z]', '', row3_texts[i]).strip()
    row4_cleaned = re.sub(r'[0-9]+\.[0-9]+\.[A-Z]', '', row4_texts[i]).strip()
    row5_cleaned = re.sub(r'[0-9]+\.[0-9]+\.[A-Z]', '', row5_texts[i]).strip()
    row6_cleaned = re.sub(r'[0-9]+\.[0-9]+\.[A-Z]', '', row6_texts[i]).strip()
    row7_cleaned = re.sub(r'[0-9]+\.[0-9]+\.[A-Z]', '', row7_texts[i]).strip()

    # Replace '~' and '_' with a single space
    text = text.replace('~', ' ').replace('_', ' ')
    row3_cleaned = row3_cleaned.replace('~', ' ').replace('_', ' ')
    row4_cleaned = row4_cleaned.replace('~', ' ').replace('_', ' ')
    row5_cleaned = row5_cleaned.replace('~', ' ').replace('_', ' ')
    row6_cleaned = row6_cleaned.replace('~', ' ').replace('_', ' ')
    row7_cleaned = row7_cleaned.replace('~', ' ').replace('_', ' ')

    # Append the cleaned data to the data list
    data.append([index, text, row3_cleaned, row4_cleaned, row5_cleaned, row6_cleaned, row7_cleaned])

# Create a DataFrame with the specified columns
df = pd.DataFrame(data, columns=["Index", "संस्कृतम्", "Morphological Analysis", "शब्दविश्लेषणम्", "हिन्दी-विभक्ति:", "हिन्दी अर्ध", "English Meaning"])

# Path for the output CSV file
csv_output_path = "/home/dell/Desktop/web-txt/output/Geeta-complete.csv"

# Save the DataFrame to a CSV file
df.to_csv(csv_output_path, index=False, encoding="utf-8")

print(f"Parallel corpus has been created and saved to: {csv_output_path}")
