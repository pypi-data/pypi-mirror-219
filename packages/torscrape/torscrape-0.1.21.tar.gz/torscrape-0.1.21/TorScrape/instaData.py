import aiohttp
import asyncio
import requests
from bs4 import BeautifulSoup

def get_insta_followers(username):
    # Send a GET request to fetch the profile page
    response = requests.get(f"https://www.instagram.com/{username}/")

    if response.status_code == 200:
        try:
            soup = BeautifulSoup(response.content, "html.parser")
            # Extract the meta description from the HTML
            meta_description = soup.find("meta", property="og:description")["content"]

            # Extract the followers count from the meta description
            followers_count = meta_description.split("-")[0].strip().split(" ")[0]
            return followers_count
        except (KeyError, ValueError):
            return "Unable to fetch followers count."
    else:
        return "Unable to fetch profile page. Please check the profile name."


def get_insta_following(username):
    # Send a GET request to fetch the profile page
    response = requests.get(f"https://www.instagram.com/{username}/")

    if response.status_code == 200:
        try:
            soup = BeautifulSoup(response.content, "html.parser")
            # Extract the meta description from the HTML
            meta_description = soup.find("meta", property="og:description")["content"]

            # Extract the following count from the meta description
            following_count = meta_description.split("-")[0].strip().split(" ")[2]
            return following_count
        except (KeyError, ValueError):
            return "Unable to fetch following count."
    else:
        return "Unable to fetch profile page. Please check the profile name."


def get_insta_posts(username):
    # Send a GET request to fetch the profile page
    response = requests.get(f"https://www.instagram.com/{username}/")

    if response.status_code == 200:
        try:
            soup = BeautifulSoup(response.content, "html.parser")
            # Extract the meta description from the HTML
            meta_description = soup.find("meta", property="og:description")["content"]

            # Extract the posts count from the meta description
            posts_count = meta_description.split("-")[0].strip().split(" ")[4]
            return posts_count
        except (KeyError, ValueError):
            return "Unable to fetch posts count."
    else:
        return "Unable to fetch profile page. Please check the profile name."


def search_insta_comments(username, keyword):
    url = f"https://www.instagram.com/{username}/"

    response = requests.get(url)
    if response.ok:
        soup = BeautifulSoup(response.text, "html.parser")
        comments = soup.find_all("div", class_="_a9zo")

        for comment in comments:
            profile_picture = comment.find("img")["src"]
            username = comment.find("a", class_="x1qjc9v5").text
            comment_text = comment.find("span", class_="_aacl").text

            if keyword in comment_text:
                print(f"Profile Picture: {profile_picture}")
                print(f"Username: {username}")
                print(f"Comment: {comment_text}")
                print()

def get_insta_comment(username, keyword):
    search_insta_comments(username, keyword)

get_insta_comment("oskarwesterlin", "TOP")