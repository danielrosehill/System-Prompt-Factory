import os
import streamlit as st
from dotenv import load_dotenv
import base64
from openai import OpenAI
from repo_library.prompts import combine_prompts, get_available_prompts

# Load environment variables
load_dotenv()

def refine_with_openai(prompt: str, api_key: str) -> str:
    """
    Use OpenAI to refine and improve the combined prompt.
    """
    if not api_key:
        return prompt
    
    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert at crafting system prompts. Your task is to take the provided prompt components and combine them into a natural, cohesive system prompt that maintains the essence of each component while ensuring they flow together seamlessly."
                },
                {
                    "role": "user",
                    "content": f"Please refine this system prompt while maintaining its core elements:\n\n{prompt}"
                }
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error refining prompt with OpenAI: {str(e)}")
        return prompt

def get_download_link(text, filename="system_prompt.txt"):
    """Generate a download link for text content."""
    b64 = base64.b64encode(text.encode()).decode()
    return f'<a href="data:text/plain;base64,{b64}" download="{filename}" style="text-decoration: none;">📥 Download System Prompt</a>'

def reset_all_fields():
    """Reset all session state variables."""
    for key in st.session_state.keys():
        del st.session_state[key]
def display_prompt_preview(prompt: str):
    """Display a preview of the prompt with proper formatting."""
    st.code(prompt, language="markdown")

def main():
    st.set_page_config(
        page_title="System Prompt Generator",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 System Prompt Generator")
    st.write("""
    Create a custom system prompt by selecting components from each category.
    The components will be combined to create a cohesive prompt that matches your needs.
    """)
    
    # Get available prompts
    available_prompts = get_available_prompts()
    
    # OpenAI API Key input in sidebar
    with st.sidebar:
        st.subheader("OpenAI Integration")
        api_key = st.text_input(
            "OpenAI API Key (optional)",
            type="password",
            help="Enter your OpenAI API key to enable AI-powered prompt refinement"
        )
        
        st.subheader("Prompt Settings")
        target_length = st.selectbox(
            "Target Word Length",
            options=[0, 100, 200, 300, 400, 500],
            help="Set a target word length for the prompt. Select 0 for no limit.",
            format_func=lambda x: "No Limit" if x == 0 else f"{x} words"
        )
        st.divider()
        st.markdown("""
        ### About
        This tool helps you create custom system prompts by combining different components:
        - Model Personality
        - User Location/Culture
        - User Type/Background
        - Worldview/Perspective
        
        Each component adds a unique aspect to the final prompt.
        """)
    
    # Create two columns for model and user characteristics
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style='background-color: #f0f7ff; padding: 20px; border-radius: 10px;'>
        <h2 style='color: #1e88e5; font-size: 24px;'>🤖 AI Identity & Behavior</h2>
        <p>Configure the AI's identity and how it should behave</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### Identity")
        identity_type = st.selectbox(
            "How should the AI identify itself?",
            options=available_prompts["model_identity"],
            help="Select how the AI should present its identity",
            format_func=lambda x: {
                "neutral": "Standard AI Assistant",
                "bot": "Proud AI Bot",
                "alien": "Extraterrestrial Intelligence",
                "sloth": "Laid-back Sloth"
            }.get(x, x.replace("_", " ").title())
        )
        
        ai_name = st.text_input(
            "Custom AI Name (optional)",
            help="Give your AI assistant a unique name",
            placeholder="e.g., Atlas, Nova, Sage"
        )
        
        backstory = st.text_area(
            "AI Backstory (optional)",
            help="Add a one-sentence backstory for your AI",
            placeholder="e.g., Created in a secret lab beneath Mount Everest, trained on ancient texts and quantum computing.",
            max_chars=200
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("### Formality Level")
        formality = st.selectbox(
            "How formal should the AI's communication be?",
            options=available_prompts["model_formality"],
            help="Select a formality level, from very casual to extremely formal",
            format_func=lambda x: x.replace("_", " ").title()
        )

        st.markdown("### Response Style")
        response_style = st.selectbox(
            "How should responses be structured?",
            options=available_prompts["model_response_style"],
            help="Select how information should be presented and structured",
            format_func=lambda x: x.replace("_", " ").title()
        )

        st.markdown("### Expertise Level")
        expertise = st.selectbox(
            "What level of expertise should be demonstrated?",
            options=available_prompts["model_expertise"],
            help="Select the depth and specialization of knowledge",
            format_func=lambda x: x.replace("_", " ").title()
        )

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div style='border-top: 1px solid #e0e0e0; margin: 10px 0;'></div>
        """, unsafe_allow_html=True)
        
        st.markdown("### Personality")
        personality = st.selectbox(
            "How should the AI assistant behave?",
            options=available_prompts["model_personalities"],
            help="Select a personality style, or choose 'Neutral' for a balanced approach",
            format_func=lambda x: x.replace("_", " ").title()
        )
        
        st.markdown("### Language Style")
        language_style = st.selectbox(
            "How should the AI express itself?",
            options=available_prompts["model_language_style"],
            help="Select a language style, from modern to historical English",
            format_func=lambda x: {
                "neutral": "Modern English",
                "shakespearean": "Shakespearean English",
                "middle_ages": "Middle Ages English",
                "rhyming": "Always Rhyming"
            }.get(x, x.replace("_", " ").title())
        )
    
    with col2:
        st.markdown("""
        <div style='background-color: #f5f5f5; padding: 20px; border-radius: 10px;'>
        <h2 style='color: #424242; font-size: 24px;'>👤 User Preferences</h2>
        <p>Define the context and preferences for user interaction</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### Location/Culture")
        location = st.selectbox(
            "What cultural context should the AI understand?",
            options=available_prompts["user_geolocation"],
            help="Select a cultural context, or choose 'Neutral' for a culturally-agnostic approach",
            format_func=lambda x: x.replace("_", " ").title()
        )
        
        st.markdown("### Political Leaning")
        political_leaning = st.selectbox(
            "What political perspective should be considered?",
            options=available_prompts["user_political_leaning"],
            help="Select a political leaning, or choose 'Neutral' for balanced perspective",
            format_func=lambda x: x.replace("_", " ").title()
        )

        st.markdown("### Learning Style")
        learning_style = st.selectbox(
            "How do you prefer to learn and process information?",
            options=available_prompts["user_learning_style"],
            help="Select your preferred way of learning and understanding",
            format_func=lambda x: x.replace("_", " ").title()
        )

        st.markdown("### Communication Pace")
        communication_pace = st.selectbox(
            "What pace of communication works best for you?",
            options=available_prompts["user_communication_pace"],
            help="Select your preferred pace of information exchange",
            format_func=lambda x: x.replace("_", " ").title()
        )
        
        st.markdown("### Type/Background")
        user_type = st.selectbox(
            "What type of user interaction do you prefer?",
            options=available_prompts["user_personality"],
            help="Select a user interaction style, or choose 'Neutral' to adapt automatically",
            format_func=lambda x: x.replace("_", " ").title()
        )
        
        st.markdown("### Worldview")
        worldview = st.selectbox(
            "What perspective should the AI maintain?",
            options=available_prompts["user_worldview"],
            help="Select a perspective style, or choose 'Neutral' for a balanced viewpoint",
            format_func=lambda x: x.replace("_", " ").title()
        )
    
    # Add a new section for output preferences
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background-color: #fff3e0; padding: 20px; border-radius: 10px;'>
    <h2 style='color: #e65100; font-size: 24px;'>📝 Output Format Preferences</h2>
    <p>Customize how content and data should be formatted</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create two columns for output preferences
    format_col1, format_col2 = st.columns(2)
    
    with format_col1:
        st.markdown("### Documentation Style")
        doc_style = st.selectbox(
            "How should documentation be structured?",
            options=available_prompts["user_output_preference"],
            help="Select your preferred documentation format",
            format_func=lambda x: x.replace("_", " ").title()
        )
    
    with format_col2:
        st.markdown("### Data Format")
        data_format = st.selectbox(
            "How should data be formatted?",
            options=["neutral", "data_format"],
            help="Select specific data formatting rules",
            format_func=lambda x: "Standard Format" if x == "neutral" else "Strict Data Format (CSV, JSON, etc.)"
        )
    
    # Add some spacing before the generate button
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Create a row for the action buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Generate System Prompt", type="primary", use_container_width=True):
            generate_prompt = True
        
    with col2:
        if st.button("🗑️ Reset All Fields", type="secondary", use_container_width=True, on_click=reset_all_fields):
            st.rerun()
    
    if 'generate_prompt' in locals():
        # Combine selected components
        combined_prompt = combine_prompts(
            personality=personality,
            geolocation=location,
            user_type=user_type,
            worldview=worldview,
            response_style=response_style,
            expertise=expertise,
            learning_style=learning_style,
            communication_pace=communication_pace,
            political_leaning=political_leaning,
            formality=formality,
            language_style=language_style,
            identity_type=identity_type,
            ai_name=ai_name,
            backstory=backstory,
            output_preference=doc_style,
            data_format=data_format,
            target_length=target_length if target_length > 0 else None
        )
        
        # Create tabs for different views
        raw_tab, refined_tab = st.tabs(["Raw Combined Prompt", "AI-Refined Prompt"])
        
        with raw_tab:
            st.subheader("Combined Prompt Components")
            display_prompt_preview(combined_prompt)
            
            # Add copy button for raw prompt
            if st.button("Copy Raw Prompt", type="secondary"):
                st.toast("Raw prompt copied to clipboard!")
            
            # Add download button for raw prompt
            st.markdown(get_download_link(combined_prompt), unsafe_allow_html=True)
        
        with refined_tab:
            if api_key:
                st.subheader("AI-Refined Version")
                with st.spinner("Refining prompt with AI..."):
                    refined_prompt = refine_with_openai(combined_prompt, api_key)
                display_prompt_preview(refined_prompt)
                
                # Add copy button for refined prompt
                if st.button("Copy Refined Prompt", type="secondary"):
                    st.toast("Refined prompt copied to clipboard!")
                
                # Add download button for refined prompt
                st.markdown(get_download_link(refined_prompt, "refined_system_prompt.txt"), unsafe_allow_html=True)
            else:
                st.info("Enter an OpenAI API key in the sidebar to enable AI refinement.")
    
    # Add footer
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
    Created by <a href="https://danielrosehill.com" target="_blank">Daniel Rosehill</a> in collaboration with Claude 3.5 Sonnet
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()