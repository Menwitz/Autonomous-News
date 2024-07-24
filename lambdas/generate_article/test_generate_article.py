# test_generate_article.py

import unittest
from generate_article_v1 import generate_article

class TestOpenAI(unittest.TestCase):

    headlines = [
        'Swimming star famed for Michael Phelps upset eyes another Olympic gold',
        'Supreme Court declines to halt former Colorado official trial on charges related to election security breach'

    ]
    def test_generate_article(self):
        #self.assertEqual(generate_article(self.headlines[0]), 0)
        print(generate_article(self.headlines[0]))
        print(generate_article(self.headlines[1]))


if __name__ == '__main__':
    unittest.main()
