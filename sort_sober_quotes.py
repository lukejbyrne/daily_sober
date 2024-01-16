import csv, re
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
    translation_table = str.maketrans({'―': '-', '~': '-', '–': '-', '(': '-', '“': '"', '”': '"', '’': '\'', '‘': '\''})
    quote_element_text = quote_element_text.translate(translation_table)


    # Create regex to split by either '"-' or just ' -'
    pattern = (r'"\s*-\s*|\s+-\s*')

    # Split text by the regex
    matches = re.split(pattern, quote_element_text)

    # Set quote text as first half of the match
    quote_text = matches[0]

    # Set author text as either the second half or Anonymous
    if len(matches) > 1:
        author_text = matches[1]
    else:
        author_text = "Anonymous"
    
    # Add quote to list
    rows.append([quote_text, author_text])

# Write to CSV file
with open(csv_output_path, 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Quote', 'Author', 'Comments'])  # Write header
    csv_writer.writerows(rows)
    