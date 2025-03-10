import requests

def validate_variant_refseq(variant, genome_build):
    base_url = "https://rest.variantvalidator.org/VariantValidator/variantvalidator"
    url = f"{base_url}/{genome_build}/{variant}/all?content-type=application%2Fjson"

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def validate_variant_ensembl(variant, genome_build):
    base_url = "https://rest.variantvalidator.org/VariantValidator/variantvalidator_ensembl"
    url = f"{base_url}/{genome_build}/{variant}/all?content-type=application%2Fjson"

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None