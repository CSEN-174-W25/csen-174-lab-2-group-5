from flask import Flask, render_template, request, jsonify, session
import uuid
from openai import OpenAI

app = Flask(__name__)
app.secret_key = "your-secret-key"  # Change this to a secure random key

# Set your OpenAI API key
OPENAI_API_KEY = "KEY"
client = OpenAI(api_key=OPENAI_API_KEY)

# Global in-memory stores
conversation_cache = {}  # Ongoing conversation per session
favorites_store = {}     # Favorited recipes per session (list of dicts with id, title, content)
past_chats_store = {}    # Saved past chats per session (list of dicts with id, messages, summary)

def get_openai_response(messages):
    """Call the OpenAI API with the conversation history."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # your chosen model
        messages=messages,
        max_tokens=2500,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()

def extract_title(recipe_text):
    """
    Extract the title from the recipe text (assumes title is the first non-empty line).
    Removes any leading "### " if present and removes all "*" characters.
    """
    lines = recipe_text.strip().splitlines()
    for line in lines:
        if line.strip():
            title = line.strip()
            if title.startswith("### "):
                title = title[4:].strip()
            # Remove all "*" characters from the title
            title = title.replace("*", "").replace("#", "").replace("-", "")
            return title
    return "No summary available"

@app.before_request
def assign_session():
    """Ensure every visitor has a session and initialize their stores."""
    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())
    sess_id = session["session_id"]
    if sess_id not in conversation_cache:
        conversation_cache[sess_id] = [
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant that provides recipes. When given ingredients you output a single recipe and include: recipe title (without saying recipe title), ingredients, possible missing ingredients, instructions, any additional comments."
                )
            }
        ]
    if sess_id not in favorites_store:
        favorites_store[sess_id] = []
    if sess_id not in past_chats_store:
        past_chats_store[sess_id] = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message")
    sess_id = session["session_id"]
    conversation = conversation_cache.get(sess_id, [])

    # Append user's message to conversation
    conversation.append({"role": "user", "content": user_message})

    # Get assistant response with full conversation context
    assistant_response = get_openai_response(conversation)
    conversation.append({"role": "assistant", "content": assistant_response})

    return jsonify({"response": assistant_response})

@app.route("/favorites", methods=["GET", "POST"])
def favorites():
    sess_id = session["session_id"]
    if request.method == "POST":
        data = request.get_json()
        recipe_text = data.get("recipe")
        title = extract_title(recipe_text)
        # Check for duplicates by title
        for fav in favorites_store[sess_id]:
            if fav["title"] == title:
                return jsonify({"status": "duplicate", "message": "Recipe already favorited."})
        favorite = {"id": str(uuid.uuid4()), "title": title, "content": recipe_text}
        favorites_store[sess_id].append(favorite)
        return jsonify({"status": "success", "favorite": favorite})
    else:
        return jsonify({"favorites": favorites_store.get(sess_id, [])})

@app.route("/delete_favorite/<favorite_id>", methods=["POST"])
def delete_favorite(favorite_id):
    sess_id = session["session_id"]
    favorites_store[sess_id] = [fav for fav in favorites_store.get(sess_id, []) if fav["id"] != favorite_id]
    return jsonify({"status": "success"})

@app.route("/new_chat", methods=["POST"])
def new_chat():
    """
    Save the current conversation (if any) with its recipe title (from the first assistant response)
    and reset conversation for a new chat.
    """
    sess_id = session["session_id"]
    current_conv = conversation_cache.get(sess_id, [])
    summary = "No summary available"
    for msg in current_conv:
        if msg["role"] == "assistant":
            summary = extract_title(msg["content"])
            break
    if len(current_conv) > 1:
        conv_id = str(uuid.uuid4())
        past_chats_store[sess_id].append({"id": conv_id, "messages": current_conv.copy(), "summary": summary})
    conversation_cache[sess_id] = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant that provides recipes. When given ingredients you output a single recipe and include: recipe title (without saying recipe title), ingredients, possible missing ingredients, instructions, any additional comments."
            )
        }
    ]
    return jsonify({"status": "new chat started"})

@app.route("/all_chats", methods=["GET"])
def all_chats():
    """
    Returns a combined list of past chats plus the current conversation (if any).
    The current conversation is included as an item with id "current" using its recipe title.
    """
    sess_id = session["session_id"]
    chats = past_chats_store.get(sess_id, []).copy()
    current_conv = conversation_cache.get(sess_id, [])
    if len(current_conv) > 1:
        summary = "No summary available"
        for msg in current_conv:
            if msg["role"] == "assistant":
                summary = extract_title(msg["content"])
                break
        # Insert current conversation summary at the beginning with id "current"
        chats.insert(0, {"id": "current", "summary": summary})
    return jsonify({"chats": chats})

@app.route("/delete_chat/<chat_id>", methods=["POST"])
def delete_chat(chat_id):
    sess_id = session["session_id"]
    # Prevent deletion of current chat
    if chat_id == "current":
        return jsonify({"status": "error", "message": "Cannot delete current chat."})
    past_chats_store[sess_id] = [chat for chat in past_chats_store.get(sess_id, []) if chat["id"] != chat_id]
    return jsonify({"status": "success"})

@app.route("/load_chat/<chat_id>", methods=["GET"])
def load_chat(chat_id):
    sess_id = session["session_id"]
    if chat_id == "current":
        messages = conversation_cache.get(sess_id, [])
        return jsonify({"messages": messages})
    for chat in past_chats_store.get(sess_id, []):
        if chat["id"] == chat_id:
            return jsonify({"messages": chat["messages"]})
    return jsonify({"error": "Chat not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
