import json
import csv
import requests
from collections import defaultdict

# Fetch the JSON data from the provided URL
url = "https://sanskrit.uohyd.ac.in/raghu-gold/assets/data/analysis.json"
response = requests.get(url)
data = response.json()

# Dictionary to hold sentences with the same chpatno, slokano, and sentno
grouped_sentences = defaultdict(lambda: {'words': [], 'sandhied_words': [], 'hindi_meanings': [], 'english_meanings': []})

# Group the data by chpatno, slokano, and sentno
for entry in data:
    chpatno = entry.get('chpatno', '')
    slokano = entry.get('slokano', '')
    sentno = entry.get('sentno', '')
    
    # Use a tuple of (chpatno, slokano, sentno) as the key
    key = (chpatno, slokano, sentno)
    
    # Add values to the respective lists
    grouped_sentences[key]['words'].append(entry.get('Word', ''))
    grouped_sentences[key]['sandhied_words'].append(entry.get('sandhied_word', ''))
    grouped_sentences[key]['hindi_meanings'].append(entry.get('hindi_meaning', ''))
    grouped_sentences[key]['english_meanings'].append(entry.get('english_meaning', ''))

# Open CSV file for writing
with open("/home/dell/Desktop/web-txt/output/raghu-par_sent_grouped.csv", mode="w", newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    
    # Write the header row
    csv_writer.writerow(['chpatno', 'slokano', 'sentno', 'Words', 'Sandhied Words', 'Hindi Meanings', 'English Meanings'])
    
    # Iterate through the grouped data and write to CSV
    for (chpatno, slokano, sentno), values in grouped_sentences.items():
        words = ' '.join(values['words']).strip()
        sandhied_words = ' '.join(values['sandhied_words']).strip()
        hindi_meanings = ' '.join(values['hindi_meanings']).strip()
        english_meanings = ' '.join(values['english_meanings']).strip()
        
        # Write the row with concatenated values
        csv_writer.writerow([chpatno, slokano, sentno, words, sandhied_words, hindi_meanings, english_meanings])

print("CSV file 'parallel_sentences_grouped.csv' created successfully.")
