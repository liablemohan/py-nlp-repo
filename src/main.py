//html to txt fomat conversion

from bs4 import BeautifulSoup

# Path to your input HTML file
input_html_path = "/home/dell/Desktop/pdf-txt/test.html"

# Path for the output text file
output_text_path = "/home/dell/Desktop/pdf-txt/text_output.txt"

# Read the HTML file
with open(input_html_path, "r", encoding="utf-8") as html_file:
    html_content = html_file.read()

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, "lxml")

# Extract all the text content
text_content = soup.get_text(separator="\n", strip=True)

# Write the extracted text to the output text file
with open(output_text_path, "w", encoding="utf-8") as text_file:
    text_file.write(text_content)

print(f"HTML content has been converted to plain text and saved to '{output_text_path}'")

