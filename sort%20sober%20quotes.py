import csv
from bs4 import BeautifulSoup

html_file_path = "Draft 2 - Quote organisation 65e3f45f4c3d432bbc2c633b96098b9b.html"
csv_output_path = "output.csv"

# Read content from the HTML file
with open(html_file_path, 'r', encoding='utf-8') as html_file:
    html_content = html_file.read()

# Parse HTML using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find all bulleted list items containing quotes and authors
quote_elements = soup.find_all('ul', class_='bulleted-list')

# Initialize a list to store rows
rows = []

# Extract quotes and authors
for quote_element in quote_elements:
    quote_element_text = quote_element.li.get_text(strip=True)
    quote_element_text = quote_element_text.replace('~','-')
    quote_element_text = quote_element_text.replace('–','-')
    quote_element_text = quote_element_text.replace('(','-')
    quote_element_text = quote_element_text.replace('”','\"')

    author_text = quote_element_text.split(' - ')
    
    # Check if there is an author part after the dash
    if len(author_text) > 1:
        author_text = author_text[1]
        quote_text = quote_element_text[1:-4-len(author_text)]  # Remove leading and trailing quotes, and author len

    else:
        author_text = "Anonx"  # Set to an empty string if there is no author
        quote_text = quote_element_text[1:-1]  # Remove leading and trailing quotes

    rows.append([quote_text, author_text])

# Write to CSV file
with open(csv_output_path, 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Quote', 'Author'])  # Write header
    csv_writer.writerows(rows)
