# test_generate_article.py

import unittest
from generate_article_v1 import generate_article
import json
import time

class TestOpenAI(unittest.TestCase):

    def test_generate_article(self):
        #self.assertEqual(generate_article(self.headlines[0]), 0)
            # Load the input file
        with open('tu_in_generate_article.json', 'r') as file:
            headlines = json.load(file)

       
        test_results = []
        
        i = 0
        for test_case in headlines['tu_headlines']:
            print(test_case)
            start_time = time.time()
            output = generate_article(test_case)
            end_time = time.time()

            count_test_time = end_time - start_time

            test_results.append({
                "input": test_case,
                "output": output,
                "time": count_test_time
            })
            i = i + 1

            # Log the results to an output file
        with open('tu_out_generate_article.json', 'w') as file:
            json.dump(test_results, file, indent=4)

        print("All test cases logged to tu_out_generate_article.json")


if __name__ == '__main__':
    unittest.main()
