import requests
from bs4 import BeautifulSoup

# Base URL structure with placeholders for chapter and page numbers
base_url = "http://scl.samsaadhanii.in/scl/e-readers/sbg/{chapter}/{chapter}-{page}/{chapter}-{page}.html"

# Start the iteration from chapter 1
chapter_number = 1

# Open a single file to write all HTML content
output_file_path = "/home/dell/Desktop/pdf-txt/GeetA.html"
with open(output_file_path, "w", encoding="utf-8") as output_file:
    # Write the initial HTML structure
    output_file.write("<html>\n<head>\n<meta charset='UTF-8'>\n<title>Combined Pages</title>\n</head>\n<body>\n")

    while True:
        page_number = 1
        pages_found_in_chapter = False  # Flag to track if any page was found in the current chapter
        
        while True:
            # Construct the URL based on the current chapter and page
            page_identifier = f"{chapter_number}/{chapter_number}-{page_number}/{chapter_number}-{page_number}"
            url = base_url.format(chapter=chapter_number, page=page_number)

            # Make a GET request to the URL
            response = requests.get(url)

            # Check if the page was found
            if response.status_code == 200:
                pages_found_in_chapter = True
                print(f"Page {page_identifier} found. Extracting content...")
                
                # Decode the response content correctly
                response.encoding = response.apparent_encoding
                html_content = response.content.decode(response.encoding, errors='ignore')
                
                # Parse the HTML content with BeautifulSoup
                soup = BeautifulSoup(html_content, "html.parser")
                
                # Extract the outer HTML of the page
                body_content = soup.find("body")
                if body_content:
                    # Append the outer HTML of the body to the combined content
                    output_file.write(str(body_content))
                
                # Increment the page number for the next iteration
                page_number += 1
            elif response.status_code == 404:
                print(f"Page {page_identifier} not found. Ending chapter {chapter_number} iteration.")
                break  # Exit the inner loop to move to the next chapter
            else:
                print(f"Encountered an error: Status code {response.status_code}")
                break

        # Check if any pages were found in the current chapter
        if not pages_found_in_chapter:
            print(f"No pages found in chapter {chapter_number}. Ending the process.")
            break  # Exit the outer loop if no pages were found in the chapter
        
        # Move to the next chapter
        chapter_number += 1

    # Write the closing tags for the combined HTML file
    output_file.write("\n</body>\n</html>")

print(f"All pages have been combined and saved in '{output_file_path}'. Program finished.")
