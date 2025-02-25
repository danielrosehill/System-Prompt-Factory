import os
import streamlit as st
import streamlit.components.v1 as components
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
    # Initialize session state
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = 0

    st.set_page_config(
        page_title="System Prompt Factory",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://github.com/All-Hands-AI/OpenHands',
            'About': 'System Prompt Factory - Enhanced by OpenHands'
        }
    )
    
    # Set sidebar width and ensure it's always expanded
    st.markdown("""
        <style>
        section[data-testid="stSidebar"] {
            width: 350px !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Custom CSS for better styling
    st.markdown("""
        <style>
        .main {
            padding: 2rem;
        }
        .stButton button {
            border-radius: 20px;
        }
        .stExpander {
            border: none !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header with improved design
    st.markdown("""
        <div style='text-align: center; padding: 2rem 0; background: linear-gradient(135deg, #f6f8fa, #e9ecef); border-radius: 15px; margin-bottom: 2rem;'>
            <h1 style='color: #1a1a1a; margin-bottom: 1rem;'>🎯 System Prompt Factory</h1>
            <p style='color: #666; font-size: 1.2em; max-width: 600px; margin: 0 auto;'>
                Create perfectly tailored AI system prompts
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Add welcome message
    st.markdown("""
        <div style='text-align: center; margin: 2rem 0;'>
            <p style='color: #666; font-size: 1.1em; margin-bottom: 2rem;'>
                Follow the steps in the sidebar to create your perfect AI assistant. 
                Each step builds upon the last to create a comprehensive system prompt.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
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
    
    # Style tabs
    st.markdown("""
        <style>
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding: 8px 16px;
            border-radius: 4px;
        }
        
        .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
            background: rgba(25, 118, 210, 0.1);
            border-bottom: none;
            color: rgb(25, 118, 210);
            font-weight: 600;
        }
        </style>
    """, unsafe_allow_html=True)

    # Create sections using tabs with active tab from session state
    tab_titles = ["🤖 Configure AI Assistant", "👤 Set User Preferences", "📝 Choose Output Format"]
    tabs = st.tabs(tab_titles)
    
    # Ensure the correct tab is shown based on sidebar selection
    current_tab = st.session_state.active_tab
    
    with tabs[0]:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #e3f2fd, #bbdefb); padding: 1.5rem; border-radius: 10px; margin-bottom: 1.5rem;'>
            <h2 style='color: #1565c0; margin: 0; font-size: 1.5em;'>AI Identity & Behavior</h2>
            <p style='color: #1565c0; margin-top: 0.5rem; margin-bottom: 0;'>Configure how your AI assistant should present itself and interact</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create three sections with cards
        st.markdown("""
        <div style='display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem;'>
            <div style='background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
                <h3 style='color: #1565c0; font-size: 1.2em; margin-bottom: 1rem;'>🎭 Core Identity</h3>
            </div>
            <div style='background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
                <h3 style='color: #1565c0; font-size: 1.2em; margin-bottom: 1rem;'>💬 Communication Style</h3>
            </div>
            <div style='background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
                <h3 style='color: #1565c0; font-size: 1.2em; margin-bottom: 1rem;'>🎨 Personality & Expression</h3>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Core Identity Section
        with st.container():
            st.markdown("##### Core Identity Settings")
            identity_type = st.selectbox(
                "AI Identity Type",
                options=available_prompts["model_identity"],
                help="Choose how your AI assistant should present itself",
                format_func=lambda x: {
                    "neutral": "🤖 Standard AI Assistant",
                    "bot": "⚡ Proud AI Bot",
                    "alien": "👽 Extraterrestrial Intelligence",
                    "sloth": "🦥 Laid-back Sloth"
                }.get(x, "🤖 " + x.replace("_", " ").title())
            )
            
            col1, col2 = st.columns(2)
            with col1:
                ai_name = st.text_input(
                    "AI Name",
                    help="Give your AI assistant a unique name",
                    placeholder="e.g., Atlas, Nova, Sage"
                )
            
            with col2:
                personality = st.selectbox(
                    "Base Personality",
                    options=available_prompts["model_personalities"],
                    help="Select the core personality trait",
                    format_func=lambda x: "😊 " + x.replace("_", " ").title()
                )

            backstory = st.text_area(
                "Backstory (optional)",
                help="Add a brief backstory to give your AI more character",
                placeholder="e.g., Created in a secret lab beneath Mount Everest...",
                max_chars=200,
                height=100
            )

        st.divider()

        # Communication Style Section
        st.markdown("##### Communication Preferences")
        col1, col2 = st.columns(2)
        
        with col1:
            formality = st.select_slider(
                "Formality Level",
                options=available_prompts["model_formality"],
                help="Adjust how formal or casual the AI should be",
                format_func=lambda x: x.replace("_", " ").title()
            )
            
            expertise = st.select_slider(
                "Expertise Level",
                options=available_prompts["model_expertise"],
                help="Set the depth of knowledge and explanation",
                format_func=lambda x: x.replace("_", " ").title()
            )

        with col2:
            response_style = st.selectbox(
                "Response Style",
                options=available_prompts["model_response_style"],
                help="How should the AI structure its responses?",
                format_func=lambda x: x.replace("_", " ").title()
            )

            language_style = st.selectbox(
                "Language Style",
                options=available_prompts["model_language_style"],
                help="Choose the linguistic style",
                format_func=lambda x: {
                    "neutral": "🔤 Modern English",
                    "shakespearean": "📜 Shakespearean",
                    "middle_ages": "⚔️ Medieval",
                    "rhyming": "🎵 Rhyming"
                }.get(x, "🔤 " + x.replace("_", " ").title())
            )

    with tabs[1]:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #e8f5e9, #c8e6c9); padding: 1.5rem; border-radius: 10px; margin-bottom: 1.5rem;'>
            <h2 style='color: #2e7d32; margin: 0; font-size: 1.5em;'>User Preferences</h2>
            <p style='color: #2e7d32; margin-top: 0.5rem; margin-bottom: 0;'>Customize how the AI understands and interacts with you</p>
        </div>
        """, unsafe_allow_html=True)

        # Create three card sections
        st.markdown("""
        <div style='display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem;'>
            <div style='background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
                <h3 style='color: #2e7d32; font-size: 1.2em; margin-bottom: 1rem;'>👤 Personal Profile</h3>
            </div>
            <div style='background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
                <h3 style='color: #2e7d32; font-size: 1.2em; margin-bottom: 1rem;'>🌍 Context & Background</h3>
            </div>
            <div style='background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
                <h3 style='color: #2e7d32; font-size: 1.2em; margin-bottom: 1rem;'>🎯 Learning Preferences</h3>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Personal Profile Section
        st.markdown("##### Personal Information")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            user_name = st.text_input(
                "Name (optional)",
                help="Your preferred name for personalized interactions",
                placeholder="e.g., John Doe"
            )
        
        with col2:
            age_group = st.selectbox(
                "Age Group",
                options=["", "Under 18", "18-25", "26-35", "36-50", "51+"],
                help="Help the AI adjust its communication style",
                format_func=lambda x: "🔹 " + (x if x else "Not specified")
            )
        
        with col3:
            occupation = st.text_input(
                "Occupation",
                help="Helps the AI provide relevant examples",
                placeholder="e.g., Software Engineer"
            )

        st.divider()

        # Context & Background Section
        st.markdown("##### Cultural & Perspective Settings")
        col1, col2 = st.columns(2)
        
        with col1:
            location = st.selectbox(
                "Cultural Context",
                options=available_prompts["user_geolocation"],
                help="Adapt responses to your cultural background",
                format_func=lambda x: "🌍 " + x.replace("_", " ").title()
            )
            
            worldview = st.selectbox(
                "Worldview",
                options=available_prompts["user_worldview"],
                help="Choose a philosophical perspective",
                format_func=lambda x: "🔮 " + x.replace("_", " ").title()
            )

        with col2:
            political_leaning = st.selectbox(
                "Political Perspective",
                options=available_prompts["user_political_leaning"],
                help="Select your preferred political framing",
                format_func=lambda x: "⚖️ " + x.replace("_", " ").title()
            )

            user_type = st.selectbox(
                "Interaction Style",
                options=available_prompts["user_personality"],
                help="How would you like the AI to interact with you?",
                format_func=lambda x: "🤝 " + x.replace("_", " ").title()
            )

        st.divider()

        # Learning Preferences Section
        st.markdown("##### Learning & Communication Style")
        col1, col2 = st.columns(2)
        
        with col1:
            learning_style = st.select_slider(
                "Learning Approach",
                options=available_prompts["user_learning_style"],
                help="How do you prefer to learn new information?",
                format_func=lambda x: x.replace("_", " ").title()
            )

        with col2:
            communication_pace = st.select_slider(
                "Communication Pace",
                options=available_prompts["user_communication_pace"],
                help="How detailed should the responses be?",
                format_func=lambda x: x.replace("_", " ").title()
            )

    
    with tabs[2]:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #fff3e0, #ffe0b2); padding: 1.5rem; border-radius: 10px; margin-bottom: 1.5rem;'>
            <h2 style='color: #e65100; margin: 0; font-size: 1.5em;'>Output Format</h2>
            <p style='color: #e65100; margin-top: 0.5rem; margin-bottom: 0;'>Customize how the AI should structure and present information</p>
        </div>
        """, unsafe_allow_html=True)

        # Create two card sections
        st.markdown("""
        <div style='display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem;'>
            <div style='background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
                <h3 style='color: #e65100; font-size: 1.2em; margin-bottom: 1rem;'>📄 Documentation Style</h3>
            </div>
            <div style='background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
                <h3 style='color: #e65100; font-size: 1.2em; margin-bottom: 1rem;'>🔢 Data Format</h3>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Documentation Format Section
        st.markdown("##### Documentation Preferences")
        doc_style = st.select_slider(
            "Documentation Structure",
            options=available_prompts["user_output_preference"],
            help="How should information be organized and presented?",
            format_func=lambda x: x.replace("_", " ").title()
        )

        st.divider()

        # Data Structure Section
        st.markdown("##### Data Formatting")
        data_format = st.select_slider(
            "Data Structure",
            options=["neutral", "data_format"],
            help="Choose how structured data should be presented",
            format_func=lambda x: {
                "neutral": "Standard Text Format",
                "data_format": "Strict Data Format (CSV, JSON, etc.)"
            }.get(x, x.replace("_", " ").title())
        )
    
    # Final section with generate button and results
    st.markdown("""
    <div style='background: linear-gradient(135deg, #f8f9fa, #e9ecef); padding: 2rem; border-radius: 15px; margin: 2rem 0; text-align: center;'>
        <h2 style='color: #1a1a1a; margin-bottom: 1rem; font-size: 1.5em;'>🎯 Ready to Create Your System Prompt?</h2>
        <p style='color: #666; margin-bottom: 1.5rem; font-size: 1.1em;'>Review your settings and generate your customized prompt</p>
        <div style='display: flex; justify-content: center; gap: 1rem; max-width: 600px; margin: 0 auto;'>
    """, unsafe_allow_html=True)

    # Create a row for the action buttons
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if st.button("✨ Generate System Prompt", type="primary", use_container_width=True):
            generate_prompt = True
        
    with col2:
        if st.button("↺ Reset All", type="secondary", use_container_width=True, on_click=reset_all_fields):
            st.rerun()
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
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
            user_name=user_name,
            age_group=age_group,
            occupation=occupation,
            target_length=target_length if target_length > 0 else None
        )
        
        # Results section with improved design
        st.markdown("""
        <div style='background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); margin: 2rem 0;'>
            <h3 style='color: #1a1a1a; margin-bottom: 1.5rem; font-size: 1.3em;'>🎨 Generated System Prompt</h3>
        </div>
        """, unsafe_allow_html=True)

        # Create tabs for different views with custom styling
        tab_style = """
        <style>
        .stTabs [data-baseweb="tab-list"] {
            gap: 16px;
        }
        .stTabs [data-baseweb="tab"] {
            padding: 8px 16px;
            border-radius: 4px;
        }
        </style>
        """
        st.markdown(tab_style, unsafe_allow_html=True)
        
        raw_tab, refined_tab = st.tabs(["📝 Base Prompt", "✨ AI-Enhanced Version"])
        
        with raw_tab:
            st.markdown("##### Generated from your selections")
            display_prompt_preview(combined_prompt)
            
            col1, col2 = st.columns([1, 2])
            with col1:
                if st.button("📋 Copy Prompt", type="secondary", use_container_width=True):
                    st.toast("✅ Prompt copied to clipboard!")
            with col2:
                st.markdown(get_download_link(combined_prompt), unsafe_allow_html=True)
        
        with refined_tab:
            if api_key:
                st.markdown("##### Enhanced by AI for natural flow")
                with st.spinner("✨ Enhancing your prompt with AI..."):
                    refined_prompt = refine_with_openai(combined_prompt, api_key)
                display_prompt_preview(refined_prompt)
                
                col1, col2 = st.columns([1, 2])
                with col1:
                    if st.button("📋 Copy Enhanced", type="secondary", use_container_width=True):
                        st.toast("✅ Enhanced prompt copied to clipboard!")
                with col2:
                    st.markdown(get_download_link(refined_prompt, "enhanced_system_prompt.txt"), unsafe_allow_html=True)
            else:
                st.info("💡 Enter your OpenAI API key in the sidebar to enable AI enhancement of your prompt.")
    
    # Add footer with improved design
    st.markdown("""
    <div style='background: linear-gradient(135deg, #f8f9fa, #e9ecef); 
         margin-top: 4rem; 
         padding: 2rem; 
         border-radius: 15px; 
         text-align: center;'>
        <p style='color: #666; font-size: 1.1em; margin-bottom: 0.5rem;'>
            System Prompt Factory
        </p>
        <p style='color: #666; font-size: 0.9em; margin: 0;'>
            Created by <a href="https://danielrosehill.com" target="_blank" style="color: #1565c0; text-decoration: none;">Daniel Rosehill</a> 
            in collaboration with Claude 3.5 Sonnet
        </p>
        <p style='color: #666; font-size: 0.9em; margin-top: 0.5rem;'>
            Enhanced by <a href="https://github.com/All-Hands-AI/OpenHands" target="_blank" style="color: #1565c0; text-decoration: none;">OpenHands</a>
        </p>
        <p style='color: #999; font-size: 0.8em; margin-top: 1rem;'>
            Build version 1.0 • 
            <a href="https://github.com/danielrosehill/System-Prompt-Factory" target="_blank" style="color: #666; text-decoration: none;">Original Repo</a> • 
            <a href="https://github.com/All-Hands-AI/OpenHands" target="_blank" style="color: #666; text-decoration: none;">OpenHands</a>
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()