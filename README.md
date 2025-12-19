# Liftover Pipeline

Snakemake pipeline to lift a VCF file from one reference build to another given a chain file.

## How to run

Provide paths to the VCF file to be lifted, a chain file, the source reference FASTA, the target reference FASTA as well as a name to be used for the output folder in the ``config/config.yaml`` file:

```
vcf: "<path/to/variants.vcf.gz>"
chain: "<path/to/chain.gz>"
reference: "<path/to/source.fa>"
target_reference: "<path/to/target.fa>"
outname: "results"
```
Then, run the pipeline:

```
snakemake --use-conda -j <nr_threads>
```

## Results

There are two VCFs generated:

``<outname>/<outname>_liftover.vcf.gz``: Contains all variants from the input file that could be lifted, with only the position (POS) changed. REF, ALT and all other fields are left unchanged. This will likely cause some inconsistencies of the REF field with the sequence of the reference genome lifted to.

``<outname>/<outname>_liftover_fixedREF.vcf.gz``: Like ``<outname>/<outname>_liftover.vcf.gz``, but reference alleles (REF) were changed to match target reference. Variants are tagged with one of three possible tags in the INFO field:

* ``ALLELESWITCH``: If the respective target sequence at the lifted position matches the source ALT, REF and ALT were switched.
* ``REFCHANGED``: In all other cases where the target sequence does not match the source REF at the lifted position, REF was set to the respective sequence observed in target reference at the lifted position, while ALT is left unchanged.
* ``MATCH``: If target REF Sequence matches the source REF sequence, nothing is changed.
