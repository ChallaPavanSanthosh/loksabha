import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to fetch and parse a URL
def fetch_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Ensure we notice bad responses
        return BeautifulSoup(response.content, 'html.parser')
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return None

# Base URL of the main page
base_url = 'https://results.eci.gov.in/PcResultGenJune2024/'

# URL of the main page
main_url = base_url + 'index.htm'

# Fetch the main page content
soup = fetch_url(main_url)
if soup is None:
    print("Failed to fetch the main page.")
    exit()

# Extract party names, won, leading, and total counts
parties_data = []
try:
    table = soup.find('table')  # Find the appropriate table
    for row in table.find_all('tr')[1:]:  # Skip header row
        cells = row.find_all('td')
        if len(cells) >= 4:  # Ensure there are enough cells to avoid IndexError
            party_name = cells[0].text.strip()
            won = cells[1].text.strip()
            leading = cells[2].text.strip()
            total = cells[3].text.strip()
            won_link = cells[1].find('a')['href']
            full_won_link = base_url + won_link  # Concatenate base URL with the relative URL
            parties_data.append([party_name, won, leading, total, full_won_link])
except Exception as e:
    print(f"Error extracting party data: {e}")

# Create a DataFrame for the main page data
parties_df = pd.DataFrame(parties_data, columns=['Party', 'Won', 'Leading', 'Total', 'Link'])
print("Parties data extracted successfully.")

# Initialize the final DataFrame for the detailed data
detailed_data = []

# Iterate through each party's won link
for index, row in parties_df.iterrows():
    party_url = row['Link']
    print(f"Fetching details for party: {row['Party']} from {party_url}")
    party_soup = fetch_url(party_url)
    if party_soup is None:
        continue

    # Extract details for each parliament constituency
    try:
        detail_table = party_soup.find('table')  # Find the appropriate table
        for detail_row in detail_table.find_all('tr')[1:]:  # Skip header row
            detail_cells = detail_row.find_all('td')
            if len(detail_cells) >= 5:  # Ensure there are enough cells to avoid IndexError
                s_no = detail_cells[0].text.strip()
                constituency = detail_cells[1].text.strip()
                winning_candidate = detail_cells[2].text.strip()
                total_votes = detail_cells[3].text.strip()
                margin = detail_cells[4].text.strip()

                # Fetch constituency page to extract state
                try:
                    constituency_link = detail_cells[1].find('a')['href']
                    full_constituency_link = base_url + constituency_link  # Concatenate base URL with the relative URL
                    constituency_soup = fetch_url(full_constituency_link)
                    if constituency_soup is None:
                        continue
                    state_text = constituency_soup.get_text()  # Get all text from the page
                    state = state_text.split('(')[1].split(')')[0] if '(' in state_text and ')' in state_text else "Unknown"

                    party = row['Party']
                    detailed_data.append([s_no, state, constituency, winning_candidate, total_votes, margin, party])
                    print(f"Added data for constituency: {constituency}")

                except Exception as e:
                    print(f"Error extracting state for constituency {constituency}: {e}")

    except Exception as e:
        print(f"Error extracting details for party {row['Party']}: {e}")

# Create a DataFrame for the detailed data
detailed_df = pd.DataFrame(detailed_data, columns=['S.No', 'State', 'Parliament Constituency', 'Winning Candidate', 'Total Votes', 'Margin', 'Party'])

# Save the DataFrames to Excel files
parties_df.to_excel('parties_data.xlsx', index=False)
detailed_df.to_excel('detailed_data.xlsx', index=False)

print("Data extraction complete. Files saved to 'parties_data.xlsx' and 'detailed_data.xlsx'.")
