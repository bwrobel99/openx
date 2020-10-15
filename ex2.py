from typing import List, Dict
from geopy import distance
import json
import urllib.request


class EveryTitleUniqueError(Exception):
    pass


# read json data from url & decode it
def read_data_from_url(url: str) -> List[Dict]:
    with urllib.request.urlopen(url) as u:
        data = json.loads(u.read().decode())
    return data


posts_data = read_data_from_url("https://jsonplaceholder.typicode.com/posts")
users_data = read_data_from_url("https://jsonplaceholder.typicode.com/users")


# join user data with post data: username -> list of user's posts


def join_users_with_posts(users_to_connect: List[Dict], posts_to_connect: List[Dict]) -> Dict[str, List]:
    users_posts = {}
    for user in users_to_connect:
        for post in posts_to_connect:
            if post['userId'] == user['id']:
                users_posts.setdefault(user['username'], []).append(post)
    return users_posts


users_posts_connected = join_users_with_posts(users_data, posts_data)


# count every user's posts, return list of strings
def count_users_posts(users_with_posts: Dict[str, List]) -> List[str]:
    post_count_for_all_users = []
    for user, posts in users_with_posts.items():
        post_count_for_all_users.append("{} napisal(a) {} postow".format(user, len(posts)))
    return post_count_for_all_users


post_count_for_all = count_users_posts(users_posts_connected)
print(post_count_for_all)


# check if titles are unique, return list of titles that are not
# using set, because it all of its members must be unique
def return_non_unique_titles(posts_data_to_search: List[Dict]) -> List[str]:
    unique_post_titles = set()
    is_post_title_unique = {}  # title: str -> is it unique?: bool
    for post in posts_data_to_search:
        set_len_bef_adding = len(unique_post_titles)
        unique_post_titles.add(post['title'])  # if title is unique, it will be added
        set_len_aft_adding = len(unique_post_titles)
        if set_len_aft_adding == set_len_bef_adding:
            is_post_title_unique[post['title']] = False
        else:
            is_post_title_unique[post['title']] = True
    non_unique_titles = [title for title, is_unique in is_post_title_unique.items() if not is_unique]
    if not non_unique_titles:
        raise EveryTitleUniqueError
    return non_unique_titles


try:
    print(return_non_unique_titles(posts_data))
except EveryTitleUniqueError:
    print("Every title is unique!")


def find_closest_user_for_every_user(users_data_to_search: List[Dict]) -> Dict[str, str]:
    user_coordinates = {}  # dict: user's name -> geo coordinates, created to make code simpler&faster
    for user in users_data_to_search:
        user_geo = user.get('address')['geo']
        user_name = user.get('name')
        user_coordinates[user_name] = user_geo

    # using geopy.distance.distance to measure distance
    closest_users_pairs = {}  # user -> closest user to them
    for curr_name, curr_coordinates in user_coordinates.items():
        distances_from_user_to_others = {}
        for other_name, other_coordinates in user_coordinates.items():
            if other_name == curr_name:
                continue
            else:
                curr_location = float(curr_coordinates['lat']), float(curr_coordinates['lng'])
                other_location = float(other_coordinates['lat']), float(other_coordinates['lng'])
                distances_from_user_to_others[other_name] = distance.distance(curr_location, other_location).km
        closest_users_pairs[curr_name] = min(distances_from_user_to_others, key=distances_from_user_to_others.get)
    return closest_users_pairs


closest_users = find_closest_user_for_every_user(users_data)
print(closest_users)