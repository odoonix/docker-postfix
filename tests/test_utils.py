import random
import string
import unittest

from api import utils

class TestUtils(unittest.TestCase):

    def test_upper(self):
        data = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
        utils.linux.file_wirte(data, 'a.txt')
        result = utils.linux.file_read('a.txt')
        self.assertEqual(result, data)

        
