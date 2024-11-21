// Initial connection to Pepper robot
var ip = window.location.hostname;
if (ip == '') ip = '127.0.0.1';
var port = 9100;

console.log("Trying connection...");
wsrobot_init(ip, port);



// Set initial time in seconds
let timeLeft = 30;
let countdown; // Declare countdown variable here for later access
const timerElement = document.getElementById('timer');

// Function to start the timer
function startTimer() {
    // Enable answer buttons when the timer starts
    document.querySelectorAll('.answer-button').forEach(button => {
        button.disabled = false;
    });

    // Clear any existing countdown (in case the timer was restarted)
    clearInterval(countdown);

    // Reset time if needed
    timeLeft = 30;
    timerElement.textContent = `Time Left: ${timeLeft}s`;

    // Start the countdown
    countdown = setInterval(() => {
        timeLeft--;
        timerElement.textContent = `Time Left: ${timeLeft}s`;

        // Check if time has run out
        if (timeLeft <= 0) {
            clearInterval(countdown); // Stop the countdown
            timerElement.textContent = "Time's Up!"; // Display message

            // Disable buttons when time is up
            document.querySelectorAll('.answer-button').forEach(button => {
                button.disabled = true;
                button.style.backgroundColor = '#ccc'; // Optional: Change button style to indicate they're disabled
            });

        }
    }, 1000);
}

// Observe the answers container for added nodes (like the "Start" button with ID "start")
const answersContainer = document.getElementById('buttons');
const observer = new MutationObserver(() => {
    const startButton = document.getElementById('start');
    if (startButton) {
        startButton.addEventListener('click', startTimer);
        observer.disconnect(); // Stop observing once the button is found and event is attached
    }
});

observer.observe(answersContainer, { childList: true });




