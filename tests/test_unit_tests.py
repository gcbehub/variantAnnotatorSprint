import sys
from pathlib import Path
from unittest.mock import patch

import pytest

# Add the parent directory (project root) to sys.path using pathlib
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

import variantAnnotator
from variantAnnotator import resources, main

from resources import var
from main import validate_genome_build

def test_validate_genome_build_valid():
    assert validate_genome_build("GRCh37") == "GRCh37"
    assert validate_genome_build("GRCh38") == "GRCh38"

def test_validate_genome_build_invalid():
    with pytest.raises(ValueError):
        validate_genome_build("GRCh36")

@patch('resources.variantValidator_rest.validate_variant_refseq')
def test_validate_variant_refseq(mock_validate):
    mock_response = {'variant': 'mocked_response'}
    mock_validate.return_value = mock_response
    result = variantValidator_rest.validate_variant_refseq('NM_000088.3:c.589G>T', 'GRCh38')
    assert result == mock_response

@patch('resources.variantValidator_rest.validate_variant_ensembl')
def test_validate_variant_ensembl(mock_validate):
    mock_response = {'variant': 'mocked_response'}
    mock_validate.return_value = mock_response
    result = variantValidator_rest.validate_variant_ensembl('ENST00000367770.8:c.123A>T', 'GRCh38')
    assert result == mock_response

@patch('resources.vep_rest.query_ensembl_variant_grch38')
def test_query_ensembl_variant_grch38(mock_query):
    mock_response = {'annotation': 'mocked_annotation'}
    mock_query.return_value = mock_response
    result = vep_rest.query_ensembl_variant_grch38('NC_000017.11:g.50198002C>A')
    assert result == mock_response

@patch('resources.vep_rest.query_ensembl_variant_grch37')
def test_query_ensembl_variant_grch37(mock_query):
    mock_response = {'annotation': 'mocked_annotation'}
    mock_query.return_value = mock_response
    result = vep_rest.query_ensembl_variant_grch37('NC_000017.10:g.41276045C>T')
    assert result == mock_response