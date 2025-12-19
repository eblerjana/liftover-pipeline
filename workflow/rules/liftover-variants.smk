

rule prepare_vcf:
	"""
	Make sure header is complete.
	"""
	input:
		vcf = VCF,
		fai = REFERENCE + ".fai"
	output:
		temp("{results}/preprocessed-vcf.vcf.gz")
	conda: 
		"../envs/liftover.yaml"
	shell:
		"""
		bcftools reheader --fai {input.fai} {input.vcf} -o {output}
		tabix -p vcf {output}
		"""


rule vcf_to_bed:
	"""
	Convert VCF to BED format.
	"""
	input:
		"{results}/preprocessed-vcf.vcf.gz"
	output:
		"{results}/preprocessed-vcf.bed"
	resources:
		mem_mb = 10000,
		walltime = "10:00:00"
	shell:
		"""
		zcat {input} | python3 workflow/scripts/vcf-to-bed.py > {output}
		"""

rule liftover:
	"""
	Liftover coordinates.
	"""
	input:
		svs = "{results}/preprocessed-vcf.bed",
		chain = CHAIN
	output:
		liftover = "{results}/variants_liftover.bed",
		unmapped = "{results}/variants_unmapped.bed"
	log:
		"{results}/variants_liftover.log"
	conda:
		"../envs/liftover.yaml"
	resources:
		mem_mb = 50000,
		walltime = "10:00:00"
	shell:
		"""
		liftOver {input.svs} {input.chain} {output.liftover} {output.unmapped} &> {log}
		"""


rule prepare_lifted_vcf:
	"""
	Replace old coordinates by lifted over coordinates.
	"""
	input:
		liftover = "{results}/variants_liftover.bed",
		vcf = "{results}/preprocessed-vcf.vcf.gz"
	output:
		"{results}/{outname}_liftover_unsorted.vcf.gz"
	conda:
		"../envs/liftover.yaml"
	resources:
		mem_mb = 100000,
		walltime = "15:00:00"
	shell:
		"""
		zcat {input.vcf} | python3 workflow/scripts/replace-coordinates.py {input.liftover} | bgzip > {output} 
		"""


rule sort_vcf:
	"""
	Sort the VCF as coordinates might no longer be
	consecutive.
	"""
	input:
		"{results}/{outname}_liftover_unsorted.vcf.gz"
	output:
		"{results}/{outname}_liftover.vcf.gz"
	conda:
		 "../envs/liftover.yaml"
	resources:
		mem_mb = 200000,
		walltime = "10:00:00"
	params:
		temp = "{results}/{outname}-tmp/"
	shell:
		"""
		bcftools sort -o {output} -Oz {input} --temp-dir {params.temp}
		tabix -p vcf {output}
		"""


rule fix_reference_alleles:
	"""
	Fix reference alleles.
	"""
	input:
		vcf = "{results}/{outname}_liftover.vcf.gz",
		ref = TARGET_REFERENCE
	output:
		"{results}/{outname}_liftover_fixedREF.vcf.gz"
	resources:
		mem_mb = 20000,
		walltime = "10:00:00"
	conda:
		"../envs/liftover.yaml"
	shell:
		"""
		zcat {input.vcf} | python3 workflow/scripts/check-alleles.py {input.ref} | bgzip > {output}
		tabix -p vcf {output}
		"""
