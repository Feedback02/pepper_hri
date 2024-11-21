// detect_emotion.js

(function() {
    // Select the video and emotion display elements by ID
    const video = document.getElementById('video');
    const emotionDisplay = document.getElementById('emotion');

    // Function to load face-api.js models
    const loadModels = async () => {
        try {
            console.log('Loading face-api.js models...');
            await faceapi.nets.tinyFaceDetector.loadFromUri('/models');
            await faceapi.nets.faceExpressionNet.loadFromUri('/models');
            console.log('Models loaded successfully.');
        } catch (error) {
            console.error('Error loading models:', error);
        }
    };

    // Function to start the webcam video stream
    const startVideo = async () => {
        try {
            console.log('Starting video stream...');
            const stream = await navigator.mediaDevices.getUserMedia({ video: true });
            video.srcObject = stream;
            console.log('Video stream started.');
        } catch (error) {
            console.error('Error accessing the camera:', error);
        }
    };

    // Function to send emotion data via Fetch API with async/await
    const sendEmotionData = async (emotion) => {
        try {
            const response = await fetch('http://localhost:5000/emotion', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ emotion }),
            });
            const data = await response.json();
            console.log('Emotion data sent:', data);
        } catch (error) {
            console.error('Error sending emotion data:', error);
        }
    };

    // Function to detect emotions
    const detectEmotion = async () => {
        if (video.paused || video.ended) {
            return;
        }

        const detections = await faceapi
            .detectAllFaces(video, new faceapi.TinyFaceDetectorOptions())
            .withFaceExpressions();

        if (detections.length > 0) {
            const emotions = detections[0].expressions;
            const maxEmotion = Object.keys(emotions).reduce((a, b) =>
                emotions[a] > emotions[b] ? a : b
            );
            emotionDisplay.textContent = `Detected Emotion: ${maxEmotion}`;
            // Send the emotion data to the server
            sendEmotionData(maxEmotion);
        } else {
            emotionDisplay.textContent = 'Detected Emotion: None';
        }
    };

    // Start emotion detection at regular intervals
    const startEmotionDetection = () => {
        const detectionInterval = 1000; // Interval in milliseconds

        setInterval(async () => {
            await detectEmotion();
        }, detectionInterval);
    };

    // Initialize the video stream and load models
    document.addEventListener('DOMContentLoaded', async () => {
        await loadModels();
        await startVideo();
    });

    // Start emotion detection once the video starts playing
    video.addEventListener('play', () => {
        console.log('Video started playing. Starting emotion detection...');
        startEmotionDetection();
    });
})();
