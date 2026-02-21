# 🕰️ Legacy Lens

<p align="center">
  <img src="https://img.icons8.com/color/96/000000/time-machine.png" width="120" height="120">
</p>

<h1 align="center">Legacy Lens</h1>
<h3 align="center">See Your Ripple Through Time</h3>

<p align="center">
  <strong>ORIGIN Hackathon 2024 Official Submission</strong><br>
  <em>Exploring Human Origins • Impact • Memory • Responsibility • Legacy • Future of Humanity</em>
</p>

<p align="center">
  <a href="#-about-the-project">About</a> •
  <a href="#-features">Features</a> •
  <a href="#-built-with">Tech Stack</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-how-to-use">How to Use</a> •
  <a href="#-project-structure">Structure</a> •
  <a href="#-impact--vision">Impact</a>
</p>

---

## 📖 About The Project

**Legacy Lens** is an AI-powered web application that enables users to have meaningful conversations with their "Future Self from 2054," creating an emotional and philosophical journey through time. The app transforms abstract concepts of legacy and impact into a deeply personal, interactive experience.

Built entirely in Python, it combines cutting-edge AI with thoughtful design to help users understand their place in humanity's ongoing story. Whether you're seeking life advice, wanting to leave messages for future generations, or curious about your long-term impact, Legacy Lens offers a unique space for reflection.

---

## ✨ Features

| | Feature | Description |
|---|---------|-------------|
| 💬 | **Future Self Chat** | Conversational AI with your 30-years-older self from 2054 |
| 📜 | **Legacy Letters** | Generate and download personalized letters for future generations |
| 🌍 | **Impact Simulator** | Interactive visualization of how your choices ripple through decades |
| 📊 | **Humanity's Timeline** | See your place in the broader human journey |
| 🔄 | **Dual API Support** | Works with OpenRouter (GPT-3.5) or DeepSeek API |

---

## 🛠️ Built With

| Technology | Purpose |
|------------|---------|
| **[Streamlit](https://streamlit.io/)** | Python web framework for the entire UI |
| **[OpenRouter API](https://openrouter.ai/)** | AI backend (GPT-3.5 Turbo) - Free tier available |
| **[DeepSeek API](https://platform.deepseek.com/)** | Alternative AI backend |
| **[Plotly](https://plotly.com/)** | Interactive data visualizations |
| **[Pandas](https://pandas.pydata.org/)** | Data manipulation for impact calculations |
| **[Python](https://www.python.org/)** | Core programming language (3.8+) |

All AI processing happens via API calls - no local ML training required.

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.8 or higher** ([Download](https://www.python.org/downloads/))
- **Free API Key** from either:
  - [OpenRouter](https://openrouter.ai/keys) (Recommended - GPT-3.5 Turbo)
  - [DeepSeek](https://platform.deepseek.com/api_keys) (Alternative)

### Installation & Running

Open your terminal/command prompt and run:

```bash
# 1. Navigate to project folder
cd path/to/legacy-lens

# 2. Create virtual environment (recommended)
python -m venv venv

# 3. Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Launch the app
streamlit run app.py
