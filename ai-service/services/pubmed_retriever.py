import requests
import xml.etree.ElementTree as ET
from typing import List, Dict, Any, Optional
import time
import logging
from urllib.parse import quote, urlencode
import re

logger = logging.getLogger(__name__)

class PubMedRetriever:
    def __init__(self):
        self.base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
        self.tool = "ai_medical_research_assistant"
        self.email = "research@example.com"  # Should be configured
        
    def retrieve(self, query: str, max_results: int = 100) -> List[Dict[str, Any]]:
        """
        Retrieve documents from PubMed
        
        Args:
            query: Search query (already expanded with boolean operators)
            max_results: Maximum number of results to retrieve
            
        Returns:
            List of standardized document dictionaries
        """
        try:
            # Step 1: Search for article IDs
            pmids = self.search_pmids(query, max_results)
            logger.info(f"Found {len(pmids)} PMIDs for query: {query[:50]}...")
            
            if not pmids:
                return []
            
            # Step 2: Fetch article details
            articles = self.fetch_article_details(pmids)
            logger.info(f"Successfully fetched details for {len(articles)} articles")
            
            # Step 3: Standardize format
            standardized_docs = []
            for article in articles:
                doc = self.standardize_pubmed_article(article)
                if doc:
                    standardized_docs.append(doc)
            
            return standardized_docs
            
        except Exception as e:
            logger.error(f"Error retrieving from PubMed: {str(e)}")
            return []
    
    def search_pmids(self, query: str, max_results: int) -> List[str]:
        """Search PubMed and return PMIDs"""
        search_url = f"{self.base_url}/esearch.fcgi"
        
        params = {
            'db': 'pubmed',
            'term': query,
            'retmode': 'json',
            'retmax': max_results,
            'tool': self.tool,
            'email': self.email,
            'sort': 'relevance',
            'datetype': 'pdat',  # Publication date
            'reldate': 3650      # Last 10 years
        }
        
        try:
            response = requests.get(search_url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            pmids = data.get('esearchresult', {}).get('idlist', [])
            
            return pmids
            
        except requests.RequestException as e:
            logger.error(f"Error searching PubMed: {str(e)}")
            return []
    
    def fetch_article_details(self, pmids: List[str]) -> List[Dict[str, Any]]:
        """Fetch detailed information for given PMIDs"""
        fetch_url = f"{self.base_url}/efetch.fcgi"
        
        # PubMed allows up to 200 PMIDs per request
        batch_size = 200
        all_articles = []
        
        for i in range(0, len(pmids), batch_size):
            batch_pmids = pmids[i:i + batch_size]
            
            params = {
                'db': 'pubmed',
                'id': ','.join(batch_pmids),
                'retmode': 'xml',
                'tool': self.tool,
                'email': self.email
            }
            
            try:
                response = requests.get(fetch_url, params=params, timeout=60)
                response.raise_for_status()
                
                # Parse XML response
                articles = self.parse_pubmed_xml(response.text)
                all_articles.extend(articles)
                
                # Rate limiting - wait between requests
                time.sleep(0.5)
                
            except requests.RequestException as e:
                logger.error(f"Error fetching article details: {str(e)}")
                continue
        
        return all_articles
    
    def parse_pubmed_xml(self, xml_text: str) -> List[Dict[str, Any]]:
        """Parse PubMed XML response"""
        try:
            root = ET.fromstring(xml_text)
            articles = []
            
            for article in root.findall('.//PubmedArticle'):
                article_data = self.extract_article_data(article)
                if article_data:
                    articles.append(article_data)
            
            return articles
            
        except ET.ParseError as e:
            logger.error(f"Error parsing PubMed XML: {str(e)}")
            return []
    
    def extract_article_data(self, article_elem) -> Optional[Dict[str, Any]]:
        """Extract data from a single PubMed article element"""
        try:
            # PMID
            pmid_elem = article_elem.find('.//PMID')
            pmid = pmid_elem.text if pmid_elem is not None else ''
            
            # Title
            title_elem = article_elem.find('.//ArticleTitle')
            title = title_elem.text if title_elem is not None else ''
            title = self.clean_text(title)
            
            # Abstract
            abstract_elem = article_elem.find('.//AbstractText')
            abstract = abstract_elem.text if abstract_elem is not None else ''
            abstract = self.clean_text(abstract)
            
            # Authors
            authors = []
            author_list = article_elem.findall('.//Author')
            for author in author_list[:10]:  # Limit to first 10 authors
                last_name = author.find('.//LastName')
                fore_name = author.find('.//ForeName')
                if last_name is not None and fore_name is not None:
                    authors.append(f"{fore_name.text} {last_name.text}")
                elif last_name is not None:
                    authors.append(last_name.text)
            
            # Journal
            journal_elem = article_elem.find('.//Journal/Title')
            journal = journal_elem.text if journal_elem is not None else ''
            
            # Publication date
            pub_date = self.extract_publication_date(article_elem)
            year = pub_date.get('year', 0)
            
            # DOI
            doi = ''
            article_ids = article_elem.findall('.//ArticleId')
            for aid in article_ids:
                if aid.get('IdType') == 'doi':
                    doi = aid.text
                    break
            
            # Publication type
            pub_types = []
            pub_type_elems = article_elem.findall('.//PublicationType')
            for pt in pub_type_elems:
                if pt.text:
                    pub_types.append(pt.text)
            
            # MeSH terms
            mesh_terms = []
            mesh_elems = article_elem.findall('.//DescriptorName')
            for mesh in mesh_elems:
                if mesh.text:
                    mesh_terms.append(mesh.text)
            
            return {
                'pmid': pmid,
                'title': title,
                'abstract': abstract,
                'authors': authors,
                'journal': journal,
                'year': year,
                'doi': doi,
                'publication_types': pub_types,
                'mesh_terms': mesh_terms,
                'publication_date': pub_date
            }
            
        except Exception as e:
            logger.error(f"Error extracting article data: {str(e)}")
            return None
    
    def extract_publication_date(self, article_elem) -> Dict[str, Any]:
        """Extract publication date from article element"""
        pub_date_elem = article_elem.find('.//PubDate')
        
        if pub_date_elem is None:
            return {'year': 0, 'month': 0, 'day': 0}
        
        year_elem = pub_date_elem.find('.//Year')
        month_elem = pub_date_elem.find('.//Month')
        day_elem = pub_date_elem.find('.//Day')
        
        year = int(year_elem.text) if year_elem is not None else 0
        month = int(month_elem.text) if month_elem is not None else 0
        day = int(day_elem.text) if day_elem is not None else 0
        
        return {'year': year, 'month': month, 'day': day}
    
    def clean_text(self, text: str) -> str:
        """Clean text by removing HTML tags and extra whitespace"""
        if not text:
            return ''
        
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def standardize_pubmed_article(self, article: Dict[str, Any]) -> Dict[str, Any]:
        """Standardize PubMed article to common format"""
        return {
            'id': article.get('pmid', ''),
            'title': article.get('title', ''),
            'abstract': article.get('abstract', ''),
            'authors': article.get('authors', []),
            'journal': article.get('journal', ''),
            'year': article.get('year', 0),
            'doi': article.get('doi', ''),
            'pmid': article.get('pmid', ''),
            'source': 'pubmed',
            'type': 'publication',
            'url': f"https://pubmed.ncbi.nlm.nih.gov/{article.get('pmid', '')}",
            'keywords': article.get('mesh_terms', []),
            'publication_types': article.get('publication_types', []),
            'publication_date': article.get('publication_date', {}),
            'relevance_score': 0.0
        }

# Test function
def test_pubmed_retriever():
    """Test PubMed retriever"""
    retriever = PubMedRetriever()
    
    test_query = "Parkinson disease treatment[Title] AND clinical trial[Publication Type]"
    documents = retriever.retrieve(test_query, max_results=10)
    
    print(f"Retrieved {len(documents)} documents from PubMed")
    
    for i, doc in enumerate(documents[:3]):
        print(f"\n{i+1}. {doc.get('title', 'No title')}")
        print(f"   Authors: {', '.join(doc.get('authors', [])[:2])}")
        print(f"   Journal: {doc.get('journal', 'Unknown')}")
        print(f"   Year: {doc.get('year', 'Unknown')}")
        print(f"   PMID: {doc.get('pmid', 'Unknown')}")

if __name__ == "__main__":
    test_pubmed_retriever()
