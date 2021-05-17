'''
program: pngdata.py

Description: A port of the PNGDATA.pm module
'''

import binascii
import struct

# conditional module export
if __name__ == '__main__':
	from crc32 import CRC32
else:
	from .crc32 import CRC32

class PNG:
	'''
	Function to read PNG file in chunks and create
	a PNG array

	Input: entire png file
	Output: array of png chunks
	'''
	def read(data):
		pngChunks = []

		header = PNG.getHeader(data)
		pngChunks.append(header)
		data = data[8:]  # remove header bytes from data

		while len(data) > 0:
			length 		= int.from_bytes(data[0:4], byteorder='big')		# 4 bytes
			chunkType 	= data[4:8]
			chunkData	= data[8:length+8]
			crc 		= data[length+8:length+12]

			chunk = [length, chunkType, chunkData, crc]
			pngChunks.append(chunk)

			chunkSize = 12+length
			data = data[chunkSize:]		# remove the chunk from data

		return pngChunks

	'''
	function to print the PNG data from chunk array
	
	INPUT: png_chunks: array of PNG chunks
	OUTPUT: nothing
	'''
	def printPngData(chunks):
		PNG.printHeader(chunks[0])
		chunks = chunks[1:]	# truncate chunks
		for c in chunks:
			PNG.printChunk(c)
   
	'''
	Get the PNG header
	'''
	def getHeader(data):
		return data[:8]		# PNGs contain an 8-byte header

	def printHeader(header):
		# Check if the header matches the magic numbers
		status = 'OK!'
		if header != b'\x89PNG\r\n\x1a\n':
			status = 'Error'

		print('PNG Header: %s - %s' % (header, status))


	'''
	Function to print a png chunk

	Input: PNG chunk
		format: [length, chunkType, chunkData, crc]
	Output: Nothing
	'''
	def printChunk(chunk):
		length 		= chunk[0]		# stored as int
		chunkType 	= chunk[1]
		chunkData 	= chunk[2]
		crc 		= int.from_bytes(chunk[3],'big')		# stored as int

		crc32 = CRC32()
		crc32.add(chunkType+chunkData)
		computedCrc = crc32.result()

		status = 'OK'
		if computedCrc != crc:
			status = 'Error'

		print('%s %d bytes CRC: %#010x (computed %#010x) - %s)' % (chunkType, length, crc, computedCrc, status))

	'''
	INPUT: 	Name (bytes string)
			Value (bytes string)
	OUTPUT: chunk
	'''
	def makeTextChunk(name, value):
		chunkType = b'tEXt'

		data = name + b'\x00' + value
		length = len(data)
		data = chunkType + data 	# Prepend the chunk type

		crc32 = CRC32()
		crc32.add(data)
		crc = crc32.result()

		crc = struct.pack('>l',crc)		# Pack crc into 4 big-endian bytes
		length = struct.pack('>l',length)  # Pack length into 4 big-endian bytes
		chunk = length + data + crc
		return(chunk)

	def makeIendChunk():
		length = struct.pack('>l',0)
		crc = b'\xAE\x42\x60\x82'
		chunk = length + b'IEND' + crc
		return chunk

def main():
	with open('../anon.png', 'rb') as file:
		data=file.read()

		# test getHeader(), printHeader()
		header = PNG.getHeader(data)
		PNG.printHeader(header)

		# test read(), printChunk()
		chunks = PNG.read(data)
		PNG.printChunk(chunks[1])
		PNG.printPngData(chunks)

		# Test makeTextChunk()
		textChunk = PNG.makeTextChunk(b'name',b'value')
		textChunk = PNG.read(header+textChunk) # add header, read into chunk
		PNG.printChunk(textChunk[1])

		# test makeIendChunk()
		iendChunk = PNG.makeIendChunk()
		iendChunk = PNG.read(header+iendChunk) # add header, read into chunk
		PNG.printChunk(iendChunk[1])

if __name__ == '__main__':
	main()