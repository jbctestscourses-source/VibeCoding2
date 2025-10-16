import streamlit as st
import google.generativeai as genai
import os
from typing import Dict, List, Any
import json

# Configure page
st.set_page_config(
    page_title="User Story Analyzer",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #3498db;
        padding-bottom: 0.5rem;
    }
    .story-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #3498db;
        margin: 1rem 0;
    }
    .criteria-item {
        background-color: #e8f4f8;
        padding: 0.5rem;
        margin: 0.5rem 0;
        border-radius: 4px;
        border-left: 3px solid #2ecc71;
    }
    .invest-item {
        background-color: #fff3cd;
        padding: 0.5rem;
        margin: 0.5rem 0;
        border-radius: 4px;
        border-left: 3px solid #ffc107;
    }
    .argument-item {
        background-color: #f8d7da;
        padding: 0.5rem;
        margin: 0.5rem 0;
        border-radius: 4px;
        border-left: 3px solid #dc3545;
    }
</style>
""", unsafe_allow_html=True)

def initialize_gemini():
    """Initialize Gemini API with the API key from Streamlit secrets."""
    try:
        api_key = st.secrets["gemini_api_key"]
        if api_key == "your_gemini_api_key_here":
            st.error("⚠️ Please update your Gemini API key in `.streamlit/secrets.toml`")
            return None
        
        genai.configure(api_key=api_key)
        return genai.GenerativeModel('gemini-pro')
    except Exception as e:
        st.error(f"❌ Error initializing Gemini API: {str(e)}")
        return None

def generate_acceptance_criteria(model, user_story: str) -> str:
    """Generate acceptance criteria for a user story using Gemini."""
    prompt = f"""
    As a product manager, analyze the following user story and generate comprehensive acceptance criteria.
    
    User Story: "{user_story}"
    
    Please provide:
    1. Clear, testable acceptance criteria
    2. Edge cases to consider
    3. Success metrics
    4. Definition of Done
    
    Format the response in a structured way with clear sections.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating acceptance criteria: {str(e)}"

def generate_invest_analysis(model, user_story: str) -> str:
    """Generate INVEST-based story splitting suggestions using Gemini."""
    prompt = f"""
    As an agile coach, analyze the following user story using the INVEST criteria and suggest how to split it into smaller, more manageable stories.
    
    User Story: "{user_story}"
    
    INVEST Criteria:
    - Independent: Can this be developed independently?
    - Negotiable: Is the scope flexible enough for discussion?
    - Valuable: Does this deliver value to users/business?
    - Estimable: Can the team estimate effort required?
    - Small: Is this small enough to complete in a sprint?
    - Testable: Can we test this story effectively?
    
    Please provide:
    1. Assessment against each INVEST criterion
    2. Suggestions for splitting the story into smaller pieces
    3. Recommended story sizes and priorities
    4. Dependencies to consider
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating INVEST analysis: {str(e)}"

def generate_arguments_against(model, user_story: str) -> str:
    """Generate arguments against implementing the story using Gemini."""
    prompt = f"""
    As a strategic product analyst, provide critical arguments against implementing the following user story.
    Consider market benchmarks, lean waste principles, and ROI analysis.
    
    User Story: "{user_story}"
    
    Please analyze from these perspectives:
    1. Market Benchmarking: How does this compare to industry standards?
    2. Lean Waste Principles: What waste might this create?
    3. ROI Analysis: What are the potential negative returns?
    4. Opportunity Cost: What else could be built instead?
    5. Risk Assessment: What are the potential risks?
    6. Resource Allocation: Is this the best use of resources?
    
    Be thorough but constructive in your analysis.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating arguments against: {str(e)}"

def main():
    """Main Streamlit application."""
    st.markdown('<h1 class="main-header">📋 User Story Analyzer</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    This tool helps you analyze user stories and epics by:
    - Generating comprehensive acceptance criteria
    - Providing INVEST-based story splitting suggestions
    - Offering critical arguments against implementation based on market benchmarks, lean principles, and ROI
    """)
    
    # Initialize Gemini
    model = initialize_gemini()
    if model is None:
        st.stop()
    
    # Sidebar for user input
    with st.sidebar:
        st.markdown("## 📝 Input Your User Story/Epic")
        
        user_story = st.text_area(
            "Describe your user story or epic:",
            height=200,
            placeholder="As a [user type], I want [goal] so that [benefit]..."
        )
        
        analyze_button = st.button("🔍 Analyze Story", type="primary")
        
        st.markdown("---")
        st.markdown("### ℹ️ About This Tool")
        st.markdown("""
        This analyzer uses Google's Gemini AI to provide:
        - **Acceptance Criteria**: Clear, testable requirements
        - **INVEST Analysis**: Story splitting recommendations
        - **Critical Review**: Arguments against implementation
        """)
    
    # Main content area
    if analyze_button and user_story.strip():
        with st.spinner("🤖 Analyzing your user story..."):
            # Display the original story
            st.markdown('<div class="section-header">📖 Original User Story</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="story-card">{user_story}</div>', unsafe_allow_html=True)
            
            # Create tabs for different analyses
            tab1, tab2, tab3 = st.tabs(["✅ Acceptance Criteria", "🔧 INVEST Analysis", "⚠️ Arguments Against"])
            
            with tab1:
                st.markdown('<div class="section-header">Acceptance Criteria & Definition of Done</div>', unsafe_allow_html=True)
                criteria = generate_acceptance_criteria(model, user_story)
                st.markdown(criteria)
            
            with tab2:
                st.markdown('<div class="section-header">INVEST Analysis & Story Splitting</div>', unsafe_allow_html=True)
                invest_analysis = generate_invest_analysis(model, user_story)
                st.markdown(invest_analysis)
            
            with tab3:
                st.markdown('<div class="section-header">Critical Analysis: Arguments Against Implementation</div>', unsafe_allow_html=True)
                arguments = generate_arguments_against(model, user_story)
                st.markdown(arguments)
    
    elif analyze_button and not user_story.strip():
        st.warning("⚠️ Please enter a user story or epic to analyze.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #7f8c8d; margin-top: 2rem;">
        <p>Built with ❤️ using Streamlit and Google Gemini AI</p>
        <p>Make sure to update your Gemini API key in <code>.streamlit/secrets.toml</code></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
