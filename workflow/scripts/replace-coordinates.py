import sys

lifted_coordinates = sys.argv[1]
id_to_coord = {}

for line in open(lifted_coordinates, 'r'):
	fields = line.strip().split()
	id_to_coord[fields[3]] = (fields[0], fields[1])

coordinates_present = 0
total = 0

for line in sys.stdin:
	if line.startswith('#'):
		print(line.strip())
		continue
	fields = line.strip().split()
	var_id = fields[2]
	total += 1
	if var_id in id_to_coord:
		assert id_to_coord[var_id][0] == fields[0]
		coordinates_present += 1
		fields[1] = str(int(id_to_coord[var_id][1]) + 1)
#		fields[3] = "N"
#		fields[4] = "N"
		print("\t".join(fields))

sys.stderr.write("Records written: " + str(coordinates_present))
sys.stderr.write("Total input records: " + str(total))	
