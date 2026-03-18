//////////////////////////////
// 💬 MESSAGE APPENDER
//////////////////////////////

function appendMessage(text, sender = "bot") {
  const chatWindow = document.getElementById("chat-window");

  const msg = document.createElement("div");
  msg.className = `message ${sender}`;

  // Allow HTML (needed for result cards)
  msg.innerHTML = text;

  chatWindow.appendChild(msg);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}


//////////////////////////////
// ✂️ SPLIT INTO SENTENCES
//////////////////////////////

function splitSentences(text) {
  return text.match(/[^.!?]+[.!?]+/g) || [text];
}


//////////////////////////////
// 🧠 HIGHLIGHT FAKE SENTENCES
//////////////////////////////

async function analyzeArticle(text) {

  const sentences = splitSentences(text);

  let highlighted = "";
  let fakeCount = 0;

  for (const sentence of sentences) {

    const data = await analyzeText(sentence);

    if (data.prediction === "FAKE") {
      fakeCount++;
      highlighted += `<span class="highlight-fake">${sentence}</span> `;
    } else {
      highlighted += sentence + " ";
    }
  }

  const overall =
    fakeCount > sentences.length / 2 ? "FAKE" : "LIKELY REAL";

  appendMessage(`<strong>Overall Verdict: ${overall}</strong>`, "bot");
  appendMessage(highlighted, "bot");
}


//////////////////////////////
// 🏆 ELITE RESULT CARD
//////////////////////////////

function renderResult(data) {

  const percent = Math.round(data.confidence * 100);

  const verdictColor =
    data.prediction === "REAL" ? "#22c55e" : "#ef4444";

  const trust =
    percent > 80 ? "Very High"
    : percent > 60 ? "High"
    : percent > 40 ? "Medium"
    : "Low";

  return `
    <div class="result-card">

      <div class="verdict"
           style="background:${verdictColor}">
        ${data.prediction}
      </div>

      <div class="confidence">

        <div class="confidence-label">
          Confidence: ${percent}% (${trust})
        </div>

        <div class="gauge">
          <div class="gauge-fill"
               style="width:${percent}%"></div>
        </div>

      </div>

    </div>
  `;
}