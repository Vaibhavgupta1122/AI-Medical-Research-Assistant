import requests
import xml.etree.ElementTree as ET
from typing import List, Dict, Any, Optional
import time
import logging
from urllib.parse import quote, urlencode
import json

from .pubmed_retriever import PubMedRetriever
from .openalex_retriever import OpenAlexRetriever
from .clinical_trials_retriever import ClinicalTrialsRetriever

logger = logging.getLogger(__name__)

def retrieve_documents(query: str, disease: str = "", location: Dict[str, Any] = None, max_docs: int = 200) -> List[Dict[str, Any]]:
    """
    Retrieve documents from multiple sources (PubMed, OpenAlex, ClinicalTrials.gov)
    
    Args:
        query: Expanded research query
        disease: Primary disease/condition
        location: User location for clinical trials
        max_docs: Maximum total documents to retrieve
    
    Returns:
        Combined list of documents from all sources
    """
    location = location or {}
    
    # Initialize retrievers
    pubmed_retriever = PubMedRetriever()
    openalex_retriever = OpenAlexRetriever()
    clinical_trials_retriever = ClinicalTrialsRetriever()
    
    all_documents = []
    
    try:
        # 1. Retrieve from PubMed (target 100 documents)
        logger.info("Retrieving from PubMed...")
        pubmed_docs = pubmed_retriever.retrieve(query, max_results=100)
        all_documents.extend(pubmed_docs)
        logger.info(f"Retrieved {len(pubmed_docs)} documents from PubMed")
        
        # 2. Retrieve from OpenAlex (target 150 documents)
        logger.info("Retrieving from OpenAlex...")
        openalex_docs = openalex_retriever.retrieve(query, disease, max_results=150)
        all_documents.extend(openalex_docs)
        logger.info(f"Retrieved {len(openalex_docs)} documents from OpenAlex")
        
        # 3. Retrieve from ClinicalTrials.gov (target 50 trials)
        logger.info("Retrieving from ClinicalTrials.gov...")
        trial_docs = clinical_trials_retriever.retrieve(disease, location, max_results=50)
        all_documents.extend(trial_docs)
        logger.info(f"Retrieved {len(trial_docs)} clinical trials")
        
        # 4. Remove duplicates based on DOI/PMID
        logger.info("Removing duplicates...")
        unique_documents = remove_duplicates(all_documents)
        
        # 5. Limit to max_docs
        if len(unique_documents) > max_docs:
            unique_documents = unique_documents[:max_docs]
        
        logger.info(f"Total unique documents retrieved: {len(unique_documents)}")
        return unique_documents
        
    except Exception as e:
        logger.error(f"Error in document retrieval: {str(e)}")
        return []

def remove_duplicates(documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Remove duplicate documents based on DOI, PMID, or title similarity"""
    seen_ids = set()
    seen_titles = set()
    unique_docs = []
    
    for doc in documents:
        # Check for DOI
        doi = doc.get('doi', '').lower().strip()
        if doi and doi in seen_ids:
            continue
        
        # Check for PMID
        pmid = doc.get('pmid', '').lower().strip()
        if pmid and pmid in seen_ids:
            continue
            
        # Check for NCT ID (clinical trials)
        nct_id = doc.get('nct_id', '').lower().strip()
        if nct_id and nct_id in seen_ids:
            continue
        
        # Check for title similarity
        title = doc.get('title', '').lower().strip()
        if title in seen_titles:
            continue
        
        # Add to unique documents
        unique_docs.append(doc)
        
        # Mark as seen
        if doi:
            seen_ids.add(doi)
        if pmid:
            seen_ids.add(pmid)
        if nct_id:
            seen_ids.add(nct_id)
        if title:
            seen_titles.add(title)
    
    return unique_docs

def standardize_document(doc: Dict[str, Any], source: str) -> Dict[str, Any]:
    """Standardize document format across different sources"""
    standardized = {
        'id': doc.get('id', ''),
        'title': doc.get('title', ''),
        'abstract': doc.get('abstract', ''),
        'authors': doc.get('authors', []),
        'journal': doc.get('journal', ''),
        'year': doc.get('year', 0),
        'doi': doc.get('doi', ''),
        'pmid': doc.get('pmid', ''),
        'source': source,
        'type': doc.get('type', 'publication'),
        'url': doc.get('url', ''),
        'keywords': doc.get('keywords', []),
        'publication_date': doc.get('publication_date', ''),
        'relevance_score': 0.0  # Will be calculated later
    }
    
    # Add source-specific fields
    if source == 'clinical_trials':
        standardized.update({
            'nct_id': doc.get('nct_id', ''),
            'status': doc.get('status', ''),
            'phase': doc.get('phase', ''),
            'conditions': doc.get('conditions', []),
            'location': doc.get('location', ''),
            'eligibility': doc.get('eligibility', ''),
            'contacts': doc.get('contacts', []),
            'sponsor': doc.get('sponsor', ''),
            'start_date': doc.get('start_date', ''),
            'completion_date': doc.get('completion_date', '')
        })
    
    return standardized

# Test function
def test_retrieval():
    """Test the retrieval functionality"""
    test_query = "Parkinson disease treatment"
    test_disease = "Parkinson disease"
    test_location = {"country": "United States", "state": "California"}
    
    documents = retrieve_documents(test_query, test_disease, test_location, max_docs=50)
    
    print(f"Retrieved {len(documents)} documents")
    
    # Count by source
    source_counts = {}
    for doc in documents:
        source = doc.get('source', 'unknown')
        source_counts[source] = source_counts.get(source, 0) + 1
    
    print("Documents by source:")
    for source, count in source_counts.items():
        print(f"  {source}: {count}")
    
    # Show sample documents
    print("\nSample documents:")
    for i, doc in enumerate(documents[:3]):
        print(f"\n{i+1}. {doc.get('title', 'No title')}")
        print(f"   Source: {doc.get('source', 'unknown')}")
        print(f"   Year: {doc.get('year', 'unknown')}")
        print(f"   Authors: {', '.join(doc.get('authors', [])[:3])}")

if __name__ == "__main__":
    test_retrieval()
