# System Prompt Factory 🏭: A Modular System Prompt Generation Utility

## Try It Out On Hugging Face Spaces!

[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/danielrosehill/System-Prompt-Factory)
[![Streamlit App](https://img.shields.io/badge/Streamlit-App-brightgreen)](https://streamlit.io/)
[![Anthropic Sonnet 3.5](https://img.shields.io/badge/Anthropic%20Sonnet-3.5-blue)](https://www.anthropic.com/models)

![alt text](screenshots/1.png)

## Description

This section provides an index of the configurable parameters in the System Prompt Factory.

## Configurable Parameters

- [System Prompt Factory 🏭: A Modular System Prompt Generation Utility](#system-prompt-factory--a-modular-system-prompt-generation-utility)
  - [Try It Out On Hugging Face Spaces!](#try-it-out-on-hugging-face-spaces)
  - [Description](#description)
  - [Configurable Parameters](#configurable-parameters)
    - [🤖 Configure AI Assistant](#-configure-ai-assistant)
      - [🎭 Core Identity](#-core-identity)
      - [💬 Communication Style](#-communication-style)
    - [👤 Set User Preferences](#-set-user-preferences)
      - [👤 Personal Profile](#-personal-profile)
      - [🌍 Context \& Background](#-context--background)
      - [🎯 Learning Preferences](#-learning-preferences)
    - [📝 Choose Output Format](#-choose-output-format)
      - [📄 Documentation Style](#-documentation-style)
      - [🔢 Data Formatting](#-data-formatting)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Repository Structure](#repository-structure)

### 🤖 Configure AI Assistant

#### 🎭 Core Identity

| Parameter     | Description                                                                 |
| ------------- | --------------------------------------------------------------------------- |
| AI Identity Type | Choose how your AI assistant should present itself |
| AI Name         | Give your AI assistant a unique name                                        |
| Base Personality   | Select the core personality trait                                         |
| Backstory       | Add a brief backstory to give your AI more character (optional) |

#### 💬 Communication Style

| Parameter     | Description                                                                 |
| ------------- | --------------------------------------------------------------------------- |
| Formality Level | Adjust how formal or casual the AI should be |
| Expertise Level   | Set the depth of knowledge and explanation                                         |
| Response Style       | How should the AI structure its responses? |
| Language Style | Choose the linguistic style |

### 👤 Set User Preferences

#### 👤 Personal Profile

| Parameter     | Description                                                                 |
| ------------- | --------------------------------------------------------------------------- |
| Name (optional) | Your preferred name for personalized interactions |
| Age Group   | Help the AI adjust its communication style                                         |
| Occupation       | Helps the AI provide relevant examples |

#### 🌍 Context & Background

| Parameter     | Description                                                                 |
| ------------- | --------------------------------------------------------------------------- |
| Cultural Context | Adapt responses to your cultural background |
| Worldview   | Choose a philosophical perspective                                         |
| Political Perspective       | Select your preferred political framing |
| Interaction Style | How would you like the AI to interact with you? |

#### 🎯 Learning Preferences

| Parameter     | Description                                                                 |
| ------------- | --------------------------------------------------------------------------- |
| Learning Approach | How do you prefer to learn new information? |
| Communication Pace   | How detailed should the responses be?                                         |

### 📝 Choose Output Format

#### 📄 Documentation Style

| Parameter     | Description                                                                 |
| ------------- | --------------------------------------------------------------------------- |
| Documentation Structure | How should information be organized and presented? |

#### 🔢 Data Formatting

| Parameter     | Description                                                                 |
| ------------- | --------------------------------------------------------------------------- |
| Data Structure | Choose how structured data should be presented |

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/streamlit.git
   cd streamlit
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
