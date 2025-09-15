# Archived Repository

Thanks for your interest in Optum's RasaUtilityTools project! Unfortunately, we have moved on and this project is no longer actively maintained or monitored by our Open Source Program Office. This copy is provided for reference only. Please fork the code if you are interested in further development. The project and all artifacts including code and documentation remain subject to use and reference under the terms and conditions of the open source license indicated. All copyrights reserved.

# RasaUtilityTools - Automated FAQ Chatbot Deployment

An automated CI/CD system for maintaining synchronized FAQ content between Rasa-based chatbots and support websites. This tool establishes a single source of truth for FAQ data, eliminating manual maintenance across multiple systems.

## 📋 Quick Start

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Process FAQ content
python ./chatscriptStandalone.py

# Train Rasa model
rasa train
```

### CI/CD Pipeline
The Jenkins pipeline automatically processes FAQ changes, trains models, and deploys to both Rasa X and website repositories.

## 🏗️ System Architecture

**Single Source → Dual Outputs**
- **Input**: `newfaq.md` (master FAQ file)
- **Outputs**: Rasa training data + Web FAQ content
- **Automation**: Jenkins CI/CD pipeline
- **Deployment**: Rasa X + Website pull requests

## 📚 Documentation

### Core Documentation
- **[Architecture Overview](ARCHITECTURE.md)** - System design and component relationships
- **[Workflow Guide](WORKFLOWS.md)** - Local development and CI/CD processes
- **[FAQ Format Specification](FAQ_FORMAT.md)** - Master file format and processing rules
- **[Setup Guide](SETUP.md)** - Environment configuration and deployment
- **[Integrations](INTEGRATIONS.md)** - External system connections and APIs
- **[Troubleshooting](TROUBLESHOOTING.md)** - Common issues and solutions

### Quick Reference
- **Technology Stack**: Python 3.7, Rasa 1.10.x, Jenkins, Conda
- **Key Files**: `newfaq.md`, `chatscriptStandalone.py`, `jenkinsfile`
- **Generated Outputs**: `data/nlu.md`, `data/stories.md`, `domain.yml`, `faq.mdx`

## 🔄 FAQ Processing Workflow

### Master FAQ Format (`newfaq.md`)
```markdown
### Does your framework use Rasa?
intent: faq_rasa_support
answer: Yes! Our framework was built with Rasa
altquestion: What is the chatbot tool
altquestion: do you use an NLU
altquestion: Did you use rasa
```

### Generated Outputs
- **Rasa Training Data**: NLU examples, conversation stories, domain configuration
- **Web Content**: Formatted FAQ for website integration
- **Model Deployment**: Automated training and Rasa X activation

## 🚀 Execution Modes

### 1. Local Development (`chatscriptStandalone.py`)
- Interactive prompts for project configuration
- Manual model training required
- Ideal for testing and development

### 2. CI/CD Automation (`chatscriptJenkins.py`)
- Fully automated pipeline execution
- Integrated model training and deployment
- GitHub webhook triggered

### 3. Core Processing (`chatscript.py`)
- Non-interactive batch processing
- Called by Jenkins pipeline
- Optimized for automated environments

## 🛠️ Requirements

### Environment
- **Python 3.7** (Required for Rasa 1.10.x compatibility)
- **Rasa 1.10.x** (Conversational AI framework)
- **pandas 1.2.1** (Data processing)
- **Jenkins** (CI/CD automation)

### Key Dependencies
See `requirements.txt` for complete dependency list including TensorFlow 2.1.1, Rasa SDK 1.10.2, and supporting libraries.

## 📊 CI/CD Pipeline

### Pipeline Stages
1. **Environment Setup** - Conda environment and dependency installation
2. **FAQ Processing** - Parse `newfaq.md` and generate training files
3. **Model Training** - Automated Rasa model training with versioning
4. **Deployment** - Upload to Rasa X and activate as production
5. **Website Integration** - Create pull request with updated FAQ content

### Automation Features
- GitHub webhook triggers on `newfaq.md` changes
- Versioned model deployment to Rasa X
- Automated website repository updates
- Build status notifications and monitoring

## 🔧 Configuration Files

### Rasa Configuration
- **`config.yml`** - Pipeline with TEDPolicy, DIETClassifier (100 epochs each)
- **`domain.yml`** - Intents, responses, and actions (auto-updated)
- **`data/nlu.md`** - Training examples (auto-generated)
- **`data/stories.md`** - Conversation flows (auto-generated)

### Integration Configuration
- **`credentials.yml`** - Channel authentication (REST, Slack, Facebook)
- **`endpoints.yml`** - External service endpoints (action server, tracker store)
- **`jenkinsfile`** - Complete CI/CD pipeline definition

## 🎯 Use Cases

### Primary Users
- **Support Teams**: Maintain FAQ content in single location
- **Chatbot Developers**: Automated training data generation
- **DevOps Teams**: Streamlined deployment pipeline
- **Content Managers**: Synchronized web and bot content

### Benefits
- **Consistency**: Eliminates content drift between systems
- **Efficiency**: Reduces manual maintenance overhead
- **Automation**: End-to-end deployment pipeline
- **Scalability**: Handles growing FAQ content seamlessly

## 🔍 Monitoring and Maintenance

### Health Checks
- Processing success indicators (`working.txt`)
- Generated file validation
- Model deployment verification
- API connectivity monitoring

### Performance Optimization
- Efficient file processing with duplicate detection
- Configurable training parameters for development vs production
- Resource management for model training
- Caching strategies for CI/CD pipeline

## 🆘 Support

### Getting Help
1. **Check Documentation**: Review comprehensive guides above
2. **Troubleshooting Guide**: Common issues and solutions
3. **Debug Information**: Use provided diagnostic scripts
4. **Community Support**: Rasa community for framework-specific issues

### Best Practices
- Test FAQ changes locally before committing
- Monitor Jenkins build logs for processing errors
- Verify Rasa X model activation after deployment
- Use version control for all configuration changes

---

**Original Project**: Automated chatbot script for synchronized FAQ management  
**Technology**: Rasa 1.10.x, Python 3.7, Jenkins CI/CD  
**Architecture**: Single source of truth → Dual output system


