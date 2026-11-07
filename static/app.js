// ================================
// STATUS MESSAGE FUNCTION
// ================================
function setStatus(message, isError = false) {
    const status = document.getElementById("status");
    status.innerText = message;
    status.style.color = isError ? "red" : "green";
}


// ================================
// AUTO GENERATE RESUME
// ================================
async function autoGenerateResume() {

    const interest = document.getElementById("interest").value;

    if (!interest) {
        setStatus("❌ Please enter job interest", true);
        return;
    }

    // Collect profile data
    const profile = {
        name: document.getElementById("name").value,
        email: document.getElementById("email").value,
        linkedin: document.getElementById("linkedin").value,
        github: document.getElementById("github").value,
        experience: document.getElementById("experience").value,
        skills: ["Python", "FastAPI", "Automation"]  // You can improve this later
    };

    setStatus("⏳ Searching job & generating resume...");

    try {
        const response = await fetch("/auto-generate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                interest: interest,
                profile: profile
            })
        });

        const data = await response.json();

        if (data.error) {
            setStatus("❌ " + data.error, true);
            return;
        }
        // Show job info
document.getElementById("jobInfoBox").innerHTML = `
    <strong>Job:</strong> ${data.job_title} <br>
    <strong>Company:</strong> ${data.company}
`;

// Show resume
document.getElementById("resumeEditor").value = data.resume_text;

// Show ATS score
document.getElementById("atsScore").innerText = data.ats_score + "%";

       

        setStatus("✅ Resume Generated Successfully!");

    } catch (error) {
        console.error(error);
        setStatus("❌ Failed to generate resume", true);
    }
}


// ================================
// UPDATE RESUME (EDIT FEATURE)
// ================================
async function updateResume() {

    const updatedResume = document.getElementById("resumeEditor").value;

    if (!updatedResume) {
        setStatus("❌ Resume is empty", true);
        return;
    }

    setStatus("⏳ Recalculating ATS...");

    try {

        const response = await fetch("/edit-resume", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                resume_text: updatedResume,
                job_description: updatedResume  // Simple recalculation
            })
        });

        const data = await response.json();

        if (data.error) {
            setStatus("❌ " + data.error, true);
            return;
        }

        document.getElementById("atsScore").innerText = data.ats_score + "%";

        setStatus("✅ Resume Updated & ATS Recalculated!");

    } catch (error) {
        console.error(error);
        setStatus("❌ Failed to update resume", true);
    }
}


// ================================
// DOWNLOAD RESUME
// ================================
function downloadResume() {
    window.open("/download-resume", "_blank");
}


// ================================
// EVENT LISTENERS
// ================================
document.addEventListener("DOMContentLoaded", function () {

    const autoGenerateBtn = document.getElementById("autoGenerateBtn");
    if (autoGenerateBtn) {
        autoGenerateBtn.addEventListener("click", autoGenerateResume);
    }

    const updateResumeBtn = document.getElementById("updateResumeBtn");
    if (updateResumeBtn) {
        updateResumeBtn.addEventListener("click", updateResume);
    }

    const downloadBtn = document.getElementById("downloadBtn");
    if (downloadBtn) {
        downloadBtn.addEventListener("click", downloadResume);
    }

});