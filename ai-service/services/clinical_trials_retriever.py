import requests
import json
from typing import List, Dict, Any, Optional
import time
import logging
from urllib.parse import quote, urlencode
import re

logger = logging.getLogger(__name__)

class ClinicalTrialsRetriever:
    def __init__(self):
        self.base_url = "https://clinicaltrials.gov/api/query"
        self.study_url = "https://clinicaltrials.gov/api/query/full_studies"
        
    def retrieve(self, disease: str, location: Dict[str, Any] = None, max_results: int = 50) -> List[Dict[str, Any]]:
        """
        Retrieve clinical trials from ClinicalTrials.gov
        
        Args:
            disease: Primary disease/condition
            location: User location for filtering
            max_results: Maximum number of results to retrieve
            
        Returns:
            List of standardized clinical trial dictionaries
        """
        if not disease:
            logger.warning("No disease specified for clinical trials search")
            return []
        
        try:
            # Build search query
            search_query = self.build_search_query(disease, location)
            
            # Search for trials
            nct_ids = self.search_trials(search_query, max_results)
            logger.info(f"Found {len(nct_ids)} clinical trials for {disease}")
            
            if not nct_ids:
                return []
            
            # Fetch detailed information for each trial
            trials = []
            for i, nct_id in enumerate(nct_ids):
                if i >= max_results:
                    break
                    
                trial = self.fetch_trial_details(nct_id)
                if trial:
                    standardized = self.standardize_clinical_trial(trial)
                    if standardized:
                        trials.append(standardized)
                
                # Rate limiting
                time.sleep(0.1)
            
            logger.info(f"Successfully retrieved details for {len(trials)} clinical trials")
            return trials
            
        except Exception as e:
            logger.error(f"Error retrieving clinical trials: {str(e)}")
            return []
    
    def build_search_query(self, disease: str, location: Dict[str, Any] = None) -> str:
        """Build search query for clinical trials"""
        query_parts = [disease]
        
        # Add location filters if provided
        if location:
            country = location.get('country', '')
            state = location.get('state', '')
            city = location.get('city', '')
            
            if country:
                query_parts.append(f"LocationCountry:{country}")
            if state:
                query_parts.append(f"LocationState:{state}")
            if city:
                query_parts.append(f"LocationCity:{city}")
        
        # Add filter for recruiting studies (more relevant)
        query_parts.append("RECruiting")
        
        return " AND ".join(query_parts)
    
    def search_trials(self, query: str, max_results: int) -> List[str]:
        """Search for clinical trials and return NCT IDs"""
        params = {
            'expr': query,
            'fmt': 'json',
            'min_rnk': 1,
            'max_rnk': max_results
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            nct_ids = []
            
            studies = data.get('FullStudiesResponse', {}).get('FullStudies', [])
            for study in studies:
                nct_id = study.get('Study', {}).get('ProtocolSection', {}).get('IdentificationModule', {}).get('NCTId', '')
                if nct_id:
                    nct_ids.append(nct_id)
            
            return nct_ids
            
        except requests.RequestException as e:
            logger.error(f"Error searching clinical trials: {str(e)}")
            return []
    
    def fetch_trial_details(self, nct_id: str) -> Optional[Dict[str, Any]]:
        """Fetch detailed information for a specific clinical trial"""
        params = {
            'expr': f"NCTId:{nct_id}",
            'fmt': 'json',
            'min_rnk': 1,
            'max_rnk': 1
        }
        
        try:
            response = requests.get(self.study_url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            studies = data.get('FullStudiesResponse', {}).get('FullStudies', [])
            
            if studies:
                return studies[0].get('Study', {})
            
            return None
            
        except requests.RequestException as e:
            logger.error(f"Error fetching trial details for {nct_id}: {str(e)}")
            return None
    
    def standardize_clinical_trial(self, trial: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Standardize clinical trial to common format"""
        try:
            protocol = trial.get('ProtocolSection', {})
            status_module = protocol.get('StatusModule', {})
            identification_module = protocol.get('IdentificationModule', {})
            description_module = protocol.get('DescriptionModule', {})
            design_module = protocol.get('DesignModule', {})
            arms_interventions_module = protocol.get('ArmsInterventionsModule', {})
            eligibility_module = protocol.get('EligibilityModule', {})
            contacts_locations_module = protocol.get('ContactsLocationsModule', {})
            
            # Basic information
            nct_id = identification_module.get('NCTId', '')
            title = identification_module.get('OfficialTitle', '')
            if not title:
                title = identification_module.get('BriefTitle', '')
            
            # Status
            status = status_module.get('OverallStatus', '')
            phase = design_module.get('PhaseList', [''])[0] if design_module.get('PhaseList') else ''
            study_type = design_module.get('StudyType', '')
            
            # Conditions
            conditions = []
            condition_module = protocol.get('ConditionsModule', {})
            if condition_module:
                conditions = condition_module.get('ConditionList', [])
            
            # Description
            brief_summary = description_module.get('BriefSummary', '')
            detailed_description = description_module.get('DetailedDescription', '')
            description = brief_summary
            if detailed_description and len(detailed_description) > len(brief_summary):
                description = detailed_description
            
            # Sponsor
            sponsor_module = protocol.get('SponsorCollaboratorsModule', {})
            sponsor = sponsor_module.get('LeadSponsor', {}).get('LeadSponsorName', '')
            
            # Dates
            start_date = status_module.get('StartDateStruct', {}).get('StartDate', '')
            completion_date = status_module.get('CompletionDateStruct', {}).get('CompletionDate', '')
            primary_completion_date = status_module.get('PrimaryCompletionDateStruct', {}).get('PrimaryCompletionDate', '')
            
            # Enrollment
            enrollment_module = protocol.get('DesignModule', {}).get('EnrollmentInfoModule', {})
            enrollment = enrollment_module.get('EnrollmentCount', 0)
            
            # Interventions
            interventions = []
            if arms_interventions_module:
                arms = arms_interventions_module.get('ArmGroupList', [])
                for arm in arms:
                    intervention_list = arm.get('InterventionList', [])
                    for intervention in intervention_list:
                        intervention_name = intervention.get('Name', '')
                        intervention_type = intervention.get('InterventionType', '')
                        if intervention_name:
                            interventions.append(f"{intervention_type}: {intervention_name}")
            
            # Eligibility
            eligibility_criteria = eligibility_module.get('EligibilityCriteria', '')
            gender = eligibility_module.get('Sex', '')
            min_age = eligibility_module.get('MinimumAge', '')
            max_age = eligibility_module.get('MaximumAge', '')
            healthy_volunteers = eligibility_module.get('HealthyVolunteers', '')
            
            # Locations and contacts
            locations = []
            contacts = []
            
            if contacts_locations_module:
                location_list = contacts_locations_module.get('LocationsList', [])
                for location_item in location_list:
                    location_module = location_item.get('LocationModule', {})
                    facility = location_module.get('Facility', '')
                    city = location_module.get('LocationCity', '')
                    state = location_module.get('LocationState', '')
                    country = location_module.get('LocationCountry', '')
                    status = location_module.get('LocationStatus', '')
                    
                    if facility or city or state or country:
                        location_full = ', '.join(filter(None, [facility, city, state, country]))
                        locations.append({
                            'facility': facility,
                            'city': city,
                            'state': state,
                            'country': country,
                            'status': status,
                            'full_location': location_full
                        })
                
                # Central contacts
                central_contacts = contacts_locations_module.get('CentralContactsList', [])
                for contact in central_contacts:
                    contact_module = contact.get('CentralContactModule', {})
                    name = contact_module.get('CentralContactName', '')
                    role = contact_module.get('CentralContactRole', '')
                    phone = contact_module.get('CentralContactPhone', '')
                    email = contact_module.get('CentralContactEMail', '')
                    
                    if name or phone or email:
                        contacts.append({
                            'name': name,
                            'role': role,
                            'phone': phone,
                            'email': email
                        })
            
            return {
                'id': nct_id,
                'nct_id': nct_id,
                'title': title,
                'status': status,
                'phase': phase,
                'study_type': study_type,
                'conditions': conditions,
                'description': description,
                'brief_summary': brief_summary,
                'detailed_description': detailed_description,
                'sponsor': sponsor,
                'start_date': start_date,
                'completion_date': completion_date,
                'primary_completion_date': primary_completion_date,
                'enrollment': enrollment,
                'interventions': interventions,
                'eligibility': eligibility_criteria,
                'gender': gender,
                'min_age': min_age,
                'max_age': max_age,
                'healthy_volunteers': healthy_volunteers,
                'locations': locations,
                'contacts': contacts,
                'source': 'clinical_trials',
                'type': 'clinical_trial',
                'url': f"https://clinicaltrials.gov/study/{nct_id}",
                'relevance_score': 0.0
            }
            
        except Exception as e:
            logger.error(f"Error standardizing clinical trial: {str(e)}")
            return None

# Test function
def test_clinical_trials_retriever():
    """Test ClinicalTrials.gov retriever"""
    retriever = ClinicalTrialsRetriever()
    
    test_disease = "Parkinson disease"
    test_location = {"country": "United States", "state": "California"}
    
    trials = retriever.retrieve(test_disease, test_location, max_results=10)
    
    print(f"Retrieved {len(trials)} clinical trials")
    
    for i, trial in enumerate(trials[:3]):
        print(f"\n{i+1}. {trial.get('title', 'No title')}")
        print(f"   NCT ID: {trial.get('nct_id', 'Unknown')}")
        print(f"   Status: {trial.get('status', 'Unknown')}")
        print(f"   Phase: {trial.get('phase', 'Unknown')}")
        print(f"   Conditions: {', '.join(trial.get('conditions', []))}")
        print(f"   Locations: {len(trial.get('locations', []))}")

if __name__ == "__main__":
    test_clinical_trials_retriever()
