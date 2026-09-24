import gradio as gr
import os
from datetime import datetime

# Store private message histories
conversations = {}

def get_channel_key(user_a, user_b):
    u1 = (user_a or "").strip().lower()
    u2 = (user_b or "").strip().lower()
    if not u1 or not u2:
        return None
    return tuple(sorted([u1, u2]))

def send_direct_message(my_id, target_id, message):
    if not my_id.strip() or not target_id.strip():
        return "Error: Enter both your ID and the recipient ID.", ""
    
    key = get_channel_key(my_id, target_id)
    if key not in conversations:
        conversations[key] = []
        
    if message.strip():
        sender_clean = my_id.strip()
        time_str = datetime.now().strftime("%I:%M %p") 
        conversations[key].append(f"[{time_str}] {sender_clean}: {message.strip()}")
    
    return "\n".join(conversations[key]), ""

def load_conversation(my_id, target_id):
    if not my_id.strip() or not target_id.strip():
        return "Waiting for IDs..."
    
    key = get_channel_key(my_id, target_id)
    if key not in conversations or not conversations[key]:
        return f"No messages between {my_id} and {target_id} yet."
    
    return "\n".join(conversations[key])

# Removed the theme parameter from Blocks() to fix the Gradio 6 warning
with gr.Blocks() as app:
    gr.Markdown("# 💬 Direct 1-on-1 Frequency Chat")
    gr.Markdown("Share your link and tell your friend: *'Enter my ID in the Target ID box.'*")
    
    with gr.Row():
        my_id_input = gr.Textbox(label="Your ID", placeholder="e.g. akash")
        target_id_input = gr.Textbox(label="Chat With (Friend's ID)", placeholder="e.g. bob")
    
    chat_display = gr.Textbox(
        label="Private Conversation (Auto-updates every 2 seconds)",
        lines=14,
        interactive=False,
        placeholder="Conversation history will appear here..."
    )
    
    with gr.Row():
        msg_input = gr.Textbox(label="Message", placeholder="Type a message...", scale=4)
        send_btn = gr.Button("Send", variant="primary", scale=1)

    send_btn.click(
        send_direct_message,
        inputs=[my_id_input, target_id_input, msg_input],
        outputs=[chat_display, msg_input]
    )
    msg_input.submit(
        send_direct_message,
        inputs=[my_id_input, target_id_input, msg_input],
        outputs=[chat_display, msg_input]
    )
    
    # GRADIO 6 FIX: Use gr.Timer instead of app.load(every=2)
    timer = gr.Timer(2)
    timer.tick(
        load_conversation,
        inputs=[my_id_input, target_id_input],
        outputs=[chat_display]
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    # GRADIO 6 FIX: Move the theme parameter here to the launch command
    app.launch(server_name="0.0.0.0", server_port=port, theme=gr.themes.Monochrome())
