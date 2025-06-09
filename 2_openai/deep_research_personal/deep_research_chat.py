import gradio as gr
from dotenv import load_dotenv
from research_manager import ResearchManager

load_dotenv(override=True)
rm = ResearchManager()

# Global dictionary to store user states
user_states = {}

def blank_state():
    return {
        "phase": "need_topic",
        "topic": "",
        "questions": [],
        "answers": [],
        "report": "",
        "email_requested": None,
        "user_email": None,
    }

async def chat(message, history, request: gr.Request):
    session_hash = request.session_hash
    if session_hash not in user_states:
        user_states[session_hash] = blank_state()
    state = user_states[session_hash]

    # Step 1: User submits a topic
    if state["phase"] == "need_topic":
        state["topic"] = message
        qs = await rm.generate_followup_questions(message)
        if isinstance(qs, str):
            qs = [q.strip(" -*•") for q in qs.splitlines() if q.strip() and q.strip().endswith("?")]
        elif not isinstance(qs, list):
            qs = [str(qs)]
        else:
            qs = [q.strip() for q in qs if q.strip() and q.strip().endswith("?")]
        state["questions"] = qs
        state["phase"] = "collecting_answers"
        questions_str = "\n".join([f"{i+1}. {q}" for i, q in enumerate(qs)])
        bot_message = (
            "Before I start, could you answer these to help me focus the research?\n\n"
            f"{questions_str}\n\n"
            "Please reply with your answers, one per line."
        )
        yield bot_message
        return

    # Step 2: User submits all answers (one per line)
    if state["phase"] == "collecting_answers":
        state["answers"] = [a.strip() for a in message.split("\n") if a.strip()]
        state["phase"] = "research"
        yield "Thanks! Running research now..."

        # Streaming pipeline, collect final report
        pipeline = [
            ("Followup Questions Generated", "🟢"),
            ("Starting Research Pipeline", "🔍"),
            ("Search Plan Generated", "📑"),
            ("Search Results Generated", "🌐"),
            ("Report Generated", "📝"),
            ("Research complete", "✅"),
        ]
        completed = []
        full_report = ""
        current_status = ""
        
        # Initialize the display message
        display_message = "Thanks! Running research now...\n\n"
        full_report = ""
        
        async for chunk in rm.run_with_clarifications(state["topic"], state["answers"]):
            # print(f"DEBUG: Received chunk: {chunk[:100]}...")  # Debug line
            
            if chunk.startswith("View trace at"):
                continue
            
            # Check for report content with our prefix
            if chunk.startswith("REPORT_CONTENT:"):
                report_content = chunk.replace("REPORT_CONTENT:", "").strip()
                state["report"] = report_content
                full_report = report_content
                # print(f"DEBUG: Found report content, length: {len(report_content)}")  # Debug line
                
                # Add the report to our display message
                display_message += f"\n\n# 📄 Your Research Report\n\n{full_report}"
                yield display_message
                continue
            
            # Check if this chunk is a pipeline status update
            for label, emoji in pipeline:
                if label in chunk and emoji not in completed:
                    completed.append(emoji)
                    # Update the status in our display message
                    status_line = f"Status: {'  '.join(completed)}"
                    # Replace or add the status line
                    if "Status:" in display_message:
                        lines = display_message.split('\n')
                        for i, line in enumerate(lines):
                            if line.startswith("Status:"):
                                lines[i] = status_line
                                break
                        display_message = '\n'.join(lines)
                    else:
                        display_message += f"\n{status_line}"
                    
                    yield display_message
                    break
        
        # Final check and email prompt
        if not full_report:
            display_message += "\n\n⚠️ No report content was generated. Please try again."
            yield display_message
            return
        
        # Move to email phase and add email question
        state["phase"] = "ask_email_consent"
        display_message += "\n\n---\n\n**Would you like this report emailed to you?** (yes/no)"
        yield display_message
        return

    # Step 3: Ask if the user wants email
    if state["phase"] == "ask_email_consent":
        response = message.strip().lower()
        if response in ["yes", "y"]:
            state["phase"] = "get_email_address"
            yield "Please provide your email address."
        else:
            state["phase"] = "need_topic"
            yield "Okay, no email will be sent. If you'd like to start a new research topic, please enter it!"
        return

    # Step 4: Get user's email and send report
    if state["phase"] == "get_email_address":
        state["user_email"] = message.strip()
        # Send the report to the user's email address
        try:
            # Get the report object from the research manager
            if hasattr(rm, 'last_report') and rm.last_report:
                await rm.send_report_with_email(rm.last_report, state["user_email"])
            else:
                # Fallback: create a ReportData object from the stored markdown
                from writer_agent import ReportData
                report_data = ReportData(
                    short_summary="Research Report",
                    markdown_report=state["report"],
                    follow_up_questions=[],
                    references=[]
                )
                await rm.send_report_with_email(report_data, state["user_email"])
            
            state["phase"] = "need_topic"
            yield f"Report sent to {state['user_email']}! If you'd like to research another topic, please enter it."
        except Exception as e:
            yield f"Sorry, there was an error sending the email: {str(e)}. If you'd like to research another topic, please enter it."
            state["phase"] = "need_topic"
        return

    yield ""
    return

gr.ChatInterface(
    fn=chat,
    title="Deep Research Chatbot",
    description="AI-powered research assistant that asks clarifying questions before generating a custom report."
).launch()