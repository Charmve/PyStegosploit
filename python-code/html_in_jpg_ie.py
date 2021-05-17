#!/usr/bin/env python3

'''
Creates and HTML+JPG polyglot for Internet Explorer
'''

import argparse
import re
import random

RANDOM_DATA_SIZE = 1900

STEGO = """
                                  .       .
                                 / `.   .' \\
                         .---.  <    > <    >  .---.
                         |    \\  \\ - ~ ~ - /  /    |
                          ~-..-~             ~-..-~
                      \\~~~\\.'   stegosploit      `./~~~/
                       \\__/                imajs   \\__/
                         /  .    -.                 \\
                  \\~~~\\/   {       \\       .-~ ~-.    -._ _._
                   \\__/    :        }     {       \\     ~{  p'-._
    .     .   |~~. .'       \\       }      \\       )      \\  ~--'}
    \\\\   //   `-..'       _ -\\      |      _\\      )__.-~~'='''''
 `-._\\\\_//__..-'      .-~    |\\.    }~~--~~  \\=   / \\
  ``~---.._ _ _ . - ~        ) /=  /         /+  /   }
                            /_/   /         {   } |  |
                              `~---o.       `~___o.---'
"""


def genRandomHTMLChar():
	while True:
		x = random.randint(0,255)
		if x != 0 and x!=ord('<') and x!=ord('>') and x!=ord('/'):
			return x

def main():
	print(STEGO)	# print the stego

	description = 'Creates and HTML+JPG polyglot for Internet Explorer.'
	parser = argparse.ArgumentParser(description = description)
	parser.add_argument('htmlfile', 
			type=argparse.FileType('r'),
			nargs='?',					# REMOVE ME: sets the arg optional
			help='HTML file name')

	parser.add_argument('jpgfile', 
			type=argparse.FileType('rb'),
			nargs='?',					# REMOVE ME
			help='JPG file name')

	parser.add_argument('output', 
			type=argparse.FileType('wb'),
			nargs='?',					# REMOVE ME
			help='Output file name')
	args = parser.parse_args()

	htmlData = 'hello'		# FIXME
	if args.htmlfile:
		htmlData = args.htmlfile.read()
		htmlData = htmlData.rstrip()	# remove trailing whitespace

	jpgData = open('anon.jpg','rb').read()	# FIXME
	if args.jpgfile:
		jpgData = args.jpgfile.read()

	jpgStart = jpgData[:4]		# read the first 4 bytes (Magic # = 0xFFD8FFE0)
	jfifapp0 = jpgData[6:20]	# from JFIF to offset 20
	restOfJpg = jpgData[20:]	# read the rest of the file

	jpgData = None	# remove jpgData from cache for performance

	# print('',jpgStart,'\n',jfifapp0,'\n',restOfJpg)

	html = '<html><!--'
	content = ' -->'

	# remove <html>,<head> and <meta http-equiv ...> tags
	# from the html
	htmlTags = re.compile('<html>')
	headTags = re.compile('<head>')
	metaTags = re.compile('<meta http-equiv[^>]*>')

	htmlData = re.sub(htmlTags,'',htmlData)
	# htmlData = re.sub(headTags,'',htmlData)
	# htmlData = re.sub(metaTags,'',htmlData)

	content += htmlData + '<!--'

	paddingLength = 0x2f2a - len(content) - len(html)
	randomLength = random.randint(0,RANDOM_DATA_SIZE)

	padding = ''
	for i in range(paddingLength):
		x = genRandomHTMLChar()
		padding += chr(x)

	prePadding = padding[0:randomLength]
	postPadding = padding[randomLength:]
	
	finalContent = html + prePadding + content + postPadding	

	# lots of print statements
	print('HTML header length = %d' % len(html))
	print('Pre padding length = %d' % len(prePadding))
	print('Post padding length = %d' % len(postPadding))
	print('HTML data length = %d' % len(htmlData))
	print('Content length = %d' % len(content))
	print('Final content length = %d' % len(finalContent))

	newJpg = jpgStart + '/*'.encode() + jfifapp0 + finalContent.encode() + restOfJpg + '*/ -->'.encode()

	print(newJpg)		# Output to file

if __name__ == '__main__':
	main()