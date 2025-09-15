# RasaUtilityTools Workflows Documentation

## Overview

RasaUtilityTools supports three primary execution workflows designed for different use cases and environments. Each workflow processes the master FAQ file (`newfaq.md`) but differs in execution context, automation level, and integration capabilities.

## Workflow Types

### 1. Local Development Workflow
**Script**: `chatscriptStandalone.py`  
**Use Case**: Development, testing, and manual FAQ updates  
**Execution**: Interactive command-line interface

### 2. CI/CD Automation Workflow  
**Script**: `chatscriptJenkins.py`  
**Use Case**: Production deployments and automated updates  
**Execution**: Jenkins pipeline automation

### 3. Core Processing Workflow
**Script**: `chatscript.py`  
**Use Case**: Jenkins pipeline execution (called by jenkinsfile)  
**Execution**: Non-interactive batch processing

---

## Local Development Workflow

### Prerequisites
- Python 3.7 environment
- Rasa 1.10.x installation
- pandas 1.2.1
- Local Rasa project setup

### Execution Steps

#### 1. Environment Setup
```bash
# Ensure Python 3.7 is active
python --version  # Should show 3.7.x

# Install dependencies
pip install -r requirements.txt
```

#### 2. Interactive Execution
```bash
python ./chatscriptStandalone.py
```

#### 3. Interactive Prompts
The script will prompt for project configuration:
```
Are you working in a Rasa init project? (y/n):
```

**Response Options:**
- **Yes (y)**: Script will modify `domain.yml` to add required sections
  - Inserts `entities:` and `slots:` before `responses:`
  - Inserts `actions:` and `forms:` before `session_config:`
- **No (n)**: Script assumes existing Rasa project structure

#### 4. Processing Execution
The script processes `newfaq.md` and generates:
- **Rasa Training Files**: `data/nlu.md`, `data/stories.md`, updated `domain.yml`
- **Web Content**: `faq.mdx` for website integration

#### 5. Manual Model Training
After script completion, manually train the model:
```bash
rasa train
```

### Local Development Features

#### Interactive Configuration
- **Project Detection**: Automatically detects Rasa project structure
- **Safe Modifications**: Only modifies files if content doesn't already exist
- **User Feedback**: Provides real-time processing feedback

#### Development Benefits
- **Rapid Iteration**: Quick testing of FAQ changes
- **Local Validation**: Verify content before CI/CD deployment
- **Debugging Support**: Interactive prompts for troubleshooting

---

## CI/CD Automation Workflow

### Pipeline Overview
The Jenkins pipeline provides fully automated FAQ processing, model training, and deployment through a multi-stage process.

### Pipeline Stages

#### Stage 1: Environment Preparation
```groovy
stage ('Build and Deploy Chatbot/FAQ') {
    // Git configuration and repository cloning
    // Conda environment setup
    // Dependency installation
}
```

**Actions Performed:**
- Configure Git credentials and user information
- Clone target repository for FAQ updates
- Download and install Miniconda
- Create isolated Python 3 environment named `chatscript`
- Install required packages: pandas, requests, tensorflow, rasa

#### Stage 2: Content Processing
```bash
echo "Run File Creation Script"
python chatscript.py
```

**Processing Logic:**
- Parse `newfaq.md` without interactive prompts
- Generate all Rasa training files
- Create web FAQ content (`faq.mdx`)
- Write success confirmation to `working.txt`

#### Stage 3: Model Training
```bash
echo "Train Models"
python rasatrain.py
```

**Training Process:**
- Read build version from `modelname.txt`
- Execute Rasa training with versioned model name
- Generate model file: `models/{BUILD_VERSION}.tar.gz`
- Verify model creation with directory listing

#### Stage 4: Model Deployment
```bash
# Direct upload to Rasa X
curl -k -F "model=@models/\"${BUILD_VERSION}.tar.gz\"" "<rasa_url_with_token>"

# Activate as production model
python rasaUpload.py
```

**Deployment Actions:**
- Upload trained model to Rasa X instance
- Authenticate with Rasa X API
- Tag model as production version
- Verify successful activation

#### Stage 5: Website Integration
```bash
echo "Start GIT Workflow"
# Create feature branch
git checkout -b "Jenkins-Build-\"${BUILD_VERSION}\""

# Copy FAQ content to website repository
cp faq.mdx ./<website_repo_faq_location> -f

# Create pull request for website updates
git add <faq_directory>
git commit -m "Automated FAQ Update"
git push --set-upstream origin Jenkins-Build-${BUILD_VERSION}
hub pull-request --base <repo>:master --head <username>:automated-jenkins
```

### Pipeline Configuration

#### Environment Variables
- `BUILD_VERSION`: Jenkins build number for model versioning
- `BRANCH_NAME`: Source branch triggering the build
- Git credentials for repository access
- Rasa X API credentials for model deployment

#### Trigger Configuration
```groovy
triggers {
    githubPush()  // Automatic trigger on newfaq.md changes
}
```

#### Parameter Configuration
```groovy
parameters {
    string(name: 'modelname', defaultValue: '<rasa_url>')
}
```

---

## Core Processing Workflow

### Script Purpose
`chatscript.py` serves as the core processing engine called by the Jenkins pipeline. It provides non-interactive FAQ processing optimized for automated environments.

### Key Differences from Interactive Scripts

#### No User Prompts
- **Hardcoded Configuration**: No interactive project setup
- **Batch Processing**: Processes entire FAQ file without interruption
- **Silent Execution**: Minimal console output for automated environments

#### Enhanced Logging
```python
print(line)  # Debug output for each processed line
print(altquestion2)  # Alternative question processing feedback
print(noforms)  # Forms detection logic output
```

#### Success Confirmation
```python
with open("./working.txt", "a+") as myfile:
    myfile.write("It worked")
```

### Processing Logic Flow

#### 1. FAQ Content Parsing
```python
with open("newfaq.md") as file_in:
    for line in file_in:
        # Process each line type
```

#### 2. Content Type Detection
- **Questions**: Lines starting with `### `
- **Intents**: Lines starting with `intent: `
- **Answers**: Lines starting with `answer: `
- **Alternatives**: Lines starting with `altquestion:`

#### 3. Output Generation
- **Web FAQ**: Append to `faq.mdx`
- **NLU Data**: Append to `data/nlu.md`
- **Domain Updates**: Modify `domain.yml`
- **Stories**: Append to `data/stories.md`

#### 4. Duplicate Prevention
```python
if chatquestion not in open('faq.mdx').read():
    # Only add if content doesn't exist
```

---

## Model Training and Deployment Workflow

### Training Process (`rasatrain.py`)

#### Version Management
```python
f = open("modelname.txt", "r")
x = ""
for line in f:
    stripped_line = line.rstrip()
    x += stripped_line
f.close()
```

#### Training Execution
```python
model_path = rasa.train(
    domain="domain.yml",
    config="config.yml", 
    training_files=["data/"],
    output="models/",
    fixed_model_name=x
)
```

### Deployment Process (`rasaUpload.py`)

#### Authentication Flow
```python
# Authenticate with Rasa X
url = 'https://<rasa-x-route>/api/auth'
payload = '{"username": "me", "password": "rasaxpassword"}'
r = requests.post(url, data=payload, headers=headers, verify=False)
auth = output['access_token']
```

#### Production Activation
```python
# Tag model as production
url = "https://<rasa-x-route>/api/projects/default/models/" + x + "/tags/production"
response = requests.request("PUT", url, data=payload, headers=headers, verify=False)
```

---

## Workflow Comparison

| Feature | Standalone | Jenkins | Core |
|---------|------------|---------|------|
| **Execution** | Interactive | Automated | Batch |
| **Environment** | Local | CI/CD | Pipeline |
| **User Input** | Required | None | None |
| **Model Training** | Manual | Automated | N/A |
| **Deployment** | Manual | Automated | N/A |
| **Git Integration** | Manual | Automated | N/A |
| **Error Handling** | Interactive | Logged | Logged |
| **Use Case** | Development | Production | Processing |

## Best Practices

### Local Development
- Always test FAQ changes locally before committing
- Verify generated files before manual model training
- Use version control for tracking changes

### CI/CD Deployment
- Monitor Jenkins build logs for processing errors
- Verify Rasa X model activation after deployment
- Review generated pull requests before merging

### Content Management
- Follow consistent FAQ format in `newfaq.md`
- Use descriptive intent names for better organization
- Provide multiple alternative questions for robust NLU training

### Error Recovery
- Check `working.txt` for successful processing confirmation
- Review generated files for content accuracy
- Use Rasa X interface to verify model performance
