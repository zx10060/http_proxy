import unittest
from main import add_tm, modify_links


class TestStringMethods(unittest.TestCase):
    def test_add_tm(self):
        data = "abroad accept access"
        self.assertEqual(add_tm(data), "abroad™ accept™ access™")

    def test_replace_links(self):
        data = '''
            < a href = "https://news.ycombinator.com/item?id=13719368" rel = "nofollow" >
                https://news.ycombinator.com&/item?id=13719368</a>
            '''
        equals_data = '''
            <a href="http://127.0.0.1:8000/news.ycombinator.com/item?id=13719368" rel = "nofollow" >
                https://news.ycombinator.com&/item?id=13719368</a>
            '''
        data = modify_links(data)
        self.assertEqual(data, equals_data)


if __name__ == '__main__':
    unittest.main()
