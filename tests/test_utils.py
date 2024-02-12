import random
import string
import unittest
import os

from api import utils

class TestUtils(unittest.TestCase):

    def test_upper(self):
        data = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
        utils.linux.file_wirte(data, 'a.txt')
        result = utils.linux.file_read('a.txt')
        self.assertEqual(result, data)
        
    def test_copy(self):
        src = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
        utils.linux.file_wirte(src, 'a.txt')
        utils.linux.file_cp('a.txt', 'b.txt')
        dst = utils.linux.file_read('b.txt')
        self.assertEqual(src,dst)
        
    def test_move(self):
        src = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
        utils.linux.file_wirte(src, 'a.txt')
        utils.linux.file_mv('a.txt', 'b.txt')
        dst = utils.linux.file_read('b.txt')
        if not os.path.isfile('a.txt'):
            self.assertEqual(src,dst)
