// Initial connection to Pepper robot
var ip = window.location.hostname;
if (ip === '') ip = '127.0.0.1';
var port = 9100;

console.log("Trying connection...");
wsrobot_init(ip, port);

// Timer Variables
let timeLeft = 30; // Default time (will be overridden upon level selection)
let countdown; // Reference to the countdown interval
const timerElement = document.getElementById('timer'); // Timer display element

// Containers
const answersContainer = document.getElementById('buttons'); // Container for level and answer buttons
const quizContainer = document.querySelector('.quiz-container'); // Container to observe for mutations
const textStory = document.getElementById('text_story'); // Container to observe for "break"

// Game State
let selectedLevel = null; // To store the currently selected level
let quizObserver = null; // MutationObserver for quiz-container
let textStoryObserver = null; // MutationObserver for text_story
let videoModal = null; // Reference to the video modal

/**
 * Sets the timer duration based on the selected level.
 * @param {string} level - The selected level ("Easy", "Medium", "Difficult").
 */
function setLevel(level) {
    selectedLevel = level;
    switch (level) {
        case 'Easy':
            timeLeft = 30;
            break;
        case 'Medium':
            timeLeft = 20;
            break;
        case 'Difficult':
            timeLeft = 10;
            break;
        default:
            console.warn(`Unknown level: ${level}. Defaulting to 30 seconds.`);
            timeLeft = 30;
    }
    updateTimerDisplay();
}

/**
 * Updates the timer display with the current timeLeft.
 */
function updateTimerDisplay() {
    timerElement.textContent = `Time Left: ${timeLeft}s`;
}

/**
 * Starts the countdown timer.
 */
function startTimer() {
    // Clear any existing countdown to prevent multiple timers
    clearInterval(countdown);

    // Update the timer display immediately
    updateTimerDisplay();

    // Start the countdown
    countdown = setInterval(() => {
        timeLeft--;
        updateTimerDisplay();

        // Check if time has run out
        if (timeLeft <= 0) {
            clearInterval(countdown); // Stop the countdown
            timerElement.textContent = "Time's Up!"; // Display message

            // Disable answer buttons when time is up
            disableAnswerButtons();
        }
    }, 1000);
}

/**
 * Resets the timer based on the currently selected level.
 */
function resetTimer() {
    if (!selectedLevel) {
        console.warn("Timer reset attempted without a selected level.");
        return;
    }
    clearInterval(countdown); // Stop the existing timer
    setLevel(selectedLevel); // Reset time based on selected level
    startTimer(); // Start a new timer
}

/**
 * Disables all answer buttons and styles them to indicate they are disabled.
 */
function disableAnswerButtons() {
    // Select all input buttons inside answersContainer
    const buttons = answersContainer.querySelectorAll('input[type="button"]');
    buttons.forEach(button => {
        button.disabled = true;
        button.style.backgroundColor = '#ccc'; // Optional: Change button style to indicate they're disabled
        button.style.cursor = 'not-allowed'; // Change cursor to not-allowed
    });
}

/**
 * Enables all answer buttons and resets their styles.
 */
function enableAnswerButtons() {
    // Select all input buttons inside answersContainer
    const buttons = answersContainer.querySelectorAll('input[type="button"]');
    buttons.forEach(button => {
        button.disabled = false;
        button.style.backgroundColor = ''; // Reset to original style
        button.style.cursor = 'pointer'; // Reset cursor
    });
}

/**
 * Attaches click event listeners to level buttons.
 * @param {HTMLElement} button - The input button element to attach the listener to.
 */
function attachLevelButtonListener(button) {
    // Avoid attaching multiple listeners
    if (button.dataset.eventAttached) return;

    button.addEventListener('click', () => {
        const level = button.value.trim(); // Get the value attribute ("Easy", "Medium", "Difficult")
        setLevel(level); // Set the level and timer
        startTimer(); // Start the timer
        enableAnswerButtons(); // Enable answer buttons if they were disabled

        // Start observing the quiz-container for changes after level selection
        enableQuizObserver();
    });

    button.dataset.eventAttached = "true"; // Mark as having an event listener
}

/**
 * Observes the answers-container for dynamically added level buttons and attaches listeners.
 */
function observeAnswersContainer() {
    const observer = new MutationObserver((mutationsList) => {
        for (let mutation of mutationsList) {
            if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
                mutation.addedNodes.forEach(node => {
                    if (node.nodeType === Node.ELEMENT_NODE && node.tagName === 'INPUT') {
                        const buttonType = node.getAttribute('type');
                        const buttonValue = node.getAttribute('value')?.trim();
                        // Check if the input is a button and has one of the level values
                        if (buttonType === 'button' && ['Easy', 'Medium', 'Difficult'].includes(buttonValue)) {
                            attachLevelButtonListener(node);
                        }
                    }
                });
            }
        }
    });

    observer.observe(answersContainer, { childList: true, subtree: true });

    // Optionally, handle existing level buttons if any are already present
    const existingButtons = answersContainer.querySelectorAll('input[type="button"]');
    existingButtons.forEach(button => {
        const buttonValue = button.value.trim();
        if (['Easy', 'Medium', 'Difficult'].includes(buttonValue)) {
            attachLevelButtonListener(button);
        }
    });
}

/**
 * Enables the MutationObserver for the quiz-container to reset the timer on any change.
 */
function enableQuizObserver() {
    if (quizObserver) return; // Avoid setting multiple observers

    quizObserver = new MutationObserver((mutationsList) => {
        // Any mutation detected will trigger the timer reset
        resetTimer();
    });

    quizObserver.observe(quizContainer, { childList: true, subtree: true, attributes: true, characterData: true });
}

/**
 * Creates and displays a modal with a YouTube video.
 * @param {string} videoId - The YouTube video ID to play.
 */
function playYouTubeVideo(videoId) {
    // If modal already exists, remove it to avoid duplicates
    if (videoModal) {
        videoModal.remove();
    }

    // Create modal overlay
    videoModal = document.createElement('div');
    videoModal.id = 'video-modal';
    videoModal.style.position = 'fixed';
    videoModal.style.top = '0';
    videoModal.style.left = '0';
    videoModal.style.width = '100%';
    videoModal.style.height = '100%';
    videoModal.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';
    videoModal.style.display = 'flex';
    videoModal.style.justifyContent = 'center';
    videoModal.style.alignItems = 'center';
    videoModal.style.zIndex = '1000';

    // Create iframe for YouTube video
    const iframe = document.createElement('iframe');
    iframe.width = '560';
    iframe.height = '315';
    iframe.src = `https://www.youtube.com/embed/NsUWXo8M7UA?si=Vf7y5JflnjXwPe4c&autoplay=1&mute=1`; // Added mute=1 for autoplay
    iframe.title = 'YouTube video player';
    iframe.frameBorder = '0';
    iframe.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture';
    iframe.allowFullscreen = true;

    // Create close button
    const closeButton = document.createElement('span');
    closeButton.innerHTML = '&times;';
    closeButton.style.position = 'absolute';
    closeButton.style.top = '20px';
    closeButton.style.right = '35px';
    closeButton.style.color = '#f1f1f1';
    closeButton.style.fontSize = '40px';
    closeButton.style.fontWeight = 'bold';
    closeButton.style.cursor = 'pointer';
    closeButton.style.zIndex = '1001';

    // Create Unmute button (optional)
    const unmuteButton = document.createElement('button');
    unmuteButton.textContent = 'Unmute';
    unmuteButton.style.position = 'absolute';
    unmuteButton.style.bottom = '20px';
    unmuteButton.style.right = '35px';
    unmuteButton.style.padding = '10px 20px';
    unmuteButton.style.fontSize = '16px';
    unmuteButton.style.cursor = 'pointer';
    unmuteButton.style.zIndex = '1001';

    // Unmute video when unmute button is clicked
    unmuteButton.addEventListener('click', () => {
        iframe.contentWindow.postMessage('{"event":"command","func":"unMute","args":""}', '*');
    });

    // Close modal when close button is clicked
    closeButton.addEventListener('click', () => {
        videoModal.remove();
        videoModal = null;
    });

    // Close modal when clicking outside the video
    videoModal.addEventListener('click', (event) => {
        if (event.target === videoModal) {
            videoModal.remove();
            videoModal = null;
        }
    });

    // Append iframe, close button, and unmute button to modal
    videoModal.appendChild(closeButton);
    videoModal.appendChild(iframe);
    videoModal.appendChild(unmuteButton);

    // Append modal to body
    document.body.appendChild(videoModal);

    // Initialize YouTube Player API for unmute functionality
    loadYouTubeIframeAPI();

    // Helper function to load YouTube Iframe API
    function loadYouTubeIframeAPI() {
        if (window.YT && window.YT.Player) {
            // YT API already loaded
            return;
        }

        const tag = document.createElement('script');
        tag.src = "https://www.youtube.com/iframe_api";
        const firstScriptTag = document.getElementsByTagName('script')[0];
        firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

        // Replace 'onYouTubeIframeAPIReady' with the actual handler if needed
    }
}

/**
 * Observes the text_story div for the word "break" and plays a YouTube video when detected.
 */
function observeTextStory() {
    const observer = new MutationObserver((mutationsList) => {
        for (let mutation of mutationsList) {
            if (mutation.type === 'childList' || mutation.type === 'characterData') {
                const currentText = textStory.textContent || '';
                if (currentText.toLowerCase().includes('break')) {
                    // Replace 'YOUR_YOUTUBE_VIDEO_ID' with the actual video ID you want to play
                    playYouTubeVideo('YOUR_YOUTUBE_VIDEO_ID');
                }
            }
        }
    });

    observer.observe(textStory, { childList: true, subtree: true, characterData: true });

    // Optionally, handle existing text if any
    const initialText = textStory.textContent || '';
    if (initialText.toLowerCase().includes('break')) {
        playYouTubeVideo('YOUR_YOUTUBE_VIDEO_ID');
    }
}

/**
 * Initializes the script by setting up observers.
 */
function init() {
    // Start observing the answers-container for level buttons
    observeAnswersContainer();

    // Start observing the text_story div for the word "break"
    observeTextStory();
}

// Initialize the script on page load
document.addEventListener('DOMContentLoaded', init);



/**
 * OPTIONAL: Simulate dynamic changes for testing purposes.
 * Remove or comment out in production.
 */
/*
// Simulate dynamic addition of level buttons after 2 seconds
setTimeout(() => {
    const levels = ['Easy', 'Medium', 'Difficult'];
    levels.forEach(level => {
        const button = document.createElement('input');
        button.type = 'button';
        button.value = level;
        button.name = level;
        button.id = level;
        button.classList.add('level-button'); // Optional: Add a class for styling
        answersContainer.appendChild(button);
    });
}, 2000);

// Simulate dynamic text change after 7 seconds to trigger "break"
setTimeout(() => {
    textStory.textContent = "Is everything clear? Let's take a break.";
}, 7000);

// Simulate dynamic changes in the quiz-container after selecting a level
setTimeout(() => {
    const quizItem = document.createElement('div');
    quizItem.textContent = 'Question 1: What letter is this? Select the right option.';
    quizContainer.appendChild(quizItem);

    // Simulate adding answer buttons
    const answerValues = ['E', 'G', 'M'];
    const answersInnerContainer = document.createElement('div');
    answersInnerContainer.classList.add('answers-container');
    answerValues.forEach(val => {
        const answerButton = document.createElement('input');
        answerButton.type = 'button';
        answerButton.value = val;
        answerButton.name = val;
        answerButton.id = val;
        answerButton.classList.add('answer-button'); // Optional: Add a class for styling
        answersInnerContainer.appendChild(answerButton);
    });
    quizContainer.appendChild(answersInnerContainer);
}, 5000);

// Simulate another change in the quiz-container after 10 seconds
setTimeout(() => {
    // Remove the previous question
    const oldQuizItem = quizContainer.querySelector('div');
    if (oldQuizItem) {
        quizContainer.removeChild(oldQuizItem);
    }

    // Add a new question
    const newQuizItem = document.createElement('div');
    newQuizItem.textContent = 'Question 2: What is the capital of France?';
    quizContainer.appendChild(newQuizItem);

    // Simulate adding new answer buttons
    const newAnswerValues = ['P', 'F', 'L'];
    const newAnswersInnerContainer = document.createElement('div');
    newAnswersInnerContainer.classList.add('answers-container');
    newAnswerValues.forEach(val => {
        const answerButton = document.createElement('input');
        answerButton.type = 'button';
        answerButton.value = val;
        answerButton.name = val;
        answerButton.id = val;
        answerButton.classList.add('answer-button'); // Optional: Add a class for styling
        newAnswersInnerContainer.appendChild(answerButton);
    });
    quizContainer.appendChild(newAnswersInnerContainer);
}, 10000);
 */
