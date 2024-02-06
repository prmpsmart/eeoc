import pandas as pd

n = pd.read_csv("eeoc_cases-2024-02-06.csv")
m = pd.read_csv("cc.csv", sep=',')


d = pd.DataFrame(
    columns=[
        "Case Number",
        "Company",
        "Complaint",
        "Settlement Amount",
        "Date",
        "Link",
    ]
)

d['Case Number'] = n['Case Number']
d['Company'] = m['Company']
d['Complaint'] = m['Complaint']
d['Settlement Amount'] = n['Settlement Amount']
d['Date'] = n['Date']
d['Link'] = n['Link']


d.to_excel('eeoc_court_data.xlsx')