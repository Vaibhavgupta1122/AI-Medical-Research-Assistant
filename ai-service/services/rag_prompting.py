from typing import List, Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def create_research_prompt(query: str, context: List[Dict[str, Any]], 
                          conversation_history: List[Dict[str, Any]] = None,
                          user_context: Dict[str, Any] = None) -> Dict[str, str]:
    """
    Create comprehensive research prompt for RAG
    
    Args:
        query: User's original query
        context: Retrieved documents (publications and clinical trials)
        conversation_history: Previous conversation messages
        user_context: User demographic and medical context
        
    Returns:
        Dictionary with system_prompt and prompt
    """
    # System prompt
    system_prompt = """You are a medical research assistant. Your role is to provide evidence-based medical information by analyzing research papers and clinical trials.

CRITICAL GUIDELINES:
1. NEVER hallucinate or make up information. Only use the provided research context.
2. Always base your answers on the provided publications and clinical trials.
3. If the context doesn't contain relevant information, clearly state this limitation.
4. Cite sources appropriately using the provided reference numbers.
5. Maintain a professional, objective, and helpful tone.
6. Emphasize that this is for informational purposes only and not medical advice.

STRUCTURE YOUR RESPONSE AS FOLLOWS:

## Condition Overview
Brief overview of the condition based on the research context.

## Research Insights
Key findings from the provided publications. Focus on:
- Recent developments and breakthroughs
- Treatment approaches
- Efficacy and safety data
- Mechanisms of action

## Clinical Trials
Summarize relevant clinical trials, including:
- Trial status and phase
- Inclusion criteria
- Location and recruitment status
- Potential benefits/risks

## Personalized Considerations
Tailor information based on user context (age, location, etc.) if relevant.

## Limitations
Clearly state what the research doesn't cover and limitations of available information.

## Sources
List all sources with proper citations.

IMPORTANT: Always include a disclaimer that this information is not medical advice and users should consult healthcare professionals."""

    # Build context sections
    publications_context = format_publications(context)
    clinical_trials_context = format_clinical_trials(context)
    conversation_context = format_conversation_history(conversation_history)
    user_profile_context = format_user_context(user_context)
    
    # Main prompt
    prompt = f"""USER QUERY: {query}

USER CONTEXT:
{user_profile_context}

CONVERSATION HISTORY:
{conversation_context}

RESEARCH CONTEXT - PUBLICATIONS:
{publications_context}

RESEARCH CONTEXT - CLINICAL TRIALS:
{clinical_trials_context}

INSTRUCTIONS:
1. Analyze the provided research context thoroughly
2. Structure your response according to the required format
3. Focus on the most relevant and recent information
4. Provide specific details from the sources
5. Include citations like [Source 1], [Source 2] etc.
6. If information is insufficient, clearly state the limitations
7. Always maintain scientific accuracy and objectivity

Please provide a comprehensive, evidence-based response to the user's query."""

    return {
        'system_prompt': system_prompt,
        'prompt': prompt
    }

def format_publications(context: List[Dict[str, Any]]) -> str:
    """Format publications for the prompt"""
    publications = [doc for doc in context if doc.get('type') == 'publication']
    
    if not publications:
        return "No relevant publications found in the context."
    
    formatted = []
    for i, pub in enumerate(publications[:8], 1):  # Limit to top 8
        title = pub.get('title', 'No title')
        authors = pub.get('authors', [])
        journal = pub.get('journal', 'Unknown journal')
        year = pub.get('year', 'Unknown year')
        abstract = pub.get('abstract', 'No abstract available')
        doi = pub.get('doi', '')
        
        # Format authors (limit to first 3)
        author_str = ', '.join(authors[:3])
        if len(authors) > 3:
            author_str += f' et al. ({len(authors)} authors total)'
        
        pub_text = f"""Source {i}:
Title: {title}
Authors: {author_str}
Journal: {journal} ({year})
DOI: {doi}
Abstract: {abstract}
Relevance Score: {pub.get('rerank_score', 0):.3f}"""
        
        formatted.append(pub_text)
    
    return '\n\n'.join(formatted)

def format_clinical_trials(context: List[Dict[str, Any]]) -> str:
    """Format clinical trials for the prompt"""
    trials = [doc for doc in context if doc.get('type') == 'clinical_trial']
    
    if not trials:
        return "No relevant clinical trials found in the context."
    
    formatted = []
    for i, trial in enumerate(trials[:5], 1):  # Limit to top 5
        title = trial.get('title', 'No title')
        nct_id = trial.get('nct_id', 'Unknown NCT ID')
        status = trial.get('status', 'Unknown status')
        phase = trial.get('phase', 'Unknown phase')
        conditions = trial.get('conditions', [])
        description = trial.get('description', 'No description available')
        locations = trial.get('locations', [])
        eligibility = trial.get('eligibility', 'No eligibility criteria available')
        sponsor = trial.get('sponsor', 'Unknown sponsor')
        
        # Format conditions
        conditions_str = ', '.join(conditions) if conditions else 'Not specified'
        
        # Format locations (limit to first 3)
        location_strs = []
        for loc in locations[:3]:
            loc_parts = [loc.get('city', ''), loc.get('state', ''), loc.get('country', '')]
            loc_str = ', '.join(filter(None, loc_parts))
            if loc_str:
                location_strs.append(loc_str)
        locations_str = '; '.join(location_strs) if location_strs else 'Not specified'
        
        trial_text = f"""Clinical Trial {i}:
Title: {title}
NCT ID: {nct_id}
Status: {status}
Phase: {phase}
Conditions: {conditions_str}
Sponsor: {sponsor}
Description: {description}
Eligibility: {eligibility}
Locations: {locations_str}
Relevance Score: {trial.get('rerank_score', 0):.3f}"""
        
        formatted.append(trial_text)
    
    return '\n\n'.join(formatted)

def format_conversation_history(conversation_history: List[Dict[str, Any]]) -> str:
    """Format conversation history for context"""
    if not conversation_history:
        return "No previous conversation."
    
    # Get last 6 messages (3 exchanges)
    recent_history = conversation_history[-6:]
    
    formatted = []
    for msg in recent_history:
        msg_type = msg.get('type', 'unknown')
        content = msg.get('content', {})
        text = content.get('text', '')
        
        if msg_type == 'user':
            formatted.append(f"User: {text}")
        elif msg_type == 'assistant':
            # Limit assistant responses to key points
            summary = text[:200] + "..." if len(text) > 200 else text
            formatted.append(f"Assistant: {summary}")
    
    return '\n'.join(formatted)

def format_user_context(user_context: Dict[str, Any]) -> str:
    """Format user context for the prompt"""
    if not user_context:
        return "No specific user context provided."
    
    context_parts = []
    
    # Demographics
    demographics = user_context.get('demographicInfo', {})
    if demographics:
        age = demographics.get('age')
        gender = demographics.get('gender')
        
        if age and gender:
            context_parts.append(f"Age: {age}, Gender: {gender}")
        elif age:
            context_parts.append(f"Age: {age}")
        elif gender:
            context_parts.append(f"Gender: {gender}")
    
    # Location
    location = user_context.get('location', {})
    if location:
        location_parts = []
        for field in ['city', 'state', 'country']:
            value = location.get(field)
            if value:
                location_parts.append(value)
        
        if location_parts:
            context_parts.append(f"Location: {', '.join(location_parts)}")
    
    # Medical conditions
    primary_condition = user_context.get('primaryCondition')
    if primary_condition:
        context_parts.append(f"Primary Condition: {primary_condition}")
    
    secondary_conditions = user_context.get('secondaryConditions', [])
    if secondary_conditions:
        context_parts.append(f"Other Conditions: {', '.join(secondary_conditions)}")
    
    # Medications
    medications = user_context.get('medications', [])
    if medications:
        context_parts.append(f"Current Medications: {', '.join(medications)}")
    
    return '\n'.join(context_parts) if context_parts else "No specific user context provided."

def create_followup_prompt(original_query: str, previous_answer: str, 
                          followup_question: str, context: List[Dict[str, Any]]) -> Dict[str, str]:
    """
    Create prompt for follow-up questions
    
    Args:
        original_query: User's original query
        previous_answer: Previous AI response
        followup_question: User's follow-up question
        context: Same research context
        
    Returns:
        Dictionary with system_prompt and prompt
    """
    system_prompt = """You are continuing a conversation about medical research. The user has asked a follow-up question.

GUIDELINES:
1. Reference the previous context and your previous answer
2. Provide additional details or clarification based on the follow-up
3. Maintain consistency with your previous response
4. Use the same structured format as before
5. Focus on addressing the specific follow-up question
6. Continue to cite sources appropriately"""

    prompt = f"""ORIGINAL QUERY: {original_query}

PREVIOUS ANSWER: {previous_answer[:1000]}...

FOLLOW-UP QUESTION: {followup_question}

RESEARCH CONTEXT:
[Same publications and clinical trials as before]

Please provide a detailed response to the follow-up question, building upon your previous answer and the research context."""

    return {
        'system_prompt': system_prompt,
        'prompt': prompt
    }

def extract_key_insights(context: List[Dict[str, Any]]) -> List[str]:
    """Extract key insights from research context"""
    insights = []
    
    # Analyze publications
    publications = [doc for doc in context if doc.get('type') == 'publication']
    if publications:
        # Look for recent publications
        current_year = datetime.now().year
        recent_pubs = [p for p in publications if p.get('year', 0) >= current_year - 3]
        
        if recent_pubs:
            insights.append(f"Found {len(recent_pubs)} recent publications (last 3 years)")
        
        # Look for high-impact journals
        high_impact_journals = ['Nature', 'Science', 'NEJM', 'Lancet', 'JAMA']
        high_impact_pubs = [p for p in publications 
                          if any(journal in p.get('journal', '').lower() 
                               for journal in high_impact_journals)]
        
        if high_impact_pubs:
            insights.append(f"Found {len(high_impact_pubs)} publications in high-impact journals")
    
    # Analyze clinical trials
    trials = [doc for doc in context if doc.get('type') == 'clinical_trial']
    if trials:
        # Look for recruiting trials
        recruiting_trials = [t for t in trials 
                           if t.get('status', '').lower() in ['recruiting', 'active']]
        
        if recruiting_trials:
            insights.append(f"Found {len(recruiting_trials)} actively recruiting clinical trials")
        
        # Look for phase 3 trials
        phase3_trials = [t for t in trials if 'phase 3' in t.get('phase', '').lower()]
        if phase3_trials:
            insights.append(f"Found {len(phase3_trials)} Phase 3 clinical trials")
    
    return insights

# Test function
def test_rag_prompting():
    """Test RAG prompting functionality"""
    # Sample context
    test_context = [
        {
            'type': 'publication',
            'title': 'Deep Brain Stimulation for Parkinson Disease',
            'authors': ['Dr. Smith', 'Dr. Johnson'],
            'journal': 'Neurology',
            'year': 2023,
            'abstract': 'A comprehensive study on DBS effectiveness...',
            'doi': '10.1234/test',
            'rerank_score': 0.85
        },
        {
            'type': 'clinical_trial',
            'title': 'New Parkinson Drug Trial',
            'nct_id': 'NCT123456',
            'status': 'recruiting',
            'phase': 'Phase 2',
            'conditions': ['Parkinson Disease'],
            'description': 'Testing new medication for PD...',
            'locations': [{'city': 'Boston', 'state': 'MA', 'country': 'USA'}],
            'rerank_score': 0.78
        }
    ]
    
    # Sample user context
    test_user_context = {
        'demographicInfo': {'age': 65, 'gender': 'male'},
        'location': {'city': 'Boston', 'state': 'MA', 'country': 'USA'},
        'primaryCondition': 'Parkinson Disease'
    }
    
    # Create prompt
    prompt_data = create_research_prompt(
        query="What are the latest treatments for Parkinson disease?",
        context=test_context,
        user_context=test_user_context
    )
    
    print("System Prompt:")
    print(prompt_data['system_prompt'][:500] + "...")
    print("\nMain Prompt:")
    print(prompt_data['prompt'][:800] + "...")
    
    # Test insights extraction
    insights = extract_key_insights(test_context)
    print(f"\nKey Insights: {insights}")

if __name__ == "__main__":
    test_rag_prompting()
