import re
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class QueryExpander:
    def __init__(self):
        # Medical terms and synonyms
        self.medical_synonyms = {
            'heart attack': ['myocardial infarction', 'cardiac arrest', 'MI'],
            'stroke': ['cerebrovascular accident', 'CVA', 'brain attack'],
            'diabetes': ['diabetes mellitus', 'DM', 'high blood sugar'],
            'cancer': ['malignancy', 'neoplasm', 'tumor', 'carcinoma'],
            'alzheimer': ['alzheimer disease', 'dementia', 'cognitive decline'],
            'parkinson': ['parkinson disease', 'PD', 'movement disorder'],
            'depression': ['major depressive disorder', 'MDD', 'clinical depression'],
            'anxiety': ['anxiety disorder', 'GAD', 'panic disorder'],
            'hypertension': ['high blood pressure', 'HTN', 'elevated blood pressure'],
            'arthritis': ['joint inflammation', 'osteoarthritis', 'rheumatoid arthritis']
        }
        
        # Research intent keywords
        self.research_keywords = {
            'treatment': ['therapy', 'medication', 'drug', 'intervention', 'management'],
            'diagnosis': ['detection', 'screening', 'identification', 'diagnostic'],
            'prevention': ['prevention', 'prophylaxis', 'avoidance', 'risk reduction'],
            'causes': ['etiology', 'pathogenesis', 'risk factors', 'causes'],
            'symptoms': ['clinical presentation', 'manifestations', 'signs'],
            'prognosis': ['outcome', 'survival', 'progression', 'forecast'],
            'clinical_trials': ['clinical study', 'trial', 'research study', 'intervention study']
        }
        
        # Boolean operators for PubMed
        self.boolean_operators = ['AND', 'OR', 'NOT']
        
        # PubMed field tags
        self.pubmed_fields = {
            'title': '[TI]',
            'abstract': '[AB]',
            'author': '[AU]',
            'journal': '[TA]',
            'mesh': '[MH]',
            'publication_type': '[PT]'
        }

def expand_query(disease: str, user_query: str, conversation_history: List[Dict[str, Any]] = None) -> str:
    """
    Expand user query into a comprehensive research query for medical literature search.
    
    Args:
        disease: Primary disease/condition from context
        user_query: Original user query
        conversation_history: Previous conversation for context
    
    Returns:
        Expanded research query with medical terminology and boolean operators
    """
    expander = QueryExpander()
    
    # Clean and normalize input
    user_query = user_query.strip().lower()
    disease = disease.strip().lower() if disease else ""
    
    # Extract key terms from user query
    query_terms = extract_medical_terms(user_query)
    
    # Identify research intent
    intent = identify_research_intent(user_query)
    
    # Build expanded query components
    query_components = []
    
    # 1. Add disease/condition as primary focus
    if disease:
        disease_synonyms = get_synonyms(expander.medical_synonyms, disease)
        if len(disease_synonyms) > 1:
            disease_query = " OR ".join(disease_synonyms)
            query_components.append(f"({disease_query})")
        else:
            query_components.append(disease_synonyms[0])
    
    # 2. Add user query terms
    if query_terms:
        query_components.extend(query_terms)
    
    # 3. Add intent-specific terms
    intent_terms = get_intent_terms(expander.research_keywords, intent)
    if intent_terms:
        intent_query = " OR ".join(intent_terms)
        query_components.append(f"({intent_query})")
    
    # 4. Add clinical trials filter if requested
    if 'clinical trial' in user_query or 'study' in user_query:
        query_components.append("clinical trial[PT]")
    
    # 5. Add recent publication filter (last 5 years)
    if 'recent' in user_query or 'latest' in user_query:
        query_components.append('"2020"[PDAT] : "2025"[PDAT]')
    
    # 6. Add context from conversation history
    context_terms = extract_context_from_history(conversation_history)
    if context_terms:
        query_components.extend(context_terms)
    
    # Build final query with proper boolean logic
    if len(query_components) == 0:
        # Fallback to basic query
        final_query = user_query
    elif len(query_components) == 1:
        final_query = query_components[0]
    else:
        # Combine with AND for specificity, but use OR for synonyms
        final_query = " AND ".join(query_components)
    
    # Add PubMed field tags for precision
    final_query = enhance_with_field_tags(final_query, expander.pubmed_fields)
    
    logger.info(f"Query expansion: '{user_query}' -> '{final_query}'")
    return final_query

def extract_medical_terms(query: str) -> List[str]:
    """Extract medical terms from user query"""
    # Simple keyword extraction - can be enhanced with NLP
    medical_patterns = [
        r'\b(treatment|therapy|drug|medication|intervention)\b',
        r'\b(diagnosis|diagnostic|screening|detection)\b',
        r'\b(prevention|preventive|prophylaxis)\b',
        r'\b(symptoms|clinical|presentation|manifestation)\b',
        r'\b(causes|etiology|risk factors|pathogenesis)\b',
        r'\b(prognosis|outcome|survival|progression)\b',
        r'\b(clinical trial|study|research)\b'
    ]
    
    terms = []
    for pattern in medical_patterns:
        matches = re.findall(pattern, query, re.IGNORECASE)
        terms.extend(matches)
    
    return list(set(terms))  # Remove duplicates

def identify_research_intent(query: str) -> str:
    """Identify the primary research intent from user query"""
    intent_mapping = {
        'treatment': ['treatment', 'therapy', 'drug', 'medication', 'cure', 'manage'],
        'diagnosis': ['diagnosis', 'diagnostic', 'test', 'screening', 'detect', 'identify'],
        'prevention': ['prevent', 'prevention', 'avoid', 'reduce risk', 'prophylaxis'],
        'causes': ['cause', 'etiology', 'risk factor', 'why', 'pathogenesis'],
        'symptoms': ['symptom', 'sign', 'presentation', 'manifestation', 'clinical'],
        'prognosis': ['prognosis', 'outcome', 'survival', 'progress', 'forecast'],
        'clinical_trials': ['clinical trial', 'study', 'research', 'investigation']
    }
    
    query_lower = query.lower()
    
    for intent, keywords in intent_mapping.items():
        for keyword in keywords:
            if keyword in query_lower:
                return intent
    
    return 'general'

def get_synonyms(synonym_dict: Dict[str, List[str]], term: str) -> List[str]:
    """Get synonyms for medical terms"""
    term_lower = term.lower()
    
    for key, synonyms in synonym_dict.items():
        if term_lower in key.lower() or any(term_lower in syn.lower() for syn in synonyms):
            return [key] + synonyms
    
    return [term]  # Return original term if no synonyms found

def get_intent_terms(intent_dict: Dict[str, List[str]], intent: str) -> List[str]:
    """Get terms related to research intent"""
    return intent_dict.get(intent, [])

def extract_context_from_history(conversation_history: List[Dict[str, Any]]) -> List[str]:
    """Extract relevant terms from conversation history"""
    if not conversation_history:
        return []
    
    context_terms = []
    
    # Get last few exchanges for context
    recent_messages = conversation_history[-6:]  # Last 3 exchanges
    
    for message in recent_messages:
        if message.get('type') == 'user':
            content = message.get('content', {}).get('text', '')
            if content:
                # Extract medical terms from history
                terms = extract_medical_terms(content)
                context_terms.extend(terms)
    
    return list(set(context_terms))  # Remove duplicates

def enhance_with_field_tags(query: str, field_tags: Dict[str, str]) -> str:
    """Enhance query with PubMed field tags for better precision"""
    # This is a simplified version - can be enhanced with more sophisticated logic
    enhanced_query = query
    
    # Add title field tag for main concepts
    if not any(tag in enhanced_query for tag in field_tags.values()):
        # If no field tags, add title tag for better precision
        enhanced_query = f"{enhanced_query}[TI]"
    
    return enhanced_query

# Test function
def test_query_expansion():
    """Test the query expansion functionality"""
    test_cases = [
        {
            'disease': 'Parkinson disease',
            'query': 'What are the latest treatments?',
            'expected_intent': 'treatment'
        },
        {
            'disease': 'diabetes',
            'query': 'How to prevent it?',
            'expected_intent': 'prevention'
        },
        {
            'disease': 'cancer',
            'query': 'clinical trials available',
            'expected_intent': 'clinical_trials'
        }
    ]
    
    for case in test_cases:
        expanded = expand_query(case['disease'], case['query'])
        print(f"Original: {case['query']}")
        print(f"Expanded: {expanded}")
        print(f"Intent: {identify_research_intent(case['query'])}")
        print("-" * 50)

if __name__ == "__main__":
    test_query_expansion()
