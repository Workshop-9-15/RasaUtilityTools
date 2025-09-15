# GitHub Actions Migration Guide

This document explains the migration from Jenkins to GitHub Actions and the required configuration.

## Required GitHub Secrets

To use the new GitHub Actions workflow, you need to configure the following secrets in your repository settings:

### Rasa Authentication (Option 1 - Username/Password)
- `RASA_USERNAME`: Your Rasa-X username
- `RASA_PASSWORD`: Your Rasa-X password
- `RASA_SERVER_URL`: Your Rasa-X server URL (e.g., `https://your-rasa-server.com/api/auth`)

### Rasa Authentication (Option 2 - Token-based)
- `RASA_TOKEN`: Your Rasa server API token
- `RASA_SERVER_URL`: Your Rasa server API URL (e.g., `https://your-rasa-server.com/api`)

### FAQ Deployment (Optional)
- `TARGET_FAQ_REPO`: Target repository for FAQ updates (e.g., `your-org/your-faq-repo`)
- `FAQ_DIRECTORY`: Directory path in the target repo where FAQ should be deployed

## Security Improvements

The new GitHub Actions workflow addresses several security vulnerabilities from the original Jenkins pipeline:

1. **Hardcoded Credentials**: Replaced with GitHub Secrets
2. **Disabled SSL Verification**: Removed unsafe `-k` flags and `verify=False` parameters
3. **Credential Exposure**: Uses secure token-based authentication
4. **Command Injection**: Properly sanitizes build version variables
5. **Unsafe Downloads**: Uses official GitHub Actions instead of downloading scripts

## Workflow Features

- **Triggers**: Runs on push to main/master, pull requests, and manual dispatch
- **Caching**: Implements pip dependency caching for faster builds
- **Artifacts**: Saves models and FAQ files as build artifacts
- **Error Handling**: Graceful handling of missing secrets and optional steps
- **Security**: Follows GitHub Actions security best practices

## Migration Steps

1. Configure the required GitHub Secrets in your repository settings
2. Update `rasaUpload.py` to use environment variables instead of hardcoded credentials
3. Test the workflow with a small change to verify functionality
4. Remove or archive the old `jenkinsfile` once migration is complete

## Workflow File Location

The new workflow is located at: `.github/workflows/rasa-chatbot-deploy.yml`
