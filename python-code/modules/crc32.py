#!/usr/bin/env python3

'''
Generates an unsigned 32-bit integer checksum for
arbitrary data.  Instead of rolling our own CRC32
generator, we will be using binascii

Usage:
	crc32 = CRC32()
	crc32.add(data)
	checkValue = crc32.result()
'''

import binascii

class CRC32:
	def __init__(self):
		self.crc = None

	'''
	Input: bytes string
	Output: True
	'''
	def add(self, data):
		# evaluate the CRC32 checksum
		if self.crc != None:
			self.crc = binascii.crc32(data, self.crc)
		else:
			self.crc = binascii.crc32(data)

		return True

	def result(self):
		return self.crc

def main():
	crc32 = CRC32()

	crc32.add(b'hello world')
	crc = crc32.result()
	# print(crc)
	print('crc32 = {:#010x}'.format(crc))

if __name__ == '__main__':
	main()