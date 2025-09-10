# ==================== IMPORTS ====================
import gradio as gr
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from openai import OpenAI
import random
import json
from typing import List, Dict, Tuple, Optional

# ==================== CONFIGURATION ====================
class AppConfig:
    """Application configuration and constants"""
    OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"  # Fixed URL
    GPT_MODEL = "openai/gpt-oss-20b:free"
    MAX_TOKENS = 500
    TEMPERATURE = 0.7
    
    # Color scheme for UI
    COLOR_PRIMARY = "#4F46E5"
    COLOR_SECONDARY = "#10B981"
    COLOR_ACCENT = "#F59E0B"
    COLOR_BACKGROUND = "#F8FAFC"

# ==================== GPT CLIENT SERVICE ====================
class GPTClient:
    """Handles all GPT-OSS API communications"""
    
    def __init__(self, api_key: str):
        self.client = OpenAI(
            base_url=AppConfig.OPENROUTER_BASE_URL,
            api_key=api_key
        )
    
    def get_response(self, messages: List[Dict], max_tokens: int = None, temperature: float = None) -> str:
        """Get response from GPT-OSS model"""
        try:
            response = self.client.chat.completions.create(
                model=AppConfig.GPT_MODEL,
                messages=messages,
                max_tokens=max_tokens or AppConfig.MAX_TOKENS,
                temperature=temperature or AppConfig.TEMPERATURE,
            )
            return response.choices[0].message.content
        except Exception as e:
            # Return the error message for handling in the coach
            raise Exception(f"API Connection Error: {str(e)}")

# ==================== HABIT MANAGER SERVICE ====================
class HabitManager:
    """Manages habit operations and data"""
    
    def __init__(self):
        self.habits = []
        self.categories = {
            "morning": "🌅 Morning Routine",
            "evening": "🌙 Evening Routine", 
            "productivity": "⚡ Productivity",
            "health": "💪 Health & Wellness",
            "social": "👥 Social Skills",
            "learning": "📚 Learning & Development",
            "mindfulness": "🧠 Mindfulness",
            "financial": "💰 Financial Health"
        }
    
    def add_habit(self, name: str, category: str, description: str = "") -> Dict:
        """Add a new habit to track"""
        habit = {
            "id": len(self.habits) + 1,
            "name": name,
            "category": category,
            "description": description,
            "created_date": datetime.now().strftime("%Y-%m-%d"),
            "completed": False,
            "streak": 0
        }
        self.habits.append(habit)
        return habit
    
    def get_habits_by_category(self, category: str) -> List[Dict]:
        """Get habits filtered by category"""
        return [h for h in self.habits if h["category"] == category]
    
    def get_habit_suggestions(self, category: str) -> List[str]:
        """Get AI-powered habit suggestions for a category"""
        suggestions = {
            "morning": [
                "Wake up at 6 AM consistently",
                "Drink a glass of water immediately after waking up",
                "15 minutes of meditation or mindfulness",
                "Morning exercise (yoga, jogging, stretching)",
                "Plan your day and set 3 main goals",
                "Read 10 pages of a book",
                "Healthy breakfast with protein"
            ],
            "evening": [
                "Digital detox 1 hour before bed",
                "Gratitude journaling",
                "Prepare for next day (clothes, meals)",
                "Review daily accomplishments",
                "Reading before bed (no screens)",
                "Evening reflection and planning",
                "Relaxation techniques (deep breathing)"
            ],
            "productivity": [
                "Pomodoro technique (25min work, 5min break)",
                "Time blocking for important tasks",
                "Weekly review and planning session",
                "Single-tasking instead of multitasking",
                "Declutter workspace daily",
                "Set clear daily priorities",
                "Use a task management system"
            ],
            "health": [
                "30 minutes of daily exercise",
                "Drink 8 glasses of water",
                "Healthy meal preparation",
                "Regular sleep schedule",
                "Daily stretching routine"
            ],
            "learning": [
                "Read 20 pages daily",
                "Learn a new skill for 30 minutes",
                "Practice a language daily",
                "Watch educational content",
                "Take online courses regularly"
            ]
        }
        return suggestions.get(category, [])

# ==================== COACH SERVICE ====================
class LifeCoach:
    """Main coaching service that coordinates everything"""
    
    def __init__(self, api_key: str):
        self.gpt_client = GPTClient(api_key)
        self.habit_manager = HabitManager()
        
    def get_personality_advice(self, user_message: str, chat_history: List[Tuple] = None) -> str:
        """Get personalized advice from GPT-OSS with fallback to demo mode"""
        # Demo responses for common questions
        demo_responses = {
            "hello": "Hello! I'm your AI life coach. I help people build better habits and develop their personality. What would you like to work on today? 😊",
            "hi": "Hi there! I'm excited to help you with personal development. Are you looking to improve your morning routine, build new habits, or work on specific skills?",
            "help": "I can help you with:\n• 🌅 Building morning/evening routines\n• 💪 Developing new habits\n• 🧠 Personality development\n• ⚡ Productivity strategies\n• 👥 Social skills improvement\n• 📚 Learning new skills\n\nWhat interests you most?",
            "routine": "**Great morning routine template:**\n⏰ 6:00 AM - Wake up, drink water\n🧘 6:15 AM - Meditation/mindfulness (15min)\n🏃 6:30 AM - Exercise (yoga, jogging, stretching)\n🍎 7:00 AM - Healthy breakfast\n📋 7:30 AM - Plan day & set goals\n💼 8:00 AM - Start focused work",
            "habit": "**Habit formation strategy:**\n1. **Start small** - 5 minutes daily\n2. **Be consistent** - Same time every day\n3. **Track progress** - Use a habit tracker\n4. **Celebrate wins** - Reward yourself\n5. **Stay accountable** - Share your goals",
            "sleep": "**For better sleep:**\n1. 📵 Digital detox 1 hour before bed\n2. ⏰ Consistent sleep schedule\n3. 🌙 Dark, cool bedroom\n4. 🧘 Relaxation techniques\n5. ☕ No caffeine after 2 PM",
            "productivity": "**Productivity tips:**\n1. 🕒 Time blocking technique\n2. 🍅 Pomodoro method (25min work, 5min break)\n3. 🎯 Prioritize 3 main tasks daily\n4. 🔕 Eliminate distractions\n5. 🏖️ Regular breaks",
            "social": "**Social skills development:**\n1. 👂 Practice active listening\n2. 💬 Start small conversations daily\n3. 😊 Maintain eye contact and smile\n4. ❓ Ask open-ended questions\n5. 🤝 Join social groups or clubs"
        }
        
        # Check for demo responses first
        lower_msg = user_message.lower()
        for key in demo_responses:
            if key in lower_msg:
                return demo_responses[key]
        
        # Try to use real AI if possible
        try:
            system_prompt = """You are GPT-Life, an AI personality and habit development coach. You help people build better routines, develop habits, and improve their personality. Provide specific, actionable advice."""
            
            messages = [{"role": "system", "content": system_prompt}]
            
            if chat_history:
                for user_msg, assistant_msg in chat_history:
                    messages.append({"role": "user", "content": user_msg})
                    messages.append({"role": "assistant", "content": assistant_msg})
                    
            messages.append({"role": "user", "content": user_message})
            
            response = self.gpt_client.get_response(messages)
            return response
            
        except Exception as e:
            # Fallback to generic demo response
            return f"""🎯 **Demo Mode - AI Coach Response** 

For '{user_message}', I would normally provide:

• Personalized step-by-step advice
• Science-backed habit formation techniques  
• Practical implementation strategies
• Motivational guidance and encouragement

**Try asking about:**
- \"morning routine ideas\"
- \"how to build better habits\"
- \"productivity tips\"
- \"improving social skills\"

*(Real AI responses activate when API connection is available)*"""
    
    def improve_habit_with_methods(self, habit_name: str, current_method: str) -> str:
        """Get AI suggestions to improve a specific habit"""
        try:
            prompt = f"""I have a habit: '{habit_name}'. Currently I do it like this: {current_method}.
            Please suggest 3 improved methods or techniques to make this habit more effective, sustainable, and rewarding.
            Provide specific, actionable suggestions."""
            
            return self.gpt_client.get_response([{"role": "user", "content": prompt}])
        except:
            # Demo response for habit improvement
            return f"""✨ **Habit Improvement Suggestions for '{habit_name}'**:

1. **Optimize Timing**: Try doing this habit at the same time daily to build consistency
2. **Start Smaller**: Begin with just 5-10 minutes and gradually increase
3. **Add Triggers**: Pair with an existing habit (e.g., after brushing teeth)
4. **Track Progress**: Use a habit tracker app or journal
5. **Reward System**: Celebrate small wins to maintain motivation

*(Real AI suggestions activate when connection is available)*"""
    
    def generate_daily_plan(self, user_goals: List[str]) -> str:
        """Generate a personalized daily plan"""
        try:
            goals_text = ", ".join(user_goals)
            prompt = f"""Create a comprehensive daily plan for someone with these goals: {goals_text}.
            Include morning routine, work/study blocks, breaks, evening routine, and self-care activities.
            Make it realistic and time-specific."""
            
            return self.gpt_client.get_response([{"role": "user", "content": prompt}])
        except:
            # Demo daily plan
            return """📅 **Sample Daily Plan for Personal Development:**

🌅 **Morning (6:00 AM - 9:00 AM)**
- 6:00 AM: Wake up, hydrate, quick stretch
- 6:15 AM: 15-min meditation/mindfulness
- 6:30 AM: 30-min exercise (yoga/walk/jog)
- 7:00 AM: Healthy breakfast
- 7:30 AM: Plan day & set 3 main goals
- 8:00 AM: Start focused work/study

💼 **Work Block (9:00 AM - 12:00 PM)**
- 9:00 AM: Deep work session (Pomodoro: 25min work, 5min break)
- 12:00 PM: Lunch break with no screens

📚 **Learning (1:00 PM - 3:00 PM)**
- 1:00 PM: Skill development or reading
- 2:30 PM: Review and note-taking

🏋️ **Health & Wellness (4:00 PM - 5:00 PM)**
- Exercise or outdoor activity
- Hydration and healthy snack

🌙 **Evening (6:00 PM - 10:00 PM)**
- 6:00 PM: Digital detox hour
- 7:00 PM: Relaxation or social time
- 9:00 PM: Gratitude journaling
- 9:30 PM: Prepare for next day
- 10:00 PM: Reading (no screens) and sleep

*(Custom AI-generated plans activate when connection is available)*"""

# ==================== UI COMPONENTS ====================
class UIComponents:
    """Reusable UI components"""
    
    @staticmethod
    def create_progress_chart() -> go.Figure:
        """Create weekly progress chart"""
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        completed = [random.randint(3, 7) for _ in range(7)]
        planned = [7] * 7
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Planned Habits',
            x=days,
            y=planned,
            marker_color=AppConfig.COLOR_PRIMARY,
            opacity=0.6
        ))
        fig.add_trace(go.Bar(
            name='Completed Habits',
            x=days,
            y=completed,
            marker_color=AppConfig.COLOR_SECONDARY
        ))
        
        fig.update_layout(
            title='📈 Weekly Habit Completion',
            barmode='overlay',
            showlegend=True,
            height=300,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        return fig
    
    @staticmethod
    def create_habit_distribution() -> px.pie:
        """Create habit category distribution chart"""
        categories = ['Morning', 'Evening', 'Productivity', 'Health', 'Social', 'Learning']
        values = [25, 20, 18, 15, 12, 10]
        
        fig = px.pie(
            values=values, 
            names=categories,
            title='📊 Habit Category Distribution',
            hole=0.4,
            height=300,
            color_discrete_sequence=[AppConfig.COLOR_PRIMARY, AppConfig.COLOR_SECONDARY, 
                                   AppConfig.COLOR_ACCENT, '#8B5CF6', '#EC4899', '#06B6D4']
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        return fig

# ==================== APPLICATION SETUP ====================
# Initialize services
API_KEY = "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"
life_coach = LifeCoach(API_KEY)
habit_manager = HabitManager()
ui_components = UIComponents()

# ==================== GRADIO UI ====================
with gr.Blocks(
    theme=gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="green",
        neutral_hue="slate"
    ), 
    title="GPT-Life: AI Personality Coach"
) as demo:
    
    # Header
    with gr.Column():
        gr.Markdown("""
        # 🌟 GPT-Life: Your AI Personality Development Coach
        *Build better habits, develop your personality, and transform your life with AI-powered coaching*
        """)
    
    with gr.Row():
        # Left Sidebar - Progress and Quick Actions
        with gr.Column(scale=1):
            with gr.Group():
                gr.Markdown("### 📊 Your Progress Dashboard")
                progress_chart = gr.Plot(ui_components.create_progress_chart())
                distribution_chart = gr.Plot(ui_components.create_habit_distribution())
            
            with gr.Group():
                gr.Markdown("### 🎯 Quick Habit Ideas")
                category_dropdown = gr.Dropdown(
                    choices=list(habit_manager.categories.values()),
                    label="Select Category",
                    value="🌅 Morning Routine"
                )
                suggestions_output = gr.Textbox(label="AI Suggestions", interactive=False, lines=6)
                
                def update_suggestions(category):
                    reversed_categories = {v: k for k, v in habit_manager.categories.items()}
                    cat_key = reversed_categories.get(category, "morning")
                    suggestions = habit_manager.get_habit_suggestions(cat_key)
                    return "\n".join([f"• {s}" for s in suggestions[:5]])
                
                category_dropdown.change(update_suggestions, category_dropdown, suggestions_output)
        
        # Main Content Area
        with gr.Column(scale=2):
            # AI Coach Chat Tab
            with gr.Tab("💬 AI Coach Chat"):
                chatbot = gr.Chatbot(
                    label="Chat with your AI Coach",
                    height=400,
                    show_copy_button=True
                )
                
                with gr.Row():
                    msg = gr.Textbox(
                        label="What would you like to work on today?",
                        placeholder="e.g., I want to build a better morning routine or improve my social skills...",
                        lines=2,
                        scale=4
                    )
                    send_btn = gr.Button("🚀 Send", variant="primary", scale=1)
                
                clear_btn = gr.Button("🧹 Clear Chat")
                
                gr.Examples(
                    examples=[
                        "How can I become more disciplined with my morning routine?",
                        "I want to wake up at 5 AM consistently - what's the best approach?",
                        "Help me build better social skills and confidence",
                        "I need help with time management and productivity",
                        "How to develop a consistent reading habit?",
                        "Suggest ways to improve my current exercise routine"
                    ],
                    inputs=msg,
                    label="💡 Common Questions to Ask"
                )
            
            # Habit Management Tab
            with gr.Tab("📅 Habit Manager"):
                gr.Markdown("### 🎯 Manage Your Habits")
                
                with gr.Row():
                    with gr.Column(scale=2):
                        habit_name = gr.Textbox(
                            label="Habit Name",
                            placeholder="e.g., Morning meditation"
                        )
                        habit_description = gr.Textbox(
                            label="Description (Optional)",
                            placeholder="e.g., 15 minutes of mindfulness meditation"
                        )
                    
                    with gr.Column(scale=1):
                        habit_category = gr.Dropdown(
                            choices=list(habit_manager.categories.values()),
                            label="Category",
                            value="🌅 Morning Routine"
                        )
                        add_habit_btn = gr.Button("➕ Add Habit", variant="primary")
                
                # Habit improvement section
                with gr.Accordion("🔄 Improve Existing Habit", open=False):
                    gr.Markdown("Get AI suggestions to improve your habit execution:")
                    improve_habit_name = gr.Textbox(
                        label="Habit to Improve",
                        placeholder="e.g., My current exercise routine"
                    )
                    current_method = gr.Textbox(
                        label="Current Method",
                        placeholder="e.g., I go to the gym 3 times a week for 1 hour"
                    )
                    improve_btn = gr.Button("✨ Get Improvement Suggestions", variant="secondary")
                    improvement_output = gr.Textbox(label="AI Improvement Suggestions", interactive=False, lines=4)
                
                # Habits list
                habits_display = gr.Dataframe(
                    headers=["Habit", "Category", "Status", "Streak"],
                    value=[["Morning jog", "💪 Health & Wellness", "✅ Active", "7 days"]],
                    row_count=5,
                    interactive=False,
                    wrap=True
                )
            
            # Goal Setting Tab
            with gr.Tab("🎯 Goal Setting"):
                gr.Markdown("### 🎯 Set Your Development Goals")
                
                with gr.Row():
                    goal_input = gr.Textbox(
                        label="Your Goal",
                        placeholder="e.g., Read 20 books this year"
                    )
                    timeline = gr.Dropdown(
                        choices=["1 week", "2 weeks", "1 month", "3 months", "6 months", "1 year"],
                        label="Timeline",
                        value="1 month"
                    )
                    set_goal_btn = gr.Button("🎯 Set Goal", variant="primary")
                
                gr.Markdown("### 📋 Current Goals")
                goals_display = gr.Dataframe(
                    headers=["Goal", "Timeline", "Progress"],
                    value=[["Wake up at 6 AM daily", "1 month", "75%"]],
                    row_count=3,
                    interactive=False
                )
                
                # Daily plan generator
                with gr.Accordion("📅 Generate Daily Plan", open=False):
                    gr.Markdown("Get a personalized daily plan based on your goals:")
                    generate_plan_btn = gr.Button("🔄 Generate Daily Plan", variant="secondary")
                    daily_plan_output = gr.Textbox(label="Your AI-Generated Daily Plan", interactive=False, lines=6)

    # ==================== EVENT HANDLERS ====================
    # Chat functionality
    def respond(message: str, chat_history: List[Tuple]) -> Tuple[str, List[Tuple]]:
        if not message.strip():
            return "", chat_history
        
        response = life_coach.get_personality_advice(message, chat_history)
        chat_history.append((message, response))
        return "", chat_history

    # Habit management
    def add_habit(name: str, description: str, category: str) -> Dict:
        if not name.strip():
            return gr.update()
        
        habit = habit_manager.add_habit(name, category, description)
        new_row = [habit["name"], habit["category"], "⏳ Pending", "0 days"]
        return new_row

    def improve_habit(habit_name: str, current_method: str) -> str:
        if not habit_name.strip() or not current_method.strip():
            return "Please provide both habit name and current method."
        
        return life_coach.improve_habit_with_methods(habit_name, current_method)

    def generate_daily_plan() -> str:
        # In a real app, this would use actual user goals
        sample_goals = ["Improve productivity", "Exercise regularly", "Read more books"]
        return life_coach.generate_daily_plan(sample_goals)

    # Connect event handlers
    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    send_btn.click(respond, [msg, chatbot], [msg, chatbot])
    clear_btn.click(lambda: None, None, chatbot, queue=False)
    
    add_habit_btn.click(
        add_habit,
        [habit_name, habit_description, habit_category],
        habits_display
    )
    
    improve_btn.click(
        improve_habit,
        [improve_habit_name, current_method],
        improvement_output
    )
    
    generate_plan_btn.click(
        generate_daily_plan,
        [],
        daily_plan_output
    )

# ==================== APPLICATION LAUNCH ====================
if __name__ == "__main__":
    demo.launch(
        share=True,
        server_name="0.0.0.0",
        server_port=7860,
        debug=True
    )