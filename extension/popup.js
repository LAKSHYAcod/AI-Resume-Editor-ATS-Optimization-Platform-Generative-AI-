const status = document.getElementById("status");
const applyBtn = document.getElementById("applyBtn");

applyBtn.addEventListener("click", async () => {
  status.innerText = "Checking page...";

  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

  if (!tab.url.includes("linkedin.com/jobs")) {
    status.innerText = "❌ Not a LinkedIn job page";
    return;
  }

  chrome.tabs.sendMessage(
    tab.id,
    { type: "GET_JOB_URL" },
    async (response) => {
      if (chrome.runtime.lastError) {
        status.innerText = "❌ Content script not loaded";
        console.error(chrome.runtime.lastError);
        return;
      }

      const jobUrl = response.jobUrl;
      status.innerText = "🚀 Applying with AI...";

      const res = await fetch("http://127.0.0.1:8000/apply-with-ai", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          job_url: jobUrl,
          job_description: "Auto from LinkedIn",
          profile: {
            name: "John Doe",
            email: "john@example.com",
            skills: ["Python", "FastAPI"],
            experience: "3 years"
          }
        })
      });

      const data = await res.json();
      status.innerText = data.status || "✅ Done";
    }
  );
});
