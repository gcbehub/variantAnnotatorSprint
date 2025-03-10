import requests

def query_ensembl_variant_grch38(variant_description):
    base_url = "https://rest.ensembl.org/vep/human/hgvs"
    url = f"{base_url}/{variant_description}?revel=true;SpliceAI=true;merged=true;content-type=application/json"

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None


def query_ensembl_variant_grch37(variant_description):
    base_url = "https://grch37.rest.ensembl.org/vep/human/hgvs"
    url = f"{base_url}/{variant_description}?revel=true;SpliceAI=true;merged=true;content-type=application/json"

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None