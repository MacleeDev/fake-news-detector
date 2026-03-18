document.getElementById("analyzeBtn").onclick = async () => {

  const text = document.getElementById("newsText").value.trim();
  const demoMode = document.getElementById("demoToggle").checked; // ✅ demo toggle

  if (!text) return alert("Enter some text");

  // 👤 Show user message
  appendMessage(text, "user");

  // 🤖 Loading message
  appendMessage("🧠 Analyzing article...", "bot");

  try {
    // ✅ If demo mode is on, show fake output
    if (demoMode) {
      const loadingMsg = document.querySelector("#chat-window .message.bot:last-child");
      if (loadingMsg) loadingMsg.remove();

      appendMessage(
        "Prediction: <strong>FAKE</strong><br>Confidence: 95%",
        "bot"
      );
      return; // skip backend
    }

    // ❌ Normal API call for real input
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