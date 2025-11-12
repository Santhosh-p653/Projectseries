def simulate_processes(processes):
    """
    Simulate processes in FCFS manner with step-by-step states
    Returns:
        states: list of dicts containing ready, running, completed at each time unit
        gantt: list of dicts with time and running process
    """
    # Make a deep copy to avoid modifying original burst times
    processes = [p.copy() for p in sorted(processes, key=lambda x: x["arrival"])]
    time = 0
    states = []
    gantt = []

    ready = []
    completed = []
    running = None

    while len(completed) < len(processes):
        # Add arrived processes to ready queue (if not running/completed)
        for p in processes:
            if p["arrival"] <= time and p not in ready and p not in completed and p != running:
                ready.append(p)

        # Pick next process to run (FCFS)
        if running is None and ready:
            running = ready.pop(0)

        # Record current state
        states.append({
            "ready": [proc["id"] for proc in ready],
            "running": running["id"] if running else None,
            "completed": [proc["id"] for proc in completed]
        })
        gantt.append({"time": time, "process": running["id"] if running else None})

        # Execute one time unit
        if running:
            running["burst"] -= 1
            if running["burst"] == 0:
                completed.append(running)
                running = None

        time += 1

    return states, gantt
