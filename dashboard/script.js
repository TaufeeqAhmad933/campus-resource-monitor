const API_URL = "http://127.0.0.1:8000/analysis";

fetch(API_URL)
  .then(res => res.json())
  .then(data => {
    const overloadedDiv = document.getElementById("overloaded");
    const underutilizedDiv = document.getElementById("underutilized");
    const recommendationsDiv = document.getElementById("recommendations");

    // CLEAR OLD CONTENT (IMPORTANT)
    overloadedDiv.innerHTML = "";
    underutilizedDiv.innerHTML = "";
    recommendationsDiv.innerHTML = "";

    // Overloaded
    if (data.analysis.overloaded.length === 0) {
      overloadedDiv.innerHTML = "<p>No overloaded resources 🎉</p>";
    } else {
      data.analysis.overloaded.forEach(r => {
        const div = document.createElement("div");
        div.className = "card overloaded";
        div.innerText = `${r.name} — ${Math.round(r.load_ratio * 100)}% used`;
        overloadedDiv.appendChild(div);
      });
    }

    // Underutilized
    if (data.analysis.underutilized.length === 0) {
      underutilizedDiv.innerHTML = "<p>No underutilized resources</p>";
    } else {
      data.analysis.underutilized.forEach(r => {
        const div = document.createElement("div");
        div.className = "card underutilized";
        div.innerText = `${r.name} — ${Math.round(r.load_ratio * 100)}% used`;
        underutilizedDiv.appendChild(div);
      });
    }

    // Recommendations
    if (data.recommendations.length === 0) {
      recommendationsDiv.innerHTML = "<p>No recommendations</p>";
    } else {
      data.recommendations.forEach(rec => {
        const div = document.createElement("div");
        div.className = "card recommendation";
        div.innerText = rec.reason;
        recommendationsDiv.appendChild(div);
      });
    }
  })
  .catch(err => {
    console.error("Dashboard error:", err);
  });
