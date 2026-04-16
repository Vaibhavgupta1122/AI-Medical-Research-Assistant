# AI Medical Research Assistant - Deployment Guide

## Overview

This guide covers deployment options for the AI Medical Research Assistant, a production-ready MERN + Python application.

## Architecture

- **Frontend**: React + Tailwind CSS
- **Backend**: Node.js + Express
- **AI Service**: Python FastAPI
- **Database**: MongoDB Atlas
- **LLM**: Local Ollama (Mistral/Llama3)
- **Vector DB**: ChromaDB
- **External APIs**: PubMed, OpenAlex, ClinicalTrials.gov

## Deployment Options

### 1. Development Setup

**Prerequisites:**
- Node.js 18+
- Python 3.9+
- MongoDB
- Ollama

**Steps:**
```bash
# Clone repository
git clone <repository-url>
cd AI-Medical-Research-Assistant

# Run setup script
chmod +x setup.sh
./setup.sh

# Start Ollama (separate terminal)
ollama pull mistral

# Start services (3 terminals)
cd client && npm start
cd server && npm run dev
cd ai-service && uvicorn main:app --reload --port 8000
```

### 2. Docker Compose (Recommended for Production)

**Prerequisites:**
- Docker & Docker Compose
- Ollama running on host

**Steps:**
```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

**Services:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000
- AI Service: http://localhost:8000
- MongoDB: localhost:27017

### 3. Cloud Deployment

#### Frontend - Vercel

```bash
cd client
npm run build
vercel --prod
```

**Environment Variables:**
- `REACT_APP_API_URL`: Backend API URL

#### Backend & AI Service - Render

1. **Backend Service:**
   - Connect to MongoDB Atlas
   - Set environment variables
   - Deploy via GitHub integration

2. **AI Service:**
   - Deploy as separate service
   - Configure Ollama endpoint
   - Set API keys

**Required Environment Variables:**

**Backend:**
```
NODE_ENV=production
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/db
AI_SERVICE_URL=https://ai-service.onrender.com
JWT_SECRET=your-secret-key
```

**AI Service:**
```
OLLAMA_BASE_URL=http://your-ollama-server:11434
CHROMA_PERSIST_DIRECTORY=./chroma_db
PUBMED_API_KEY=your-pubmed-key
```

### 4. Kubernetes Deployment

**Prerequisites:**
- Kubernetes cluster
- kubectl configured

**Steps:**
```bash
# Apply configurations
kubectl apply -f k8s/
```

**Manifests:**
- `k8s/mongodb.yaml` - MongoDB deployment
- `k8s/backend.yaml` - Node.js API
- `k8s/ai-service.yaml` - Python FastAPI
- `k8s/frontend.yaml` - React app
- `k8s/ingress.yaml` - Load balancer

## Environment Configuration

### MongoDB Atlas Setup

1. Create cluster at [MongoDB Atlas](https://cloud.mongodb.com/)
2. Configure network access
3. Create database user
4. Get connection string

### Ollama Setup

**Local:**
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull models
ollama pull mistral
ollama pull llama3

# Start server
ollama serve
```

**Cloud:**
- Deploy on separate server
- Configure firewall rules
- Set OLLAMA_BASE_URL environment variable

### API Keys

**PubMed (Optional):**
1. Register at [NCBI](https://www.ncbi.nlm.nih.gov/account/)
2. Get API key
3. Set `PUBMED_API_KEY` environment variable

## Security Considerations

### 1. Authentication
- JWT tokens with expiration
- Secure cookie handling
- Rate limiting

### 2. Data Protection
- HTTPS everywhere
- Input validation
- SQL injection prevention
- XSS protection

### 3. API Security
- CORS configuration
- Request rate limiting
- API key management

### 4. Infrastructure
- Regular security updates
- Network segmentation
- Access control

## Monitoring & Logging

### 1. Application Monitoring
```javascript
// Add to backend
const winston = require('winston');
const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' })
  ]
});
```

### 2. Health Checks
- Backend: `/api/health`
- AI Service: `/health`
- Database connectivity

### 3. Performance Monitoring
- Response time tracking
- Error rate monitoring
- Resource usage

## Scaling Considerations

### 1. Horizontal Scaling
- Load balancer for backend instances
- Database connection pooling
- Caching layer (Redis)

### 2. AI Service Scaling
- GPU instances for Ollama
- Model caching
- Batch processing

### 3. Database Scaling
- Read replicas
- Sharding
- Index optimization

## Backup & Recovery

### 1. Database Backups
```bash
# MongoDB backup
mongodump --uri="mongodb://user:pass@host:port/db" --out=/backup/$(date +%Y%m%d)
```

### 2. Vector Database Backups
```bash
# ChromaDB backup
tar -czf chroma_backup_$(date +%Y%m%d).tar.gz ./chroma_db
```

### 3. Application Backups
- Code repository
- Configuration files
- Environment variables

## Troubleshooting

### Common Issues

1. **Ollama Connection**
   - Check OLLAMA_BASE_URL
   - Verify Ollama is running
   - Network connectivity

2. **MongoDB Connection**
   - Verify connection string
   - Check IP whitelist
   - Network access

3. **API Timeouts**
   - Increase timeout values
   - Check service health
   - Monitor resource usage

4. **Memory Issues**
   - Monitor ChromaDB size
   - Optimize embeddings
   - Cache management

### Debug Commands
```bash
# Check service status
docker-compose ps
docker-compose logs <service>

# Test API endpoints
curl http://localhost:5000/api/health
curl http://localhost:8000/health

# Database connectivity
mongosh "mongodb://user:pass@host:port/db"
```

## Performance Optimization

### 1. Frontend
- Code splitting
- Lazy loading
- Image optimization
- Caching strategies

### 2. Backend
- Response caching
- Database indexing
- Connection pooling
- Compression

### 3. AI Service
- Model quantization
- Batch processing
- Result caching
- Parallel processing

## Cost Optimization

### 1. Cloud Resources
- Right-size instances
- Spot instances
- Auto-scaling
- Reserved capacity

### 2. Database
- Storage optimization
- Query optimization
- Connection limits

### 3. Bandwidth
- CDN usage
- Compression
- Caching

## Maintenance

### 1. Regular Tasks
- Security updates
- Log rotation
- Performance monitoring
- Backup verification

### 2. Model Updates
- Retrain embeddings
- Update LLM models
- Refresh vector database

### 3. API Maintenance
- Dependency updates
- Security patches
- Performance tuning

## Support

For deployment issues:
1. Check logs
2. Verify environment variables
3. Test individual services
4. Review documentation
5. Contact support team
