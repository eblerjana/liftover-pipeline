import sys

for line in sys.stdin:
	if line.startswith('#'):
		continue
	fields = line.strip().split()
	chromosome = fields[0]
	start = int(fields[1]) -1
	end = start + 1 #start + len(fields[3])

	print("\t".join([chromosome, str(start), str(end), fields[2]]))	
