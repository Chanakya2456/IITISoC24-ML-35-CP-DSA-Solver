import requests
from bs4 import BeautifulSoup as bs

def recommend_cf(problem_rating,tags):
    problems = set()
    for tag in tags:
        if(problem_rating <= 900):
            url = f"https://codeforces.com/problemset?tags={tag},{problem_rating}-{problem_rating+100}"
        else:
            url = f"https://codeforces.com/problemset?tags={tag},{problem_rating-200}-{problem_rating+200}"
        r = requests.get(url)
        soup = bs(r.content, 'html.parser')
        elems = soup.find_all('div',style="float: left;")
        i = 0
        for elem in elems:
            anchor_tag = elem.find('a')
            href_value = anchor_tag.get('href')
            problems.append(f"https://codeforces.com{href_value}")
            i += 1
            if i == 4:
                break

    return problems