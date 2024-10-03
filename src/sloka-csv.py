import json
import csv
import requests
from bs4 import BeautifulSoup

def clean_html(raw_html):
    if raw_html is None or not isinstance(raw_html, str):
        return ''
    try:
        soup = BeautifulSoup(raw_html, 'html.parser')
        return soup.get_text(strip=True)
    except Exception as e:
        print(f"Error cleaning HTML: {e}")
        return str(raw_html)

def extract_data(json_data):
    data_rows = []
    text_only_rows = []
    canto_list = json_data.get('cantoList', {})
    for canto_key, canto_value in canto_list.items():
        canto_number = canto_key
        for item in canto_value:
            tr_rows = item.get('trRows', [])
            for row_index, row in enumerate(tr_rows):
                td_columns = row.get('tdColumns', [])
                for col_index, col in enumerate(td_columns):
                    row_type = col.get('row', '')
                    class_name = col.get('className', '')
                    data = clean_html(col.get('data', ''))
                    tooltip_image = col.get('tooltipImage', '')
                    tooltip_text = clean_html(col.get('tooltipText', ''))
                    
                    data_rows.append([
                        canto_number,
                        row_index,
                        col_index,
                        row_type,
                        class_name,
                        data,
                        tooltip_image,
                        tooltip_text
                    ])
                    
                    if data:
                        text_only_rows.append([data])
    
    return data_rows, text_only_rows

def main():
    base_url = "http://scl.samsaadhanii.in/scl/e-readers/shishu/assets/json/SV-{}.json"
    page_number = 1
    all_data_rows = []
    all_text_only_rows = []
    
    while True:
        url = base_url.format(page_number)
        try:
            response = requests.get(url)
            response.raise_for_status()
            json_data = response.json()
            
            data_rows, text_only_rows = extract_data(json_data)
            all_data_rows.extend(data_rows)
            all_text_only_rows.extend(text_only_rows)
            
            print(f"Processed SV-{page_number}")
            page_number += 1
            
        except requests.RequestException as e:
            print(f"Reached end of available pages at SV-{page_number-1}")
            break
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON for SV-{page_number}: {e}")
            break
        except Exception as e:
            print(f"Unexpected error processing SV-{page_number}: {e}")
            break

    # Write full data CSV
    output_file = "extracted_structured_data.csv"
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                "Canto Number", "Row Number", "Column Number", 
                "Row Type", "Class Name", "Data", 
                "Tooltip Image", "Tooltip Text"
            ])  # Header
            writer.writerows(all_data_rows)
        print(f"Full data successfully extracted and saved to {output_file}")
    except IOError as e:
        print(f"Error writing to full data CSV file: {e}")

    # Write text-only CSV
    text_only_file = "text_only_data.csv"
    try:
        with open(text_only_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Text"])  # Header
            writer.writerows(all_text_only_rows)
        print(f"Text-only data successfully extracted and saved to {text_only_file}")
    except IOError as e:
        print(f"Error writing to text-only CSV file: {e}")

if __name__ == "__main__":
    main()