# FAQ Format Specification

## Overview

The `newfaq.md` file serves as the single source of truth for all FAQ content in the RasaUtilityTools system. This file uses a structured markdown format that enables automated processing to generate both Rasa training data and web FAQ content.

## File Structure

### Basic FAQ Entry Format
```markdown
### <main question>
intent: <rasa_intent_name>
answer: <answer>
altquestion: <alternate way to ask question for rasa NLU training data>
altquestion: <alternate way to ask question for rasa NLU training data>
altquestion: <alternate way to ask question for rasa NLU training data>
```

### Field Definitions

#### 1. Main Question (`### <question>`)
**Purpose**: Primary question displayed on website FAQ  
**Format**: Markdown heading level 3  
**Processing**: 
- Extracted and added to `faq.mdx` for web display
- Used as primary training example in `data/nlu.md`

**Example**:
```markdown
### Does your framework use Rasa?
```

#### 2. Intent Declaration (`intent: <intent_name>`)
**Purpose**: Rasa intent identifier for NLU classification  
**Format**: Plain text following `intent: ` prefix  
**Processing**:
- Converted to intent section in `data/nlu.md`
- Added to intents list in `domain.yml`
- Used for response mapping in `domain.yml`
- Referenced in conversation stories in `data/stories.md`

**Naming Convention**: Use descriptive names with underscores
```markdown
intent: faq_rasa_support
```

#### 3. Answer (`answer: <response>`)
**Purpose**: Bot response and web FAQ answer  
**Format**: Plain text following `answer: ` prefix  
**Processing**:
- Added to `faq.mdx` as FAQ answer
- Created as `utter_<intent>` response in `domain.yml`
- Referenced in conversation stories

**Example**:
```markdown
answer: Yes! Our framework was built with Rasa
```

#### 4. Alternative Questions (`altquestion: <variant>`)
**Purpose**: Training examples for robust NLU understanding  
**Format**: Plain text following `altquestion: ` prefix  
**Processing**: Added as training examples under intent in `data/nlu.md`

**Examples**:
```markdown
altquestion: What is the chatbot tool
altquestion: do you use an NLU
altquestion: Did you use rasa
```

## Complete Example

### Input (`newfaq.md`)
```markdown
### Does your framework use Rasa?
intent: faq_rasa_support
answer: Yes! Our framework was built with Rasa
altquestion: What is the chatbot tool
altquestion: do you use an NLU
altquestion: Did you use rasa 

### What is the cost or chargeback for your services?
intent: faq_cost_chargeback
answer: Currently, there is no chargeback or cost.
altquestion: What does your service cost?
altquestion: What is your chargeback policy?
altquestion: Is there a cost?
altquestion: How much does this cost?
```

### Generated Outputs

#### Web FAQ (`faq.mdx`)
```markdown
### Does your framework use Rasa?
Yes! Our framework was built with Rasa

### What is the cost or chargeback for your services?
Currently, there is no chargeback or cost.
```

#### NLU Training Data (`data/nlu.md`)
```markdown
## intent:faq_rasa_support
- Does your framework use Rasa?
- What is the chatbot tool
- do you use an NLU
- Did you use rasa

## intent:faq_cost_chargeback
- What is the cost or chargeback for your services?
- What does your service cost?
- What is your chargeback policy?
- Is there a cost?
- How much does this cost?
```

#### Domain Configuration (`domain.yml`)
```yaml
intents:
- faq_rasa_support
- faq_cost_chargeback

responses:
  utter_faq_rasa_support:
  - text: Yes! Our framework was built with Rasa
  
  utter_faq_cost_chargeback:
  - text: Currently, there is no chargeback or cost.

actions:
- utter_faq_rasa_support
- utter_faq_cost_chargeback
```

#### Conversation Stories (`data/stories.md`)
```markdown
## faq_rasa_support
* faq_rasa_support
   - utter_faq_rasa_support
   - action_restart

## faq_cost_chargeback
* faq_cost_chargeback
   - utter_faq_cost_chargeback
   - action_restart
```

## Processing Logic

### Line-by-Line Processing
The processing scripts read `newfaq.md` sequentially and apply different logic based on line content:

```python
with open("newfaq.md") as file_in:
    for line in file_in:
        if "### " in line:
            # Process main question
        elif "intent" in line:
            # Process intent declaration
        elif "altquestion:" in line:
            # Process alternative question
        elif "answer: " in line:
            # Process answer
```

### Content Transformation

#### Question Processing
```python
if "### " in line:
    question = line
    chatquestion = question.replace('### ','')
    # Add to faq.mdx if not already present
```

#### Intent Processing
```python
if "intent" in line:
    intent = line
    chatintent = intent.replace('intent: ','')
    # Add to data/nlu.md with intent header
    # Add to domain.yml intents section
```

#### Alternative Question Processing
```python
if "altquestion:" in line:
    altquestion = line
    altquestion2 = altquestion.replace('altquestion:','-')
    # Add as training example under current intent
```

#### Answer Processing
```python
if "answer: " in line:
    answer = line
    answer2 = answer.replace('answer: ','').rstrip()
    # Add to faq.mdx
    # Create utter_ response in domain.yml
    # Add to actions list
```

### Duplicate Prevention

The system implements duplicate detection to prevent content duplication:

```python
# Check if content already exists before adding
if chatquestion not in open('faq.mdx').read():
    myfile.write("\n" + question)

if chatintent not in open('./data/nlu.md').read():
    myfile.write("\n" + "## intent:" + chatintent.replace(" ", "_"))
```

## Best Practices

### Content Guidelines

#### Question Writing
- **Clear and Specific**: Write questions as users would naturally ask them
- **Avoid Ambiguity**: Ensure questions have single, clear meanings
- **Natural Language**: Use conversational tone matching user expectations

#### Intent Naming
- **Descriptive**: Use names that clearly indicate the question topic
- **Consistent**: Follow consistent naming patterns (e.g., `faq_topic_subtopic`)
- **Underscores**: Use underscores instead of spaces for technical compatibility

#### Answer Writing
- **Concise**: Provide clear, direct answers without unnecessary detail
- **Consistent Tone**: Maintain consistent voice across all answers
- **Actionable**: Include next steps or additional resources when appropriate

#### Alternative Questions
- **Variety**: Include different ways users might phrase the same question
- **Natural Variations**: Use realistic alternative phrasings
- **Coverage**: Aim for 3-5 alternatives per main question for robust training

### File Organization

#### Logical Grouping
```markdown
# Group related FAQs together
### What is Rasa?
intent: faq_rasa_definition
answer: Rasa is an open source conversational AI framework
altquestion: Tell me about Rasa
altquestion: What does Rasa do

### Does your framework use Rasa?
intent: faq_rasa_support
answer: Yes! Our framework was built with Rasa
altquestion: What is the chatbot tool
altquestion: do you use an NLU
```

#### Consistent Formatting
- Always include blank line between FAQ entries
- Maintain consistent indentation
- Use consistent capitalization in questions and answers

### Validation Checklist

Before committing changes to `newfaq.md`:

1. **Format Validation**
   - [ ] All questions start with `### `
   - [ ] All intents follow `intent: ` format
   - [ ] All answers follow `answer: ` format
   - [ ] All alternatives follow `altquestion: ` format

2. **Content Validation**
   - [ ] Intent names are unique and descriptive
   - [ ] Answers are clear and helpful
   - [ ] Alternative questions provide good training variety
   - [ ] No duplicate content across entries

3. **Technical Validation**
   - [ ] Intent names use underscores, not spaces
   - [ ] No special characters that could break processing
   - [ ] Consistent line endings and encoding

## Common Issues and Solutions

### Processing Errors

#### Missing Content
**Problem**: Generated files missing expected content  
**Cause**: Incorrect format or missing required fields  
**Solution**: Verify all FAQ entries follow exact format specification

#### Duplicate Content
**Problem**: Content appears multiple times in generated files  
**Cause**: Running processing scripts multiple times  
**Solution**: Delete generated files and rerun processing, or use version control to reset

#### Intent Conflicts
**Problem**: Multiple FAQs using same intent name  
**Cause**: Copy-paste errors or insufficient intent naming  
**Solution**: Ensure all intent names are unique across entire file

### Format Issues

#### Spacing Problems
**Problem**: Generated content has incorrect formatting  
**Cause**: Extra spaces or missing spaces in format markers  
**Solution**: Ensure exact format: `### `, `intent: `, `answer: `, `altquestion: `

#### Character Encoding
**Problem**: Special characters not processing correctly  
**Cause**: File encoding issues  
**Solution**: Ensure `newfaq.md` uses UTF-8 encoding

#### Line Ending Issues
**Problem**: Processing fails on different operating systems  
**Cause**: Different line ending formats (Windows vs Unix)  
**Solution**: Use consistent line endings (LF) across all environments

## Advanced Features

### Entity Support
While not shown in basic examples, the system supports Rasa entity annotations:

```markdown
### What is the weather in Seattle?
intent: request_weather
answer: I can help you check the weather. Let me look that up for you.
altquestion: weather in [Seattle](city)
altquestion: temperature in [New York](city)
altquestion: is it raining in [Portland](city)
```

### Multi-line Answers
For longer answers, ensure proper formatting:

```markdown
answer: Our support model includes multiple channels: GitHub issues for bug reports, documentation wiki for guides, and community forums for general questions. Response times vary by channel and issue complexity.
```

### Special Characters
Handle special characters carefully in answers:

```markdown
answer: Yes, we support API integration. Use the endpoint: https://api.example.com/v1/
```

The system will properly escape and format special characters for both web and Rasa outputs.
