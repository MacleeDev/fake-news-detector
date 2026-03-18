document.getElementById("analyzeBtn").onclick = async () => {

  const text = document.getElementById("newsText").value.trim();

  if (!text) return alert("Enter some text");

  // 👤 Show user message
  appendMessage(text, "user");

  // 🤖 Loading message
  appendMessage("🧠 Analyzing article...", "bot");

  try {

    const response = await fetch("http://127.0.0.1:8000/api/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text })
    });

    if (!response.ok) throw new Error("Server error");

    const data = await response.json();

    // ❌ Remove loading message
    const loadingMsg =
      document.querySelector("#chat-window .message.bot:last-child");

    if (loadingMsg) loadingMsg.remove();

    // 🏆 ELITE RESULT CARD
    appendMessage(renderResult(data), "bot");

  } catch (err) {

    console.error(err);

    appendMessage(
      "❌ Unable to contact AI server. Check backend.",
      "bot"
    );
  }
};


//////////////////////////////
// 📄 FILE UPLOAD HANDLER
//////////////////////////////

document.getElementById("uploadBtn").onclick = () => {

  const input = document.createElement("input");
  input.type = "file";
  input.accept = ".txt,.pdf";

  input.onchange = async e => {

    const file = e.target.files[0];
    if (!file) return;

    // TXT support
    if (file.type === "text/plain") {

      const text = await file.text();
      document.getElementById("newsText").value = text;

    }

    // PDF placeholder
    else if (file.type === "application/pdf") {

      alert("📄 PDF support coming soon. Paste text for now.");

    }

  };

  input.click();
};