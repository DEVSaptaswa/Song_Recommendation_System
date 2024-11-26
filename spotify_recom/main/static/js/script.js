const body = document.body;

    // Add an event listener to track mouse movements
document.addEventListener("mousemove", (e) => {
    // Calculate mouse position as a percentage of the viewport
    const x = (e.clientX / window.innerWidth) * 100;
    const y = (e.clientY / window.innerHeight) * 100;

        // Update the background gradient to follow the cursor
    body.style.background = `radial-gradient(circle at ${x}% ${y}%, #b6f0b0 0%, white 80%)`;
});