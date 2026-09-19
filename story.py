import streamlit as st



st.markdown("""
<style>
    body, .stApp {
        font-family: Georgia, serif;
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
    {"key": "name", "prompt": "What is your character's name?"},
    {"key": "wound", "prompt": "What is the character's wound?"},
    {"key": "flaw", "prompt": "What flaw has arisen from that wound?"},
    {"key": "misbelief", "prompt": "What misbelief has arisen from that wound?"},
    {"key": "strength", "prompt": "Where have those same negative traits served them well?"}
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

page = st.sidebar.radio("Go to", ["Character Builder", "Characters", "Beats", "Flaw Arc"])

if page == "Character Builder":
    st.title("Character Builder")
    if st.session_state.step < len(questions):
        current_question = questions[st.session_state.step]

        with st.form(key="question_form"):
            answer = st.text_input(current_question["prompt"])
            submitted = st.form_submit_button("Next")

        if submitted:
            st.session_state.answers[current_question["key"]] = answer
            st.session_state.step = st.session_state.step + 1
    else:
        st.write("All questions answered!")
        st.write("**Name:**", st.session_state.answers.get("name", ""))
        st.write("**Wound:**", st.session_state.answers.get("wound", ""))
        st.write("**Flaw:**", st.session_state.answers.get("flaw", ""))
        st.write("**Misbelief:**", st.session_state.answers.get("misbelief", ""))
        st.write("**Strength:**", st.session_state.answers.get("strength", ""))
       

    
        if st.button("Save Character"):
            st.session_state.characters.append(st.session_state.answers)
            st.session_state.answers = {}
            st.session_state.step = 0
            

elif page== "Characters":

    st.subheader("Your Characters")
    for c in st.session_state.characters:
        st.write("**Name:**", c["name"])
        st.write("**Wound:**", c["wound"])
        st.markdown(f"""
        <div style="border-left: 3px solid #9A2B25; padding-left: 10px; margin-bottom: 10px;">
            <b>Flaw:</b> {c["flaw"]}
        </div>
        """, unsafe_allow_html=True)
        st.write("**Misbelief:**", c["misbelief"])

        st.markdown(f"""
        <div style="border-left: 3px solid #7A6A35; padding-left: 10px; margin-bottom: 10px;">
        <b>Strength:</b> {c["strength"]}
        </div>
        """, unsafe_allow_html=True)
        st.write("---")


elif page == "Beats":
    if not st.session_state.structure_locked:
        st.title("Choose Your Plot Structure")
        st.write("Pick the structure you'll use for this story. Once you start adding beats, this can't be changed.")

        choice = st.selectbox("Plot structure", list(PLOT_STRUCTURES.keys()))

        if st.button("Confirm structure"):
            st.session_state.selected_structure = choice
            st.session_state.structure_locked = True
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
                        st.write("**Title:**", b["title"])
                        st.write("**Character:**", b["character_name"])
                        st.write("**Type:**", b["trait_type"])
                        if b["trait_type"] == "External":
                            st.write("**Response:**", b["response_to_trigger"])
                        st.write("**Cost:**", b["cost"])
                        st.write("---")

                        
                    trait_type = st.radio("What kind of beat is this?", ["Flaw", "Strength", "External"], key=f"trait_{stage}")
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
    st.write("Flaw-driven beats:", flaw_count)
    st.write("Strength-driven beats:", strength_count)
    st.write("External triggers:", external_count)

    if external_count> flaw_count+strength_count:
        st.write("More than half of your beats are external triggers- check if your character's strength or flaw is really driving the plot.")

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

        st.header("Flaw Arc")
        st.line_chart(costs)