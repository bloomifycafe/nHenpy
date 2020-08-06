#!/usr/bin/env python3
import discord, random, requests, functools
from discord.ext import commands
from bs4 import BeautifulSoup

client = commands.Bot(command_prefix='.')
LINK = "https://nhentai.net/"
TOKEN = "NzQwODA2MTc5MjE4OTE1NDA5.XyuXhA.P8UNdagobZirSLjgpbbCGvrdNMc"

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

henpy = Henpy()

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    await client.process_commands(message)

@client.command()
async def sex(ctx, code):
    """Parses given code to the handler and returns an embed containing a chosen hentai's data.

    Args:
        code ([int, "random"]): 6-digit code for whatever you desire to beat your meat to, or put "random" in to test your luck.
    """
    try:
        if ctx.author.id not in henpy.id_ban:
            f_data = henpy.get_page(code)
            if f_data == False:
                await ctx.send("Illegal content detected, retrying...")
                f_data = henpy.get_page("random")
            desc = "Tags: "
            for i in f_data[3]:
                desc += "[%s](%s), " % (i, ("https://nhentai.net/tag/" + i.replace(" ", "-")))
            embed = discord.Embed(title=f_data[0], url=f_data[1], description=desc, color=0xf50000)
            embed.set_author(name="nHenpy", icon_url="https://cdn.discordapp.com/avatars/740806179218915409/6b4da565bce7050f089e5d5ae6ab69f8.png?size=128")
            embed.set_footer(text="powered by sex.")
            embed.set_image(url=f_data[2])
            await ctx.send(embed=embed)
        else:
            await ctx.send("CON CHÓ DƯƠNG NHẬT DUY CƯỠNG DÂM TRẺ EM, BẮT CÓC HỌC SINH TIỂU HỌC!")
    except Exception as e:
        print(e)

@client.command()
async def tags(ctx, *args:str):
    """Parses given list of arguments as tags, and then finds a hentai according to those tags.

    WARNING: Are you really sure you want to reveal your fetishes to this entire server?

    Args:
        *args (str): Tags to look for.
    """
    try:
        if ctx.author.id not in henpy.id_ban:
            code_list = []
            for i in args:
                code_list.append(i)
            f_data = henpy.get_page_by_tags(code_list)
            if f_data == False:
                await ctx.send("Illegal content detected, retrying...")
                f_data = henpy.get_page_by_tags(code_list)
            desc = "Tags: "
            for i in f_data[3]:
                desc += "[%s](%s), " % (i, ("https://nhentai.net/tag/" + i.replace(" ", "-")))
            embed = discord.Embed(title=f_data[0], url=f_data[1], description=desc, color=0xf50000)
            embed.set_author(name="nHenpy", icon_url="https://cdn.discordapp.com/avatars/740806179218915409/6b4da565bce7050f089e5d5ae6ab69f8.png?size=128")
            embed.set_footer(text="powered by sex.")
            embed.set_image(url=f_data[2])
            await ctx.send(embed=embed)
        else:
            await ctx.send("CON CHÓ DƯƠNG NHẬT DUY CƯỠNG DÂM TRẺ EM, BẮT CÓC HỌC SINH TIỂU HỌC!")
    except Exception as e:
        print(e)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        if error.param.name == "code":
            await ctx.send("What the fuck are you trying to do?")
    if isinstance(error, commands.BadArgument):
        await ctx.send("Wrong argument!")

if __name__ == "__main__":
    client.run(TOKEN)
