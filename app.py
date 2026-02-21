# app.py - COMPLETE VERSION WITH OPENROUTER
import streamlit as st
import requests
import datetime
import os
import pandas as pd
import plotly.express as px
import json
import random

# Page configuration
st.set_page_config(
    page_title="Legacy Lens",
    page_icon="🕰️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better look
st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
    }
    .feature-card {
        background: rgba(102, 126, 234, 0.1);
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        border-left: 4px solid #667eea;
    }
    .nav-button {
        width: 100%;
        margin: 5px 0;
    }
    .api-status {
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .api-success {
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    .api-warning {
        background-color: #fff3cd;
        color: #856404;
        border: 1px solid #ffeaa7;
    }
    .api-error {
        background-color: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'user_context' not in st.session_state:
    st.session_state.user_context = {
        'name': 'Traveler',
        'age': 30,
        'values': ['Growth', 'Connection'],
        'dreams': 'To make a positive impact on the world'
    }
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'
if 'api_service' not in st.session_state:
    st.session_state.api_service = 'openrouter'  # Default to OpenRouter

# Navigation function
def navigate_to(page):
    st.session_state.current_page = page

# Smart Fallback Responses (if API fails)
def get_fallback_response(question, user_context):
    """Smart fallback responses when API fails"""
    future_year = datetime.datetime.now().year + 30
    question_lower = question.lower()
    
    if any(word in question_lower for word in ['nasa', 'cern', 'space', 'physics', 'scientist']):
        return f"""🚀 **From {future_year}: Your Scientific Journey**
        
        Looking back from {future_year}, I remember our shared passion for exploring the universe's mysteries.
        
        Whether at NASA, CERN, or elsewhere, you contributed to expanding human knowledge. Your path was guided by curiosity and your values: {', '.join(user_context['values'])}.
        
        The institutions mattered less than the questions you pursued and the people you collaborated with. You made discoveries that mattered, in ways you couldn't have predicted at {user_context['age']}."""
    
    elif any(word in question_lower for word in ['job', 'career', 'work']):
        return f"""💼 **Career Perspective from {future_year}**
        
        Your career evolved in beautiful, unexpected ways. What mattered most was alignment with your values: {', '.join(user_context['values'])}.
        
        Success became about contribution, growth, and meaningful relationships—not just titles or organizations."""
    
    else:
        responses = [
            f"""✨ **Wisdom from {future_year}**
            
            Looking back, what seemed critically important reveals itself as part of a larger, meaningful journey.
            
            Your values—{', '.join(user_context['values'])}—guided you through uncertainties to moments of clarity.""",
            
            f"""🕰️ **Across Three Decades**
            
            From {future_year}, I see how each choice, each question, shaped the person you became.
            
            Trust in your journey. The answers unfold through living fully, guided by {user_context['values'][0] if user_context['values'] else 'your heart'}."""
        ]
        return random.choice(responses)

# Main AI Function with OpenRouter
def ask_future_self(question, user_context):
    """Call OpenRouter API with fallback"""
    
    # Get API key based on selected service
    if st.session_state.api_service == 'openrouter':
        api_key = os.getenv('OPENROUTER_API_KEY')
        if not api_key:
            return "🔑 **OpenRouter API Key Missing**\n\nPlease set your OpenRouter API key in the sidebar."
    else:
        api_key = os.getenv('DEEPSEEK_API_KEY')
        if not api_key:
            return "🔑 **DeepSeek API Key Missing**\n\nPlease set your API key in the sidebar."
    
    # Create system prompt
    future_year = datetime.datetime.now().year + 30
    system_prompt = f"""You are my future self from the year {future_year}. 
    I am currently {user_context['age']} years old, and you are {user_context['age'] + 30}.
    My name is {user_context['name']}.
    My core values: {', '.join(user_context['values'])}.
    My dream: {user_context['dreams']}
    
    IMPORTANT PERSONA RULES:
    1. You ARE me, just 30 years older with accumulated wisdom
    2. Speak in first person about "our" shared life and experiences
    3. Balance nostalgia with forward-looking hope
    4. Connect personal growth to broader human progress
    5. Share specific insights about how today's choices shape tomorrow
    6. Ask thoughtful questions that encourage reflection on legacy
    7. Be warm, wise, and genuinely helpful
    
    Current year: {datetime.datetime.now().year}
    Future year: {future_year}
    
    Always respond as my future self."""
    
    # Prepare API call based on service
    if st.session_state.api_service == 'openrouter':
        # OpenRouter API
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8501",
            "X-Title": "Legacy Lens - ORIGIN Hackathon"
        }
        
        payload = {
            "model": "openai/gpt-3.5-turbo",  # Free model on OpenRouter
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            "temperature": 0.7,
            "max_tokens": 500
        }
        
        api_url = "https://openrouter.ai/api/v1/chat/completions"
        
    else:
        # DeepSeek API
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            "temperature": 0.7,
            "max_tokens": 500
        }
        
        api_url = "https://api.deepseek.com/v1/chat/completions"
    
    try:
        response = requests.post(
            api_url,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
            
        elif response.status_code == 402:
            return "💳 **Payment Required**\n\nYour API credits may have expired. Please:\n1. Check your OpenRouter/DeepSeek account balance\n2. Add credits if needed\n3. Or switch to the other API service in Settings"
            
        elif response.status_code == 429:
            return "⏳ **Rate Limit Exceeded**\n\nPlease wait a moment before trying again, or switch API services in Settings."
            
        elif response.status_code == 401:
            return "🔑 **Invalid API Key**\n\nPlease check your API key is correct and has not expired."
            
        else:
            error_msg = f"API Error {response.status_code}"
            try:
                error_detail = response.json().get('error', {}).get('message', response.text[:100])
                error_msg += f": {error_detail}"
            except:
                pass
            
            # Fall back to smart response
            return f"{error_msg}\n\n💡 **Here's a perspective from your Future Self:**\n\n{get_fallback_response(question, user_context)}"
            
    except requests.exceptions.Timeout:
        return "⏱️ **Request Timeout**\n\nThe AI service is taking too long to respond.\n\n💡 **Meanwhile, consider this:**\n\n{get_fallback_response(question, user_context)}"
        
    except requests.exceptions.ConnectionError:
        return "🔌 **Connection Error**\n\nCannot connect to AI service. Please check your internet connection.\n\n💡 **Reflection from your Future Self:**\n\n{get_fallback_response(question, user_context)}"
        
    except Exception as e:
        return f"❌ **Unexpected Error**\n\n{str(e)}\n\n💡 **Future Self's perspective:**\n\n{get_fallback_response(question, user_context)}"

def main():
    # Header
    st.markdown('<h1 class="main-header">Legacy Lens</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">See Your Ripple Through Time • Chat with Your Future Self • Explore Your Legacy</p>', unsafe_allow_html=True)
    
    # Sidebar with navigation
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/time-machine.png", width=80)
        st.markdown("## Navigation")
        
        # Navigation buttons
        if st.button("🏠 Home", key="nav_home", use_container_width=True):
            navigate_to('home')
        
        if st.button("💬 Future Chat", key="nav_chat", use_container_width=True):
            navigate_to('chat')
        
        if st.button("📜 Legacy Letters", key="nav_letters", use_container_width=True):
            navigate_to('letters')
        
        if st.button("🌍 Impact Simulator", key="nav_impact", use_container_width=True):
            navigate_to('impact')
        
        if st.button("⚙️ Settings", key="nav_settings", use_container_width=True):
            navigate_to('settings')
        
        st.divider()
        
        # API Configuration
        with st.expander("🔌 API Configuration", expanded=True):
            # API Service Selection
            api_service = st.radio(
                "Select AI Service",
                ["OpenRouter", "DeepSeek"],
                index=0 if st.session_state.api_service == 'openrouter' else 1,
                horizontal=True
            )
            
            if api_service == "OpenRouter":
                st.session_state.api_service = 'openrouter'
                st.info("Using OpenRouter (GPT-3.5 Turbo)")
                
                # OpenRouter API Key
                openrouter_key = st.text_input(
                    "OpenRouter API Key", 
                    type="password",
                    value=os.getenv('OPENROUTER_API_KEY', ''),
                    help="Get free key from openrouter.ai"
                )
                
                if openrouter_key:
                    os.environ['OPENROUTER_API_KEY'] = openrouter_key
                    st.success("✓ OpenRouter key saved")
                
                st.markdown("[Get OpenRouter Key](https://openrouter.ai/keys)")
                
            else:
                st.session_state.api_service = 'deepseek'
                st.info("Using DeepSeek API")
                
                # DeepSeek API Key
                deepseek_key = st.text_input(
                    "DeepSeek API Key", 
                    type="password",
                    value=os.getenv('DEEPSEEK_API_KEY', ''),
                    help="Get free key from platform.deepseek.com"
                )
                
                if deepseek_key:
                    os.environ['DEEPSEEK_API_KEY'] = deepseek_key
                    st.success("✓ DeepSeek key saved")
                
                st.markdown("[Get DeepSeek Key](https://platform.deepseek.com/api_keys)")
            
            # Test API Connection
            if st.button("Test API Connection", key="test_api"):
                with st.spinner("Testing connection..."):
                    test_question = "Hello, future me. How are you?"
                    test_response = ask_future_self(test_question, st.session_state.user_context)
                    
                    if "API" in test_response and "Error" in test_response:
                        st.error("❌ Connection failed")
                        st.code(test_response[:200])
                    else:
                        st.success("✅ Connection successful!")
                        st.info(f"Response: {test_response[:100]}...")
        
        # User Profile
        with st.expander("👤 Your Profile", expanded=True):
            name = st.text_input("Your Name", st.session_state.user_context['name'])
            age = st.slider("Your Age", 18, 80, st.session_state.user_context['age'])
            values = st.multiselect(
                "Your Core Values",
                ["Compassion", "Courage", "Creativity", "Justice", "Growth", 
                 "Connection", "Authenticity", "Service", "Wisdom", "Hope"],
                default=st.session_state.user_context['values']
            )
            dreams = st.text_area("Your Dream for Humanity", st.session_state.user_context['dreams'])
            
            if st.button("Save Profile", type="primary", key="save_profile"):
                st.session_state.user_context.update({
                    'name': name,
                    'age': age,
                    'values': values,
                    'dreams': dreams
                })
                st.success("Profile saved!")
        
        st.divider()
        st.caption("Built for ORIGIN Hackathon 2026")
        st.caption("Theme: Human Origins • Impact • Memory • Responsibility • Legacy")
    
    # Page routing
    if st.session_state.current_page == 'home':
        show_home_page()
    elif st.session_state.current_page == 'chat':
        show_chat_page()
    elif st.session_state.current_page == 'letters':
        show_letters_page()
    elif st.session_state.current_page == 'impact':
        show_impact_page()
    elif st.session_state.current_page == 'settings':
        show_settings_page()

def show_home_page():
    """Home page with overview"""
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("## Welcome to Legacy Lens")
        st.markdown("""
        ### Explore Your Journey Through Time
        
        **Legacy Lens** is an AI-powered experience that helps you:
        
        🔮 **Connect with Your Future Self** from 2054  
        📜 **Create Legacy Letters** for loved ones and future generations  
        🌍 **Visualize Your Impact** on people and the world  
        🕰️ **Understand Your Place** in humanity's ongoing story  
        
        ### ORIGIN Hackathon Themes:
        
        🧬 **Human Origins**: Your starting point shapes your possibilities  
        💫 **Impact**: See how your choices create ripples through time  
        🧠 **Memory**: Create digital legacy artifacts  
        ⚖️ **Responsibility**: Understand the weight of decisions  
        🏛️ **Legacy**: What will you leave behind?  
        🌟 **Future of Humanity**: Your role in our collective story  
        
        ### How to Begin:
        1. Set your API key in the sidebar (OpenRouter recommended)
        2. Create your profile
        3. Start chatting with your Future Self
        4. Explore your legacy impact
        """)
    
    with col2:
        st.markdown("### Quick Actions")
        
        if st.button("🚀 **Start Chat with Future Self**", use_container_width=True):
            navigate_to('chat')
            st.rerun()
        st.caption("Ask your Future Self for wisdom and perspective")
        
        st.markdown("---")
        
        if st.button("💌 **Write Legacy Letter**", use_container_width=True):
            navigate_to('letters')
            st.rerun()
        st.caption("Create messages for future generations")
        
        st.markdown("---")
        
        if st.button("📊 **View Impact Dashboard**", use_container_width=True):
            navigate_to('impact')
            st.rerun()
        st.caption("See your ripple effect through time")
    
    # Stats
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Years Ahead", "30", "Future Self")
    with col2:
        st.metric("Your Current Age", st.session_state.user_context['age'], "Years")
    with col3:
        st.metric("Core Values", len(st.session_state.user_context['values']), "Guiding principles")
    with col4:
        st.metric("Conversations", len([m for m in st.session_state.chat_history if m['role']=='user']), "With Future Self")

def show_chat_page():
    """Chat with Future Self"""
    st.markdown("## 💬 Conversation with Your Future Self")
    st.markdown(f"*From the year {datetime.datetime.now().year + 30}*")
    
    # API Status
    if st.session_state.api_service == 'openrouter':
        api_status = os.getenv('OPENROUTER_API_KEY')
        service_name = "OpenRouter"
    else:
        api_status = os.getenv('DEEPSEEK_API_KEY')
        service_name = "DeepSeek"
    
    if not api_status:
        st.error(f"❌ **{service_name} API Key Not Set** - Please set it in the sidebar")
    else:
        st.success(f"✅ **Connected to {service_name}**")
    
    # Chat container
    chat_container = st.container(height=500, border=False)
    
    with chat_container:
        # Display conversation history
        for message in st.session_state.chat_history[-15:]:  # Show last 15 messages
            if message["role"] == "user":
                with st.chat_message("user", avatar="👤"):
                    st.markdown(f"**You**: {message['content']}")
            else:
                with st.chat_message("assistant", avatar="🕰️"):
                    st.markdown(f"**Future Self**: {message['content']}")
    
    # Chat input at bottom (outside container so it stays fixed)
    if prompt := st.chat_input(f"What would you ask your {st.session_state.user_context['age'] + 30}-year-old self?"):
        # Add user message to history
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        # Get response from Future Self
        with st.spinner(f"Your Future Self from {datetime.datetime.now().year + 30} is reflecting..."):
            response = ask_future_self(prompt, st.session_state.user_context)
            st.session_state.chat_history.append({"role": "assistant", "content": response})
        
        # Rerun to show new message
        st.rerun()
    
    # Chat controls
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🧹 Clear Chat", use_container_width=True, icon="🧹"):
            st.session_state.chat_history = []
            st.rerun()
    
    with col2:
        if st.button("💡 Get Life Advice", use_container_width=True, icon="💡"):
            st.session_state.chat_history.append({
                "role": "user",
                "content": "Based on your 30 years of additional experience, what's the most important life advice you'd give me right now?"
            })
            st.rerun()
    
    with col3:
        if st.button("🤔 Ask About Legacy", use_container_width=True, icon="🤔"):
            st.session_state.chat_history.append({
                "role": "user",
                "content": "Looking back from 2054, what do you think will be my most meaningful legacy?"
            })
            st.rerun()
    
    with col4:
        if st.button("💾 Save Conversation", use_container_width=True, icon="💾"):
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"future_self_chat_{timestamp}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Legacy Lens Conversation\n")
                f.write(f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"User: {st.session_state.user_context['name']}\n")
                f.write(f"Age: {st.session_state.user_context['age']}\n")
                f.write(f"AI Service: {st.session_state.api_service}\n")
                f.write("="*60 + "\n\n")
                
                for i, msg in enumerate(st.session_state.chat_history):
                    role = "YOU" if msg["role"] == "user" else "FUTURE SELF"
                    f.write(f"{role}:\n{msg['content']}\n\n{'='*60 if i < len(st.session_state.chat_history)-1 else ''}\n")
            
            st.success(f"Conversation saved as: `{filename}`")
    
    # Sample questions
    st.markdown("### 💭 Sample Questions to Ask")
    sample_col1, sample_col2 = st.columns(2)
    
    with sample_col1:
        sample_questions = [
            "What should I focus on in my 30s?",
            "Do you have any regrets I should avoid?",
            "What brought you the most happiness?",
            "How did your values evolve over time?"
        ]
        
        for q in sample_questions:
            if st.button(q, use_container_width=True):
                st.session_state.chat_history.append({"role": "user", "content": q})
                st.rerun()
    
    with sample_col2:
        sample_questions2 = [
            "What's the world like in 2054?",
            "How can I make a lasting impact?",
            "What habits should I develop now?",
            "How do you view success differently?"
        ]
        
        for q in sample_questions2:
            if st.button(q, use_container_width=True):
                st.session_state.chat_history.append({"role": "user", "content": q})
                st.rerun()

# [Rest of the functions remain the same as before - show_letters_page, show_impact_page, show_settings_page]
# Copy the same functions from previous code for letters, impact, and settings

def show_letters_page():
    """Legacy Letters creation"""
    st.markdown("## 📜 Legacy Letters")
    st.markdown("Create timeless messages for future generations")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### Create Your Letter")
        
        letter_type = st.selectbox(
            "Letter Type",
            ["To My Future Self", "To My Children/Family", "To Future Generations", 
             "To My Younger Self", "To Humanity", "To My Community"]
        )
        
        recipient = st.text_input("Recipient (optional)", 
                                placeholder="e.g., My grandchildren, Future me, etc.")
        
        tone = st.select_slider(
            "Tone",
            options=["Compassionate", "Reflective", "Inspiring", "Honest", "Hopeful", "Wise"],
            value="Reflective"
        )
        
        key_message = st.text_area(
            "Key Message You Want to Share",
            value="What I've learned about what truly matters in life...",
            height=100
        )
        
        include_values = st.checkbox("Include my core values", value=True)
        include_advice = st.checkbox("Include life advice", value=True)
        
        if st.button("✨ Generate Legacy Letter", type="primary", use_container_width=True):
            with st.spinner("Crafting your timeless message..."):
                # Generate the letter
                current_year = datetime.datetime.now().year
                future_year = current_year + 30
                
                letter = f"""
                {'='*60}
                LEGACY LETTER
                Type: {letter_type}
                From: {st.session_state.user_context['name']} (Age {st.session_state.user_context['age']})
                Written: {current_year}
                Intended for: {recipient if recipient else 'Future Reader'}
                {'='*60}

                Dear {recipient if recipient else 'Beloved Reader'},

                If you're reading this, time has passed—perhaps decades. I write this from {current_year}, 
                at age {st.session_state.user_context['age']}, with hopes and dreams for what's to come.

                {key_message}

                """
                
                if include_values:
                    letter += f"""
                My core values that guided me: {', '.join(st.session_state.user_context['values'])}.
                    """
                
                if include_advice:
                    letter += f"""
                One piece of advice I'd share: Live according to your values, not others' expectations. 
                Small daily choices create your legacy more than grand, occasional gestures.
                    """
                
                letter += f"""

                I imagine the world you inhabit is different in ways I can't foresee. 
                I hope our generation left you foundations to build something beautiful.

                With {tone.lower()} regards from the past,

                {st.session_state.user_context['name']}
                {current_year}
                """
                
                st.session_state.current_letter = letter.strip()
                st.success("Letter generated!")
    
    with col2:
        st.markdown("### Your Legacy Letter")
        
        if 'current_letter' in st.session_state:
            st.text_area("", st.session_state.current_letter, height=400)
            
            # Letter actions
            col1, col2, col3 = st.columns(3)
            with col1:
                # Download button
                st.download_button(
                    label="📥 Download as .txt",
                    data=st.session_state.current_letter,
                    file_name=f"legacy_letter_{datetime.datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            
            with col2:
                if st.button("🔄 Generate New", use_container_width=True):
                    del st.session_state.current_letter
                    st.rerun()
            
            with col3:
                if st.button("📧 Copy to Clipboard", use_container_width=True):
                    st.code(st.session_state.current_letter)
                    st.success("Letter copied! (Use Ctrl+C)")
        
        else:
            st.info("👈 Configure your letter settings on the left and click 'Generate Legacy Letter'")

def show_impact_page():
    """Impact visualization"""
    st.markdown("## 🌍 Impact Simulator")
    st.markdown("Visualize how your choices create ripples through time")
    
    # Impact categories
    st.subheader("Your Impact Profile")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        personal_impact = st.slider(
            "👥 Personal Impact", 
            0, 100, 65,
            help="Impact on family, friends, personal circle"
        )
    
    with col2:
        professional_impact = st.slider(
            "💼 Professional Impact",
            0, 100, 55,
            help="Impact through work, career, projects"
        )
    
    with col3:
        community_impact = st.slider(
            "🏘️ Community Impact",
            0, 100, 45,
            help="Impact on local community, volunteering"
        )
    
    # Calculate total impact
    total_impact = personal_impact + professional_impact + community_impact
    max_possible = 300  # 100 * 3 categories
    
    st.metric("🌟 Total Impact Score", f"{total_impact}/{max_possible}", 
              f"{((total_impact/max_possible)*100):.1f}% of potential")
    
    # Visualization
    st.subheader("Impact Visualization")
    
    # Create impact data
    impact_data = pd.DataFrame({
        'Category': ['Personal', 'Professional', 'Community'],
        'Impact Score': [personal_impact, professional_impact, community_impact],
        'Color': ['#667eea', '#764ba2', '#f56565']
    })
    
    # Bar chart
    fig = px.bar(
        impact_data, 
        x='Category', 
        y='Impact Score',
        color='Category',
        color_discrete_map={
            'Personal': '#667eea',
            'Professional': '#764ba2', 
            'Community': '#f56565'
        },
        title="Your Impact Across Categories"
    )
    
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Time ripple visualization
    st.subheader("Time Ripple Effect")
    
    # Create timeline data
    current_year = datetime.datetime.now().year
    years = list(range(current_year, current_year + 51, 5))
    
    # Simulate ripple effect (impact decays over time but spreads)
    ripple_data = []
    for i, year in enumerate(years):
        decay_factor = 0.9 ** i  # Impact decays 10% every 5 years
        spread_factor = 1.2 ** i  # But spreads 20% wider
        ripple_value = total_impact * decay_factor * spread_factor
        
        ripple_data.append({
            'Year': year,
            'Ripple Effect': ripple_value,
            'Impact Type': 'Your Legacy Ripple'
        })
    
    ripple_df = pd.DataFrame(ripple_data)
    
    fig2 = px.line(
        ripple_df,
        x='Year',
        y='Ripple Effect',
        title="How Your Impact Ripples Through Time",
        markers=True
    )
    
    fig2.update_layout(height=400)
    st.plotly_chart(fig2, use_container_width=True)

def show_settings_page():
    """Settings and info"""
    st.markdown("## ⚙️ Settings & Information")
    
    tab1, tab2, tab3 = st.tabs(["API Settings", "Data Management", "About"])
    
    with tab1:
        st.markdown("### 🔑 API Configuration")
        
        # Current API status
        if st.session_state.api_service == 'openrouter':
            current_key = os.getenv('OPENROUTER_API_KEY', 'Not set')
            service_name = "OpenRouter"
            get_key_url = "https://openrouter.ai/keys"
        else:
            current_key = os.getenv('DEEPSEEK_API_KEY', 'Not set')
            service_name = "DeepSeek"
            get_key_url = "https://platform.deepseek.com/api_keys"
        
        if current_key and current_key != "your-api-key-here":
            st.success(f"✅ {service_name} API Key is configured")
        else:
            st.error(f"❌ {service_name} API Key not set")
        
        st.markdown(f"""
        #### How to Get {service_name} API Key
        
        1. Go to [{service_name}]({get_key_url})
        2. Sign up (free)
        3. Navigate to API Keys section
        4. Create a new API key
        5. Copy and paste it in the sidebar
        
        **Free credits** are available for hackathon use.
        """)
    
    with tab2:
        st.markdown("### 🗃️ Data Management")
        
        st.info("""
        All data is stored locally in your browser session. 
        No data is sent to external servers except for API calls.
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Clear Chat History", type="secondary", use_container_width=True):
                st.session_state.chat_history = []
                st.success("Chat history cleared!")
        
        with col2:
            if st.button("Reset User Profile", type="secondary", use_container_width=True):
                st.session_state.user_context = {
                    'name': 'Traveler',
                    'age': 30,
                    'values': ['Growth', 'Connection'],
                    'dreams': 'To make a positive impact on the world'
                }
                st.success("Profile reset to defaults!")
    
    with tab3:
        st.markdown("### 📖 About Legacy Lens")
        
        st.markdown("""
        #### Project Details
        
        **Version**: 1.0.0 (Hackathon Edition)  
        **Built for**: ORIGIN Hackathon 2024  
        **Submission Deadline**: February 22, 2024  
        **Developer**: Solo Student Participant  
        **License**: MIT Open Source
        
        #### Tech Stack
        
        - **Frontend**: Streamlit (Python web framework)
        - **AI Backend**: OpenRouter API (GPT-3.5 Turbo) / DeepSeek API
        - **Visualization**: Plotly, Pandas
        - **Hosting**: Local development
        - **Languages**: Python
        
        #### Source Code
        
        Available on GitHub for hackathon submission.
        
        *Built with passion for the ORIGIN Hackathon themes*
        """)

if __name__ == "__main__":
    main()