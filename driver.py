import os
from D3StringGrabber import StlFile

DIR_INPUT = 'input'
DIR_OUTPUT = 'output'

FILE_ARGS = [
	('Affixes', 2208, 2.0),
	('Bnet_Store', 300),
	('BnetStore_ItemDescriptions', 293),
	('General', 285),
	('Items', 6242),
]

def setup():
	os.mkdir(DIR_OUTPUT) if not os.path.exists else None

def run():
	[parse(*args) for args in FILE_ARGS]

def parse(filename, lines, scale=1.0, sortResults=True):
	stl = StlFile('{0}/{1}.stl'.format(DIR_INPUT, filename), lines, scale, sortResults)
	stl.writeToFile('{0}/{1}.txt'.format(DIR_OUTPUT, filename))
	print('Parsed file: {0}.stl'.format(filename))

if __name__ == '__main__':
	setup()
	run()