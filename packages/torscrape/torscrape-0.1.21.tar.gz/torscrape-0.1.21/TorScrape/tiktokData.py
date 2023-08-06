import asyncio
import json
import re
import time
from typing import Dict, List, Callable, Union
from pathlib import Path

import aiohttp
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement

BASE_URL = "https://www.tiktok.com/@"
URL_SUFFIX = "/video/"

CONTENT_LIST = "tiktok-x6y88p-DivItemContainerV2"
ERROR_BANNER = "css-14feuhu-notice"
LOADING_WHEEL = "tiktok-qmnyxf-SvgContainer"


class DoesNotExistException(Exception):
    """Raised when the username does not exist"""

    pass


def data_file_check(func: Callable):
    def wrapper(*args):
        data_file = Path("./data.json")
        if not data_file.exists():
            with open("./data.json", "w") as write:
                json.dump({}, write, indent=4)

        return func(*args)

    return wrapper


@data_file_check
def check_profile(username: str) -> Union[Dict, None]:
    """Checks if the profile data is stale"""

    with open("./data.json", "r") as read:
        data: Dict = json.load(read)
        return data.get(username)


@data_file_check
async def get_profile_data(username: str) -> Dict:
    """Returns a dictionary of the user's profile data"""

    async with aiohttp.ClientSession() as session:
        async with session.get(BASE_URL + username) as response:
            # If the username is valid, the response will be 200-299 otherwise 404
            if response.status in range(200, 299):
                soup = BeautifulSoup(await response.text(), "html.parser")
                avatar_tag = soup.find(
                    "img", attrs={"class": "tiktok-1zpj2q-ImgAvatar"}
                )
                bio_tag = soup.find("h2", attrs={"class": "tiktok-vdfu13-H2ShareDesc"})
                following_tag = soup.find("strong", attrs={"title": "Following"})
                followers_tag = soup.find("strong", attrs={"title": "Followers"})
                likes_tag = soup.find("strong", attrs={"title": "Likes"})

                avatar_url = avatar_tag.attrs.get("src")
                expiry_epoch = "".join(
                    [
                        char
                        for char in avatar_url[
                            avatar_url.find("expires=") + 8 : avatar_url.find("&x")
                        ]
                    ]
                )

                with open("./data.json", "r") as read:
                    data: Dict = json.load(read)

                if not data.get(username):
                    data[username] = {
                        "avatar": avatar_url,
                        "bio": bio_tag.text,
                        "following": following_tag.text,
                        "followers": followers_tag.text,
                        "likes": likes_tag.text,
                        "video_count": None,
                        "videos": None,
                        "expiry_epoch": expiry_epoch,
                        "last_checked": None,  # Implement a way to check if the data is stale in the future
                        # TODO: Create a k/v pair to decide when cache has to be refreshed for all videos
                    }

                with open("./data.json", "w") as write:
                    json.dump(data, write, indent=4)

                return data[username]

            raise DoesNotExistException


@data_file_check
async def get_all_videos(username: str) -> str:
    """Renders all videos on a user's page and returns the video URLs"""

    await get_profile_data(username)

    user_regex = re.compile(BASE_URL + username + URL_SUFFIX)

    options = webdriver.EdgeOptions()

    # Disable the automation info banner
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Edge(options=options)

    # Can't run headless so keep the window small
    driver.set_window_size(32, 32)

    driver.get(BASE_URL + username)

    # Tracking
    iterations = 0

    def jitter_scroll(page: WebElement):
        """Scrolls up and down to force the page to load more content"""

        for _ in range(5):
            page.send_keys(Keys.ARROW_UP)

        for _ in range(7):
            page.send_keys(Keys.ARROW_DOWN)

        return

    while True:
        posted_videos_list = driver.find_elements(By.CLASS_NAME, CONTENT_LIST)
        base_page = driver.find_element(By.CSS_SELECTOR, "html")

        # This list always exist but possibly hasn't rendered yet
        if not posted_videos_list:
            continue

        last_video = posted_videos_list[-1]

        last_video.location_once_scrolled_into_view

        # Give the page time to load the first time
        time.sleep(3 if iterations == 0 else 1)

        # It's either use a try/except or take longer finding the element without raising an except.
        # Looks ugly but faster than the alternative
        try:
            error_banner = driver.find_element(By.CLASS_NAME, ERROR_BANNER)
            if error_banner:
                jitter_scroll(base_page)

        except NoSuchElementException:
            error_banner = None

        try:
            is_loading = driver.find_element(By.CLASS_NAME, LOADING_WHEEL)
            if is_loading:
                jitter_scroll(base_page)

        except NoSuchElementException:
            is_loading = None

        # Really wanted to avoid repeating this but it's the only way to get the new content list
        refreshed_content_list = driver.find_elements(By.CLASS_NAME, CONTENT_LIST)

        if iterations < 3:
            jitter_scroll(base_page)
            iterations += 1
            continue

        if all(
            [
                refreshed_content_list[-1] == last_video,
                not error_banner,
                not is_loading,
            ]
        ):
            unsorted_videos = [
                (match.start(), match.end())
                for match in re.finditer(user_regex, driver.page_source)
            ]

            videos = set(
                [
                    driver.page_source[start : finish + 19]
                    for start, finish in unsorted_videos
                ]
            )

            with open("./data.json", "r") as read:
                data: Dict = json.load(read)

            data[username]["video_count"] = len(videos)
            data[username]["videos"] = videos

            with open("./data.json", "w") as write:
                json.dump(data, write, indent=4)

            return videos

        iterations += 1


@data_file_check
async def get_latest_videos(username: str, count: int):
    await get_profile_data(username)

    async with aiohttp.ClientSession() as session:
        async with session.get(BASE_URL + username) as response:
            html = await response.text()

            soup = BeautifulSoup(html, "html.parser")

            scripts = soup.find_all("script", attrs={"type": "application/json"})

            for script in scripts:
                if "user-post" not in str(script):
                    continue

                profile_data: Dict = json.loads(script.string)
                item_list: Dict = profile_data.get("ItemList")

                user_post: Dict = item_list.get("user-post")
                post_urls: List[str] = user_post.get("list")

                complete_url = [
                    BASE_URL + username + URL_SUFFIX + id for id in post_urls[:count]
                ]

                with open("./data.json", "r") as read:
                    data: Dict = json.load(read)

                data[username]["videos"] = complete_url

                with open("./data.json", "w") as write:
                    json.dump(data, write, indent=4)

                return complete_url


async def followers(username: str) -> str:
    cached_data = check_profile(username)
    if not cached_data.get("following"):
        data: Dict = await get_profile_data(username)
        return data.get("followers")

    return cached_data.get("followers")


async def likes(username: str) -> str:
    cached_data = check_profile(username)
    if not cached_data or not cached_data.get("following"):
        data: Dict = await get_profile_data(username)
        return data.get("likes")

    return cached_data.get("likes")


async def following(username: str) -> str:
    cached_data = check_profile(username)
    if not cached_data or not cached_data.get("following"):
        data: Dict = await get_profile_data(username)
        return data.get("following")

    return cached_data.get("following")


async def latest_videos(username, count):
    cached_data = check_profile(username)
    if not cached_data or not cached_data.get("videos"):
        result = await get_latest_videos(username, count)
        return result

    return cached_data.get("videos")


async def all_videos(username: str):
    # TODO: Eventually check cache on all videos and return that instead of long running function
    result = await get_all_videos(username)
    return result


all_videos("tiktok")