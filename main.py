import gradio as gr

# This global list acts as your "frequency" - it stores the chat history for anyone on the link
chat_room = []


def submit_message(name, message):
    if not name:
        name = "Anonymous"
    if message:
        chat_room.append(f"[{name}]: {message}")

    # Returns the updated chat history and clears the message box
    return "\n".join(chat_room), ""


def refresh_chat():
    return "\n".join(chat_room)


# Build the web interface
with gr.Blocks(theme=gr.themes.Monochrome()) as app:
    gr.Markdown("# 📻 Secret Frequency Chat")
    gr.Markdown("Share the public link with your friend. They just need a web browser!")

    with gr.Row():
        name_box = gr.Textbox(label="Your ID / Name", placeholder="Enter your name here...")

    chat_box = gr.Textbox(label="Live Chat (Click Refresh to see new messages)", lines=12, interactive=False)

    with gr.Row():
        msg_box = gr.Textbox(label="Your Message", placeholder="Type your message and press Enter...")
        send_btn = gr.Button("Send Message", variant="primary")

    refresh_btn = gr.Button("🔄 Refresh Chat")

    # Wire up the buttons to the functions
    send_btn.click(submit_message, inputs=[name_box, msg_box], outputs=[chat_box, msg_box])
    msg_box.submit(submit_message, inputs=[name_box, msg_box], outputs=[chat_box, msg_box])  # Enter key
    refresh_btn.click(refresh_chat, inputs=[], outputs=[chat_box])

# share=True is the magic command that generates the public internet link
if __name__ == "__main__":
    app.launch(server_name="0.0.0.0", server_port=10000)
