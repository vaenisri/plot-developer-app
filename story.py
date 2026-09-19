import streamlit as st



st.markdown("""
<style>

body, .stApp {
    font-family: Georgia, serif;
    background-color: #F8F1E7;
    color: #332820;
}

/* Main content */
.block-container {
    max-width: 950px;
    padding-top: 3rem;
    padding-bottom: 4rem;
}

/* Main headings */
h1 {
    color: #63372C;
    font-size: 42px !important;
    letter-spacing: -1px;
}

h2, h3 {
    color: #63372C;
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
    font-size: 16px;
}

.stButton > button:hover {
    background-color: #63372C;
    color: white;
}

/* Text inputs */
.stTextInput input {
    background-color: #FFFDF9;
    border: 1px solid #CDBBA5;
    border-radius: 8px;
    padding: 12px;
    font-family: Georgia, serif;
}

/* Expanders */
[data-testid="stExpander"] {
    background-color: #FFFDF9;
    border: 1px solid #D8C7B4;
    border-radius: 10px;
    margin-bottom: 10px;
}

/* Cards */
.story-card {
    background-color: #FFFDF9;
    border: 1px solid #D8C7B4;
    border-radius: 12px;
    padding: 22px;
    margin: 12px 0;
    box-shadow: 0 3px 12px rgba(80, 50, 30, 0.08);
}

.story-label {
    color: #8A5A45;
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 1.5px;
}

.story-value {
    color: #332820;
    font-size: 17px;
    line-height: 1.5;
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
PLOT_STRUCTURES = {
    "Hero's Journey": [
        "Ordinary World",
        "Call to Adventure",
        "Refusal of the Call",
        "Meeting the Mentor",
        "Crossing the Threshold",
        "Tests, Allies, Enemies",
        "Approach to the Inmost Cave",
        "Ordeal",
        "Reward",
        "The Road Back",
        "Resurrection",
        "Return with the Elixir",
    ],
    "Three Act Structure": [
        "Act I: Setup",
        "Inciting Incident",
        "First Plot Point",
        "Rising Action",
        "Midpoint",
        "Second Plot Point",
        "Climax",
        "Resolution",
    ],
}

st.sidebar.markdown("""
<h2 style="color:#63372C;">Your Story</h2>
<p style="color:#8A5A45;">
Build your characters, shape your plot, follow the consequences.
</p>
""", unsafe_allow_html=True)

page = st.sidebar.radio(
    "WORKSPACE",
    ["Character Builder", "Characters", "Beats", "Flaw Arc"]
)

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

        st.title("Character Complete")

        st.write("You've built the core of your character.")

        st.markdown(f"""
        <div class="story-card">

        <div class="story-label">CHARACTER CORE</div>

        <h2>{st.session_state.answers["name"]}</h2>

        <hr>

        <p><b>Wound</b><br>
        {st.session_state.answers["wound"]}</p>

        <p><b>Flaw</b><br>
        {st.session_state.answers["flaw"]}</p>

        <p><b>Misbelief</b><br>
        {st.session_state.answers["misbelief"]}</p>

        <p><b>Strength</b><br>
        {st.session_state.answers["strength"]}</p>

        </div>
        """, unsafe_allow_html=True)

        st.write("These pieces give your character an internal chain:")

        st.info(
        "Wound → Flaw → Misbelief → Strength"
        )

    if st.button("Save Character"):
        st.session_state.characters.append({
            "name": st.session_state.answers["name"],
            "wound": st.session_state.answers["wound"],
            "flaw": st.session_state.answers["flaw"],
            "misbelief": st.session_state.answers["misbelief"],
            "strength": st.session_state.answers["strength"],
        })

        st.success("Character saved!")

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

elif page == "Beats":
    if not st.session_state.structure_locked:
        st.title("Choose Your Plot Structure")
        st.write("A **beat** is a single moment or turning point in your story — a scene where something happens. We'll organize your beats using whichever structure you pick below.")
        st.write("Pick the structure you'll use for this story. Once you confirm, this can't be changed.")

        choice = st.selectbox("Plot structure", list(PLOT_STRUCTURES.keys()))

        def confirm_structure():
            st.session_state.selected_structure = choice
            st.session_state.structure_locked = True
        st.button("Confirm structure", on_click=confirm_structure)
    else:
        stages = PLOT_STRUCTURES[st.session_state.selected_structure]

        if len(st.session_state.characters) == 0:
            st.write("Create a character before adding beats!")
        else:
            names = []
            for c in st.session_state.characters:
                names.append(c["name"])

            st.header("Beats by Stage")

            

            for stage in stages:
                with st.expander(stage):
                    stage_beats = []
                    for b in st.session_state.beats:
                        if b["stage"] == stage:
                            stage_beats.append(b)

                    for b in stage_beats:
                        st.markdown(f"""
        <div class="story-card">

        <div class="story-label">{b["stage"]}</div>

        <h3>{b["title"]}</h3>

        <p><b>Character:</b> {b["character_name"]}</p>

        <p><b>Driven by:</b> {b["trait_type"]}</p>

        <p><b>Cost:</b> {b["cost"]}/10</p>

    </div>
    """, unsafe_allow_html=True)

                        

                    trait_type = st.radio("What kind of beat is this?", ["Flaw", "Strength", "External"], key=f"trait_{stage}")
                    st.caption("Flaw = this beat happens because of your character's flaw. Strength = it happens because of their strength. External = it's outside their control (but you'll need to say what they DO about it).")
                    response_to_trigger = ""
                    if trait_type == "External":
                        response_to_trigger = st.text_input("This is outside the character's control - what does the character DO about it?", key=f"response_{stage}")

                    with st.form(key=f"beat_form_{stage}"):
                        chosen_name = st.selectbox("Which character?", names, key=f"name_{stage}")
                        
                        beat_title = st.text_input("Briefly explain what happens in this beat.", key=f"title_{stage}")
                        cost = st.slider("How much is this beat costing the character? (1=low stakes, 10=devastating)", 1, 10, key=f"cost_{stage}")
                        submitted = st.form_submit_button("Save beat")

                    if submitted:
                        beat = {
                            "stage": stage,
                            "title": beat_title,
                            "character_name": chosen_name,
                            "trait_type": trait_type,
                            "response_to_trigger": response_to_trigger,
                            "cost": cost,
                        }
                        st.session_state.beats.append(beat)
                        st.write("Beat saved!")
    

    flaw_count= 0
    strength_count=0
    external_count=0
    for b in st.session_state.beats:
        if b["trait_type"]=="Flaw":
            flaw_count= flaw_count + 1
        elif b["trait_type"]== "Strength":
            strength_count= strength_count +1
        elif b["trait_type"]=="External":
            external_count= external_count+1


    st.header("BEAT CHECKER")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Flaw", flaw_count)

    with col2:
        st.metric("Strength", strength_count)

    with col3:
        st.metric("External", external_count)

    if external_count > flaw_count + strength_count:
        st.warning(
        "Your plot currently relies heavily on external events. "
        "Try checking whether your character's flaw or strength could "
        "change what happens next."
        )
    else:
        st.success(
            "Your character is actively influencing the story."
        )

elif page == "Flaw Arc":
    if not st.session_state.structure_locked:
        st.write("Choose a plot structure on the Beats page first.")
    else:
        stages = PLOT_STRUCTURES[st.session_state.selected_structure]

        relevant_beats = []
        for b in st.session_state.beats:
            if b["stage"] in stages:
                relevant_beats.append(b)

        def stage_position(beat):
            return stages.index(beat["stage"])

        sorted_beats = sorted(relevant_beats, key=stage_position)

        costs = []
        for b in sorted_beats:
            costs.append(b["cost"])

        st.header("Character Stakes Arc")
        st.caption("How much does each beat raise the stakes of your story?")
        st.caption("Rising costs create a page-turning story.")
        st.line_chart(costs)