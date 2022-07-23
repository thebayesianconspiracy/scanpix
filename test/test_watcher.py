import unittest
from worker.watch_and_index import extract_filename,check_if_image

class TestWatcher(unittest.TestCase):

    def test_extract_filename(self):
        self.assertEqual(extract_filename("/home/what/abcd_efgh.jpg"),"abcd_efgh.jpg")

    def test_check_if_image(self):
        self.assertTrue(check_if_image("abcdef.jpg"))
        self.assertTrue(check_if_image("xyzwe.jpeg"))
        self.assertTrue(check_if_image("dog.png"))
        self.assertFalse(check_if_image("cat.mov"))


if __name__ == "__main__":
    unittest.main()
