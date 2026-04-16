import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict, Any, Optional
import logging
import os
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self, persist_directory: str = None):
        """Initialize ChromaDB with sentence-transformers embeddings"""
        self.persist_directory = persist_directory or os.getenv('CHROMA_PERSIST_DIRECTORY', './chroma_db')
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(path=self.persist_directory)
        
        # Initialize sentence transformer model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="medical_documents",
            metadata={"description": "Medical research documents and clinical trials"}
        )
        
        logger.info(f"Vector store initialized with {self.collection.count()} documents")
    
    def add_documents(self, documents: List[Dict[str, Any]]) -> List[str]:
        """
        Add documents to vector store
        
        Args:
            documents: List of document dictionaries
            
        Returns:
            List of document IDs that were added
        """
        if not documents:
            return []
        
        added_ids = []
        
        try:
            # Prepare documents for embedding
            texts_to_embed = []
            metadatas = []
            ids = []
            
            for doc in documents:
                # Create unique ID
                doc_id = doc.get('id', '')
                if not doc_id:
                    doc_id = str(uuid.uuid4())
                
                # Create text for embedding (title + abstract + key terms)
                text_parts = []
                
                # Title (most important)
                title = doc.get('title', '')
                if title:
                    text_parts.append(title)
                
                # Abstract
                abstract = doc.get('abstract', '')
                if abstract:
                    # Truncate very long abstracts
                    if len(abstract) > 1000:
                        abstract = abstract[:1000] + "..."
                    text_parts.append(abstract)
                
                # Keywords/conditions for clinical trials
                if doc.get('type') == 'clinical_trial':
                    conditions = doc.get('conditions', [])
                    if conditions:
                        text_parts.append(' '.join(conditions))
                    
                    interventions = doc.get('interventions', [])
                    if interventions:
                        text_parts.append(' '.join(interventions))
                else:
                    # For publications, add keywords
                    keywords = doc.get('keywords', [])
                    if keywords:
                        text_parts.append(' '.join(keywords[:10]))  # Limit keywords
                
                # Combine text
                combined_text = ' '.join(text_parts)
                
                if combined_text.strip():
                    texts_to_embed.append(combined_text)
                    
                    # Prepare metadata
                    metadata = {
                        'id': doc_id,
                        'title': title[:200],  # Limit title length
                        'authors': ', '.join(doc.get('authors', [])[:5]),  # Limit authors
                        'journal': doc.get('journal', '')[:100],
                        'year': str(doc.get('year', 0)),
                        'source': doc.get('source', 'unknown'),
                        'type': doc.get('type', 'publication'),
                        'doi': doc.get('doi', ''),
                        'pmid': doc.get('pmid', ''),
                        'url': doc.get('url', ''),
                        'added_date': datetime.now().isoformat()
                    }
                    
                    # Add type-specific metadata
                    if doc.get('type') == 'clinical_trial':
                        metadata.update({
                            'nct_id': doc.get('nct_id', ''),
                            'status': doc.get('status', ''),
                            'phase': doc.get('phase', ''),
                            'conditions': ', '.join(doc.get('conditions', [])),
                            'location': doc.get('location', ''),
                            'sponsor': doc.get('sponsor', '')
                        })
                    
                    metadatas.append(metadata)
                    ids.append(doc_id)
                    added_ids.append(doc_id)
            
            if not texts_to_embed:
                logger.warning("No valid texts to embed")
                return []
            
            # Generate embeddings
            logger.info(f"Generating embeddings for {len(texts_to_embed)} documents...")
            embeddings = self.model.encode(texts_to_embed, show_progress_bar=False)
            
            # Add to collection in batches
            batch_size = 100
            for i in range(0, len(texts_to_embed), batch_size):
                batch_texts = texts_to_embed[i:i+batch_size]
                batch_embeddings = embeddings[i:i+batch_size]
                batch_metadatas = metadatas[i:i+batch_size]
                batch_ids = ids[i:i+batch_size]
                
                self.collection.add(
                    embeddings=batch_embeddings.tolist(),
                    metadatas=batch_metadatas,
                    ids=batch_ids
                )
            
            logger.info(f"Successfully added {len(added_ids)} documents to vector store")
            return added_ids
            
        except Exception as e:
            logger.error(f"Error adding documents to vector store: {str(e)}")
            return []
    
    def search(self, query: str, k: int = 20, filter_dict: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Search for similar documents
        
        Args:
            query: Search query
            k: Number of results to return
            filter_dict: Optional filters for metadata
            
        Returns:
            List of similar documents with scores
        """
        try:
            # Generate query embedding
            query_embedding = self.model.encode([query])
            
            # Prepare search parameters
            search_params = {
                'query_embeddings': query_embedding.tolist(),
                'n_results': k
            }
            
            # Add filters if provided
            if filter_dict:
                search_params['where'] = filter_dict
            
            # Search collection
            results = self.collection.query(**search_params)
            
            # Format results
            documents = []
            if results['ids'] and results['ids'][0]:
                for i in range(len(results['ids'][0])):
                    doc_id = results['ids'][0][i]
                    metadata = results['metadatas'][0][i] if results['metadatas'] and results['metadatas'][0] else {}
                    distance = results['distances'][0][i] if results['distances'] and results['distances'][0] else 0
                    
                    # Convert distance to similarity score (ChromaDB uses L2 distance)
                    similarity_score = 1 / (1 + distance)
                    
                    document = {
                        'id': doc_id,
                        'similarity_score': similarity_score,
                        'distance': distance,
                        **metadata
                    }
                    
                    documents.append(document)
            
            logger.info(f"Found {len(documents)} similar documents for query: {query[:50]}...")
            return documents
            
        except Exception as e:
            logger.error(f"Error searching vector store: {str(e)}")
            return []
    
    def get_document_by_id(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific document by ID"""
        try:
            results = self.collection.get(ids=[doc_id])
            
            if results['ids'] and results['ids'][0]:
                metadata = results['metadatas'][0] if results['metadatas'] else {}
                return {
                    'id': doc_id,
                    **metadata
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting document {doc_id}: {str(e)}")
            return None
    
    def update_document(self, doc_id: str, metadata: Dict[str, Any]) -> bool:
        """Update document metadata"""
        try:
            self.collection.update(
                ids=[doc_id],
                metadatas=[metadata]
            )
            return True
            
        except Exception as e:
            logger.error(f"Error updating document {doc_id}: {str(e)}")
            return False
    
    def delete_documents(self, doc_ids: List[str]) -> bool:
        """Delete documents from vector store"""
        try:
            self.collection.delete(ids=doc_ids)
            logger.info(f"Deleted {len(doc_ids)} documents from vector store")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting documents: {str(e)}")
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Get vector store statistics"""
        try:
            count = self.collection.count()
            
            # Get sample of documents to analyze
            sample_results = self.collection.get(limit=100)
            
            source_counts = {}
            type_counts = {}
            year_distribution = {}
            
            if sample_results['metadatas']:
                for metadata in sample_results['metadatas']:
                    source = metadata.get('source', 'unknown')
                    doc_type = metadata.get('type', 'unknown')
                    year = metadata.get('year', '0')
                    
                    source_counts[source] = source_counts.get(source, 0) + 1
                    type_counts[doc_type] = type_counts.get(doc_type, 0) + 1
                    year_distribution[year] = year_distribution.get(year, 0) + 1
            
            return {
                'total_documents': count,
                'sample_source_distribution': source_counts,
                'sample_type_distribution': type_counts,
                'sample_year_distribution': year_distribution,
                'collection_name': self.collection.name
            }
            
        except Exception as e:
            logger.error(f"Error getting vector store stats: {str(e)}")
            return {}
    
    def clear_collection(self) -> bool:
        """Clear all documents from the collection"""
        try:
            # Delete all documents
            all_docs = self.collection.get()
            if all_docs['ids']:
                self.collection.delete(ids=all_docs['ids'])
            
            logger.info("Cleared all documents from vector store")
            return True
            
        except Exception as e:
            logger.error(f"Error clearing vector store: {str(e)}")
            return False

# Test function
def test_vector_store():
    """Test vector store functionality"""
    store = VectorStore()
    
    # Test documents
    test_docs = [
        {
            'id': 'test1',
            'title': 'Deep Brain Stimulation for Parkinson Disease',
            'abstract': 'A clinical trial examining the effectiveness of deep brain stimulation in treating Parkinson disease symptoms.',
            'authors': ['Dr. Smith', 'Dr. Johnson'],
            'journal': 'Neurology Journal',
            'year': 2023,
            'source': 'pubmed',
            'type': 'publication',
            'doi': '10.1234/test',
            'keywords': ['Parkinson', 'deep brain stimulation', 'clinical trial']
        },
        {
            'id': 'test2',
            'title': 'Novel Treatment for Alzheimer Disease',
            'abstract': 'Research on new therapeutic approaches for Alzheimer disease treatment.',
            'authors': ['Dr. Brown'],
            'journal': 'Medical Research',
            'year': 2022,
            'source': 'openalex',
            'type': 'publication',
            'keywords': ['Alzheimer', 'treatment', 'therapy']
        }
    ]
    
    # Add documents
    added_ids = store.add_documents(test_docs)
    print(f"Added {len(added_ids)} documents")
    
    # Search
    results = store.search("Parkinson disease treatment", k=5)
    print(f"Search results: {len(results)} documents found")
    
    for i, result in enumerate(results[:2]):
        print(f"\n{i+1}. {result.get('title', 'No title')}")
        print(f"   Similarity: {result.get('similarity_score', 0):.3f}")
        print(f"   Source: {result.get('source', 'unknown')}")
    
    # Get stats
    stats = store.get_stats()
    print(f"\nVector store stats: {stats}")

if __name__ == "__main__":
    test_vector_store()
