(function () {
  const form = document.getElementById("predict-form");
  const zipcodeInput = document.getElementById("zipcode");
  const countryInput = document.getElementById("country");
  const submitBtn = document.getElementById("submit-btn");
  const resultEl = document.getElementById("result");
  const resultTitle = document.getElementById("result-title");
  const resultBody = document.getElementById("result-body");
  const statusEl = document.getElementById("status");
  const statusText = document.getElementById("status-text");

  function showStatus(text, loading) {
    statusEl.hidden = false;
    statusText.textContent = text;
    statusEl.classList.toggle("status--loading", !!loading);
  }

  function hideStatus() {
    statusEl.hidden = true;
    statusEl.classList.remove("status--loading");
  }

  function showResult(success, title, body) {
    resultEl.hidden = false;
    resultEl.classList.toggle("result--error", !success);
    resultTitle.textContent = title;
    resultBody.textContent = body;
  }

  function hideResult() {
    resultEl.hidden = true;
  }

  form.addEventListener("submit", async function (e) {
    e.preventDefault();
    const zipcode = (zipcodeInput.value || "").trim();
    const country = (countryInput.value || "US").trim() || "US";

    if (!zipcode) {
      showResult(false, "Error", "Please enter a zipcode.");
      return;
    }

    hideResult();
    submitBtn.disabled = true;
    showStatus("Getting weather prediction…", true);

    try {
      const res = await fetch("/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ zipcode, country }),
      });

      const data = await res.json();

      if (!res.ok) {
        showResult(false, "Error", data.detail || data.message || "Request failed.");
        return;
      }

      if (data.success) {
        showResult(true, "Prediction", data.message);
      } else {
        showResult(false, "Error", data.message || data.error || "Unknown error.");
      }
    } catch (err) {
      showResult(false, "Error", err.message || "Network error. Is the server running?");
    } finally {
      hideStatus();
      submitBtn.disabled = false;
    }
  });
})();
