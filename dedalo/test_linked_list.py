
import unittest
from linked_list import LinkedNode

class TestLinkedList(unittest.TestCase):
    def test_create(self):
        l = LinkedNode(1)
        self.assertEqual(len(l), 1)

    def test_empty_enumerate(self):
        l = LinkedNode(1)
        count = 0
        for _ in l:
            count += 1
        self.assertEqual(count, 1)

    def test_len_1(self):
        l = LinkedNode(1)
        self.assertEqual(len(l), 1)

    def test_len_2(self):
        l = LinkedNode(1)
        l2 = LinkedNode(2, l)
        self.assertEqual(len(l2), 2)

    def test_add_string(self):
        s = "test"
        l = LinkedNode(s)
        self.assertEqual(len(l), 1)
        for v in l:
            self.assertEqual(v, s)

    def test_subscript(self):
        i = 1
        l = LinkedNode(i)
        self.assertEqual(l[0], i)

    def test_index_error(self):
        l = LinkedNode(1)
        with self.assertRaises(IndexError):
            l[1]

    def test_append(self):
        l = LinkedNode(1)
        l2 = LinkedNode(2, l)
        l3 = LinkedNode(3, l2)
        self.assertEqual(l3[0], 1)
        self.assertEqual(l3[1], 2)
        self.assertEqual(l3[2], 3)

    def test_equal(self):
        l = LinkedNode(1)
        l2 = LinkedNode(2, l)
        l3 = LinkedNode(2, l)
        self.assertEqual(l2, l3)

    def test_equal_longer(self):
        l = LinkedNode(1)
        l2 = LinkedNode(1, l)
        self.assertNotEqual(l, l2)

    def test_equal_shorter(self):
        l = LinkedNode(1)
        l2 = LinkedNode(1, l)
        self.assertNotEqual(l2, l)

    def test_str(self):
        l = LinkedNode(1)
        l2 = LinkedNode(2, l)
        self.assertEqual(str(l2), "[1,2]")

if __name__ == '__main__':
    unittest.main()
