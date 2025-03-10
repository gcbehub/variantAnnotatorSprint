from resources import variantValidator_rest, vep_rest

def validate_genome_build(build):
    valid_builds = ['GRCh37', 'GRCh38']
    if build not in valid_builds:
        raise ValueError(f"Invalid genome build. Choose from {valid_builds}.")
    return build

def main():
    variant = input("Enter HGVS compliant c. variant description (e.g., NM_000088.3:c.589G>T): ")
    genome_build = input("Enter genome build (GRCh37 or GRCh38): ")

    try:
        genome_build = validate_genome_build(genome_build)
    except ValueError as e:
        print(e)
        return

    print(f"Variant Description: {variant}")
    print(f"Genome Build: {genome_build}")

    if "ENST" not in variant:
        validation = variantValidator_rest.validate_variant_refseq(variant, genome_build)
    else:
        validation = variantValidator_rest.validate_variant_ensembl(variant, genome_build)
    print(validation)

    if "GRCh38" in genome_build:
        annotation = vep_rest.query_ensembl_variant_grch38(validation[variant]["primary_assembly_loci"]["grch38"]
                                                           ["hgvs_genomic_description"])
    else:
        annotation = vep_rest.query_ensembl_variant_grch37(validation[variant]["primary_assembly_loci"]["grch37"]
                                                           ["hgvs_genomic_description"])

    print(annotation)

if __name__ == '__main__':
    main()