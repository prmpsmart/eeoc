import time
import re

import bs4
import pandas
import requests

m_pattern = r"\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?"
money_pattern = re.compile(m_pattern)
payment_pattern = re.compile(rf"{m_pattern}")
# money_pattern = re.compile(r'\$\s*(?:\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?|\d+ million)')
# money_pattern = re.compile(r'\$\s*(?:\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?|\d+\s*million|\d+)')
money_pattern = re.compile(
    r"\$\s*(?:\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?|\d+\s*million|\d+(\.\d{1,3})?\s*Million)"
)

case_number_pattern = re.compile(r"\b\d+:\d+-cv-\d+\b")
date_pattern = re.compile(r"\b\d{2}-\d{2}-\d{4}\b")


space = " "
double_space = space * 2


def remove_double_spaces(text: str):
    cleaned_text = text.replace(double_space, space)
    if double_space in cleaned_text:
        return remove_double_spaces(cleaned_text)
    else:
        return cleaned_text.strip()


case_numbers = []
titles = []
amounts = []
links = []
dates = []

host = "https://www.eeoc.gov"

article = 0
page = 148

try:
    for index in range(page, 290):
        url = f"{host}/newsroom/search?page={index}"

        content = requests.get(url, timeout=10).content
        soup = bs4.BeautifulSoup(content, features="html.parser")

        a_tags = soup.find_all("a", attrs=dict(rel="bookmark"))

        a_tag: bs4.BeautifulSoup
        for a_tag in a_tags:
            _link = a_tag["href"]
            title_span = a_tag.find("span")

            if title_span:
                amount = ""
                title = remove_double_spaces(title_span.text)
                if amount := money_pattern.search(title):
                    amount = amount.group()

                    print(title)

                    if " Pay " in title and " to " in title:
                        link = host + _link
                        content = requests.get(link, timeout=10).content

                        sub_soup = bs4.BeautifulSoup(content, features="html.parser")
                        article_tag = sub_soup.find("article")

                        date = article_tag.find("div").text
                        date = date_pattern.search(date).group()

                        for p in article_tag.find_all("p"):
                            if case_number_match := case_number_pattern.search(p.text):
                                case_number = case_number_match.group()

                                titles.append(title)
                                case_numbers.append(f"Case No. {case_number}")
                                amounts.append(amount)
                                links.append(link)
                                dates.append(date)

                                article += 1

                                print(
                                    f"Page : {page}   <>   Number articles found : {article}   <>    Latest : {title}"
                                )
                                break

        page += 1

except KeyboardInterrupt:
    ...
except Exception:
    ...

data = {
    "Case Number": case_numbers,
    "Title": titles,
    "Settlement Amount": amounts,
    "Date": dates,
    "Link": links,
}

df = pandas.DataFrame(data, columns=data.keys())


name = f"eeoc_cases-{int(time.time)}"
df.to_csv(f"{name}.csv", index=False)
df.to_excel(f"{name}.xlsx", index=False)
