import os
import re
import unittest


def readfile(name):
	f = open(name)
	res = f.read()
	f.close()
	return res


here = os.path.dirname(os.path.abspath(__file__))
parent = os.path.dirname(here)


class TestCase(unittest.TestCase):

	def test_version(self):
		setup = readfile(os.path.join(parent, 'setup.py'))
		init = readfile(os.path.join(parent, 'ModernGL', '__init__.py'))
		main = readfile(os.path.join(parent, 'ModernGL', '__main__.py'))
		docs = readfile(os.path.join(parent, 'docs', 'conf.py'))

		match0 = re.search(r'\'version\': \'(\d+\.\d+\.\d+)\'', setup, flags = re.M)
		version = match0.group(1)

		match1 = re.search(r'version = \'(\d+\.\d+\.\d+)\'', init, flags = re.M)
		match2 = re.search(r'version = \'%\(prog\)s (\d+\.\d+\.\d+)\'', main, flags = re.M)
		match3 = re.search(r'version = \'(\d+\.\d+\.\d+)\'', docs, flags = re.M)
		match4 = re.search(r'release = \'(\d+\.\d+\.\d+)\'', docs, flags = re.M)

		self.assertEqual(version, match1.group(1), msg = 'Version error: ModernGL/__init__.py')
		self.assertEqual(version, match2.group(1), msg = 'Version error: ModernGL/__main__.py')
		self.assertEqual(version, match3.group(1), msg = 'Version error: docs/conf.py')
		self.assertEqual(version, match4.group(1), msg = 'Version error: docs/conf.py')


if __name__ == '__main__':
	unittest.main()
