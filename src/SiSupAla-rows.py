import requests
import csv
import json

# Base URL of the JSON files
base_url = "http://scl.samsaadhanii.in/scl/e-readers/shishu/assets/json/canto{}.json"

# CSV file path
csv_file = "/home/dell/Desktop/web-txt/output/SiSupAla_detailed.csv"

# Initialize a list to store headers
headers = set()

# Add 'canto' as one of the headers
headers.add("canto")

# Loop through 'canto1' to 'canto10'
all_records = []
for canto_number in range(1, 11):
    # Fetch the JSON data from the URL
    url = base_url.format(canto_number)
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()

        # Collect all unique keys from all entries for the current canto
        for record in data:
            # Add 'canto' detail to each record
            record['canto'] = f"canto{canto_number}"
            
            # Update headers based on the current record's keys
            headers.update(record.keys())
            
            # Add the modified record to the list of all records
            all_records.append(record)
    else:
        print(f"Failed to fetch data from {url}")

# Convert the set to a sorted list to ensure consistent column ordering
headers = sorted(headers)

# Write data to CSV
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    
    # Writing the header
    writer.writeheader()
    
    # Writing each record (row) in the CSV file
    for record in all_records:
        # Ensuring all missing keys are added with empty values if not present in the record
        for header in headers:
            if header not in record:
                record[header] = ''
        
        writer.writerow(record)

print(f"CSV file '{csv_file}' created successfully.")
