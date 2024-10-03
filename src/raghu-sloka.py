import json
import csv
import requests

# URL of the JSON file
url = "https://sanskrit.uohyd.ac.in/raghu-gold/assets/data/sloka.json"

# Fetch the JSON data from the URL
response = requests.get(url)
data = response.json()

# Open a CSV file to write the output
with open('/home/dell/Desktop/web-txt/output/raghu_verses.csv', 'w', newline='', encoding='utf-8') as csvfile:
    # Define the CSV writer
    writer = csv.writer(csvfile)
    
    # Write the header
    writer.writerow(['chaptno', 'slokano', 'spart1', 'spart2'])
    
    # Loop through each entry in the JSON data
    for entry in data:
        chaptno = entry.get('chaptno')
        slokano = entry.get('slokano')
        spart1 = entry.get('spart1')
        spart2 = entry.get('spart2')
        
        # Write to CSV if both spart1 and spart2 exist
        if spart1 and spart2:
            writer.writerow([chaptno, slokano, spart1, spart2])

print("CSV file 'parallel_verses.csv' has been created successfully.")
