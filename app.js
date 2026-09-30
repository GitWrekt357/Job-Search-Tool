async function loadJobs() {
    const keyword = document.getElementById("keyword").value;
    const minSalary = document.getElementById("min-salary").value;
    const remoteOnly = document.getElementById("remote-only").checked;

    let url = `/api/jobs?min_salary=${minSalary}&remote_only=${remoteOnly}`;
    if (keyword) url += `&keyword=${encodeURIComponent(keyword)}`;

    setStatus("Searching...");

    try {
        const response = await fetch(url);
        const jobs = await response.json();
        renderJobs(jobs);
        setStatus(`${jobs.length} job${jobs.length !== 1 ? "s" : ""} found`);
    } catch (err) {
        setStatus("Error loading jobs. Is the server running?");
        console.error(err);
    }
}

async function fetchNew() {
    const keyword = document.getElementById("keyword").value || "technical support";
    setStatus("Fetching new listings from APIs...");

    try {
        const response = await fetch(`/api/fetch?keyword=${encodeURIComponent(keyword)}`);
        const data = await response.json();
        setStatus(data.message);
        loadJobs();
    } catch (err) {
        setStatus("Fetch failed. Is the server running?");
        console.error(err);
    }
}

function renderJobs(jobs) {
    const container = document.getElementById("results");

    if (jobs.length === 0) {
        container.innerHTML = `<p style="color:#666;">No jobs found. Try adjusting filters or fetching new listings.</p>`;
        return;
    }

    container.innerHTML = jobs.map(job => `
    <div class="job-card">
    <a class="job-title" href="${job.url}" target="_blank">${job.title}</a>
    <div class="job-meta">
    <span>${job.company}</span>
    <span>${job.location}</span>
    ${job.remote ? '<span class="remote-badge">Remote</span>' : ""}
    ${job.salary_min ? `<span class="salary">$${Math.round(job.salary_min / 1000)}k${job.salary_max && job.salary_max !== job.salary_min ? ` – $${Math.round(job.salary_max / 1000)}k` : ""}</span>` : ""}
    </div>
    <div class="job-description">${job.description || "No description available."}</div>
    <div class="source-tag">via ${job.source} · ${formatDate(job.date_posted)}</div>
    </div>
    `).join("");
}

function formatDate(dateStr) {
    if (!dateStr) return "unknown date";
    const d = new Date(dateStr);
    return d.toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" });
}

function setStatus(msg) {
    document.getElementById("status").textContent = msg;
}

window.onload = loadJobs;
