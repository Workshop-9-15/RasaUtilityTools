# GitHub Actions Migration

This repository has been migrated from Jenkins to GitHub Actions. The new workflow file is located at `.github/workflows/rasa-faq-pipeline.yml`.

## Required Secrets

To use this workflow, you need to configure the following secrets in your GitHub repository settings:

### Rasa X Integration
- `RASA_URL`: Base URL of your Rasa X server (e.g., `https://your-rasa-server.com`)
- `RASA_URL_WITH_TOKEN`: Complete URL with token for model upload (e.g., `https://your-rasa-server.com/api/projects/default/models?token=your-token`)
- `RASA_USERNAME`: Username for Rasa X authentication
- `RASA_PASSWORD`: Password for Rasa X authentication

### Git Configuration
- `GIT_USER_NAME`: Name to use for Git commits (e.g., "GitHub Actions Bot")
- `GIT_USER_EMAIL`: Email to use for Git commits (e.g., "actions@github.com")

### Website Repository Integration
- `WEBSITE_REPO_URL`: Target website repository in format `owner/repo` (e.g., `myorg/website`)
- `WEBSITE_FAQ_PATH`: Path within the website repository where FAQ file should be placed (e.g., `src/content/faq`)

### GitHub Token
- `GITHUB_TOKEN`: This is automatically provided by GitHub Actions, no manual configuration needed

## Workflow Features

The GitHub Actions workflow replicates all functionality from the original Jenkins pipeline:

1. **Environment Setup**: Sets up Python 3.7 and installs dependencies from requirements.txt
2. **FAQ Processing**: Runs `chatscript.py` to process `newfaq.md` and generate Rasa training files
3. **Model Training**: Executes `rasatrain.py` to train a new Rasa model with versioned naming
4. **Model Deployment**: Uploads the trained model to Rasa X and tags it as production
5. **Website Integration**: Creates a branch in the target website repository and submits a PR with updated FAQ content

## Build Versioning

The workflow uses GitHub's `run_number` for build versioning, maintaining the same approach as the Jenkins pipeline.

## Build Retention

The workflow automatically cleans up old runs, keeping only the last 5 executions to match the Jenkins configuration.

## Triggering

The workflow triggers on:
- Push to `main` or `master` branches
- Manual workflow dispatch from the GitHub Actions UI

## Artifacts

Each workflow run creates artifacts containing:
- Trained models
- Generated FAQ files
- Training data
- Success markers

Artifacts are retained for 30 days.
