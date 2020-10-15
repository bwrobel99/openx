import unittest
from collections import Counter
from ex2 import *


class ExerciseTest(unittest.TestCase):

    def test_read_data_gets_all_posts(self):
        test_posts_data = read_data_from_url("https://jsonplaceholder.typicode.com/posts")
        self.assertEqual(100, len(test_posts_data))

    def test_read_data_gets_all_users(self):
        test_users_data = read_data_from_url("https://jsonplaceholder.typicode.com/users")
        self.assertEqual(10, len(test_users_data))

    def test_join_users_with_posts_type(self):
        test_posts_data = [{'userId': "1"}, {'userId': "2"}, {'userId': "3"}]
        test_users_data = [{'id': "1", 'username': "user1"}, {'id': "2", 'username': "user2"},
                           {'id': "3", 'username': "user3"}]
        test_data_joined = join_users_with_posts(test_users_data, test_posts_data)
        self.assertTrue(type(test_data_joined) is dict)

    def test_join_users_length(self):
        test_posts_data = [{'userId': "1"}, {'userId': "2"}, {'userId': "3"}]
        test_users_data = [{'id': "1", 'username': "user1"}, {'id': "2", 'username': "user2"},
                           {'id': "3", 'username': "user3"}]
        test_data_joined = join_users_with_posts(test_users_data, test_posts_data)
        self.assertEqual(3, len(test_data_joined))

    def test_post_count(self):
        test_data_joined = {'user1': ["1", "2", "3"], 'user2': ["1", "2"]}
        test_post_count = count_users_posts(test_data_joined)
        ideal_count = ["{} napisal(a) {} postow".format(name, len(posts)) for name, posts in test_data_joined.items()]
        self.assertEqual(test_post_count, ideal_count)

    def test_return_non_unique_titles_NON_UNIQUE_TITLE_EXISTS(self):
        test_posts_data = [{'title': "test1"}, {'title': "test2"}, {'title': "test1"}, {'title': "test4"}]
        non_unique_titles = return_non_unique_titles(test_posts_data)
        self.assertEqual(non_unique_titles, ["test1"])

    def test_return_non_unique_titles_ALL_UNIQUE(self):
        test_posts_data = [{'title': "test1"}, {'title': "test2"}, {'title': "test3"}, {'title': "test4"}]
        with self.assertRaises(EveryTitleUniqueError):
            non_unique_titles = return_non_unique_titles(test_posts_data)

    def test_finding_closest_user(self):
        test_users_data = [{'name': "user1", 'address': {'geo': {'lat': 50.049683, 'lng': 19.944544}}},
                           {'name': "user2", 'address': {'geo': {'lat': 52.237049, 'lng': 21.017532}}},
                           {'name': "user3", 'address': {'geo': {'lat': -31.953512, 'lng': 115.857048}}},
                           {'name': "user4", 'address': {'geo': {'lat': -33.870453, 'lng': 151.208755}}},
                           {'name': "user5", 'address': {'geo': {'lat': 50.270908, 'lng': 19.039993}}}]
        closest_pairs = find_closest_user_for_every_user(test_users_data)
        self.assertEqual(closest_pairs, {'user1': "user5", 'user2': "user1", 'user3': "user4", "user4": "user3",
                                         "user5": "user1"})








if __name__ == '__main__':
    unittest.main()