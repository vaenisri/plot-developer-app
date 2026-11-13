import streamlit as st
import json
import os


def render_visitor_counter():
    st.sidebar.divider()
    st.sidebar.markdown("### 📊 App Impact")
    
    counter_file = "visitor_count.json"
    
    try:
    
        if os.path.exists(counter_file):
            with open(counter_file, "r") as f:
                data = json.load(f)
                count = data.get("count", 15)
        else:
            count = 15
  
        if "counted_visit" not in st.session_state:
            count += 1
            st.session_state["counted_visit"] = True
            with open(counter_file, "w") as f:
                json.dump({"count": count}, f)
                
        st.sidebar.metric(label="Total Storytellers", value=count)
    except Exception:
     
        st.sidebar.metric(label="Total Storytellers", value="15+")

st.set_page_config(
    page_title="Character-Driven Story Tool",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded"  
)

st.markdown("""
    <style>

    [data-testid="stSidebar"] {
        background-color: #F4ECE1;
        border-right: 3px solid #D9C8B4;
    }

    [data-testid="stSidebarCollapsedControl"] {
        background-color: #FF5A5A;
        color: white;
        border-radius: 0 12px 12px 0;
        padding: 8px 12px;
        transform: scale(1.3);
        box-shadow: 2px 2px 8px rgba(0,0,0,0.2);
    }

    [data-testid="stSidebar"] .stRadio label {
        font-size: 16px !important;
        font-weight: 600 !important;
        padding: 6px 4px;
    }
    </style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
body, .stApp {
    font-family: Georgia, serif;
    background-color: #F8F1E7;
    color: #332820;
}

/* Main content container */
.block-container {
    max-width: 1050px;
    padding-top: 2.5rem;
    padding-bottom: 4rem;
}

/* Main Headings */
h1, h2, h3, h4 {
    color: #63372C;
    font-family: Georgia, serif;
}

h1 {
    font-size: 38px !important;
    letter-spacing: -0.5px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #E9DCCB;
    border-right: 1px solid #D6C5B1;
}

/* Buttons */
.stButton > button {
    background-color: #7D3028;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.55rem 1.3rem;
    font-family: Georgia, serif;
    font-size: 15px;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background-color: #63372C;
    color: white;
}

/* Form Controls & Inputs */
.stTextInput input, .stTextArea textarea, .stSelectbox > div {
    background-color: #FFFDF9 !important;
    border: 1px solid #CDBBA5 !important;
    border-radius: 8px !important;
    font-family: Georgia, serif !important;
}

/* Expanders */
[data-testid="stExpander"] {
    background-color: #FFFDF9;
    border: 1px solid #D8C7B4;
    border-radius: 10px;
    margin-bottom: 12px;
}

/* Custom Cards */
.story-card {
    background-color: #FFFDF9;
    border: 1px solid #D8C7B4;
    border-radius: 12px;
    padding: 22px;
    margin: 12px 0;
    box-shadow: 0 3px 12px rgba(80, 50, 30, 0.05);
}

.story-label {
    color: #8A5A45;
    font-size: 12px;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 6px;
}

/* Stage Guidance Banner */
.stage-guide {
    background-color: #F1E5D5;
    border-left: 4px solid #7D3028;
    padding: 14px 18px;
    border-radius: 0 8px 8px 0;
    margin-bottom: 18px;
}

.stage-guide-title {
    color: #63372C;
    font-weight: bold;
    font-size: 15px;
    margin-bottom: 4px;
}

.stage-guide-desc {
    color: #524136;
    font-size: 14px;
    line-height: 1.4;
}

/* Trait Badge Styles */
.badge-flaw {
    background-color: #FADBD8;
    color: #78281F;
    padding: 3px 8px;
    border-radius: 4px;
    font-size: 12px;
    font-weight: bold;
}
.badge-strength {
    background-color: #D4EFDF;
    color: #145A32;
    padding: 3px 8px;
    border-radius: 4px;
    font-size: 12px;
    font-weight: bold;
}
.badge-external {
    background-color: #E8DAEF;
    color: #512E5F;
    padding: 3px 8px;
    border-radius: 4px;
    font-size: 12px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)


 

if "step" not in st.session_state:
    st.session_state.step = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "characters" not in st.session_state:
    st.session_state.characters = []
if "beats" not in st.session_state:
    st.session_state.beats = []
if "structure_locked" not in st.session_state:
    st.session_state.structure_locked = False
if "selected_structure" not in st.session_state:
    st.session_state.selected_structure = None
if "draft_text" not in st.session_state:
    st.session_state.draft_text = {}

STAGE_GUIDES = {
    "Hero's Journey": {
        "Ordinary World": "The status quo. Show the protagonist's comfort zone, everyday life, and the misbelief that keeps them stuck.",
        "Call to Adventure": "An external disruption or invitation that threatens to disrupt the status quo and forces the character to act.",
        "Refusal of the Call": "The character hesitates or tries to stay in their comfort zone because their wound/fear makes change terrifying.",
        "Meeting the Mentor": "A guide, lesson, or discovery gives the character the courage, wisdom, or push needed to take a leap.",
        "Crossing the Threshold": "Point of no return. The protagonist steps into the unknown, leaving their familiar world behind.",
        "Tests, Allies, Enemies": "Navigating the new world. The character's flaw causes clashes, while new allies force them to adapt.",
        "Approach to the Inmost Cave": "Preparing for the biggest challenge yet. Doubt and internal fear creep back in.",
        "Ordeal": "The central crisis. The character faces their deepest fear or flaw head-on. They must sacrifice something to survive.",
        "Reward": "Having survived the ordeal, the character earns a vital insight, object, or sense of clarity.",
        "The Road Back": "Consequences of the ordeal emerge. The story pushes urgently toward the final resolution.",
        "Resurrection": "The ultimate psychological exam. Can the character prove they've truly overcome their flaw/misbelief?",
        "Return with the Elixir": "The return home. The character enters a new status quo, permanently changed from within."
    },
    "Three Act Structure": {
        "Act I: Setup": "Establish the protagonist's status quo, primary flaw, and current life before disruption.",
        "Inciting Incident": "The event that disrupts balance and triggers the entire story chain.",
        "First Plot Point": "The character makes an irreversible choice to commit to the journey.",
        "Rising Action": "Obstacles escalate as the character's flaws and choices complicate their path.",
        "Midpoint": "A major revelation or turning point shifts the character from reactive to proactive.",
        "Second Plot Point": "All hope seems lost. The character's misbelief reaches a catastrophic breaking point.",
        "Climax": "The final showdown where the character must act from strength or overcome their flaw.",
        "Resolution": "The dust settles, revealing the newly transformed character and new reality."
    }
}

PLOT_STRUCTURES = {
    "Hero's Journey": list(STAGE_GUIDES["Hero's Journey"].keys()),
    "Three Act Structure": list(STAGE_GUIDES["Three Act Structure"].keys())
}

questions = [
    {
        "key": "name",
        "prompt": "What is your character's name?",
        "label": "START WITH THE BASICS",
        "description": "Give your character a name. It can be temporary if you haven't decided yet.",
        "example": "Example: Maya, Daniel, Arjun, Elara..."
    },
    {
        "key": "wound",
        "prompt": "What is your character's wound?",
        "label": "WHAT SHAPED THEM?",
        "description": "A wound is a past experience that changed how your character sees themselves or the world.",
        "example": "Example: Their parents constantly compared them to their older sibling."
    },
    {
        "key": "flaw",
        "prompt": "What flaw arose from that wound?",
        "label": "THEIR FLAW",
        "description": "A flaw is a pattern of behavior that causes problems for your character or the people around them.",
        "example": "Example: They become competitive with everyone, even their friends."
    },
    {
        "key": "misbelief",
        "prompt": "What does your character now believe because of that wound?",
        "label": "THEIR MISBELIEF",
        "description": "A misbelief is something your character believes about themselves or the world that isn't completely true.",
        "example": "Example: 'If I'm not the best, people won't value me.'"
    },
    {
        "key": "strength",
        "prompt": "How has that same trait helped them?",
        "label": "THE OTHER SIDE",
        "description": "The qualities that cause problems can also help your character. Find the strength hiding inside the flaw.",
        "example": "Example: Their competitiveness makes them incredibly determined."
    }
]
st.sidebar.markdown("""
<h2 style="color:#63372C;">Your Story</h2>
<p style="color:#8A5A45; font-size:14px;">
Build characters, map character-driven beats, and write scene drafts.
</p>
""", unsafe_allow_html=True)

st.info("👈 **Open the menu on the top-left** to switch between **Story Builder**, **Beats Engine**, and **Kids Studio 🚀**!") 
page = st.sidebar.radio(
    "WORKSPACE",
    ["Character Builder", "Characters", "Beats Engine", "Cost Arc", "Drafting Studio","Kids Studio 🚀",],
    key="nav_page" 
)
render_visitor_counter()
if page == "Character Builder":
    st.title("Build Your Character")
    st.caption(
    "CHARACTER BUILDER  ·  STEP {} OF {}".format(
        min(st.session_state.step + 1, len(questions)),
        len(questions)
    )
)

    
    st.progress(
    min(st.session_state.step + 1, len(questions)) / len(questions)
)

    if st.session_state.step < len(questions):

        current_question = questions[st.session_state.step]

        st.markdown(f"""
        <div class="story-card">

        <div class="story-label">
        {current_question["label"]}
        </div>
        <h2>
        {current_question["prompt"]}
        </h2>

        <p style="font-size:17px; line-height:1.6;">
            {current_question["description"]}
        </p>

        <p style="color:#8A5A45; font-style:italic;">
            {current_question["example"]}
        </p>

        </div>
        """, unsafe_allow_html=True)

        def go_next():
            st.session_state.answers[current_question["key"]] = st.session_state.answer_input
            st.session_state.step = st.session_state.step + 1
            st.session_state.answer_input = ""

        with st.form(key="question_form"):

            answer = st.text_input(
            "Your answer",
            key="answer_input",
            placeholder="Start writing..."
            )

            st.form_submit_button("Continue →", on_click=go_next) 
    
    else:

        st.title("Character Core")

        st.caption("YOU'VE BUILT THE FOUNDATION")

        st.markdown(f"""
        <div class="story-card">

        <div class="story-label">YOUR CHARACTER</div>

        <h2>{st.session_state.answers["name"]}</h2>

        <p style="font-size:17px; line-height:1.6;">
        Your character's experiences, flaws, beliefs, and strengths
        are connected. Here's the chain you've created.
        </p>

        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="story-card">

        <div class="story-label">WHAT SHAPED THEM</div>

        <h3>Wound</h3>

        <p>{st.session_state.answers["wound"]}</p>

        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="text-align:center; font-size:25px; color:#8A5A45;">
            ↓
        </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="story-card">

        <div class="story-label">HOW THEY RESPOND</div>

        <h3>Flaw</h3>

        <p>{st.session_state.answers["flaw"]}</p>

        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="text-align:center; font-size:25px; color:#8A5A45;">
         ↓
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="story-card">

        <div class="story-label">WHAT THEY BELIEVE</div>

        <h3>Misbelief</h3>

        <p>{st.session_state.answers["misbelief"]}</p>

        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="text-align:center; font-size:25px; color:#8A5A45;">
            ↓
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="story-card">

        <div class="story-label">THE OTHER SIDE</div>

        <h3>Strength</h3>

        <p>{st.session_state.answers["strength"]}</p>

        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="story-card">

        <div class="story-label">NOW WHAT?</div>

        <h3>Put the character into the story.</h3>

        <p style="font-size:17px; line-height:1.6;">
        Your character's flaw and strength can influence the choices
        they make when something happens to them.
        </p>

        <p style="font-style:italic; color:#8A5A45;">
        Ask yourself: What happens when this character has to make
        a difficult choice?
        </p>

        </div>
        """, unsafe_allow_html=True)

        def save_character():
                character = {
                    "name": st.session_state.answers["name"],
                    "wound": st.session_state.answers["wound"],
                    "flaw": st.session_state.answers["flaw"],
                    "misbelief": st.session_state.answers["misbelief"],
                    "strength": st.session_state.answers["strength"],
                    }
                st.session_state.characters.append(character)
                st.session_state.answers = {}
                st.session_state.step = 0

        st.button("Save Character", on_click=save_character)

elif page== "Characters":

    st.subheader("Your Characters")
    for c in st.session_state.characters:
        st.markdown(f"""
        <div class="story-card">

        <div class="story-label">CHARACTER</div>

        <h2>{c["name"]}</h2>

        <hr>

        <p><b>Wound</b><br>
        {c["wound"]}</p>

        <p><b>Flaw</b><br>
        {c["flaw"]}</p>

        <p><b>Misbelief</b><br>
        {c["misbelief"]}</p>

        <p><b>Strength</b><br>
        {c["strength"]}</p>

        </div>
        """, unsafe_allow_html=True)

elif page == "Beats Engine":
    st.title("Shape Your Story Beats")

    if not st.session_state.structure_locked:
        st.write("Choose a plot framework to organize your character's journey:")
        choice = st.selectbox("Plot Structure", list(PLOT_STRUCTURES.keys()))

        def confirm_structure():
            st.session_state.selected_structure = choice
            st.session_state.structure_locked = True
        st.button("Confirm Structure", on_click=confirm_structure)

    else:
        structure = st.session_state.selected_structure
        stages = PLOT_STRUCTURES[structure]
        guides = STAGE_GUIDES[structure]

        col_left, col_right = st.columns([1.8, 1])

        with col_left:
            st.subheader("Story Stages & Beats")
            
            if len(st.session_state.characters) == 0:
                st.warning("⚠️ Create at least one character in the Character Builder before adding beats!")
            else:
                char_names = [c["name"] for c in st.session_state.characters]

                for stage in stages:
                    with st.expander(f"{stage}"):
                        
                        st.markdown(f"""
                        <div class="stage-guide">
                            <div class="stage-guide-title">What happens at this stage?</div>
                            <div class="stage-guide-desc">{guides.get(stage, "")}</div>
                        </div>
                        """, unsafe_allow_html=True)

                        
                        stage_beats = [b for b in st.session_state.beats if b["stage"] == stage]
                        for b in stage_beats:
                            badge_class = f"badge-{b['trait_type'].lower()}"
                            st.markdown(f"""
                            <div class="story-card">
                                <div style="display:flex; justify-content:space-between; align-items:center;">
                                    <h3>{b["title"]}</h3>
                                    <span class="{badge_class}">{b["trait_type"]} Driven</span>
                                </div>
                                <p><b>Character:</b> {b["character_name"]}</p>
                                <p><b>Choice Made:</b> {b["character_choice"]}</p>
                                <p><b>Emotional Cost:</b> {b["cost"]}/10</p>
                            </div>
                            """, unsafe_allow_html=True)

                        st.markdown("---")
                        st.markdown("##### ➕ Add Beat to Stage")

                        with st.form(key=f"form_{stage}"):
                            chosen_name = st.selectbox("Who is taking action?", char_names, key=f"name_{stage}")
                            beat_title = st.text_input("What happens in this beat?", placeholder="e.g., Refuses the promotion offer", key=f"title_{stage}")
                            
                            trait_type = st.radio(
                                "What drives this beat?",
                                ["Flaw", "Strength", "External"],
                                help="Flaw = Action stems from fear/misbelief. Strength = Action stems from personal growth/virtue. External = Circumstance forces action.",
                                key=f"trait_{stage}"
                            )

                            character_choice = st.text_input("What active choice does the character make?", placeholder="e.g., Quits on the spot to avoid being judged", key=f"choice_{stage}")
                            cost = st.slider("Emotional/Physical Stakes Cost (1-10)", 1, 10, value=5, key=f"cost_{stage}")
                            
                            submitted = st.form_submit_button("Save Beat")
                            if submitted:
                                if beat_title and character_choice:
                                    st.session_state.beats.append({
                                        "stage": stage,
                                        "title": beat_title,
                                        "character_name": chosen_name,
                                        "trait_type": trait_type,
                                        "cost": cost,
                                        "character_choice": character_choice
                                    })
                                    st.rerun()
                                else:
                                    st.error("Please fill out the beat description and choice.")

        with col_right:
            st.subheader("Beat Checker")
            
            flaw_count = sum(1 for b in st.session_state.beats if b["trait_type"] == "Flaw")
            strength_count = sum(1 for b in st.session_state.beats if b["trait_type"] == "Strength")
            external_count = sum(1 for b in st.session_state.beats if b["trait_type"] == "External")

            c1, c2, c3 = st.columns(3)
            c1.metric("Flaw", flaw_count)
            c2.metric("Strength", strength_count)
            c3.metric("External", external_count)

            st.markdown("---")
            if external_count > flaw_count + strength_count:
                st.warning(
                    "⚠️ **High External Plot Agency**\n\n"
                    "Your story currently relies heavily on external events. "
                    "Try revising beats so that your character's flaws or strengths force the story forward."
                )
            elif flaw_count + strength_count > 0:
                st.success(
                    " **Strong Character Agency**\n\n"
                    "Your character's decisions, fears, and growth are actively shaping the narrative trajectory."
                )
            else:
                st.info("Add story beats to analyze character agency vs. external plot events.")

elif page == "Cost Arc":
    st.title("Character Stakes Arc")
    
    if not st.session_state.structure_locked:
        st.info("Please select a plot structure on the Beats Engine page first.")
    else:
        stages = PLOT_STRUCTURES[st.session_state.selected_structure]
        
      
        stage_order = {stage: idx for idx, stage in enumerate(stages)}
        sorted_beats = sorted(
            st.session_state.beats, 
            key=lambda b: stage_order.get(b["stage"], 0)
        )

        costs = [b["cost"] for b in sorted_beats]

        if costs:
            st.caption("Visualization of emotional and physical stakes rising across story beats.")
            st.line_chart(costs)
        else:
            st.info("No beats recorded yet. Populate beats in the Beats Engine to view the stakes curve.")

elif page == "Drafting Studio":
    st.title("Drafting Studio")
    st.caption("Write scenes directly alongside character psychology and beat requirements.")

    if not st.session_state.beats:
        st.info("No beats saved yet! Add beats in the Beats Engine to begin drafting scene scenes.")
    else:
        beat_options = [f"{b['stage']}: {b['title']}" for b in st.session_state.beats]
        selected_beat_str = st.selectbox("Select Beat to Draft", beat_options)
        
       
        selected_index = beat_options.index(selected_beat_str)
        beat = st.session_state.beats[selected_index]
        
       
        char = next((c for c in st.session_state.characters if c["name"] == beat["character_name"]), None)

        col_editor, col_context = st.columns([2, 1])

        with col_context:
            st.markdown("### Scene Reference")
            
            st.markdown(f"""
            <div class="story-card">
                <div class="story-label">BEAT DETAILS</div>
                <h4>{beat["title"]}</h4>
                <p><b>Stage:</b> {beat["stage"]}</p>
                <p><b>Choice:</b> {beat["character_choice"]}</p>
                <p><b>Driver:</b> <span class="badge-{beat['trait_type'].lower()}">{beat['trait_type']}</span></p>
            </div>
            """, unsafe_allow_html=True)

            if char:
                st.markdown(f"""
                <div class="story-card">
                    <div class="story-label">CHARACTER PSYCHOLOGY</div>
                    <h4>{char["name"]}</h4>
                    <p><b>Wound:</b> {char["wound"]}</p>
                    <p><b>Misbelief:</b> {char["misbelief"]}</p>
                    <p><b>Flaw:</b> {char["flaw"]}</p>
                </div>
                """, unsafe_allow_html=True)

        with col_editor:
            st.markdown(f"### Scene Draft: {beat['title']}")
            
            current_draft = st.session_state.draft_text.get(selected_beat_str, "")
            
            draft = st.text_area(
                "Write your scene here...",
                value=current_draft,
                height=450,
                key=f"editor_{selected_beat_str}"
            )
            
            if st.button("Save Scene Draft"):
                st.session_state.draft_text[selected_beat_str] = draft
                st.success("Draft saved successfully!")
        
elif page == "Kids Studio 🚀":
    def render_kids_studio():
    
        st.markdown("""
        <style>
        .stApp { background-color: #FAF5EF; }
        .kid-header {
            font-family: 'Comic Sans MS', 'Chalkboard SE', sans-serif;
            color: #4A3E3D;
            text-align: center;
            padding: 10px;
        }
        .card-flaw { background-color: #FFE5E5; border-left: 6px solid #FF5A5A; padding: 15px; border-radius: 8px; margin-bottom: 10px; }
        .card-strength { background-color: #E5FFE9; border-left: 6px solid #4CAF50; padding: 15px; border-radius: 8px; margin-bottom: 10px; }
        .card-external { background-color: #FFFDE5; border-left: 6px solid #FFC107; padding: 15px; border-radius: 8px; margin-bottom: 10px; }
        </style>
    """, unsafe_allow_html=True)
    st.markdown("<h1 class='kid-header'>🚀 Story Hero Studio</h1>", unsafe_allow_html=True)
    st.caption("Build awesome main characters and make sure *THEY* drive the adventure!")
    st.divider()

    # Step 1: Hero Setup
    st.header("1. Build Your Hero 🦸‍♂️")
    col1, col2 = st.columns(2)
    with col1:
        hero_name = st.text_input("What is your hero's name?", value="Leo")
        superpower = st.text_input("⚡ Their Superpower / Best Quality", value="Super Fast & Super Brave")
    with col2:
        bad_habit = st.text_input("😈 Their Bad Habit (What gets them in trouble?)", value="Gets angry too fast")
        wrong_idea = st.text_input("🧠 Their Wrong Idea (What do they believe that isn't true?)", value="I have to do everything alone")

    st.divider()

    # Step 2: Story Beats
    st.header("2. Add Story Events 🎬")
    if "kid_beats" not in st.session_state:
        st.session_state.kid_beats = [
            {"title": f"{hero_name} loses their temper and breaks a clue", "type": "Flaw"},
            {"title": "A sudden thunderstorm strikes the neighborhood", "type": "External"},
            {"title": f"{hero_name} trusts a friend and asks for help", "type": "Strength"}
        ]

    with st.form("add_beat_form", clear_on_submit=True):
        beat_title = st.text_input("What happens next in the story?")
        beat_type = st.radio(
            "Why did this happen?",
            ["Because of a Bad Habit / Mistake", "Because of a Superpower / Good Choice", "It was a Surprise / External Event"],
            horizontal=True
        )
        submit = st.form_submit_button("➕ Add Story Event")

        if submit and beat_title:
            mapped_type = "Flaw" if "Bad Habit" in beat_type else ("Strength" if "Superpower" in beat_type else "External")
            st.session_state.kid_beats.append({"title": beat_title, "type": mapped_type})
            st.rerun()

    # Step 3: Agency Meter
    st.subheader("📊 Hero Agency Meter")
    total_beats = len(st.session_state.kid_beats)
    if total_beats > 0:
        hero_beats = sum(1 for b in st.session_state.kid_beats if b["type"] in ["Flaw", "Strength"])
        hero_percent = int((hero_beats / total_beats) * 100)
        st.progress(hero_percent / 100)
        
        if hero_percent >= 66:
            st.success(f"🌟 **{hero_percent}% Hero-Driven!** {hero_name} is totally in control of this story!")
        elif hero_percent >= 40:
            st.info(f"⚖️ **{hero_percent}% Hero-Driven!** Good balance of surprises and character choices.")
        else:
            st.warning(f"⚠️ **Only {hero_percent}% Hero-Driven!** Too many random surprises happen! Give {hero_name} more big choices.")

    st.divider()

    # Step 4: Display Cards
    st.header("3. Your Story Cards 🃏")
    for idx, beat in enumerate(st.session_state.kid_beats):
        col_card, col_del = st.columns([6, 1])
        with col_card:
            if beat["type"] == "Flaw":
                st.markdown(f"<div class='card-flaw'><b>😈 Bad Habit Beat #{idx+1}:</b> {beat['title']}</div>", unsafe_allow_html=True)
            elif beat["type"] == "Strength":
                st.markdown(f"<div class='card-strength'><b>⚡ Superpower Beat #{idx+1}:</b> {beat['title']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='card-external'><b>⚡ Surprise Event #{idx+1}:</b> {beat['title']}</div>", unsafe_allow_html=True)
        with col_del:
            if st.button("❌", key=f"del_{idx}"):
                st.session_state.kid_beats.pop(idx)
                st.rerun()
    render_kids_studio()  


    
