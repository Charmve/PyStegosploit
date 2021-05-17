'''

Description: Creates an HTML+PNG polyglot

'''


import struct
import re
import random
import argparse


class Polyglot:
	def __init__(self, decoder_html, encoded_jpg, out_polyglot):
		self.infile = open(encoded_jpg,'rb')
		self.outfile = open(out_polyglot,'wb')		# poly.html
		self.decoder_html = decoder_html

	def genRandomHTMLChar():
		while True:
			x = random.randint(0,255)
			if x != 0 and x!=ord('<') and x!=ord('>') and x!=ord('/'):
				return x


	def create(self, debug=True):
		infile = self.infile
		outfile = self.outfile

		scanning = False

		prevByte = infile.read(2)
		outfile.write(prevByte)

		while True:
			curByte = infile.read(1)
			if not curByte:
				break

			# Write the 
			if 0xff in prevByte and curByte[0] in range(0xe0,0xe9):
				outfile.write(curByte)
				exifLen = struct.unpack('>H',infile.read(2))[0]-2	# convert exif length
				outfile.write(struct.pack('>H', 0x2f2a))	# set the exif header to 0
				exifData = infile.read(exifLen)				# write the exif header to the file
				outfile.write(exifData)

				with open(self.decoder_html, 'rb') as f:
					decoder = f.read()

				html = b'<html><!--'
				content = b'-->'+decoder+b'<!--'
				paddingLen = 0x2f2a - len(content) - len(html) - exifLen - 2
				randomLength = random.randint(0,paddingLen)
				padding = b''
				for i in range(paddingLen):
					x = Polyglot.genRandomHTMLChar()
					padding += bytes([x])

				prePadding = padding[0:randomLength]
				postPadding = padding[randomLength:]

				finalContent = html + prePadding + content + postPadding
				outfile.write(finalContent)				# write payload into the exif
				curByte = infile.read(1)

				if debug:
					print('Write out exif data','\n')
				

			# Define Quantization Table(s) 
			elif 0xff in prevByte and 0xdb in curByte:
				outfile.write(curByte)
				dqtLen = struct.unpack('>H',infile.read(2))[0]-2
				data = infile.read(dqtLen)
				outfile.write(struct.pack('>H',dqtLen+2))
				outfile.write(data)
				
				if debug:
					print('Define Quantization Tables')
					print(data,'\n')

				curByte = infile.read(1)

			# Frame Header:
			#
			# Indicates that this is a baseline DCT-based JPEG, and 
			# specifies the width, height, number of components, and 
			# component subsampling (e.g., 4:2:0) 
			elif 0xff in prevByte and 0xc0 in curByte:
				outfile.write(curByte)
				frameHeaderLen = struct.unpack('>H',infile.read(2))[0]-2
				data = infile.read(frameHeaderLen)
				outfile.write(struct.pack('>H',frameHeaderLen+2))
				outfile.write(data)
				if debug:
					print('Frame header')
					print(data,'\n')
					# http://lad.dsc.ufcg.edu.br/multimidia/jpegmarker.pdf
				curByte = infile.read(1)

			# Frame Header:
			#
			# Indicates that this is a progressive DCT-based JPEG, and 
			# specifies the width, height, number of components, and 
			# component subsampling (e.g., 4:2:0). 
			elif 0xff in prevByte and 0xc2 in curByte:
				outfile.write(curByte)
				frameHeaderLen = struct.unpack('>H',infile.read(2))[0]-2
				data = infile.read(frameHeaderLen)
				outfile.write(struct.pack('>H',frameHeaderLen+2))
				outfile.write(data)
				if debug:
					print('Frame header')
					print(data,'\n')
				curByte = infile.read(1)

			# Start Huffman tables
			elif 0xff in prevByte and 0xc4 in curByte:
				outfile.write(curByte)
				huffmanTableLen = struct.unpack('>H',infile.read(2))[0]-2
				data = infile.read(huffmanTableLen)
				
				outfile.write(struct.pack('>H',huffmanTableLen+2))
				outfile.write(data)
				if debug:
					print('Start Huffman table')
					print(data,'\n')
				curByte = infile.read(1)

			# Start of scan (SOS)
			elif 0xff in prevByte and 0xda in curByte:
				outfile.write(curByte)
				sosLen = struct.unpack('>H',infile.read(2))[0]-2
				data = infile.read(sosLen)

				outfile.write(struct.pack('>H',sosLen+2))
				outfile.write(data)
				if debug:
					print('Start of scan (SOS)')
					print(data,'\n')
				scanning=True
				curByte = infile.read(1)


			# NOTE: Scanning image data
			elif scanning:
				# print(curByte)
				pass

			# End of frame marker
			elif 0xff in prevByte and 0xd9 in curByte:
				print(prevByte, curByte)
				print('end')

			else:
				pass

			outfile.write(curByte)
			prevByte = curByte

		# end all content
		outfile.write(b'\x2a\x2f -->')
		
		outfile.close()
		infile.close()

	def bits(debug=True):
		infile = open('out2.jpg','rb')

		prevByte = infile.read(1)
		while True:
			curByte = infile.read(1)
			if not curByte:
				break

			# Start of scan (SOS)
			if 0xff in prevByte and 0xda in curByte:
				sosLen = struct.unpack('>H',infile.read(2))[0]
				data = infile.read(sosLen-2)
				if debug:
					print('Start of scan (SOS)')
					print(data,'\n')
				infile.seek(-2,1)
				break

		while True:

			# NOTE: The actual image data is between the SOS and 
			# the end of frame marker


			# End of frame marker
			if 0xff in prevByte and 0xd9 in curByte:
				print(prevByte, curByte)
				print('end')

			prevByte = curByte

		infile.close()


def main():
	description = 'Creates an HTML+JPG polyglot for Internet Explorer.'
	parser = argparse.ArgumentParser(description = description)
	parser.add_argument('html_file', 
			help='HTML file name')

	parser.add_argument('jpg_file', 
			help='JPG file name')

	parser.add_argument('out_polyglot', 
			help='Output file name')
	args = parser.parse_args()

	Polyglot(args.html_file, args.jpg_file, args.out_polyglot).create(debug=False)

if __name__ == '__main__':
	main()