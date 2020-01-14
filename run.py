import subprocess
import argparse

def makeBlocks(outputLines):
	blocks = []
	last = -1

	for count, line in enumerate(outputLines):

		if len(line) == 0:
			if( last != count+1 ):
				blocks.append(outputLines[last+1:count])
			last = count

	# Remove empty blocks
	blocks = filter(lambda a: a != [], blocks)

	# Perform some cleaning
	newBlocks = []
	for i,block in enumerate(blocks):
		newBlocks.append([])
		for s in block:
			field = s.split(':')[0].strip()
			value = "".join(s.split(':')[1:]).strip()


			inserted = False
			for i2,x in enumerate(newBlocks[i]):
				if( field in x ):
					newBlocks[i][i2][field] += " " + value
					inserted = True

			if not inserted:
				newBlocks[i].append({field:value})

	return newBlocks

def findBlock(blocks, searchField, searchValue):
	for block in blocks:
		fieldValue = findValue(block, searchField)

		if( fieldValue == searchValue ):
			return block

	return None

def findValue(block, searchField):
	for x in block:
		if( searchField in x ):
			return x[searchField]
	
	return None


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--domains', nargs='+', help='A list of domains (space separated) that you wish to query', required=True)
	parser.add_argument('--sections', nargs='+', help='A list of sections (space separated) that you wish to pull from. Must be in the format (eg: contact=technical)', required=True)
	parser.add_argument('--fields', nargs='+', help='A list of fields (space separated) within the sections that you wish to output.', required=True)
	args = parser.parse_args()

	# Output the headings
	print("\t".join(args.fields))

	for domainName in args.domains:
		proc = subprocess.Popen(["whois %s" % domainName], stdout=subprocess.PIPE, shell=True)
		(out, err) = proc.communicate()

		if err is not None:
			print("Failed to run whois command, are you sure you have it installed?")
			exit(1)

		out = out.splitlines()

		# Clean the output (decode)
		out = [x.decode("utf-8") for x in out]

		# Clean the output (remove comments)
		out = [x for x in out if (len(x) > 0 and (x[0] != "#" and x[0] != "%") or len(x) == 0)]

		# Trim content
		out = [x.strip() for x in out]

		# Turn it into block arrays
		blocks = makeBlocks(out)

		for section in args.sections:
			field,value = section.split('=')
			
			block = findBlock(blocks, field, value)

			if( block is None ):
				print("Failed to find block with %s" % section)
				exit(2)

			values = []
			for argField in args.fields:
				values.append(findValue(block, argField))

			print("\t".join(values))