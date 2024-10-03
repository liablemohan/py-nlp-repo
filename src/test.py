import csv
import re

# Function to separate Roman index from Devanagari text and remove the alphabet from the index
def separate_text(text):
    # Regex pattern to match the Roman script (structural index)
    roman_index = re.match(r'([0-9.]+)[A-Z]', text)
    
    if roman_index:
        # Get the Roman index without the alphabet (e.g., 1.1 from 1.1.A)
        roman_part = roman_index.group(1)
        devanagari_part = text[len(roman_index.group()):]
        return roman_part, devanagari_part
    return None, text  # If no Roman part is found, treat the whole text as Devanagari
# Input and output file names
input_csv = '/home/dell/Desktop/web-txt/output/geeta-complete.csv'  # Replace with your input file path
output_csv = '/home/dell/Desktop/web-txt/output/geeta2.csv'  # This will be the output file

# Open the input CSV file and read the data
with open(input_csv, mode='r', encoding='utf-8') as infile:
    reader = csv.reader(infile)
    
    # Open the output CSV file to write the separated content
    with open(output_csv, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        
        # Write header row
        writer.writerow(['Structural Index', 'Devanagari Text'])
        
        # Read each row from the input file
        for row in reader:
            roman_part = None  # Reset the Roman index tracker for each row
            
            # Initialize a list to hold the row data for writing
            row_data = []
            
            for text in row:  # Process each cell in the row
                temp_roman_part, temp_devanagari_part = separate_text(text)
                
                if roman_part is None and temp_roman_part:
                    # Keep the first structural index (with alphabet removed)
                    roman_part = temp_roman_part
                    row_data.append(roman_part)  # Add to the row data
                    row_data.append(temp_devanagari_part)  # Add Devanagari text
                elif roman_part is not None and temp_roman_part:
                    # Skip writing the additional Roman index
                    row_data.append("")  # Empty for additional Roman index
                    row_data.append(temp_devanagari_part)  # Add Devanagari text
                elif roman_part is not None:
                    # Write only Devanagari text for remaining cells
                    row_data.append("")  # Empty for the Roman index
                    row_data.append(temp_devanagari_part)  # Add Devanagari text
            
            # Write the horizontal row data if any data exists
            if row_data:
                writer.writerow(row_data)

print("CSV file created successfully.")
