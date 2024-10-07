import json
import csv
import requests

# URL of the JSON file
url = "https://scl.samsaadhanii.in/scl/e-readers/SR_NEW/assets/data/analysis.json"

# Function to fetch JSON data from URL
def fetch_json_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve data. HTTP Status code: {response.status_code}")
        return None

# Function to write JSON data to CSV
def json_to_csv(json_data, csv_filename):
    # Open the CSV file for writing
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
        # Create a CSV writer object
        csv_writer = csv.writer(file)

        # Get the keys from the first dictionary object in the JSON data
        headers = list(json_data[0].keys())
        csv_writer.writerow(headers)  # Write the header row

        # Iterate over the JSON data and write each row to the CSV file
        for entry in json_data:
            row = [entry.get(header, "") for header in headers]
            csv_writer.writerow(row)

# Main function
def main():
    # Fetch JSON data from the URL
    json_data = fetch_json_data(url)

    if json_data:
        # Specify the CSV file name
        csv_filename = '/home/dell/Desktop/web-txt/output/json-rows.csv'
        
        # Convert JSON to CSV
        json_to_csv(json_data, csv_filename)
        print(f"Data successfully written to {csv_filename}")

if __name__ == "__main__":
    main()
