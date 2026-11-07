console.log("✅ JobScanner content script loaded");

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  console.log("📩 Message received in content.js:", request);

  if (request.type === "GET_JOB_URL") {
    const jobUrl = window.location.href;
    sendResponse({ jobUrl });
  }

  return true; // IMPORTANT
});
