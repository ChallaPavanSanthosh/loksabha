
import pandas as pd

# List of parties in the NDA alliance
nda_parties = [
    'Bharatiya Janata Party - BJP', 'Telugu Desam - TDP', 'Janata Dal (United) - JD(U)','Shiv Sena - SHS', 'Shiv Sena (Uddhav Balasaheb Thackrey) - SHSUBT','Lok Janshakti Party (Ram Vilas) - LJPRV','Nationalist Congress Party – Sharadchandra Pawar - NCPSP', 'Janata Dal  (Secular) - JD(S)', 'Apna Dal (Soneylal) - ADAL',  'Asom Gana Parishad - AGP', 'Janasena Party - JnP', 'Rashtriya Lok Dal - RLD', 'AJSU Party - AJSUP', 'Hindustani Awam Morcha (Secular) - HAMS', 'Sikkim Krantikari Morcha - SKM', 'United People’s Party, Liberal - UPPL', 'Independent - IND','Viduthalai Chiruthaigal Katchi - VCK','Jammu & Kashmir National Conference - JKN'
]

# Read the dataset
file_path = 'detailed_data.xlsx'
df = pd.read_excel(file_path)

# Add the "Alliance" column
df['Alliance'] = df['Party'].apply(lambda x: 'NDA' if x in nda_parties else 'INC')

# Save the result back to the same Excel file
df.to_excel(file_path, index=False)

# Count the number of NDA and INC
nda_count = df['Alliance'].value_counts().get('NDA', 0)
inc_count = df['Alliance'].value_counts().get('INC', 0)

print(f'Total NDA count: {nda_count}')
print(f'Total INC count: {inc_count}')