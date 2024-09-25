// Roman text extraction from Sansadhini  http://scl.samsaadhanii.in/scl/e-readers/sankshepa_ramayanam/ramayana-interface/index2.html




// This copies OuterHTML element of html pages and creates sigle body html page.

//pip install requests beautifulsoup4 lxml (Dependencies)


//extractor
import requests
from bs4 import BeautifulSoup

# Base URL without the changing digit
base_url = "http://scl.samsaadhanii.in/scl/e-readers/sankshepa_ramayanam/ramayana-interface/anusaaraka/"
file_extension = ".html"

# Start the iteration from 1
page_number = 1

# Open a single file to write all HTML content
with open("all_pages.html", "w", encoding="utf-8") as output_file:
    # Start the combined body content
    combined_body_content = ""

    while True:
        # Construct the URL
        url = f"{base_url}{page_number}{file_extension}"
        
        # Make a GET request to the URL
        response = requests.get(url)
        
        # Check if the page was found
        if response.status_code == 200:
            print(f"Page {page_number} found. Extracting content...")
            
            # Parse the HTML content with BeautifulSoup
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Extract the content of the body tag
            body_content = soup.find("body")
            if body_content:
                # Append the body content to the combined content
                combined_body_content += str(body_content)
            
            # Increment the page number for the next iteration
            page_number += 1
        elif response.status_code == 404:
            print(f"Page {page_number} not found. Ending the process.")
            break
        else:
            print(f"Encountered an error: Status code {response.status_code}")
            break

    # Write the combined body content inside a single body tag
    output_file.write("<html>\n<head>\n<title>Combined Pages</title>\n</head>\n<body>\n")
    output_file.write(combined_body_content)
    output_file.write("\n</body>\n</html>")

print("All pages have been combined and saved in 'all_pages.html'. Program finished.")



//=======================================================================================//


//Specific row sorting after extraction.

from bs4 import BeautifulSoup

# Path to your HTML file
file_path = "all_pages.html"

# Open and read the HTML file
with open(file_path, "r", encoding="utf-8") as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, "lxml")

# Find all elements with class 'row7'
row7_elements = soup.find_all(class_="row7")

# Extract text content of these elements
row7_texts = [element.get_text(strip=True) for element in row7_elements]

# Path for the output text file
output_file_path = "row7_texts.txt"

# Open the output file in write mode and write the extracted texts
with open(output_file_path, "w", encoding="utf-8") as output_file:
    for text in row7_texts:
        output_file.write(text + "\n")  # Write each text on a new line

# The output file path is now available for further use
print(f"Extracted texts have been saved to: {output_file_path}")

//===========================================================//