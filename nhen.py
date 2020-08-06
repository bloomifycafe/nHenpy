import random, requests
from bs4 import BeautifulSoup
LINK = "https://nhentai.net/"

class Henpy():
    """Main class for Henpy requests and data handling.
    """
    def __init__(self):
        self.ban_list = ["lolicon", "shotacon", "loli", "shotacon", "netorare", "ntr", "NTR"]
        self.id_ban = [504458025063677964]
        self.data = ""

    def get_request(self, url:str):
        """Retrieves a page's data through a GET request.

        Args:
            url (str): URL to get data from.
        """
        self.req = requests.get(url)
        self.data = BeautifulSoup(self.req.text, features="html.parser")

    def get_page(self, code):
        """Sends a GET request to the designated link containing the parsed code and retrieves some data.

        Args:
            code (int): 6-digit code for whatever you desire to jack off to. Put "random" in if you're feeling adventurous.
        """
        if code != "random":
            self.get_request(LINK + "g/" + str(code))
        else:
            self.get_request(LINK + "random")
        self.title = self.data.find("meta", itemprop="name")["content"]
        self.thumbnail = self.data.find("meta", itemprop="image")["content"]
        self.tags = self.data.find("meta", {"name":"twitter:description"})["content"].split(",")
        self.esc_tags = []
        self.url = self.req.url
        for i in self.tags:
            self.esc_tags.append(i.strip())
        if any(i in self.esc_tags for i in self.ban_list):
            return False
        else:
            return self.title, self.url, self.thumbnail, self.esc_tags

    def get_page_by_tags(self, tags:list):
        """Returns a random page's data matching a list of tags.

        Args:
            tags (list): List of desired tags.
        """
        self.search_link = LINK + "search/?q="
        for i in tags:
            self.search_link += i + "+"
        self.get_request(self.search_link)
        try:
            self.last = int(self.data.find("a", {"class":"last"})["href"].split("=")[-1])
        except:
            self.last = 1
        if self.last != 1:
            self.get_request(self.search_link + "&page=" + str(random.randrange(1, self.last)))
        else:
            self.get_request(self.search_link)
        self.found_codes = self.data.find_all("a", {"class":"cover"})
        self.esc_list = []
        for i in self.found_codes:
            self.esc_list.append(i["href"].replace("/","").strip("g"))
        self.values = self.get_page(random.choice(self.esc_list))
        return self.values

if __name__ == "__main__":
    henpy = Henpy()