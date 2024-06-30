# Lok Sabha Election Results Scraper

## Project Description

This project aims to scrape the general parliamentary election results from the Election Commission of India's website. The main page contains a table with party names, number of seats won, leading, and total seats. Each party's "won" column contains hyperlinks to detailed pages, listing all constituencies where the party won. Each constituency hyperlink further contains detailed information about the state. The goal is to compile all this information into two Excel sheets: one for the main party results and another for detailed constituency results.

## Technologies Used

- Python
- Requests Library
- BeautifulSoup Library
- Pandas Library

## Project Files

- `main_scrap.py`: The main script to scrape data and save it to Excel files.
- `parties_data.xlsx`: Excel file containing party-wise results.
- `detailed_data.xlsx`: Excel file containing detailed constituency results.

## Detailed Code Explanation

### Step-by-Step Code Breakdown

```python
import requests
from bs4 import BeautifulSoup
import pandas as pd
```
- Import necessary libraries: `requests` for making HTTP requests, `BeautifulSoup` for parsing HTML, and `pandas` for handling data.

```python
def fetch_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Ensure we notice bad responses
        return BeautifulSoup(response.content, 'html.parser')
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return None
```
- Define a function to fetch and parse a URL. Handle any HTTP request errors and return `None` if there's an error.

```python
base_url = 'https://results.eci.gov.in/PcResultGenJune2024/'
main_url = base_url + 'index.htm'
```
- Set the base URL and the URL of the main page.

```python
soup = fetch_url(main_url)
if soup is None:
    print("Failed to fetch the main page.")
    exit()
```
- Fetch the main page content. If fetching fails, print an error message and exit.

#### Extracting Party Data

```python
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
```
- Extract party names, seats won, leading, total seats, and the "won" link for each party. Store this data in a list.

```python
parties_df = pd.DataFrame(parties_data, columns=['Party', 'Won', 'Leading', 'Total', 'Link'])
print("Parties data extracted successfully.")
```
- Create a DataFrame for the main page data and print a success message.

#### Extracting Detailed Constituency Data

```python
detailed_data = []
```
- Initialize a list to store detailed constituency data.

```python
for index, row in parties_df.iterrows():
    party_url = row['Link']
    print(f"Fetching details for party: {row['Party']} from {party_url}")
    party_soup = fetch_url(party_url)
    if party_soup is None:
        continue
```
- Iterate through each party's "won" link. Fetch the page content for each link.

```python
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
```
- Extract details for each parliament constituency. For each constituency, fetch the page content to extract the state information.

```python
detailed_df = pd.DataFrame(detailed_data, columns=['S.No', 'State', 'Parliament Constituency', 'Winning Candidate', 'Total Votes', 'Margin', 'Party'])
```
- Create a DataFrame for the detailed constituency data.

#### Saving Data to Excel Files

```python
parties_df.to_excel('parties_data.xlsx', index=False)
detailed_df.to_excel('detailed_data.xlsx', index=False)

print("Data extraction complete. Files saved to 'parties_data.xlsx' and 'detailed_data.xlsx'.")
```
- Save the DataFrames to Excel files.

## Problems Faced and Solutions

### Problem 1: Handling Relative URLs
- **Issue**: Relative URLs in the "won" column.
- **Solution**: Concatenate the base URL with the relative URL.

### Problem 2: Extracting State Information
- **Issue**: Extracting the state name from the constituency page.
- **Solution**: Convert the entire page text to a string and split based on `(` and `)` to extract the state name.

### Problem 3: Handling Missing or Incorrect Data
- **Issue**: Potential missing or incorrect data causing `IndexError`.
- **Solution**: Use `try` and `except` blocks to catch exceptions and print error messages for debugging.

## Data Structure

### parties_data.xlsx
| Party | Won | Leading | Total | Link |
|-------|-----|---------|-------|------|
| Bharatiya Janata Party - BJP | 240 | 0 | 240 | https://results.eci.gov.in/PcResultGenJune2024/partywisewinresultState-369.htm |
| Indian National Congress - INC | 99 | 0 | 99 | https://results.eci.gov.in/PcResultGenJune2024/partywisewinresultState-370.htm |
| ... | ... | ... | ... | ... |

### detailed_data.xlsx
| S.No | State | Parliament Constituency | Winning Candidate | Total Votes | Margin | Party |
|------|-------|-------------------------|-------------------|-------------|--------|-------|
| 1 | Andhra Pradesh | Anakapalle(5) | C.M.RAMESH | 762069 | 296530 | Bharatiya Janata Party - BJP |
| 2 | Andhra Pradesh | Rajahmundry(8) | DAGGUBATI PURANDHESHWARI | 726515 | 239139 | Bharatiya Janata Party - BJP |
| ... | ... | ... | ... | ... | ... | ... |

## How to Run the Project

1. **Install dependencies**:
    ```sh
    pip install requests beautifulsoup4 pandas
    ```

2. **Run the script**:
    ```sh
    python main_scrap.py
    ```

3. **Check the output files**:
    - `parties_data.xlsx`
    - `detailed_data.xlsx`

## Conclusion

This project demonstrates web scraping techniques to extract structured data from a government website and save it in a user-friendly format (Excel). The project involved handling various challenges, such as relative URLs and extracting information from unstructured text, showcasing practical problem-solving skills.

# Lok Sabha Parliamentary Constituency Results Analysis

## Introduction

This project analyzes the results of the Lok Sabha parliamentary constituency elections. The analysis is performed using various data visualization techniques implemented in a Jupyter notebook. Additionally, a Power BI dashboard is created to provide an interactive analysis of the election results.

## Dataset Details

The dataset contains the results of 543 parliamentary constituencies. Each entry includes details such as the state, constituency, winning candidate, total votes, margin, party, and alliance.

- *Columns*:
  - S.No: Serial number of the entry
  - State: State in which the constituency is located
  - Parliament Constituency: Name of the parliamentary constituency
  - Winning Candidate: Name of the winning candidate
  - Total Votes: Total votes received by the winning candidate
  - Margin: Margin of victory
  - Party: Political party of the winning candidate
  - Alliance: Political alliance of the winning candidate's party

## Steps in the Analysis

1. **Importing Libraries**:
    - Importing necessary libraries such as pandas, matplotlib, seaborn, etc.

2. **Loading Data**:
    - Loading the election results data into pandas DataFrames for processing and analysis.

3. **Data Cleaning and Preparation**:
    - Handling missing values and performing necessary data transformations.

4. **Exploratory Data Analysis (EDA)**:
    - Visualizing the distribution of seats won by different parties.
    - Analyzing vote share percentages.
    - State-wise analysis of election results.
    - Mapping the geographical distribution of election results.

5. **Results Visualization**:
    - Bar charts, pie charts, and maps to illustrate the findings.
    - Interactive visualizations to explore the data in detail.

## Power BI Dashboard

The Power BI dashboard provides an interactive analysis of the 2024 Lok Sabha election results. It includes various visualizations that depict the election results, such as the number of constituencies won by each party, vote share percentages, and state-wise seat distribution. The dashboard offers filters to view data based on different states and political alliances.

### Key Visualizations

1. **Total Number of Constituencies Won by Party**:
   - A bar chart showing the number of constituencies won by each party.
   - The Bharatiya Janata Party (BJP) leads with 240 constituencies, followed by the Indian National Congress (INC) with 99 constituencies.

2. **Vote-wise Share for Each Party**:
   - A pie chart representing the vote share percentage of each party.
   - The BJP has the highest vote share at 44.2%, followed by the INC at 18.23%.

3. **State-wise Seats**:
   - A pie chart displaying the distribution of seats won by different parties across various states.

4. **Alliance View**:
   - A donut chart showing the overall seat distribution between major alliances (INC and NDA).
   - The NDA has a majority with 303 seats (55.8%), while the INC has 240 seats (44.2%).

5. **Geographical Distribution**:
   - A map visualization highlighting the geographical spread of constituencies won by different parties across India.


## Conclusion

This project provides insights into the 2024 Lok Sabha election results through data visualization. The visualizations help in understanding the electoral performance of different parties across various states and constituencies.
