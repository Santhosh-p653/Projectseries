let processes = [];

document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("processForm");
    const runBtn = document.getElementById("runSim");

    // Add process dynamically
    form.addEventListener("submit", (e) => {
        e.preventDefault();
        const pid = document.getElementById("pid").value;
        const arrival = parseInt(document.getElementById("arrival").value);
        const burst = parseInt(document.getElementById("burst").value);

        processes.push({ id: pid, arrival: arrival, burst: burst });
        alert(`Process ${pid} added!`);
        form.reset();
    });

    // Run simulation
    runBtn.addEventListener("click", async () => {
        if (processes.length === 0) {
            alert("Add processes first!");
            return;
        }

        const res = await fetch("/simulate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ processes })
        });

        const data = await res.json();
        const states = data.states;   // Step-by-step queue states
        const ganttData = data.gantt; // Gantt chart

        const readyDiv = document.getElementById("readyQueue");
        const runningDiv = document.getElementById("runningProcess");
        const completedDiv = document.getElementById("completedQueue");
        const ganttDiv = document.getElementById("gantt");

        // Clear previous content
        readyDiv.innerHTML = "";
        runningDiv.innerHTML = "";
        completedDiv.innerHTML = "";
        ganttDiv.innerHTML = "";

        // Animate queues and Gantt chart step by step
        for (let i = 0; i < states.length; i++) {
            const step = states[i];

            // Ready queue
            readyDiv.innerHTML = step.ready.length
                ? step.ready.map(id => `<div class="queue-box">${id}</div>`).join("")
                : "<div style='color:#aaa'>Empty</div>";

            // Running process
            runningDiv.innerHTML = step.running
                ? `<div class="running-box">${step.running}</div>`
                : "<div style='color:#aaa'>None</div>";

            // Completed queue
            completedDiv.innerHTML = step.completed.length
                ? step.completed.map(id => `<div class="completed-box">${id}</div>`).join("")
                : "<div style='color:#aaa'>Empty</div>";

            // Gantt chart
            ganttDiv.innerHTML = ganttData.slice(0, i + 1)
                .map(g => `<div class="gantt-box">${g.process || "-"}</div>`).join("");

            await new Promise(r => setTimeout(r, 500)); // animation speed
        }
    });
});
