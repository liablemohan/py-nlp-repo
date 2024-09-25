

from bs4 import BeautifulSoup

# Path to your HTML file
file_path = "/home/dell/Desktop/pdf-txt/all_pages.html"

# Open and read the HTML file
with open(file_path, "r", encoding="utf-8") as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, "lxml")

# Find all elements with classes 'row1', 'row6', and 'row7'
selected_rows = soup.find_all(class_=["row1", "row6", "row7"])

# Extract text content of these elements
selected_texts = [element.get_text(strip=True) for element in selected_rows]

# Path for the output text file
output_file_path = "selected_rows_texts.txt"

# Open the output file in write mode and write the extracted texts
with open(output_file_path, "w", encoding="utf-8") as output_file:
    for text in selected_texts:
        output_file.write(text + "\n")  # Write each text on a new line

# The output file path is now available for further use
print(f"Extracted texts from rows 1, 6, and 7 have been saved to: {output_file_path}")
