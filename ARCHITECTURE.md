# RasaUtilityTools Architecture Documentation

## System Overview

RasaUtilityTools is an automated FAQ chatbot deployment system that maintains synchronized content between a Rasa-based chatbot and support website. The system solves the common problem of content drift by establishing a single source of truth for FAQ data, eliminating manual maintenance across multiple systems.

### Core Purpose
- **Single Source of Truth**: Maintain all FAQ content in one master file (`newfaq.md`)
- **Dual Output Generation**: Automatically generate both Rasa training data and web FAQ content
- **Automated Deployment**: CI/CD pipeline for seamless chatbot model updates and website synchronization
- **Content Consistency**: Ensure chatbot responses match website FAQ content

## Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   newfaq.md     │───▶│  Processing      │───▶│  Dual Outputs   │
│ (Single Source) │    │  Scripts         │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │                         │
                              ▼                         ▼
                    ┌──────────────────┐    ┌─────────────────┐
                    │ chatscript*.py   │    │ 1. Rasa Files  │
                    │ - Standalone     │    │ 2. Web Content │
                    │ - Jenkins        │    └─────────────────┘
                    │ - Core           │
                    └──────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │ CI/CD Pipeline   │
                    │ (Jenkins)        │
                    └──────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │ Deployment       │
                    │ - Rasa X         │
                    │ - Website PR     │
                    └──────────────────┘
```

## Core Components

### 1. Content Processing Layer

**Primary Components:**
- `chatscriptStandalone.py` - Interactive local development script
- `chatscriptJenkins.py` - Automated CI/CD execution script  
- `chatscript.py` - Core processing logic (used by Jenkins)

**Processing Workflow:**
1. Parse `newfaq.md` line by line
2. Extract structured data (questions, intents, answers, alternatives)
3. Generate Rasa training files (`data/nlu.md`, `data/stories.md`, `domain.yml`)
4. Create web FAQ content (`faq.mdx`)
5. Implement duplicate detection to prevent content duplication

### 2. Rasa Integration Layer

**Configuration Files:**
- `config.yml` - Rasa pipeline configuration with TEDPolicy and DIETClassifier
- `domain.yml` - Bot domain definition with intents, responses, and actions
- `data/nlu.md` - Natural Language Understanding training data
- `data/stories.md` - Conversation flow definitions
- `actions.py` - Custom action framework (template provided)

**Model Management:**
- `rasatrain.py` - Automated model training with versioning
- `rasaUpload.py` - Rasa X integration for model deployment
- Model versioning using Jenkins build numbers

### 3. CI/CD Automation Layer

**Jenkins Pipeline (`jenkinsfile`):**
- Conda environment setup with Python 3.7 and Rasa 1.10.x
- Automated FAQ processing and model training
- Rasa X model upload and activation
- GitHub integration with automated PR creation
- Website FAQ synchronization

**Integration Points:**
- GitHub webhook triggers for `newfaq.md` changes
- Rasa X API for model deployment
- Support website repository for FAQ updates

## Technology Stack

### Core Technologies
- **Python 3.7** - Primary development language
- **Rasa 1.10.x** - Conversational AI framework
- **Jenkins** - CI/CD automation platform
- **Conda** - Environment and dependency management

### Key Dependencies
- **pandas 1.2.1** - Data processing
- **tensorflow 2.1.1** - Machine learning backend
- **rasa-sdk 1.10.2** - Custom actions framework
- **requests 2.24.0** - HTTP client for API integration

### Pipeline Components
- **TEDPolicy** - Transformer-based dialogue policy (100 epochs, max_history: 5)
- **DIETClassifier** - Intent classification and entity extraction (100 epochs)
- **FormPolicy** - Conversational form handling
- **FallbackPolicy** - Fallback handling with configurable thresholds

## Data Flow Architecture

### Input Processing
```
newfaq.md
├── ### <question>          → faq.mdx + data/nlu.md
├── intent: <intent_name>    → domain.yml + data/stories.md
├── answer: <response>       → domain.yml (responses) + faq.mdx
└── altquestion: <variant>   → data/nlu.md (training examples)
```

### Output Generation
```
Rasa Training Data:
├── data/nlu.md       - Intent examples and entity annotations
├── data/stories.md   - Conversation flows with action sequences
└── domain.yml        - Intents, responses, and action definitions

Web Content:
└── faq.mdx          - Formatted FAQ content for website integration
```

### Model Deployment Flow
```
1. rasatrain.py      → Generate versioned model (models/{version}.tar.gz)
2. Jenkins upload    → Deploy to Rasa X via API
3. rasaUpload.py     → Activate as production model
4. GitHub PR         → Update website FAQ content
```

## Scalability Considerations

### Content Management
- **Append-only Processing**: Scripts use file appending with duplicate detection
- **Incremental Updates**: Only new content is added, existing content preserved
- **Version Control**: All changes tracked through Git workflow

### Performance Optimization
- **Efficient File Processing**: Line-by-line parsing minimizes memory usage
- **Conditional Updates**: Content only added if not already present
- **Parallel Processing**: Jenkins pipeline stages can run concurrently where possible

### Extensibility Points
- **Custom Actions**: Framework provided in `actions.py` for complex logic
- **Channel Integration**: Multiple messaging platforms supported via `credentials.yml`
- **Storage Backends**: Configurable tracker stores (Redis, MongoDB) via `endpoints.yml`

## Security Architecture

### Authentication Management
- **Jenkins Credentials**: Secure storage of GitHub and Rasa X credentials
- **API Token Management**: Automated token refresh for Rasa X integration
- **Repository Access**: HTTPS authentication for GitHub operations

### Data Protection
- **Credential Isolation**: Sensitive data stored in Jenkins credential store
- **API Security**: Bearer token authentication for Rasa X API calls
- **Network Security**: HTTPS/TLS for all external communications

## Monitoring and Observability

### Build Monitoring
- **Jenkins Build Status**: Automated success/failure notifications
- **Model Training Metrics**: Rasa training logs and performance metrics
- **Deployment Verification**: Automated checks for successful model activation

### Error Handling
- **Graceful Degradation**: Scripts continue processing on non-critical errors
- **Rollback Capability**: Previous models remain available in Rasa X
- **Audit Trail**: Complete Git history of all FAQ changes and deployments
