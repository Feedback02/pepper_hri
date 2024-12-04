(async function() {
    // Select the video and display elements by ID
    const video = document.getElementById('video');
    const emotionDisplay = document.getElementById('emotion');
    const userDisplay = document.getElementById('user_identified');

    // Array to hold labeled face descriptors
    let labeledFaceDescriptors = [];

    // Initialize face matcher
    let faceMatcher;

    // Function to load face-api.js models
    const loadModels = async () => {
        try {
            console.log('Loading face-api.js models...');
            await faceapi.nets.tinyFaceDetector.loadFromUri('/models');
            await faceapi.nets.faceExpressionNet.loadFromUri('/models');
            await faceapi.nets.faceRecognitionNet.loadFromUri('/models');
            console.log('Models loaded successfully.');
        } catch (error) {
            console.error('Error loading models:', error);
        }
    };

    // Function to load labeled images and create descriptors
    const loadLabeledImages = async () => {
        const labels = ['Alice', 'Bob']; // Replace with your known names

        return Promise.all(
            labels.map(async label => {
                const descriptions = [];
                for (let i = 1; i <= 5; i++) { // Assuming 5 images per person
                    try {
                        const img = await faceapi.fetchImage(`/known_faces/${label}/img${i}.jpg`);
                        const detections = await faceapi
                            .detectSingleFace(img, new faceapi.TinyFaceDetectorOptions())
                            .withFaceLandmarks()
                            .withFaceDescriptor();
                        if (!detections) {
                            console.warn(`No face detected in image: /known_faces/${label}/img${i}.jpg`);
                            continue;
                        }
                        descriptions.push(detections.descriptor);
                    } catch (error) {
                        console.error(`Error processing image /known_faces/${label}/img${i}.jpg:`, error);
                    }
                }
                if (descriptions.length === 0) {
                    console.warn(`No valid faces found for label: ${label}`);
                }
                return new faceapi.LabeledFaceDescriptors(label, descriptions);
            })
        );
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

    // Function to send recognized user data via Fetch API
    const sendUserData = async (userName, emotion) => {
        try {
            const response = await fetch('http://localhost:5000/user_data', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user: userName, emotion: emotion }),
            });
            const data = await response.json();
            console.log('User data sent:', data);
        } catch (error) {
            console.error('Error sending user data:', error);
        }
    };

    // Function to detect emotions and recognize faces
    const detectAndRecognize = async () => {
        if (video.paused || video.ended) {
            return;
        }

        const detections = await faceapi
            .detectAllFaces(video, new faceapi.TinyFaceDetectorOptions())
            .withFaceLandmarks()
            .withFaceExpressions()
            .withFaceDescriptors();

        if (detections.length > 0) {
            detections.forEach(detection => {
                const { expressions, descriptor } = detection;
                
                // Emotion Detection
                const maxEmotion = Object.keys(expressions).reduce((a, b) =>
                    expressions[a] > expressions[b] ? a : b
                );
                emotionDisplay.textContent = `Detected Emotion: ${maxEmotion}`;
                
                // Face Recognition
                const bestMatch = faceMatcher.findBestMatch(descriptor);
                if (bestMatch.label !== 'unknown') {
                    userDisplay.textContent = `User: ${bestMatch.label}`;
                    // Send data to backend
                    sendUserData(bestMatch.label, maxEmotion);
                } else {
                    userDisplay.textContent = `User: Unknown`;
                }
            });
        } else {
            emotionDisplay.textContent = 'Detected Emotion: None';
            userDisplay.textContent = `User: Unknown`;
        }
    };

    // Start detection at regular intervals
    const startDetection = () => {
        const detectionInterval = 1000; // 1 second

        setInterval(async () => {
            await detectAndRecognize();
        }, detectionInterval);
    };

    // Initialize everything
    document.addEventListener('DOMContentLoaded', async () => {
        await loadModels();
        labeledFaceDescriptors = await loadLabeledImages();
        faceMatcher = new faceapi.FaceMatcher(labeledFaceDescriptors, 0.6); // 0.6 is the tolerance
        await startVideo();
    });

    // Start detection once the video starts playing
    video.addEventListener('play', () => {
        console.log('Video started playing. Starting emotion and face recognition...');
        startDetection();
    });
})();
