# System Prompt Factory: A Modular System Prompt Generation Utility

[![Streamlit App](https://img.shields.io/badge/Streamlit-App-brightgreen)](https://streamlit.io/)
[![Anthropic Sonnet 3.5](https://img.shields.io/badge/Anthropic%20Sonnet-3.5-blue)](https://www.anthropic.com/models)

## Description

System Prmopt Factory is a Streamlit application designed to generate custom but general system prompts by combining different building blocks reflecting user's personalities and desired interaction styles when working with AI systems.

The idea is to provide a convenient way to create first iterations of system prompts that move general purpose AI tools into slightly closer alignment with the very diverse types of humans who encounter them every day. 

 These building blocks represent various aspects of the user and the desired AI interaction, such as:

- User Location
- Political Views
- Personality
- Model Expertise
- Model Formality
- Model Identity
- Model Language Style
- Model Personalities
- Model Response Style
- User Communication Pace
- User Learning Style
- User Output Preference
- User Personality
- User Worldview

 

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/streamless.git
   cd streamless
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```

2. The application will open in your web browser. Use the interface to select building blocks from each category.

3. The combined system prompt will be displayed in the output area.

## Repository Structure

- `app.py`: The main Streamlit application file.
- `library/`: A Git submodule containing the original system prompts.
- `repo_library/`: Contains programmatic versions of the prompts that can be easily combined.
- `requirements.txt`: Lists the required Python packages.
- `README.md`: This file.

 
