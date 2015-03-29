#!/usr/bin/python

import argparse
import json
import os.path
import re
import xml.etree.ElementTree

class JsonToPlist:
	ISO8601_PATTERN = re.compile(r'\d+-\d+-\d+T\d+:\d+:\d+Z')

	#
	# Main function
	def main(self):
		# Parse arguments
		parser = argparse.ArgumentParser(description = 'Convert JSON to Plist.')
		parser.add_argument('--ext', nargs='?', help='extension of output files', default='plist')
		parser.add_argument('files', nargs='+', help='files to convert')
		args = parser.parse_args()

		for filePath in args.files:
			self.convertFile(filePath, args.ext)

	#
	# Convert json file to Plist file
	def convertFile(self, filePath, ext):
		print 'Processing ' + filePath

		file = open(filePath, 'r')
		jsonData = json.load(file)

		top = xml.etree.ElementTree.Element('plist')
		top.set('version', '1.0')
		self.parseObject(top, jsonData)

		path, orgExt = os.path.splitext(filePath)
		tree = xml.etree.ElementTree.ElementTree(top)
		tree.write(path + '.' + ext, encoding='UTF-8')

	#
	# Parse each object
	def parseObject(self, parent, obj):
		if isinstance(obj, dict):
			self.parseDict(parent, obj)
		elif isinstance(obj, list):
			self.parseList(parent, obj)
		elif isinstance(obj, unicode):
			self.parseUnicode(parent, obj)
		elif isinstance(obj, int) or isinstance(obj, long):
			self.parseInteger(parent, obj)
		elif isinstance(obj, float):
			self.parseFloat(parent, obj)
		elif isinstance(obj, bool):
			self.parseBool(parent, obj)
		else:
			raise ValueError

	#
	# Parse dict
	def parseDict(self, parent, obj):
		child = xml.etree.ElementTree.SubElement(parent, 'dict')
		for item in obj.items():
			grandchild = xml.etree.ElementTree.SubElement(child, 'key')
			grandchild.text = item[0]

			self.parseObject(child, item[1])

	#
	# Parse list
	def parseList(self, parent, obj):
		child = xml.etree.ElementTree.SubElement(parent, 'array')
		for item in obj:
			self.parseObject(child, item)

	#
	# Parse unicode
	def parseUnicode(self, parent, obj):
		child = xml.etree.ElementTree.SubElement(parent, 'date' if JsonToPlist.ISO8601_PATTERN.match(obj) else 'string')
		child.text = obj
	#
	# Parse int or long
	def parseInteger(self, parent, obj):
		child = xml.etree.ElementTree.SubElement(parent, 'integer')
		child.text = str(obj)

	#
	# Parse float
	def parseFloat(self, parent, obj):
		child = xml.etree.ElementTree.SubElement(parent, 'real')
		child.text = str(obj)

	# Parse bool
	def parseBool(self, parent, obj):
		parent.SubElement('true' if obj else 'false')


jsonToPlist = JsonToPlist()
jsonToPlist.main()
