# User Story Analyzer

A Streamlit application that analyzes user stories and epics using Google's Gemini AI to provide comprehensive insights for product management and agile development.

## Features

- **Acceptance Criteria Generation**: Creates clear, testable acceptance criteria for user stories
- **INVEST Analysis**: Provides story splitting suggestions based on INVEST principles (Independent, Negotiable, Valuable, Estimable, Small, Testable)
- **Critical Analysis**: Generates arguments against implementation based on:
  - Market benchmarking
  - Lean waste principles
  - ROI analysis
  - Opportunity cost assessment
  - Risk evaluation

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Gemini API Key

1. Get your Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Update the `.streamlit/secrets.toml` file:
   ```toml
   gemini_api_key = "your_actual_api_key_here"
   ```

### 3. Run the Application

```bash
streamlit run user_story_analyzer.py
```

## Usage

1. **Input Your Story**: Enter your user story or epic in the sidebar text area
2. **Click Analyze**: Press the "Analyze Story" button to start the analysis
3. **Review Results**: The application will generate three types of analysis:
   - **Acceptance Criteria**: Clear requirements and definition of done
   - **INVEST Analysis**: Story splitting recommendations
   - **Arguments Against**: Critical analysis and potential concerns

## Example User Story Format

```
As a customer, I want to be able to save my favorite products so that I can easily find and purchase them later without having to search through the entire catalog again.
```

## Output Sections

### Acceptance Criteria
- Testable requirements
- Edge cases to consider
- Success metrics
- Definition of Done

### INVEST Analysis
- Assessment against each INVEST criterion
- Story splitting suggestions
- Recommended priorities
- Dependency considerations

### Arguments Against Implementation
- Market benchmark comparisons
- Lean waste analysis
- ROI considerations
- Opportunity cost assessment
- Risk evaluation

## Requirements

- Python 3.8+
- Streamlit >= 1.28.0
- Google Generative AI >= 0.3.0
- Valid Gemini API key

## File Structure

```
vibecoding-cursor-template/
├── user_story_analyzer.py          # Main Streamlit application
├── .streamlit/
│   └── secrets.toml               # API key configuration
├── requirements.txt               # Python dependencies
└── README_user_story_analyzer.md  # This file
```

## Troubleshooting

- **API Key Error**: Ensure your Gemini API key is correctly set in `.streamlit/secrets.toml`
- **Import Error**: Make sure all dependencies are installed with `pip install -r requirements.txt`
- **Connection Issues**: Check your internet connection and API key validity

## Contributing

Feel free to enhance this tool by:
- Adding more analysis frameworks
- Improving the UI/UX
- Adding export functionality
- Integrating with other AI models
