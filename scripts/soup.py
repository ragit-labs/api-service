from bs4 import BeautifulSoup


def _remove_all_attrs(soup):
    for tags in soup.find_all():
        for key in list(tags.attrs):
            del tags.attrs[key]
    return soup


with open("scripts/medium.html", "r") as f:
    data = f.read()
    soup = BeautifulSoup(data)
    body = soup.find("body")
    ret = _remove_all_attrs(body)
    with open("scripts/soupout", "w") as f1:
        f1.write(str(ret))
