import gradio as gr
from typing import List
from dotenv import load_dotenv
from research_manager import ResearchManager

load_dotenv(override=True)
rm = ResearchManager()

def blank_state():
    return {
        "phase": "need_topic",
        "topic": "",
        "questions": [],
        "answers": []
    }

async def chat(user_input:str, st:dict):
    #1st message = research topic
    if st["phase"] == "need_topic":
        st['topic'] = user_input
        qs = await rm.generate_followup_questions(user_input)
        print ("DEBUG: qs = ", qs)
        # defensive: ensure we have a list of strings
        if isinstance(qs, str):
            qs = [q.strip(" -*•") for q in qs.splitlines() if q.strip()]
        elif not isinstance(qs, list):
            qs = [str(qs)]

        st['questions'] = qs
        st['phase'] = "collecting_answers"
        print("FIRST QUESTION:", repr(st['questions'][0]))

        yield st['questions'].pop(0), st
        return
    
    # 2nd gather answers
    if st['phase'] == "collecting_answers":
        st['answers'].append(user_input)
        if st['questions']:
            yield st['questions'].pop(0), st
            return
        # no more questions, perform research
        st['phase'] = "research"
        async for chunk in rm.run_with_clarifications(st['topic'], st['answers']):
            yield chunk, st
        return

# async def run(query: str, history):
#     async for chunk in ResearchManager().run(query):
#         yield chunk

with gr.Blocks(theme=gr.themes.Default(primary_hue="blue")) as ui:
    gr.Markdown("# Deep Research Chat")
    query_textbox = gr.Textbox(label="What topic do you want to research?")
    run_button = gr.Button("Run", variant="primary")
    report = gr.Markdown(label = "Report")
    state = gr.State(blank_state())
    
    run_button.click(fn=chat, inputs=[query_textbox, state], outputs=[report, state])
    query_textbox.submit(fn=chat, inputs=[query_textbox, state], outputs=[report, state])

ui.launch(inbrowser=True)
