// =========================================
// CHAT WITH AI
// =========================================

const askButton = document.getElementById("askAIButton");
const chatMessages = document.getElementById("chatMessages");
const input = document.getElementById("chatQuestion");

askButton.addEventListener("click", askAI);

input.addEventListener("keydown", function (e) {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    askAI();
  }
});

// auto-grow textarea
input.addEventListener("input", function () {
  input.style.height = "auto";
  input.style.height = Math.min(input.scrollHeight, 100) + "px";
});

// suggestion chip clicks
chatMessages.addEventListener("click", function (e) {
  const chip = e.target.closest(".chip");
  if (chip) {
    input.value = chip.dataset.q;
    askAI();
  }
});

async function askAI() {
  const question = input.value.trim();
  if (question === "") return;

  appendUserMessage(question);
  input.value = "";
  input.style.height = "auto";
  askButton.disabled = true;

  const typing = document.createElement("div");
  typing.className = "ai-message";
  typing.id = "typing";
  typing.innerHTML = `
    <div class="msg-avatar">🤖</div>
    <div class="msg-bubble">
      <div class="typing-indicator"><span></span><span></span><span></span></div>
    </div>`;
  chatMessages.appendChild(typing);
  scrollBottom();

  try {
    const response = await fetch("/dashboard-chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: question }),
    });

    const data = await response.json();
    document.getElementById("typing")?.remove();
    appendAIMessage(data.answer);
  } catch (error) {
    document.getElementById("typing")?.remove();
    appendAIMessage("⚠️ Unable to contact AI. Please try again.");
    console.error(error);
  } finally {
    askButton.disabled = false;
  }
}

function appendUserMessage(message) {
  const row = document.createElement("div");
  row.className = "user-message-row";
  row.innerHTML = `<div class="user-message"></div>`;
  row.querySelector(".user-message").textContent = message;
  chatMessages.appendChild(row);
  scrollBottom();
}

function appendAIMessage(message) {
  const div = document.createElement("div");
  div.className = "ai-message";
  div.innerHTML = `<div class="msg-avatar">🤖</div><div class="msg-bubble"></div>`;
  div.querySelector(".msg-bubble").textContent = message;
  chatMessages.appendChild(div);
  scrollBottom();
}

function scrollBottom() {
  chatMessages.scrollTop = chatMessages.scrollHeight;
}