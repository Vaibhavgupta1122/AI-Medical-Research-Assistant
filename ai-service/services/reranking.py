import numpy as np
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)

class DocumentReranker:
    def __init__(self):
        """Initialize the reranking engine"""
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2),
            lowercase=True
        )
        
        # Source credibility weights
        self.source_weights = {
            'pubmed': 1.0,
            'openalex': 0.9,
            'clinical_trials': 0.95
        }
        
        # Publication type weights
        self.pub_type_weights = {
            'clinical_trial': 1.1,
            'randomized_controlled_trial': 1.2,
            'meta_analysis': 1.15,
            'systematic_review': 1.15,
            'review': 0.9,
            'case_report': 0.8
        }
        
        # Recency boost parameters
        self.recency_half_life = 5.0  # years
        self.max_recency_boost = 0.3
        
    def rerank_documents(self, query: str, documents: List[Dict[str, Any]], 
                        context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Rerank documents based on multiple factors
        
        Args:
            query: Original user query
            documents: List of documents with similarity scores
            context: User context (location, demographics, etc.)
            
        Returns:
            Reranked list of documents
        """
        if not documents:
            return []
        
        logger.info(f"Reranking {len(documents)} documents")
        
        # Calculate reranking scores for each document
        reranked_docs = []
        for doc in documents:
            score = self.calculate_rerank_score(doc, query, context)
            doc['rerank_score'] = score
            reranked_docs.append(doc)
        
        # Sort by rerank score (descending)
        reranked_docs.sort(key=lambda x: x['rerank_score'], reverse=True)
        
        logger.info(f"Reranking completed. Top document: {reranked_docs[0].get('title', 'Unknown')}")
        return reranked_docs
    
    def calculate_rerank_score(self, doc: Dict[str, Any], query: str, 
                            context: Dict[str, Any] = None) -> float:
        """
        Calculate comprehensive reranking score for a document
        
        Args:
            doc: Document dictionary
            query: Search query
            context: User context
            
        Returns:
            Reranking score (0-1, higher is better)
        """
        base_score = 0.0
        
        # 1. Semantic similarity score (from vector search)
        semantic_score = doc.get('similarity_score', 0.0)
        base_score += semantic_score * 0.4  # 40% weight
        
        # 2. Source credibility
        source = doc.get('source', 'unknown')
        source_weight = self.source_weights.get(source, 0.8)
        base_score += source_weight * 0.15  # 15% weight
        
        # 3. Recency boost
        recency_score = self.calculate_recency_score(doc)
        base_score += recency_score * 0.15  # 15% weight
        
        # 4. Publication type boost
        pub_type_score = self.calculate_pub_type_score(doc)
        base_score += pub_type_score * 0.1  # 10% weight
        
        # 5. Text relevance (TF-IDF)
        text_relevance_score = self.calculate_text_relevance(doc, query)
        base_score += text_relevance_score * 0.1  # 10% weight
        
        # 6. Context relevance
        context_score = self.calculate_context_relevance(doc, context)
        base_score += context_score * 0.1  # 10% weight
        
        # Ensure score is between 0 and 1
        final_score = min(max(base_score, 0.0), 1.0)
        
        return final_score
    
    def calculate_recency_score(self, doc: Dict[str, Any]) -> float:
        """Calculate recency score based on publication year"""
        year = doc.get('year', 0)
        if not year or year < 1900:
            return 0.0
        
        current_year = datetime.now().year
        years_old = current_year - year
        
        # Exponential decay based on half-life
        recency_score = np.exp(-np.log(2) * years_old / self.recency_half_life)
        
        # Apply maximum boost
        return min(recency_score, self.max_recency_boost)
    
    def calculate_pub_type_score(self, doc: Dict[str, Any]) -> float:
        """Calculate publication type score"""
        if doc.get('type') == 'clinical_trial':
            # Clinical trials get automatic boost
            status = doc.get('status', '').lower()
            if status in ['recruiting', 'active', 'enrolling']:
                return 0.2  # Higher boost for active trials
            else:
                return 0.1
        
        # For publications, check publication types
        pub_types = doc.get('publication_types', [])
        if not pub_types:
            return 0.0
        
        max_score = 0.0
        for pub_type in pub_types:
            pub_type_lower = pub_type.lower()
            score = self.pub_type_weights.get(pub_type_lower, 0.0)
            max_score = max(max_score, score)
        
        return max_score * 0.1  # Scale down to 0-0.2 range
    
    def calculate_text_relevance(self, doc: Dict[str, Any], query: str) -> float:
        """Calculate text relevance using TF-IDF"""
        try:
            # Combine title and abstract for text analysis
            title = doc.get('title', '')
            abstract = doc.get('abstract', '')
            
            if not title and not abstract:
                return 0.0
            
            # Create document text
            doc_text = f"{title} {abstract}"
            
            # Simple keyword matching score
            query_terms = re.findall(r'\b\w+\b', query.lower())
            doc_terms = re.findall(r'\b\w+\b', doc_text.lower())
            
            if not query_terms:
                return 0.0
            
            # Calculate term overlap
            query_set = set(query_terms)
            doc_set = set(doc_terms)
            
            overlap = len(query_set.intersection(doc_set))
            coverage = overlap / len(query_set) if query_terms else 0.0
            
            return min(coverage * 2, 1.0)  # Scale to 0-1 range
            
        except Exception as e:
            logger.error(f"Error calculating text relevance: {str(e)}")
            return 0.0
    
    def calculate_context_relevance(self, doc: Dict[str, Any], 
                                 context: Dict[str, Any] = None) -> float:
        """Calculate context relevance score"""
        if not context:
            return 0.0
        
        score = 0.0
        
        # Location relevance for clinical trials
        if doc.get('type') == 'clinical_trial':
            location_score = self.calculate_location_relevance(doc, context)
            score += location_score * 0.5
        
        # Condition relevance
        condition_score = self.calculate_condition_relevance(doc, context)
        score += condition_score * 0.3
        
        # Demographic relevance
        demographic_score = self.calculate_demographic_relevance(doc, context)
        score += demographic_score * 0.2
        
        return min(score, 0.3)  # Cap at 0.3
    
    def calculate_location_relevance(self, doc: Dict[str, Any], 
                                   context: Dict[str, Any]) -> float:
        """Calculate location relevance for clinical trials"""
        user_location = context.get('location', {})
        if not user_location:
            return 0.0
        
        trial_locations = doc.get('locations', [])
        if not trial_locations:
            return 0.0
        
        user_country = user_location.get('country', '').lower()
        user_state = user_location.get('state', '').lower()
        user_city = user_location.get('city', '').lower()
        
        max_score = 0.0
        
        for location in trial_locations:
            location_score = 0.0
            
            trial_country = location.get('country', '').lower()
            trial_state = location.get('state', '').lower()
            trial_city = location.get('city', '').lower()
            
            # Country match
            if user_country and trial_country and user_country in trial_country:
                location_score += 0.3
            
            # State match
            if user_state and trial_state and user_state in trial_state:
                location_score += 0.4
            
            # City match
            if user_city and trial_city and user_city in trial_city:
                location_score += 0.3
            
            max_score = max(max_score, location_score)
        
        return max_score
    
    def calculate_condition_relevance(self, doc: Dict[str, Any], 
                                    context: Dict[str, Any]) -> float:
        """Calculate condition relevance"""
        primary_condition = context.get('primaryCondition', '').lower()
        secondary_conditions = [c.lower() for c in context.get('secondaryConditions', [])]
        
        if not primary_condition:
            return 0.0
        
        score = 0.0
        
        # Check title
        title = doc.get('title', '').lower()
        if primary_condition in title:
            score += 0.4
        
        # Check abstract/description
        text = doc.get('abstract', '') or doc.get('description', '')
        text_lower = text.lower()
        if primary_condition in text_lower:
            score += 0.3
        
        # Check conditions list (for clinical trials)
        conditions = [c.lower() for c in doc.get('conditions', [])]
        if primary_condition in conditions:
            score += 0.5
        
        # Check secondary conditions
        for condition in secondary_conditions:
            if condition in title or condition in text_lower or condition in conditions:
                score += 0.1
        
        return min(score, 0.5)
    
    def calculate_demographic_relevance(self, doc: Dict[str, Any], 
                                      context: Dict[str, Any]) -> float:
        """Calculate demographic relevance"""
        demographics = context.get('demographicInfo', {})
        if not demographics:
            return 0.0
        
        score = 0.0
        
        # Age relevance for clinical trials
        if doc.get('type') == 'clinical_trial':
            age_score = self.calculate_age_relevance(doc, demographics)
            score += age_score * 0.5
            
            gender_score = self.calculate_gender_relevance(doc, demographics)
            score += gender_score * 0.5
        
        return min(score, 0.2)
    
    def calculate_age_relevance(self, doc: Dict[str, Any], 
                              demographics: Dict[str, Any]) -> float:
        """Calculate age relevance for clinical trials"""
        user_age = demographics.get('age')
        if not user_age:
            return 0.0
        
        min_age = doc.get('min_age', '')
        max_age = doc.get('max_age', '')
        
        try:
            # Parse age strings
            min_age_num = self.parse_age_string(min_age)
            max_age_num = self.parse_age_string(max_age)
            
            if min_age_num and user_age >= min_age_num:
                return 0.3
            if max_age_num and user_age <= max_age_num:
                return 0.3
            if min_age_num and max_age_num and min_age_num <= user_age <= max_age_num:
                return 0.5
                
        except (ValueError, TypeError):
            pass
        
        return 0.0
    
    def parse_age_string(self, age_str: str) -> Optional[int]:
        """Parse age string to extract numeric age"""
        if not age_str:
            return None
        
        # Extract numbers from age string
        numbers = re.findall(r'\d+', age_str)
        if numbers:
            return int(numbers[0])
        return None
    
    def calculate_gender_relevance(self, doc: Dict[str, Any], 
                                 demographics: Dict[str, Any]) -> float:
        """Calculate gender relevance for clinical trials"""
        user_gender = demographics.get('gender', '').lower()
        if not user_gender:
            return 0.0
        
        trial_gender = doc.get('gender', '').lower()
        
        if trial_gender == 'all':
            return 0.2
        elif user_gender in trial_gender:
            return 0.3
        
        return 0.0

def rerank_documents(query: str, documents: List[Dict[str, Any]], 
                    context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
    """
    Convenience function to rerank documents
    
    Args:
        query: Search query
        documents: List of documents
        context: User context
        
    Returns:
        Reranked documents
    """
    reranker = DocumentReranker()
    return reranker.rerank_documents(query, documents, context)

# Test function
def test_reranking():
    """Test the reranking engine"""
    # Sample documents
    documents = [
        {
            'id': 'doc1',
            'title': 'Deep Brain Stimulation for Parkinson Disease',
            'abstract': 'A 2023 clinical trial on deep brain stimulation',
            'authors': ['Dr. Smith'],
            'journal': 'Neurology',
            'year': 2023,
            'source': 'pubmed',
            'type': 'publication',
            'similarity_score': 0.8,
            'publication_types': ['clinical trial']
        },
        {
            'id': 'doc2',
            'title': 'Old Parkinson Study',
            'abstract': 'A 2010 review of Parkinson treatments',
            'authors': ['Dr. Jones'],
            'journal': 'Old Journal',
            'year': 2010,
            'source': 'openalex',
            'type': 'publication',
            'similarity_score': 0.7,
            'publication_types': ['review']
        },
        {
            'id': 'doc3',
            'title': 'Parkinson Clinical Trial',
            'abstract': 'Recruiting trial for new Parkinson medication',
            'authors': ['Dr. Brown'],
            'journal': 'Clinical Research',
            'year': 2024,
            'source': 'clinical_trials',
            'type': 'clinical_trial',
            'similarity_score': 0.6,
            'status': 'recruiting',
            'locations': [{'country': 'United States', 'state': 'California'}]
        }
    ]
    
    # Context
    context = {
        'primaryCondition': 'Parkinson disease',
        'location': {'country': 'United States', 'state': 'California'},
        'demographicInfo': {'age': 65, 'gender': 'male'}
    }
    
    # Rerank
    reranked = rerank_documents("Parkinson disease treatment", documents, context)
    
    print("Reranked documents:")
    for i, doc in enumerate(reranked):
        print(f"{i+1}. {doc.get('title', 'Unknown')} - Score: {doc.get('rerank_score', 0):.3f}")
        print(f"   Source: {doc.get('source', 'unknown')}, Year: {doc.get('year', 'unknown')}")

if __name__ == "__main__":
    test_reranking()
