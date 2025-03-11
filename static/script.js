document.addEventListener("DOMContentLoaded", function () {
  // Configure marked.js to preserve newlines (breaks: true)
  marked.setOptions({
    breaks: true,
  });
  
  const chatLog = document.getElementById("chat-log");
  const messageInput = document.getElementById("message-input");
  const sendBtn = document.getElementById("send-btn");
  const newChatBtn = document.getElementById("new-chat-btn");
  const favoritesBtn = document.getElementById("favorites-btn");
  const pastChatsListEl = document.getElementById("past-chats-list");
  const chatView = document.getElementById("chat-view");
  const favoritesView = document.getElementById("favorites-view");
  const favoritesListView = document.getElementById("favorites-list-view");

  let loadingInterval = null;

  // Utility: Format markdown for assistant responses
  function formatAssistantMarkdown(content) {
    // Normalize line breaks
    content = content.replace(/(\r\n|\n|\r)/g, "\n");
  
    return content;
  }

  // Append message to chat log; if loading, show cycling dots
  function appendMessage(role, content, isLoading = false) {
    const msgDiv = document.createElement("div");
    msgDiv.classList.add("message", role);

    if (isLoading) {
      msgDiv.classList.add("loading");
      const loadingSpan = document.createElement("span");
      loadingSpan.textContent = "";
      msgDiv.appendChild(loadingSpan);

      let dotCount = 0;
      loadingInterval = setInterval(() => {
        dotCount = (dotCount + 1) % 4;
        loadingSpan.textContent = ".".repeat(dotCount);
      }, 500);
    } else {
      if (role === "assistant") {
        const formatted = formatAssistantMarkdown(content);
        msgDiv.innerHTML = marked.parse(formatted);
      } else {
        msgDiv.textContent = content;
      }
      if (role === "assistant") {
        const star = document.createElement("span");
        star.classList.add("favorite-star");
        star.innerHTML = "&#9733;";
        star.title = "Add to Favorites";
        star.addEventListener("click", function () {
          addToFavorites(content);
        });
        msgDiv.appendChild(star);
      }
    }

    chatLog.appendChild(msgDiv);
    chatLog.scrollTop = chatLog.scrollHeight;
    return msgDiv;
  }

  // Send message to backend
  function sendMessage() {
    const message = messageInput.value.trim();
    if (!message) return;
    appendMessage("user", message);
    messageInput.value = "";

    updatePastChats();

    const loadingMsg = appendMessage("assistant", "", true);

    fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: message }),
    })
      .then((response) => response.json())
      .then((data) => {
        clearInterval(loadingInterval);
        loadingMsg.remove();
        appendMessage("assistant", data.response);
        updatePastChats();
      })
      .catch((error) => {
        clearInterval(loadingInterval);
        console.error("Error:", error);
        loadingMsg.textContent = "Error retrieving response.";
      });
  }

  // Add recipe to favorites via backend POST (no alert popups)
  function addToFavorites(recipe) {
    fetch("/favorites", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ recipe: recipe }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status !== "duplicate") {
          console.log("Recipe saved to favorites.");
        }
      })
      .catch((error) => console.error("Error:", error));
  }

  // Update past chats list by fetching from /all_chats
  function updatePastChats() {
    fetch("/all_chats")
      .then((response) => response.json())
      .then((data) => {
        pastChatsListEl.innerHTML = "";
        data.chats.forEach((chat) => {
          const item = document.createElement("div");
          item.classList.add("past-chat-item");
          item.textContent = chat.summary || "No summary available";

          // Only add trash icon if not the current chat
          if (chat.id !== "current") {
            const trashIcon = document.createElement("span");
            trashIcon.classList.add("delete-chat-icon");
            trashIcon.innerHTML = "&#128465;";
            trashIcon.title = "Delete Chat";
            trashIcon.addEventListener("click", (e) => {
              e.stopPropagation();
              deletePastChat(chat.id);
            });
            item.appendChild(trashIcon);
          }

          // Clicking loads the chat into the chat view
          item.addEventListener("click", () => {
            loadChat(chat.id);
          });

          pastChatsListEl.appendChild(item);
        });
      })
      .catch((error) => console.error("Error:", error));
  }

  // Load a specific chat (past or current) into the chat log
  function loadChat(chatId) {
    favoritesView.classList.add("hidden");
    chatView.classList.remove("hidden");
    fetch(`/load_chat/${chatId}`)
      .then((response) => response.json())
      .then((data) => {
        if (data.error) {
          alert(data.error);
          return;
        }
        chatLog.innerHTML = "";
        data.messages.forEach((msg) => {
          if (msg.role === "assistant") {
            appendMessage("assistant", msg.content);
          } else if (msg.role === "user") {
            appendMessage("user", msg.content);
          }
        });
      })
      .catch((error) => console.error("Error:", error));
  }

  // Delete a past chat via backend
  function deletePastChat(chatId) {
    fetch(`/delete_chat/${chatId}`, { method: "POST" })
      .then((response) => response.json())
      .then(() => updatePastChats())
      .catch((error) => console.error("Error:", error));
  }

  // Load favorites and display them in the favorites view
  function loadFavorites() {
    fetch("/favorites")
      .then((response) => response.json())
      .then((data) => {
        favoritesListView.innerHTML = "";
        if (data.favorites.length === 0) {
          favoritesListView.innerHTML = "<p>No favorites yet.</p>";
        } else {
          data.favorites.forEach((fav) => {
            const item = document.createElement("div");
            item.classList.add("favorite-item");
            
            // Create title element without markdown header symbols
            const titleEl = document.createElement("div");
            titleEl.classList.add("favorite-title");
            titleEl.innerHTML = `<strong>${fav.title}</strong>`;
            item.appendChild(titleEl);
            
            // Create content element rendered in markdown (using same formatting as assistant)
            const contentEl = document.createElement("div");
            // Apply the same assistant formatting classes so it looks the same
            contentEl.classList.add("message", "assistant", "favorite-content", "hidden");
            contentEl.innerHTML = marked.parse(formatAssistantMarkdown(fav.content));
            item.appendChild(contentEl);
            
            // Toggle expansion on title click
            titleEl.addEventListener("click", function () {
              contentEl.classList.toggle("hidden");
            });
            
            // Trash icon for deletion
            const trashIcon = document.createElement("span");
            trashIcon.classList.add("delete-fav-icon");
            trashIcon.innerHTML = "&#128465;";
            trashIcon.title = "Delete Favorite";
            trashIcon.addEventListener("click", (e) => {
              e.stopPropagation();
              deleteFavorite(fav.id);
            });
            item.appendChild(trashIcon);

            favoritesListView.appendChild(item);
          });
        }
      })
      .catch((error) => console.error("Error:", error));
  }

  // Delete a favorite via backend
  function deleteFavorite(favId) {
    fetch(`/delete_favorite/${favId}`, { method: "POST" })
      .then((response) => response.json())
      .then(() => loadFavorites())
      .catch((error) => console.error("Error:", error));
  }

  // Toggle between Chat view and Favorites view when the favorites button is clicked
  favoritesBtn.addEventListener("click", () => {
    if (favoritesView.classList.contains("hidden")) {
      // Show favorites view and hide chat view
      loadFavorites();
      chatView.classList.add("hidden");
      favoritesView.classList.remove("hidden");
    } else {
      // Hide favorites view and show chat view
      favoritesView.classList.add("hidden");
      chatView.classList.remove("hidden");
    }
  });

  sendBtn.addEventListener("click", sendMessage);
  messageInput.addEventListener("keydown", function (e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });

  newChatBtn.addEventListener("click", () => {
    favoritesView.classList.add("hidden");
    chatView.classList.remove("hidden");
    fetch("/new_chat", { method: "POST" })
      .then((response) => response.json())
      .then(() => {
        chatLog.innerHTML = "";
        messageInput.placeholder = "enter ingredients here";
        updatePastChats();
      })
      .catch((error) => console.error("Error:", error));
  });

  // Initial update of past chats on page load
  updatePastChats();
});