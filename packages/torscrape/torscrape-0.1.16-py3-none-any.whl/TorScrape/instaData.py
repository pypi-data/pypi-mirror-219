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