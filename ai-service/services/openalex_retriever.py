import requests
import json
from typing import List, Dict, Any, Optional
import time
import logging
from urllib.parse import quote

logger = logging.getLogger(__name__)

class OpenAlexRetriever:
    def __init__(self):
        self.base_url = "https://api.openalex.org"
        self.per_page = 50  # OpenAlex max per page
        
    def retrieve(self, query: str, disease: str = "", max_results: int = 150) -> List[Dict[str, Any]]:
        """
        Retrieve documents from OpenAlex
        
        Args:
            query: Search query
            disease: Primary disease/condition for filtering
            max_results: Maximum number of results to retrieve
            
        Returns:
            List of standardized document dictionaries
        """
        try:
            # Build OpenAlex query
            openalex_query = self.build_openalex_query(query, disease)
            
            # Calculate number of pages needed
            pages_needed = (max_results + self.per_page - 1) // self.per_page
            
            all_works = []
            
            for page in range(1, pages_needed + 1):
                logger.info(f"Fetching OpenAlex page {page}/{pages_needed}")
                
                works = self.fetch_works_page(openalex_query, page)
                all_works.extend(works)
                
                if len(all_works) >= max_results:
                    break
                
                # Rate limiting
                time.sleep(0.1)
            
            # Limit to max_results
            all_works = all_works[:max_results]
            
            # Standardize format
            standardized_docs = []
            for work in all_works:
                doc = self.standardize_openalex_work(work)
                if doc:
                    standardized_docs.append(doc)
            
            logger.info(f"Successfully retrieved {len(standardized_docs)} documents from OpenAlex")
            return standardized_docs
            
        except Exception as e:
            logger.error(f"Error retrieving from OpenAlex: {str(e)}")
            return []
    
    def build_openalex_query(self, query: str, disease: str = "") -> str:
        """Build OpenAlex search query"""
        # Clean and prepare query
        query_terms = []
        
        # Add disease if provided
        if disease:
            query_terms.append(disease)
        
        # Add main query terms (remove PubMed-specific syntax)
        clean_query = self.clean_query_for_openalex(query)
        if clean_query:
            query_terms.append(clean_query)
        
        # Combine terms
        if query_terms:
            return ' '.join(query_terms)
        else:
            return "medical research"  # Fallback
    
    def clean_query_for_openalex(self, query: str) -> str:
        """Clean PubMed-specific syntax for OpenAlex"""
        # Remove field tags like [TI], [AB], etc.
        cleaned = re.sub(r'\[TI\]|\[AB\]|\[AU\]|\[MH\]|\[PT\]|\[PDAT\]', '', query)
        
        # Remove boolean operators (OpenAlex uses different syntax)
        cleaned = re.sub(r'\bAND\b|\bOR\b|\bNOT\b', '', cleaned, flags=re.IGNORECASE)
        
        # Remove quotes and clean up
        cleaned = cleaned.replace('"', '').replace('(', '').replace(')', '')
        
        # Remove extra whitespace
        cleaned = ' '.join(cleaned.split())
        
        return cleaned
    
    def fetch_works_page(self, query: str, page: int = 1) -> List[Dict[str, Any]]:
        """Fetch a single page of works from OpenAlex"""
        url = f"{self.base_url}/works"
        
        params = {
            'search': query,
            'filter': 'type:journal-article',  # Only journal articles
            'select': 'id,title,abstract,authorships,primary_location,publication_year,doi,concepts,open_access',
            'per-page': self.per_page,
            'page': page,
            'sort': 'relevance_score:desc'
        }
        
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            works = data.get('results', [])
            
            return works
            
        except requests.RequestException as e:
            logger.error(f"Error fetching OpenAlex page {page}: {str(e)}")
            return []
    
    def standardize_openalex_work(self, work: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Standardize OpenAlex work to common format"""
        try:
            # Basic info
            work_id = work.get('id', '').split('/')[-1]  # Extract ID from URL
            title = work.get('title', '')
            
            # Abstract
            abstract = work.get('abstract', '')
            if abstract and len(abstract) > 2000:
                abstract = abstract[:2000] + "..."  # Truncate very long abstracts
            
            # Authors
            authors = []
            authorships = work.get('authorships', [])
            for authorship in authorships[:10]:  # Limit to first 10 authors
                author = authorship.get('author', {})
                display_name = author.get('display_name', '')
                if display_name:
                    authors.append(display_name)
            
            # Journal/Source
            journal = ''
            primary_location = work.get('primary_location', {})
            source = primary_location.get('source', {})
            if source:
                journal = source.get('display_name', '')
            
            # Publication year
            year = work.get('publication_year', 0)
            
            # DOI
            doi = work.get('doi', '')
            
            # Concepts (keywords)
            concepts = work.get('concepts', [])
            keywords = []
            for concept in concepts[:10]:  # Limit to top 10 concepts
                concept_name = concept.get('display_name', '')
                if concept_name:
                    keywords.append(concept_name)
            
            # Open access info
            open_access = work.get('open_access', {})
            is_oa = open_access.get('is_oa', False)
            oa_url = open_access.get('oa_url', '')
            
            # URL
            url = work.get('id', '')
            
            # Relevance score (OpenAlex provides this)
            relevance_score = work.get('relevance_score', 0.0)
            
            return {
                'id': work_id,
                'title': title,
                'abstract': abstract,
                'authors': authors,
                'journal': journal,
                'year': year,
                'doi': doi,
                'pmid': '',  # OpenAlex doesn't provide PMID
                'source': 'openalex',
                'type': 'publication',
                'url': url,
                'keywords': keywords,
                'open_access': is_oa,
                'oa_url': oa_url,
                'concepts': concepts,
                'relevance_score': relevance_score
            }
            
        except Exception as e:
            logger.error(f"Error standardizing OpenAlex work: {str(e)}")
            return None

# Test function
def test_openalex_retriever():
    """Test OpenAlex retriever"""
    retriever = OpenAlexRetriever()
    
    test_query = "Parkinson disease treatment"
    test_disease = "Parkinson disease"
    
    documents = retriever.retrieve(test_query, test_disease, max_results=20)
    
    print(f"Retrieved {len(documents)} documents from OpenAlex")
    
    for i, doc in enumerate(documents[:3]):
        print(f"\n{i+1}. {doc.get('title', 'No title')}")
        print(f"   Authors: {', '.join(doc.get('authors', [])[:2])}")
        print(f"   Journal: {doc.get('journal', 'Unknown')}")
        print(f"   Year: {doc.get('year', 'Unknown')}")
        print(f"   Open Access: {doc.get('open_access', False)}")

if __name__ == "__main__":
    import re
    test_openalex_retriever()
