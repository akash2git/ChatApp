import gradio as gr
import os

# Store private message histories: key is sorted pair tuple, e.g. ("akash", "bob")
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
        conversations[key].append(f"[{sender_clean}]: {message.strip()}")
    
    return "\n".join(conversations[key]), ""

def load_conversation(my_id, target_id):
    if not my_id.strip() or not target_id.strip():
        return "Enter both IDs above and hit Refresh to view the chat."
    
    key = get_channel_key(my_id, target_id)
    if key not in conversations or not conversations[key]:
        return f"No messages between {my_id} and {target_id} yet."
    
    return "\n".join(conversations[key])

with gr.Blocks(theme=gr.themes.Monochrome()) as app:
    gr.Markdown("# 💬 Direct 1-on-1 Frequency Chat")
    gr.Markdown("Share your link and tell your friend: *'Enter my ID in the Target ID box.'*")
    
    with gr.Row():
        my_id_input = gr.Textbox(label="Your ID", placeholder="e.g. akash")
        target_id_input = gr.Textbox(label="Chat With (Friend's ID)", placeholder="e.g. bob")
    
    chat_display = gr.Textbox(
        label="Private Conversation",
        lines=14,
        interactive=False,
        placeholder="Conversation history will appear here..."
    )
    
    with gr.Row():
        msg_input = gr.Textbox(label="Message", placeholder="Type a message...", scale=4)
        send_btn = gr.Button("Send", variant="primary", scale=1)
        
    refresh_btn = gr.Button("🔄 Refresh / Load Chat")

    # Wire actions
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
    refresh_btn.click(
        load_conversation,
        inputs=[my_id_input, target_id_input],
        outputs=[chat_display]
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.launch(server_name="0.0.0.0", server_port=port)
