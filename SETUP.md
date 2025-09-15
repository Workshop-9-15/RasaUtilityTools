# RasaUtilityTools Setup and Configuration Guide

## System Requirements

### Environment Prerequisites
- **Python 3.7** (Required for Rasa 1.10.x compatibility)
- **Git** (For version control and CI/CD integration)
- **Jenkins** (For automated CI/CD pipeline)
- **Conda/Miniconda** (Recommended for environment management)

### Hardware Requirements
- **Minimum**: 4GB RAM, 2 CPU cores
- **Recommended**: 8GB RAM, 4 CPU cores (for model training)
- **Storage**: 2GB free space for dependencies and models

## Local Development Setup

### 1. Environment Preparation

#### Python Environment Setup
```bash
# Using pyenv (recommended)
pyenv install 3.7.17
pyenv local 3.7.17

# Verify Python version
python --version  # Should show 3.7.x
```

#### Alternative: Conda Environment
```bash
# Create isolated environment
conda create -n rasatools python=3.7
conda activate rasatools
```

### 2. Dependency Installation

#### Install Required Packages
```bash
# Clone repository
git clone <repository-url>
cd RasaUtilityTools

# Install dependencies
pip install -r requirements.txt
```

#### Key Dependencies Verification
```bash
# Verify critical packages
python -c "import rasa; print(f'Rasa version: {rasa.__version__}')"
python -c "import pandas; print(f'Pandas version: {pandas.__version__}')"
python -c "import tensorflow; print(f'TensorFlow version: {tensorflow.__version__}')"
```

### 3. Rasa Configuration

#### Initial Rasa Setup
If starting with a fresh Rasa project:
```bash
# Initialize Rasa project (optional)
rasa init --no-prompt

# Or use existing configuration files
# The repository includes pre-configured files:
# - config.yml
# - domain.yml
# - data/nlu.md
# - data/stories.md
```

#### Configuration Files Overview

**`config.yml` - Rasa Pipeline Configuration**
```yaml
language: en
pipeline:
- name: WhitespaceTokenizer
  case_sensitive: false
- name: RegexFeaturizer
- name: LexicalSyntacticFeaturizer
- name: CountVectorsFeaturizer
- name: CountVectorsFeaturizer
  analyzer: char_wb
  min_ngram: 1
  max_ngram: 4
- name: DIETClassifier
  epochs: 100
- name: EntitySynonymMapper
- name: ResponseSelector
  epochs: 100

policies:
- name: MemoizationPolicy
- name: FormPolicy
- name: TEDPolicy
  max_history: 5
  epochs: 100
- name: FallbackPolicy
  nlu_threshold: 0.5
  core_threshold: 0.2
  fallback_action_name: action_default_fallback
- name: MappingPolicy
```

**Key Configuration Notes:**
- **TEDPolicy**: Transformer-based policy with 100 epochs and max_history of 5
- **DIETClassifier**: Intent classification with 100 training epochs
- **Fallback Thresholds**: NLU (0.5) and Core (0.2) confidence thresholds

### 4. Local Execution

#### Running the Standalone Script
```bash
# Execute FAQ processing
python ./chatscriptStandalone.py

# Follow interactive prompts
Are you working in a Rasa init project? (y/n): y
```

#### Manual Model Training
```bash
# Train Rasa model after FAQ processing
rasa train

# Test the model
rasa shell
```

#### Verify Generated Files
```bash
# Check generated files
ls -la data/          # Should contain nlu.md and stories.md
ls -la faq.mdx        # Web FAQ content
cat domain.yml        # Updated domain configuration
```

## CI/CD Pipeline Setup

### 1. Jenkins Configuration

#### Prerequisites
- Jenkins server with Docker support
- GitHub integration plugin
- Conda/Python environment support

#### Jenkins Credentials Setup
Configure the following credentials in Jenkins:

1. **GitHub Credentials**
   - Credential ID: `<Jenkins credentials username>`
   - Type: Username with password
   - Username: GitHub username
   - Password: GitHub personal access token

2. **Rasa X Credentials** (if using Rasa X)
   - Configure in `rasaUpload.py`
   - Username and password for Rasa X instance

#### Pipeline Configuration

**Jenkinsfile Parameters:**
```groovy
parameters {
    string(name: 'modelname', defaultValue: '<your rasa url>')
}
```

**Environment Variables:**
```groovy
environment {
    BUILD_VERSION = "$currentBuild.number".trim()
    BRANCH = "$BRANCH_NAME"
}
```

### 2. GitHub Integration

#### Webhook Configuration
1. Navigate to GitHub repository settings
2. Add webhook for Jenkins integration
3. Configure payload URL: `<jenkins-url>/github-webhook/`
4. Select "Push" events for automatic triggering

#### Repository Setup
Update `jenkinsfile` with your specific values:

```groovy
// Replace placeholders with actual values
git config --global user.name "<your name>"
git config --global user.email "<your email>"
git clone https://${username}:${password}@github.com/<org>/<repo>.git
```

### 3. Rasa X Integration

#### Rasa X Setup
If using Rasa X for model management:

1. **Install Rasa X**
   ```bash
   pip install rasa-x
   ```

2. **Configure API Access**
   Update `rasaUpload.py` with your Rasa X details:
   ```python
   url = 'https://<rasa-x-route>/api/auth'
   payload = '{"username": "me", "password": "rasaxpassword"}'
   ```

3. **Model Upload Configuration**
   ```python
   url = "https://<rasa-x-route>/api/projects/default/models/" + x + "/tags/production"
   ```

## Configuration Files Reference

### 1. Domain Configuration (`domain.yml`)

#### Structure Overview
```yaml
session_config:
  session_expiration_time: 60
  carry_over_slots_to_new_session: true

intents:
- request_weather
- greet
# FAQ intents added automatically by processing scripts

entities:
- city
# Additional entities can be defined here

slots:
  city:
    type: unfeaturized
# Additional slots for conversation state

responses:
  utter_greet:
  - text: Hi there! How can I help?
  # FAQ responses added automatically as utter_<intent>

actions:
- utter_greet
# FAQ actions added automatically

forms:
- weather_form
# Conversational forms for complex interactions
```

#### Automatic Modifications
The processing scripts automatically modify `domain.yml`:
- Add new intents from `newfaq.md`
- Create `utter_<intent>` responses for each FAQ
- Add response actions to actions list
- Maintain existing configuration structure

### 2. Credentials Configuration (`credentials.yml`)

#### Channel Setup
```yaml
# REST API (default)
rest:
  # No credentials required for basic REST API

# Rasa X Integration
rasa:
  url: "http://localhost:5002/api"

# Optional: Additional channels
# slack:
#   slack_token: "<your slack token>"
#   slack_channel: "<the slack channel>"

# facebook:
#   verify: "<verify>"
#   secret: "<your secret>"
#   page-access-token: "<your page access token>"
```

### 3. Endpoints Configuration (`endpoints.yml`)

#### Service Endpoints
```yaml
# Custom Actions (if using)
# action_endpoint:
#   url: "http://localhost:5055/webhook"

# Tracker Store (for conversation persistence)
# tracker_store:
#   type: redis
#   url: <redis-host>
#   port: 6379
#   db: 0
#   password: <redis-password>

# Event Broker (for conversation events)
# event_broker:
#   url: localhost
#   username: username
#   password: password
#   queue: queue
```

## Environment-Specific Configuration

### Development Environment

#### Local Configuration
```bash
# Set environment variables
export RASA_ENV=development
export RASA_LOG_LEVEL=DEBUG

# Use local endpoints
# endpoints.yml configured for localhost services
```

#### Development Workflow
1. Edit `newfaq.md` with new FAQ content
2. Run `python ./chatscriptStandalone.py`
3. Train model with `rasa train`
4. Test with `rasa shell` or `rasa interactive`

### Production Environment

#### Jenkins Environment Setup
```bash
# Conda environment creation (in jenkinsfile)
conda create -y -q -n chatscript python=3
source activate chatscript

# Production dependencies
pip install --upgrade pip
pip install pandas requests tensorflow rasa
```

#### Production Configuration
- Use production Rasa X instance URLs
- Configure secure credential storage
- Enable monitoring and logging
- Set up backup and recovery procedures

## Troubleshooting

### Common Setup Issues

#### Python Version Conflicts
**Problem**: Rasa installation fails or behaves unexpectedly  
**Solution**: Ensure Python 3.7 is being used
```bash
python --version
which python
```

#### Dependency Conflicts
**Problem**: Package version conflicts during installation  
**Solution**: Use clean virtual environment
```bash
# Create fresh environment
conda create -n rasatools-clean python=3.7
conda activate rasatools-clean
pip install -r requirements.txt
```

#### Permission Issues
**Problem**: File permission errors during processing  
**Solution**: Check file permissions and ownership
```bash
chmod +w domain.yml data/nlu.md data/stories.md
```

### Jenkins Pipeline Issues

#### Build Failures
**Problem**: Jenkins build fails during environment setup  
**Solution**: Verify Jenkins agent has required tools
```bash
# Check available tools on Jenkins agent
which conda
which python
which git
```

#### Git Authentication
**Problem**: Git operations fail in Jenkins  
**Solution**: Verify credentials configuration
```groovy
withCredentials([usernamePassword(credentialsId: '<credential-id>', 
                 passwordVariable: 'password', 
                 usernameVariable: 'username')]) {
    // Git operations
}
```

#### Model Upload Failures
**Problem**: Rasa X model upload fails  
**Solution**: Check Rasa X connectivity and credentials
```bash
# Test Rasa X API connectivity
curl -k -X POST https://<rasa-x-url>/api/auth \
  -H "Content-Type: application/json" \
  -d '{"username": "me", "password": "password"}'
```

### File Processing Issues

#### Missing Generated Content
**Problem**: Expected files not generated or incomplete  
**Solution**: Check `newfaq.md` format and processing logs
```bash
# Verify newfaq.md format
cat newfaq.md | grep -E "^###|^intent:|^answer:|^altquestion:"

# Check for processing success
cat working.txt  # Should contain "It worked"
```

#### Encoding Issues
**Problem**: Special characters not processed correctly  
**Solution**: Ensure UTF-8 encoding
```bash
# Check file encoding
file -bi newfaq.md

# Convert if necessary
iconv -f ISO-8859-1 -t UTF-8 newfaq.md > newfaq_utf8.md
```

## Performance Optimization

### Model Training Optimization

#### Training Configuration
```yaml
# config.yml optimizations
policies:
- name: TEDPolicy
  max_history: 5      # Reduce for faster training
  epochs: 50          # Reduce for development
```

#### Resource Management
```bash
# Limit TensorFlow memory usage
export TF_FORCE_GPU_ALLOW_GROWTH=true

# Set CPU thread limits
export OMP_NUM_THREADS=4
```

### Pipeline Optimization

#### Parallel Processing
```groovy
// Jenkins pipeline optimization
parallel {
    stage('Model Training') {
        steps { /* training steps */ }
    }
    stage('Content Processing') {
        steps { /* content steps */ }
    }
}
```

#### Caching Strategies
```groovy
// Cache dependencies
stage('Setup') {
    steps {
        cache(maxCacheSize: 250, caches: [
            arbitraryFileCache(path: 'miniconda', fingerprint: 'conda-env')
        ]) {
            // Environment setup
        }
    }
}
```

## Security Considerations

### Credential Management
- Store all sensitive credentials in Jenkins credential store
- Use environment variables for configuration
- Never commit credentials to version control
- Rotate credentials regularly

### API Security
- Use HTTPS for all external API calls
- Implement proper authentication for Rasa X
- Validate all input data before processing
- Monitor API usage and access logs

### File Security
- Set appropriate file permissions
- Validate file content before processing
- Implement backup and recovery procedures
- Monitor file system access
