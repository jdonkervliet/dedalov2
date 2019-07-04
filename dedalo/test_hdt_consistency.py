
import codecs
import unittest

import hdt

from example import Examples


def strict_handler(exception):
    return u"", exception.end
codecs.register_error("strict", strict_handler)

class TestConsistentAnswers(unittest.TestCase):

    test_file = "../datasets/examples/1_western_zodiac_examples.txt"

    def get_examples(self):
        return Examples.fromCSV(TestConsistentAnswers.test_file)

    def get_all_triples(self, examples):
        doc = hdt.HDTDocument("/scratch/wbeek/data/LOD-a-lot/data.hdt")
        res = set()
        for example in examples:
            enum, _ = doc.search_triples(example.uri, "", "")
            for triple in enum:
                res.add(triple)
        return res

    def get_examples_and_all_triples(self):
        doc = hdt.HDTDocument("/scratch/wbeek/data/LOD-a-lot/data.hdt")
        examples = Examples.fromCSV(TestConsistentAnswers.test_file)
        res = set()
        for example in examples:
            enum, _ = doc.search_triples(example.uri, "", "")
            for triple in enum:
                res.add(triple)
        return res

    def test_get_examples(self):
        e1 = self.get_examples()
        e2 = self.get_examples()
        self.assertEqual(len(e1), len(e2))
        self.assertEqual(e1, e2)

    def test_get_correct_number_of_examples(self):
        e = self.get_examples()
        self.assertEqual(len(e), 160)

    def test_get_triples(self):
        examples = self.get_examples()
        n1 = self.get_all_triples(examples)
        n2 = self.get_all_triples(examples)
        self.assertEqual(len(n1), len(n2))
        self.assertEqual(n1, n2)

    def test_get_correct_number_of_triples(self):
        num_triples = 248726
        triples = self.get_examples_and_all_triples()
        self.assertEqual(len(triples), num_triples)

if __name__ == '__main__':
    unittest.main()
