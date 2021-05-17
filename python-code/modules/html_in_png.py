#!/usr/bin/env python3

'''
Creates an HTML+png polyglot for Internet Explorer
'''

import argparse
import re
import random
import pngdata

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

	description = 'Creates and HTML+png polyglot for Internet Explorer.'
	parser = argparse.ArgumentParser(description = description)
	parser.add_argument('htmlfile', 
			type=argparse.FileType('r'),
			nargs='?',					# REMOVE ME: sets the arg optional
			help='HTML file name')

	parser.add_argument('pngfile', 
			type=argparse.FileType('rb'),
			nargs='?',					# REMOVE ME
			help='PNG file name')

	parser.add_argument('output', 
			type=argparse.FileType('wb'),
			nargs='?',					# REMOVE ME
			help='Output file name')
	args = parser.parse_args()

	htmlData = ''		
	if args.htmlfile:
		htmlData = args.htmlfile.read()
		htmlData = htmlData.rstrip()	# remove trailing whitespace

	# pngData = open('anon.png','rb').read()	# FIXME
	if args.pngfile:
		png_data = args.pngfile.read()
		# print(png_data)

	open_comment = pngdata.make_text_chunk("<html>", "<!-- ")
	png_data_array = list(png_data)
	png_data_array[2:2] = open_comment

	# pngStart = pngData[:4]		# read the first 4 bytes (Magic # = 0xFFD8FFE0)
	# jfifapp0 = pngData[6:20]	# from JFIF to offset 20
	# restOfpng = pngData[20:]	# read the rest of the file

	# pngData = None	# remove pngData from cache for performance

	# print('',pngStart,'\n',jfifapp0,'\n',restOfpng)

	# html = '<html><!--'
	# content = ' -->'

	# remove <html>,<head> and <meta http-equiv ...> tags
	# from the html
	htmlTags = re.compile('<html>')
	headTags = re.compile('<head>')
	metaTags = re.compile('<meta http-equiv[^>]*>')

	htmlData = re.sub(htmlTags,'',htmlData)

	htmlData = " -->" + htmlData +  "<script type='text/undefined'>/*"

	# htmlData = re.sub(headTags,'',htmlData)
	# htmlData = re.sub(metaTags,'',htmlData)

	# content += htmlData + '<!--'

	# paddingLength= 0x2f2a - len(content) - len(html)
	paddingLength = random.randint(0,RANDOM_DATA_SIZE)

	# 	padding = ''
	for i in range(paddingLength):
		x = genRandomHTMLChar()
		htmlData = chr(x) + htmlData

	# prePadding = padding[0:randomLength]
	# postPadding = padding[randomLength:]
	
	html_Content = pngdata.make_text_chunk("_", htmlData)
	png_data_array[3:3] = html_Content

	# lots of print statements
	# print('HTML header length = %d' % len(html))
	# print('Pre padding length = %d' % len(prePadding))
	# print('Post padding length = %d' % len(postPadding))
	# print('HTML data length = %d' % len(htmlData))
	# print('Content length = %d' % len(content))
	# print('Final content length = %d' % len(finalContent))

	# newpng = ''.join(png_data_array)
	print(png_data_array)
	newpng = bytes(png_data_array)
	# pp

	# print(newpng)		# Output to file
	
	with open(args.output, 'wb') as f: 
		f.write(newpng) 

if __name__ == '__main__':
	main()