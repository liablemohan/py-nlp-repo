
import requests
from bs4 import BeautifulSoup

# Base URL without the changing digit
base_url = "http://scl.samsaadhanii.in/scl/e-readers/sbg/1/sloka_infrm.html"
file_extension = ".html"

# Start the iteration from 1
page_number = 1

# Open a single file to write all HTML content
with open("/home/dell/Desktop/pdf-txt/test.html", "w", encoding="utf-8") as output_file:
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
            
            # Decode the response content correctly
            response.encoding = response.apparent_encoding
            html_content = response.content.decode(response.encoding, errors='ignore')
            
            # Parse the HTML content with BeautifulSoup
            soup = BeautifulSoup(html_content, "html.parser")
            
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
    output_file.write("<html>\n<head>\n<meta charset='UTF-8'>\n<title>Combined Pages</title>\n</head>\n<body>\n")
    output_file.write(combined_body_content)
    output_file.write("\n</body>\n</html>")

print("All pages have been combined and saved in 'all_pages.html'. Program finished.")
