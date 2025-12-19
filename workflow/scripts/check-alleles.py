import sys

def parse_fasta(fastafile):
	chrom_to_sequence = {}
	cur_chrom = None
	sequence = ""
	for line in open(fastafile, 'r'):
		if line.startswith('>'):
			if cur_chrom is not None:
				chrom_to_sequence[cur_chrom] = sequence
			cur_chrom = line.strip().split()[0][1:]
			sequence = ""
			continue
		else:
			sequence += line.strip()
	chrom_to_sequence[cur_chrom] = sequence
	return chrom_to_sequence

fastafile = sys.argv[1]
chrom_to_sequence = parse_fasta(fastafile)

no_match = 0
vars_flipped = 0
total = 0

for line in sys.stdin:
	if line.startswith('##'):
		print(line.strip())
		continue
	if line.startswith('#'):
		print("##INFO=<ID=ALLELESWITCH,Number=0,Type=Flag,Description=\"REF and ALT were switched during liftover.\">")
		print("##INFO=<ID=REFCHANGED,Number=0,Type=Flag,Description=\"REF was changed to match new reference sequence.\">")
		print("##INFO=<ID=MATCH,Number=0,Type=Flag,Description=\"REF matches new reference.\">")
		print(line.strip())
		continue
	fields = line.strip().split()
	ref = fields[3]
	alt = fields[4]
	chrom = fields[0]
	pos = int(fields[1]) - 1
	end = pos + len(ref)

	expected_ref = chrom_to_sequence[chrom][pos : end]
	if expected_ref != ref:
		if expected_ref == alt:
			# REF/ALT are switched. Correct.
			fields[4] = ref
			fields[3] = expected_ref
			fields[7] += ";ALLELESWITCH"
			vars_flipped += 1
		else:
			# replace REF with respective GRCh38 sequence.
			fields[3] = expected_ref
			fields[7] += ";REFCHANGED"
			no_match += 1
	else:
			fields[7] += ";MATCH"
	total += 1
	print('\t'.join(fields))

	if total % 100000 == 0:
		sys.stderr.write("processed " + str(total) + " lines.\n")

sys.stderr.write("Switched REF/ALT: " + str(vars_flipped) + '\n')
sys.stderr.write("No allele matches: " + str(no_match) + '\n')
sys.stderr.write("Total: " + str(total) + '\n')
