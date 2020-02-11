import re
import struct
from collections import namedtuple

class StlFile:
	sizeDesc      = 0x28 # Default description size is 40 bytes (sometimes 80 bytes)
	sizeHeader    = 0x28 # Default header size is 40 bytes
	sizeMPQHeader = 0x10 # Default MPQ header size is 16 bytes
	sizeRecord    = 0x10 # Default record size is 16 bytes

	def __init__(self, filePath, recordCount, scaleDesc=1.0, sortResult=False):
		self.recordCount = recordCount
		self.sizeDesc = int(self.sizeDesc * scaleDesc) # Sometimes this is 2x the size
		self.sortResult = sortResult
		
		try:
			self.fileHandle = open(filePath, 'rb')
		except IOError:
			print('StlFile: That .stl file does not exist or is read protected')
		else:
			if not self.readHeader():
				print('Error: this is not a correct STL file!')
			else:
				self.readStrings()
		self.fileHandle.close()
				
	def readHeader(self):
		stlHeader = namedtuple('stlHeader', 'magic unk1 free1 unk2 free2 free3 free4 unk3 dataStart free5')
		self.header = stlHeader(*struct.unpack('@IILIILLIIL', self.fileHandle.read(self.sizeHeader)))
		#print(self.header)
		if (not self.header.magic == 0xDEADBEEF):
			return False
		return True
	
	def readStrings(self):
		stlRecord = namedtuple('stlRecord', 'type free1 start length')
		stlDesc = namedtuple('stlDesc', 'name value add1 add2 end')
		numOfRecords = (self.header.dataStart - self.sizeHeader) // self.sizeDesc
		#print(self.header.dataStart, self.sizeHeader)
		self.desc = []
		self.stringList = []
		for i in range(self.recordCount):
			desc = []
			string = []
			for j in range(5):
				self.fileHandle.seek((i * self.sizeDesc) + self.sizeHeader + j * self.sizeRecord)	
				record = stlRecord(*struct.unpack('@IIII', self.fileHandle.read(self.sizeRecord)))
				self.fileHandle.seek(record.start + self.sizeMPQHeader)
				string.append(self.fileHandle.read(record.length))
				desc.append(record)
			sDesc = stlDesc(desc[0], desc[1], desc[2], desc[3], desc[4])
			self.desc.append(sDesc)
			self.stringList.append(string)
		if self.sortResult:
			self.stringList = sorted(self.stringList, key=lambda string: self.decodeValue(string[1]).lower()) # Sort by key

	def printList(self):
		for string in self.stringList:
			print(self.decodeValue(string[1]) + ' => ' + self.decodeValue(string[2]))

	def writeToFile(self, filename):
		with open(filename, 'w') as f:
			for string in self.stringList:
				f.write("{0}\t{1}\n".format(self.decodeValue(string[1]), self.decodeValue(string[2])))

	def decodeValue(self, unicodeValue):
		return self.trim(unicodeValue.decode('UTF-8').strip())

	def trim(self, stringValue):
		return re.sub(r'^\W*|\W*$', "", stringValue, flags=re.UNICODE)
