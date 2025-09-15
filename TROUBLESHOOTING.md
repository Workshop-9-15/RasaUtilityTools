# RasaUtilityTools Troubleshooting Guide

## Overview

This guide provides comprehensive troubleshooting information for common issues encountered when using RasaUtilityTools. Issues are organized by category with detailed diagnostic steps and solutions.

## Quick Diagnostic Checklist

Before diving into specific issues, run this quick diagnostic checklist:

```bash
# 1. Verify Python version
python --version  # Should be 3.7.x

# 2. Check Rasa installation
python -c "import rasa; print(rasa.__version__)"  # Should be 1.10.x

# 3. Verify file permissions
ls -la newfaq.md domain.yml data/

# 4. Check for processing success indicator
cat working.txt  # Should contain "It worked"

# 5. Verify generated files exist
ls -la faq.mdx data/nlu.md data/stories.md
```

## FAQ Processing Issues

### Issue: Script Fails to Process newfaq.md

#### Symptoms
- Processing script exits without generating files
- No error messages or unclear error output
- `working.txt` file not created or empty

#### Diagnostic Steps
```bash
# Check file existence and permissions
ls -la newfaq.md
file newfaq.md  # Check file type and encoding

# Verify file format
head -20 newfaq.md
grep -E "^###|^intent:|^answer:|^altquestion:" newfaq.md

# Check for hidden characters
cat -A newfaq.md | head -10
```

#### Common Causes and Solutions

**1. File Encoding Issues**
```bash
# Problem: File not in UTF-8 encoding
file -bi newfaq.md

# Solution: Convert to UTF-8
iconv -f ISO-8859-1 -t UTF-8 newfaq.md > newfaq_utf8.md
mv newfaq_utf8.md newfaq.md
```

**2. Incorrect Format Markers**
```bash
# Problem: Missing spaces or incorrect prefixes
# Incorrect:
###Question without space
intent:missing_space
answer:missing_space

# Correct:
### Question with space
intent: correct_format
answer: correct_format
```

**3. Line Ending Issues**
```bash
# Problem: Windows line endings on Unix system
dos2unix newfaq.md

# Or manually convert
sed -i 's/\r$//' newfaq.md
```

### Issue: Duplicate Content in Generated Files

#### Symptoms
- Same content appears multiple times in output files
- NLU training data has repeated intent sections
- Domain.yml has duplicate entries

#### Diagnostic Steps
```bash
# Check for duplicates in generated files
grep -n "## intent:" data/nlu.md | sort
grep -n "utter_" domain.yml | sort
```

#### Solutions

**1. Clean Generated Files**
```bash
# Remove generated content and regenerate
rm -f faq.mdx data/nlu.md data/stories.md working.txt

# Reset domain.yml to base state (backup first)
cp domain.yml domain.yml.backup
# Manually remove FAQ-generated content from domain.yml

# Rerun processing
python chatscriptStandalone.py
```

**2. Prevent Future Duplicates**
The scripts include duplicate detection, but if files are corrupted:
```python
# Manual duplicate removal in Python
def remove_duplicates(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    unique_lines = []
    seen = set()
    for line in lines:
        if line not in seen:
            unique_lines.append(line)
            seen.add(line)
    
    with open(filename, 'w') as f:
        f.writelines(unique_lines)
```

### Issue: Missing or Incomplete Generated Content

#### Symptoms
- Some FAQ entries not appearing in generated files
- Partial content generation
- Missing intents or responses

#### Diagnostic Steps
```bash
# Count FAQ entries in source
grep -c "^### " newfaq.md

# Count generated intents
grep -c "^## intent:" data/nlu.md

# Check for processing errors
python chatscriptStandalone.py 2>&1 | tee processing.log
grep -i error processing.log
```

#### Solutions

**1. Verify FAQ Format Consistency**
```bash
# Check each FAQ entry structure
awk '/^### /{print NR ": " $0}' newfaq.md
awk '/^intent:/{print NR ": " $0}' newfaq.md
awk '/^answer:/{print NR ": " $0}' newfaq.md

# Ensure each ### has corresponding intent and answer
```

**2. Debug Processing Logic**
Add debug output to processing script:
```python
# Add to chatscript*.py for debugging
print(f"Processing line {line_number}: {line.strip()}")
print(f"Current intent: {chatintent if 'chatintent' in locals() else 'None'}")
```

## Model Training Issues

### Issue: Rasa Training Fails

#### Symptoms
- `rasa train` command fails with errors
- Model files not generated in `models/` directory
- Training process hangs or crashes

#### Diagnostic Steps
```bash
# Check Rasa installation
rasa --version
python -c "import tensorflow; print(tensorflow.__version__)"

# Validate training data
rasa data validate

# Check for data format issues
rasa data validate --domain domain.yml --data data/
```

#### Common Training Errors

**1. Invalid Training Data Format**
```bash
# Problem: Incorrect NLU format
## intent:missing_space  # Missing space after colon

# Solution: Fix format
## intent: correct_format
```

**2. Domain Configuration Errors**
```yaml
# Problem: Missing responses for intents
intents:
- faq_example
# Missing corresponding response

# Solution: Add response
responses:
  utter_faq_example:
  - text: "Example response"
```

**3. Memory Issues During Training**
```bash
# Problem: Insufficient memory for training
# Solution: Reduce model complexity
# In config.yml:
policies:
- name: TEDPolicy
  epochs: 50  # Reduce from 100
  max_history: 3  # Reduce from 5
```

### Issue: Model Training Takes Too Long

#### Symptoms
- Training process runs for hours without completion
- High CPU/memory usage during training
- System becomes unresponsive

#### Solutions

**1. Optimize Training Configuration**
```yaml
# config.yml optimizations
pipeline:
- name: DIETClassifier
  epochs: 50  # Reduce from 100
  
policies:
- name: TEDPolicy
  epochs: 50  # Reduce from 100
  max_history: 3  # Reduce from 5
```

**2. Resource Management**
```bash
# Limit TensorFlow resource usage
export TF_CPP_MIN_LOG_LEVEL=2
export OMP_NUM_THREADS=2

# Monitor resource usage
top -p $(pgrep -f "rasa train")
```

## Jenkins Pipeline Issues

### Issue: Jenkins Build Fails

#### Symptoms
- Jenkins pipeline fails at various stages
- Build logs show errors in environment setup
- Conda environment creation fails

#### Diagnostic Steps
```bash
# Check Jenkins agent capabilities
# On Jenkins agent:
which conda
which python
which git

# Verify network connectivity
curl -I https://repo.anaconda.com/miniconda/
ping github.com
```

#### Common Pipeline Failures

**1. Conda Installation Fails**
```bash
# Problem: Network issues or permissions
# Solution: Check network and use alternative approach
# In Jenkinsfile:
sh '''
    # Alternative conda installation
    if [ ! -d "$PWD/miniconda" ]; then
        wget -q https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
        bash Miniconda3-latest-Linux-x86_64.sh -b -p $PWD/miniconda
    fi
'''
```

**2. Git Authentication Failures**
```groovy
// Problem: Invalid credentials
// Solution: Verify credential configuration
withCredentials([usernamePassword(
    credentialsId: 'github-credentials',
    passwordVariable: 'GIT_PASSWORD',
    usernameVariable: 'GIT_USERNAME'
)]) {
    sh '''
        git config --global user.name "${GIT_USERNAME}"
        git config --global user.email "${GIT_USERNAME}@example.com"
        git clone https://${GIT_USERNAME}:${GIT_PASSWORD}@github.com/org/repo.git
    '''
}
```

**3. Python Package Installation Fails**
```bash
# Problem: Package conflicts or network issues
# Solution: Use specific package versions
pip install --no-cache-dir \
    pandas==1.2.1 \
    requests==2.24.0 \
    tensorflow==2.1.1 \
    rasa==1.10.12
```

### Issue: Model Upload to Rasa X Fails

#### Symptoms
- Model training succeeds but upload fails
- Authentication errors with Rasa X API
- Network connectivity issues

#### Diagnostic Steps
```bash
# Test Rasa X connectivity
curl -k -I https://<rasa-x-url>/api/health

# Test authentication
curl -k -X POST https://<rasa-x-url>/api/auth \
  -H "Content-Type: application/json" \
  -d '{"username": "me", "password": "password"}'

# Check model file
ls -la models/
file models/*.tar.gz
```

#### Solutions

**1. Authentication Issues**
```python
# Update rasaUpload.py with correct credentials
url = 'https://<correct-rasa-x-url>/api/auth'
payload = {
    'username': '<correct-username>',
    'password': '<correct-password>'
}

# Add error handling
try:
    response = requests.post(url, json=payload, headers=headers, verify=False)
    response.raise_for_status()
    auth_token = response.json()['access_token']
except requests.exceptions.RequestException as e:
    print(f"Authentication failed: {e}")
    sys.exit(1)
```

**2. Network/SSL Issues**
```python
# Disable SSL verification if using self-signed certificates
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Or configure proper SSL context
import ssl
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE
```

## File Permission and Access Issues

### Issue: Permission Denied Errors

#### Symptoms
- Cannot write to generated files
- Permission denied when modifying domain.yml
- File access errors during processing

#### Diagnostic Steps
```bash
# Check file permissions
ls -la domain.yml data/ faq.mdx

# Check directory permissions
ls -ld data/

# Check file ownership
stat domain.yml
```

#### Solutions

**1. Fix File Permissions**
```bash
# Make files writable
chmod 644 domain.yml data/nlu.md data/stories.md
chmod 755 data/

# Fix ownership if needed
sudo chown $USER:$USER domain.yml data/nlu.md data/stories.md
```

**2. Directory Structure Issues**
```bash
# Ensure data directory exists
mkdir -p data/

# Create missing files with proper permissions
touch data/nlu.md data/stories.md
chmod 644 data/nlu.md data/stories.md
```

## Environment and Dependency Issues

### Issue: Python Version Conflicts

#### Symptoms
- Rasa installation fails
- Import errors for Rasa modules
- Unexpected behavior during processing

#### Diagnostic Steps
```bash
# Check Python version
python --version
which python

# Check virtual environment
echo $VIRTUAL_ENV
conda info --envs

# Verify Rasa compatibility
python -c "import sys; print(sys.version_info)"
```

#### Solutions

**1. Use Correct Python Version**
```bash
# Install Python 3.7 with pyenv
pyenv install 3.7.17
pyenv local 3.7.17

# Or create conda environment
conda create -n rasatools python=3.7
conda activate rasatools
```

**2. Clean Environment Setup**
```bash
# Remove existing environment
conda env remove -n rasatools

# Create fresh environment
conda create -n rasatools python=3.7
conda activate rasatools
pip install -r requirements.txt
```

### Issue: Package Version Conflicts

#### Symptoms
- Import errors for specific packages
- Unexpected behavior from dependencies
- Version compatibility warnings

#### Diagnostic Steps
```bash
# Check installed packages
pip list
pip show rasa tensorflow pandas

# Check for conflicts
pip check
```

#### Solutions

**1. Use Exact Versions from requirements.txt**
```bash
# Install exact versions
pip install -r requirements.txt --force-reinstall

# Or install specific versions
pip install rasa==1.10.12 tensorflow==2.1.1 pandas==1.2.1
```

**2. Resolve Conflicts**
```bash
# Uninstall conflicting packages
pip uninstall tensorflow tensorflow-gpu

# Reinstall with correct versions
pip install tensorflow==2.1.1
```

## Performance Issues

### Issue: Slow Processing Performance

#### Symptoms
- FAQ processing takes excessive time
- High memory usage during processing
- System becomes unresponsive

#### Diagnostic Steps
```bash
# Monitor resource usage
top -p $(pgrep -f python)
free -h
df -h

# Profile script execution
time python chatscriptStandalone.py
```

#### Solutions

**1. Optimize File Operations**
```python
# Instead of reading file multiple times
if chatquestion not in open('faq.mdx').read():

# Read once and cache
with open('faq.mdx', 'r') as f:
    existing_content = f.read()

if chatquestion not in existing_content:
    # Process
```

**2. Batch File Operations**
```python
# Collect all changes first, then write once
changes = []
# ... collect changes ...

# Write all changes at once
with open('domain.yml', 'w') as f:
    f.writelines(updated_content)
```

## Data Quality Issues

### Issue: Inconsistent FAQ Content

#### Symptoms
- Bot responses don't match website FAQ
- Missing or incorrect intent mappings
- Inconsistent answer formatting

#### Diagnostic Steps
```bash
# Compare source and generated content
diff <(grep "^### " newfaq.md) <(grep "^### " faq.mdx)

# Check intent consistency
grep "^intent:" newfaq.md | sort
grep "^## intent:" data/nlu.md | sort
```

#### Solutions

**1. Validate FAQ Format**
```python
# Validation script
def validate_faq_format(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    current_question = None
    current_intent = None
    current_answer = None
    
    for i, line in enumerate(lines, 1):
        if line.startswith('### '):
            if current_question and not (current_intent and current_answer):
                print(f"Line {i}: Incomplete FAQ entry")
            current_question = line.strip()
            current_intent = None
            current_answer = None
        elif line.startswith('intent: '):
            current_intent = line.strip()
        elif line.startswith('answer: '):
            current_answer = line.strip()

validate_faq_format('newfaq.md')
```

**2. Content Consistency Checks**
```bash
# Check for orphaned content
grep -n "^intent:" newfaq.md | while read line; do
    intent=$(echo "$line" | cut -d: -f3 | tr -d ' ')
    if ! grep -q "utter_$intent" domain.yml; then
        echo "Missing response for intent: $intent"
    fi
done
```

## Monitoring and Alerting

### Setting Up Monitoring

#### Health Check Script
```python
#!/usr/bin/env python3
# health_check.py

import os
import sys
from datetime import datetime

def check_files():
    """Check if required files exist and are readable"""
    required_files = [
        'newfaq.md',
        'domain.yml',
        'config.yml',
        'data/nlu.md',
        'data/stories.md'
    ]
    
    for file_path in required_files:
        if not os.path.exists(file_path):
            return False, f"Missing file: {file_path}"
        if not os.access(file_path, os.R_OK):
            return False, f"Cannot read file: {file_path}"
    
    return True, "All files accessible"

def check_processing_status():
    """Check if last processing was successful"""
    if os.path.exists('working.txt'):
        with open('working.txt', 'r') as f:
            content = f.read().strip()
        return content == "It worked", f"Processing status: {content}"
    return False, "No processing status file found"

def main():
    checks = [
        ("File accessibility", check_files),
        ("Processing status", check_processing_status)
    ]
    
    all_passed = True
    for check_name, check_func in checks:
        passed, message = check_func()
        status = "PASS" if passed else "FAIL"
        print(f"{datetime.now().isoformat()} - {check_name}: {status} - {message}")
        if not passed:
            all_passed = False
    
    sys.exit(0 if all_passed else 1)

if __name__ == "__main__":
    main()
```

#### Automated Monitoring
```bash
# Add to crontab for regular health checks
# crontab -e
*/15 * * * * cd /path/to/RasaUtilityTools && python health_check.py >> health.log 2>&1
```

### Log Analysis

#### Log Parsing Script
```python
#!/usr/bin/env python3
# analyze_logs.py

import re
from collections import defaultdict

def analyze_jenkins_logs(log_file):
    """Analyze Jenkins build logs for common issues"""
    error_patterns = {
        'conda_install': r'conda.*failed|miniconda.*error',
        'git_auth': r'authentication failed|permission denied.*git',
        'python_import': r'ImportError|ModuleNotFoundError',
        'rasa_train': r'rasa train.*failed|training.*error',
        'model_upload': r'upload.*failed|rasa.*api.*error'
    }
    
    errors = defaultdict(list)
    
    with open(log_file, 'r') as f:
        for line_num, line in enumerate(f, 1):
            for error_type, pattern in error_patterns.items():
                if re.search(pattern, line, re.IGNORECASE):
                    errors[error_type].append((line_num, line.strip()))
    
    return errors

# Usage
errors = analyze_jenkins_logs('jenkins.log')
for error_type, occurrences in errors.items():
    print(f"\n{error_type.upper()} ERRORS:")
    for line_num, line in occurrences:
        print(f"  Line {line_num}: {line}")
```

## Recovery Procedures

### Complete System Reset

If all else fails, use this procedure to reset the system:

```bash
#!/bin/bash
# reset_system.sh

echo "Starting RasaUtilityTools system reset..."

# 1. Backup current state
mkdir -p backup/$(date +%Y%m%d_%H%M%S)
cp -r data/ domain.yml faq.mdx working.txt backup/$(date +%Y%m%d_%H%M%S)/ 2>/dev/null || true

# 2. Clean generated files
rm -f faq.mdx working.txt
rm -f data/nlu.md data/stories.md

# 3. Reset domain.yml to base state
git checkout domain.yml || echo "Warning: Could not reset domain.yml from git"

# 4. Recreate data directory structure
mkdir -p data/
touch data/nlu.md data/stories.md

# 5. Set proper permissions
chmod 644 domain.yml data/nlu.md data/stories.md
chmod 755 data/

# 6. Verify newfaq.md format
python -c "
import sys
with open('newfaq.md', 'r') as f:
    content = f.read()
    if '### ' not in content or 'intent:' not in content:
        print('ERROR: newfaq.md appears to be malformed')
        sys.exit(1)
print('newfaq.md format appears valid')
"

# 7. Run processing
echo "Running FAQ processing..."
python chatscriptStandalone.py

# 8. Verify success
if [ -f "working.txt" ] && grep -q "It worked" working.txt; then
    echo "System reset completed successfully"
else
    echo "ERROR: System reset failed - check logs"
    exit 1
fi
```

### Emergency Rollback

```bash
#!/bin/bash
# emergency_rollback.sh

# Rollback to last known good state
BACKUP_DIR=$(ls -1t backup/ | head -1)

if [ -z "$BACKUP_DIR" ]; then
    echo "ERROR: No backup found for rollback"
    exit 1
fi

echo "Rolling back to backup: $BACKUP_DIR"

# Restore files
cp backup/$BACKUP_DIR/* . 2>/dev/null || true
cp backup/$BACKUP_DIR/data/* data/ 2>/dev/null || true

echo "Rollback completed"
```

## Getting Help

### Information to Collect

When seeking help, collect this information:

```bash
#!/bin/bash
# collect_debug_info.sh

echo "=== RasaUtilityTools Debug Information ==="
echo "Date: $(date)"
echo "System: $(uname -a)"
echo

echo "=== Python Environment ==="
python --version
which python
echo "Virtual env: $VIRTUAL_ENV"
echo

echo "=== Package Versions ==="
pip list | grep -E "(rasa|tensorflow|pandas)"
echo

echo "=== File Status ==="
ls -la newfaq.md domain.yml faq.mdx working.txt 2>/dev/null || echo "Some files missing"
ls -la data/ 2>/dev/null || echo "Data directory missing"
echo

echo "=== Recent Errors ==="
tail -20 *.log 2>/dev/null || echo "No log files found"
echo

echo "=== FAQ Format Check ==="
head -20 newfaq.md
echo

echo "=== Generated Content Sample ==="
head -10 data/nlu.md 2>/dev/null || echo "NLU file not found"
head -10 faq.mdx 2>/dev/null || echo "FAQ file not found"
```

### Support Channels

1. **Check Documentation**: Review all documentation files first
2. **Search Issues**: Look for similar problems in project issues
3. **Create Detailed Issue**: Include debug information and steps to reproduce
4. **Community Forums**: Rasa community for Rasa-specific issues

### Best Practices for Prevention

1. **Regular Backups**: Backup working configurations before changes
2. **Version Control**: Use Git for all configuration changes
3. **Testing**: Test changes in development environment first
4. **Monitoring**: Implement health checks and monitoring
5. **Documentation**: Keep local notes of customizations and fixes
