#!/usr/bin/env python3

'''
Simple PNG enumerator
'''

import argparse

from modules.pngdata import PNG

def main():
	parser = argparse.ArgumentParser(description='A PNG enumerator.')
	parser.add_argument('filename', 
			type=argparse.FileType('rb'),
			help='PNG file name')
	args = parser.parse_args()
	
	with args.filename as file:
		data=file.read()

		png = PNG.read(data)
		PNG.printPngData(png)

if __name__ == '__main__':
	main()