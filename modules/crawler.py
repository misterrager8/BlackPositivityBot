import requests
from bs4 import BeautifulSoup

from modules.models import Article


class Crawler:
    @staticmethod
    def afrotech() -> list:
        base_url = "http://afrotech.com"
        soup = BeautifulSoup(requests.get("http://afrotech.com/news").text, "html.parser")
        return [Article(url=base_url + i.get("href"), title=i.get_text(), source="AfroTech") for i in
                soup.find_all("a", class_="article-link")]

    @staticmethod
    def becauseofthemwecan() -> list:
        base_url = "http://www.becauseofthemwecan.com"
        soup = BeautifulSoup(requests.get(base_url).text, "html.parser")
        return [Article(url=base_url + i.get("href"), title=i.get_text(), source="Because Of Them We Can") for i in
                [j.find("h3").find("a") for j in soup.find_all("div", class_="desc")] if i]

    @staticmethod
    def face2faceafrica() -> list:
        base_url = "http://face2faceafrica.com"
        soup = BeautifulSoup(requests.get(base_url).text, "html.parser")
        return [Article(url=j.find("a").get("href"), title=j.find("a").get_text(), source="Face2Face Africa") for j in
                [i.find("li").find("p") for i in soup.find_all("ul", class_="list-gallery-c")] if j]

    @staticmethod
    def goodblacknews() -> list:
        base_url = "http://goodblacknews.org"
        return [base_url]

    @staticmethod
    def theroot() -> list:
        base_url = "http://www.theroot.com"
        return [base_url]

    @staticmethod
    def thegrio() -> list:
        base_url = "http://thegrio.com"
        soup = BeautifulSoup(requests.get(base_url).text, "html.parser")
        return [Article(url=j.find("a").get("href"), title=j.find("a").get_text(), source="The Grio") for j in
                [i.find("h2") for i in soup.find_all("div", class_="tpd-card-title")]]
