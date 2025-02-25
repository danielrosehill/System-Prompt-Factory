"""
Dynamic loader for system prompt components.
Automatically loads all prompt components from their respective directories.
"""

import os
import importlib.util
import re

def load_module_from_file(file_path):
    """Load a Python module from a file path."""
    module_name = os.path.splitext(os.path.basename(file_path))[0]
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def load_prompts_from_directory(directory):
    """Load all prompt components from a directory."""
    prompts = {}
    if not os.path.exists(directory):
        return prompts
    
    for file in os.listdir(directory):
        if file.endswith('.py') and file != '__init__.py':
            file_path = os.path.join(directory, file)
            try:
                module = load_module_from_file(file_path)
                name = os.path.splitext(file)[0]
                if hasattr(module, 'PROMPT'):
                    prompts[name] = module.PROMPT.strip()
            except Exception as e:
                print(f"Error loading {file}: {str(e)}")
    
    return prompts

# Get the base directory for prompt components
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load all prompt components
MODEL_PERSONALITIES = load_prompts_from_directory(
    os.path.join(BASE_DIR, 'model_personalities')
)

USER_GEOLOCATION = load_prompts_from_directory(
    os.path.join(BASE_DIR, 'user_geolocation')
)

USER_PERSONALITY = load_prompts_from_directory(
    os.path.join(BASE_DIR, 'user_personality')
)

USER_WORLDVIEW = load_prompts_from_directory(
    os.path.join(BASE_DIR, 'user_worldview')
)

USER_POLITICAL_LEANING = load_prompts_from_directory(
    os.path.join(BASE_DIR, 'user_political_leaning')
)

MODEL_FORMALITY = load_prompts_from_directory(
    os.path.join(BASE_DIR, 'model_formality')
)

MODEL_RESPONSE_STYLE = load_prompts_from_directory(
    os.path.join(BASE_DIR, 'model_response_style')
)

MODEL_EXPERTISE = load_prompts_from_directory(
    os.path.join(BASE_DIR, 'model_expertise')
)

MODEL_LANGUAGE_STYLE = load_prompts_from_directory(
    os.path.join(BASE_DIR, 'model_language_style')
)

MODEL_IDENTITY = load_prompts_from_directory(
    os.path.join(BASE_DIR, 'model_identity')
)

USER_LEARNING_STYLE = load_prompts_from_directory(
    os.path.join(BASE_DIR, 'user_learning_style')
)

USER_COMMUNICATION_PACE = load_prompts_from_directory(
    os.path.join(BASE_DIR, 'user_communication_pace')
)

USER_OUTPUT_PREFERENCE = load_prompts_from_directory(
    os.path.join(BASE_DIR, 'user_output_preference')
)

def truncate_to_word_length(text: str, target_length: int) -> str:
    """
    Adjust text to reach target word length by expanding or truncating as needed.
    
    Args:
        text: The text to truncate
        target_length: Target number of words
        
    Returns:
        Truncated text maintaining key elements
    """
    if not text or target_length <= 0:
        return text
        
    sections = text.split("\n\n")
    words = text.split()
    current_length = len(words)
    
    # If we're already at target length, return as is
    if current_length == target_length:
        return text
    
    # If we need to expand
    if current_length < target_length:
        words_to_add = target_length - current_length
        expanded_sections = []
        for section in sections:
            # Add elaborative phrases to reach target length
            expanded = section
            if "You are" in section:
                expanded += " Your purpose is to assist users effectively and professionally."
            if "approach" in section:
                expanded += " This approach ensures optimal results and user satisfaction."
            expanded_sections.append(expanded)
        return "\n\n".join(expanded_sections)
    
    # If we need to reduce
    words_per_section = target_length // len(sections)
    adjusted_sections = [" ".join(section.split()[:words_per_section]) for section in sections]
    
    return "\n\n".join(adjusted_sections)

def combine_prompts(personality: str, geolocation: str, user_type: str, 
                   worldview: str, political_leaning: str = "neutral", 
                   formality: str = "neutral",
                   response_style: str = "neutral",
                   data_format: str = "neutral",
                   output_preference: str = "neutral",
                   expertise: str = "neutral",
                   learning_style: str = "neutral",
                   communication_pace: str = "neutral",
                   language_style: str = "neutral",
                   identity_type: str = "neutral",
                   ai_name: str = None,
                   backstory: str = None,
                   target_length: int = None) -> str:
    """
    Combine selected prompts from different categories into a cohesive system prompt.
    
    Args:
        personality: Key from MODEL_PERSONALITIES
        geolocation: Key from USER_GEOLOCATION
        user_type: Key from USER_PERSONALITY
        worldview: Key from USER_WORLDVIEW
        political_leaning: Key from USER_POLITICAL_LEANING
        formality: Key from MODEL_FORMALITY
        response_style: Key from MODEL_RESPONSE_STYLE
        expertise: Key from MODEL_EXPERTISE
        learning_style: Key from USER_LEARNING_STYLE
        communication_pace: Key from USER_COMMUNICATION_PACE
        target_length: Optional target word length for the final prompt
    
    Returns:
        Combined system prompt
    """
    # Only include non-neutral components
    components = [
        f"You are {ai_name}. " if ai_name else "",
        backstory + "\n" if backstory else "",
        MODEL_IDENTITY.get(identity_type, "")
        if identity_type != "neutral" else "",
        MODEL_PERSONALITIES.get(personality, "") 
        if personality != "neutral" else "",
        USER_GEOLOCATION.get(geolocation, "") 
        if geolocation != "neutral" else "",
        USER_PERSONALITY.get(user_type, "") 
        if user_type != "neutral" else "",
        USER_WORLDVIEW.get(worldview, "")
        if worldview != "neutral" else "",
        USER_POLITICAL_LEANING.get(political_leaning, "")
        if political_leaning != "neutral" else "",
        MODEL_FORMALITY.get(formality, "")
        if formality != "neutral" else "",
        MODEL_RESPONSE_STYLE.get(response_style, "")
        if response_style != "neutral" else "",
        USER_OUTPUT_PREFERENCE.get(output_preference, "")
        if output_preference != "neutral" else "",
        USER_OUTPUT_PREFERENCE.get(data_format, "")
        if data_format != "neutral" else "",
        MODEL_EXPERTISE.get(expertise, "")
        if expertise != "neutral" else "",
        USER_LEARNING_STYLE.get(learning_style, "")
        if learning_style != "neutral" else "",
        USER_COMMUNICATION_PACE.get(communication_pace, "")
        if communication_pace != "neutral" else "",
        MODEL_LANGUAGE_STYLE.get(language_style, "")
        if language_style != "neutral" else ""
    ]
    
    # Filter out empty strings
    components = [c for c in components if c]
    
    if not components:
        return "No prompt components selected."
    
    # Join components
    combined = "\n\n".join(components)
    
    # Truncate if target length specified
    if target_length and target_length > 0:
        return truncate_to_word_length(combined, target_length)
    return combined

def get_available_prompts():
    """Get all available prompt options for each category."""
    return {
        # Model characteristics and preferences
        "model_personalities": ["neutral"] + [k for k in MODEL_PERSONALITIES.keys() if k != "neutral"],
        "model_formality": ["neutral", "very_informal", "informal", "formal", "extremely_formal"],
        "model_response_style": ["neutral", "concise", "balanced", "detailed", "socratic"],
        "model_expertise": ["neutral", "generalist", "specialist", "academic", "practical"],
        "model_language_style": ["neutral", "shakespearean", "middle_ages", "rhyming"],
        "model_identity": ["neutral", "bot", "alien", "sloth"],
        
        # User characteristics
        "user_geolocation": ["neutral"] + [k for k in USER_GEOLOCATION.keys() if k != "neutral"],
        "user_personality": ["neutral"] + [k for k in USER_PERSONALITY.keys() if k != "neutral"],
        "user_worldview": ["neutral"] + [k for k in USER_WORLDVIEW.keys() if k != "neutral"],
        "user_political_leaning": ["neutral", "conservative", "progressive"],
        "user_learning_style": ["neutral", "visual", "practical", "theoretical", "sequential"],
        "user_communication_pace": ["neutral", "methodical", "dynamic", "interactive", "contemplative"],
        "user_output_preference": ["neutral"] + [k for k in USER_OUTPUT_PREFERENCE.keys() if k != "neutral"]
    }