import os
import re, bs4, requests, pymongo


m_pattern = r"\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?"
money_pattern = re.compile(m_pattern)
payment_pattern = re.compile(rf"to Pay {m_pattern} to Settle")
case_number_pattern = re.compile(r"\b\d+:\d+-cv-\d+\b")
# date_pattern = re.compile(rb"\b\d{2}-\d{2}-\d{4}\b")


space = " "
double_space = space * 2


def remove_double_spaces(text: str):
    cleaned_text = text.replace(double_space, space)
    if double_space in cleaned_text:
        return remove_double_spaces(cleaned_text)
    else:
        return cleaned_text.strip()


case_numbers = []
companies = []
complaints = []
amounts = []
links = []
dates = []

host = "https://www.eeoc.gov"

db = pymongo.MongoClient(os.environ.get("mongodb"))["eeoc"]["cases"]

article = 0
page = 0
try:
    for index in range(290):
        url = f"{host}/newsroom/search?page={index}"

        content = requests.get(
            url,
            timeout=None,
        ).content
        soup = bs4.BeautifulSoup(content, features="html.parser")

        a_tags = soup.find_all("a", attrs=dict(rel="bookmark"))

        a_tag: bs4.BeautifulSoup
        for a_tag in a_tags:
            _link = a_tag["href"]
            title_span = a_tag.find("span")
            if title_span:
                amount = ""
                title = remove_double_spaces(title_span.text)
                if match := payment_pattern.search(title):
                    payment_text = match.group()
                    amount = money_pattern.search(payment_text).group()
                    company, complaint = title.split(payment_text)
                    company, complaint = remove_double_spaces(
                        company
                    ), remove_double_spaces(complaint)

                    link = host + _link
                    content = requests.get(
                        link,
                        timeout=None,
                    ).content

                    sub_soup = bs4.BeautifulSoup(content, features="html.parser")
                    article_tag = sub_soup.find("article")

                    date_span = article_tag.find("span")
                    date = date_span.text

                    p_span = article_tag.find("span")

                    # open("content.html", "wb").write(content)

                    if case_number_match := case_number_pattern.search(p_span.text):
                        case_number = case_number_match.group()
                        # date = date_pattern.search(content).group()

                        db.insert_one(
                            case_numbers=f"Case No. {case_number}",
                            company=company,
                            amounts=amount,
                            complaints=complaint,
                            links=link,
                            dates=date,
                        )

                        article += 1

                        print(
                            f"Page : {page}   <>   Number articles found : {article}   <>    Latest : {title}"
                        )
            break

        page + 1

except KeyboardInterrupt as e:
    ...
except KeyboardInterrupt as e:
    ...
