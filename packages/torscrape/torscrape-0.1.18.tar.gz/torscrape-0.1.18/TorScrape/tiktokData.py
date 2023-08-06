import aiohttp
import asyncio
import json
from bs4 import BeautifulSoup

url = "https://www.tiktok.com/@"
suffix = "/video/"

async def latest_links(username, count):
    async with aiohttp.ClientSession() as session:
        async with session.get(url + username) as response:
            html = await response.text()

            soup = BeautifulSoup(html, "html.parser")

            scripts = soup.find_all("script", attrs={"type": "application/json"})

            for script in scripts:
                if "user-post" not in str(script):
                    continue

                profile_data = json.loads(script.string)
                item_list = profile_data.get("ItemList")

                user_post = item_list.get("user-post")
                post_urls = user_post.get("list")

                for id in post_urls[:count]:
                    complete_url = url + username + suffix + id
                    print(complete_url)


def followers(username):
    pass

def likes(username):
    pass

def following(username):
    pass

def profileUrl(username):
    pass


async def get_latest_vid_links(username, count = None):
    if count == None:
        count == 1
    else:
        count = count
    
    await latest_links(username, count)