import logging
import requests
import json
from pathlib import Path
from resources import variantValidator_rest, vep_rest
import os

log_dir = '/Users/ganeshkumarv/gcbehub/variantAnnotatorSprint/variantAnnotator/logs/'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Set up logging
current_directory = str(Path(__file__).resolve().parent)
logging.basicConfig(level=logging.DEBUG,  # Changed to DEBUG for more detailed logs
                    format="%(asctime)s [%(levelname)s] %(message)s",
                    handlers=[logging.FileHandler(f"{current_directory}/logs/va.log"),
                              logging.StreamHandler()])

def validate_genome_build(build):
    valid_builds = ['GRCh37', 'GRCh38']
    if build not in valid_builds:
        raise ValueError(f"Invalid genome build. Choose from {valid_builds}.")
    return build

def fetch_genomic_hgvs(variant, genome_build):
    """
    This function uses the VariantValidator API to fetch genomic HGVS for a given variant.
    Returns the genomic HGVS in a dictionary with keys 'grch37' and 'grch38'.
    """
    if "ENST" not in variant:
        validation = variantValidator_rest.validate_variant_refseq(variant, genome_build)
    else:
        validation = variantValidator_rest.validate_variant_ensembl(variant, genome_build)

    genomic_hgvs = {}
    try:
        if "GRCh38" in genome_build:
            genomic_hgvs['grch38'] = validation[variant]["primary_assembly_loci"]["grch38"]["hgvs_genomic_description"]
        elif "GRCh37" in genome_build:
            genomic_hgvs['grch37'] = validation[variant]["primary_assembly_loci"]["grch37"]["hgvs_genomic_description"]
        else:
            logging.error(f"Unknown genome build: {genome_build}")
            raise ValueError(f"Invalid genome build: {genome_build}")
    except KeyError as e:
        logging.error(f"Error extracting genomic HGVS: {e}")
        raise ValueError(f"Invalid response format for variant: {variant}")

    return genomic_hgvs

def get_vep_annotations(genomic_hgvs, genome_build, variant):
    """
    This function uses the VEP API to fetch annotations for the given genomic HGVS.
    Returns a dictionary with annotations including REVEL and SPICE AI scores.
    """

    # To Use the correct HGVS based on the genome build
    genomic_description = genomic_hgvs.get('grch38') if "GRCh38" in genome_build else genomic_hgvs.get('grch37')

    if not genomic_description:
        logging.error(f"No valid genomic HGVS found for the selected genome build: {genome_build}")
        return {}

    # Log the URL and parameters for debugging
    logging.debug(f"Querying VEP with genomic HGVS: {genomic_description}")

    # VEP query for the appropriate genome build
    try:
        if "GRCh38" in genome_build:
            annotations_url = vep_rest.query_ensembl_variant_grch38(genomic_description)
        elif "GRCh37" in genome_build:
            annotations_url = vep_rest.query_ensembl_variant_grch37(genomic_description)
        else:
            logging.error(f"Unknown genome build: {genome_build}")
            return {}

        headers = {"Content-Type": "application/json"}
        response = requests.get(annotations_url, params={"hgvs": genomic_description}, headers=headers)

        if response.status_code == 200:
            annotations = response.json()
            # Extract REVEL and SPICE AI scores from annotations
            revel_score = annotations.get("REVEL_score", None)
            spice_ai_score = annotations.get("SPICE_AI_score", None)

            # Log the scores for debugging purposes
            logging.info(f"REVEL score: {revel_score}")
            logging.info(f"SPICE AI score: {spice_ai_score}")

            return {
                "genomic_hgvs": genomic_description,
                "revel_score": revel_score,
                "spice_ai_score": spice_ai_score
            }
        else:
            logging.error(f"Error fetching VEP annotations: {response.status_code} - {response.text}")
            return {}
    except requests.exceptions.RequestException as e:
        logging.error(f"Request to VEP API failed: {e}")
        return {}

def main():
    variant = input("Enter HGVS compliant c. variant description (e.g., NM_000088.3:c.589G>T): ")
    genome_build = input("Enter genome build (GRCh37 or GRCh38): ")

    try:
        genome_build = validate_genome_build(genome_build)
    except ValueError as e:
        logging.error(e)
        return

    logging.info(f"Variant Description: {variant}")
    logging.info(f"Genome Build: {genome_build}")

    try:
        genomic_hgvs = fetch_genomic_hgvs(variant, genome_build)
    except Exception as e:
        logging.error(f"Error fetching genomic HGVS: {e}")
        return

    # Get VEP annotations
    annotations = get_vep_annotations(genomic_hgvs, genome_build, variant)

    # Add gene symbol and gene ID from VariantValidator or other sources
    gene_symbol = annotations.get("gene_symbol", "N/A")
    gene_id = annotations.get("gene_id", "N/A")

    # Create the dictionary with all the gathered data, including REVEL and SPICE AI scores
    result = {
        "variant": variant,
        "genome_build": genome_build,
        "genomic_hgvs": genomic_hgvs,
        "annotations": annotations,
        "gene_symbol": gene_symbol,
        "gene_id": gene_id,
        "revel_score": annotations.get("revel_score", "N/A"),  # Include REVEL score
        "spice_ai_score": annotations.get("spice_ai_score", "N/A")  # Include SPICE AI score
    }

    # Output the result as a JSON string
    print(json.dumps(result, indent=4))


if __name__ == '__main__':
    main()
