(async function() {
    // Select the video and display elements by ID
    const video = document.getElementById('video');
    const emotionDisplay = document.getElementById('emotion');
    const userDisplay = document.getElementById('user_identified');
    const errorMessage = document.getElementById('error-message');

    // Array to hold labeled face descriptors
    let labeledFaceDescriptors = [];

    // Initialize face matcher
    let faceMatcher;

    /**
     * Function to load face-api.js models
     */
    const loadModels = async () => {
        try {
            console.log('Loading face-api.js models...');
            await faceapi.nets.tinyFaceDetector.loadFromUri('/models');
            console.log('TinyFaceDetector model loaded.');
            await faceapi.nets.faceLandmark68Net.loadFromUri('/models');
            console.log('FaceLandmark68Net model loaded.');
            await faceapi.nets.faceExpressionNet.loadFromUri('/models');
            console.log('FaceExpressionNet model loaded.');
            await faceapi.nets.faceRecognitionNet.loadFromUri('/models');
            console.log('FaceRecognitionNet model loaded.');
            console.log('All models loaded successfully.');
        } catch (error) {
            console.error('Error loading models:', error);
            errorMessage.textContent = 'Error loading models. Please check the console for details.';
        }
    };

    /**
     * Function to load labeled images and create descriptors
     */
    const loadLabeledImages = async () => {
        const labels = ['Alice', 'Bob']; // Replace with your known names
        const imagesPerLabel = {
            'Alice': 5, // Number of images for Alice
            'Bob': 4     // Number of images for Bob (assuming img5.jpg is missing)
        };

        const labeledDescriptors = await Promise.all(
            labels.map(async label => {
                const descriptions = [];
                const imageCount = imagesPerLabel[label] || 0;
                for (let i = 1; i <= imageCount; i++) {
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
                    console.warn(`No valid faces found for label: ${label}. This label will be excluded from recognition.`);
                    return null; // Exclude this label
                }
                console.log(`Loaded ${descriptions.length} descriptors for label: ${label}`);
                return new faceapi.LabeledFaceDescriptors(label, descriptions);
            })
        );

        console.log('Labeled face descriptors loaded:', labeledDescriptors);
        return labeledDescriptors.filter(ld => ld !== null); // Exclude labels with no valid descriptors
    };

    /**
     * Function to start the webcam video stream
     */
    const startVideo = async () => {
        try {
            console.log('Starting video stream...');
            const stream = await navigator.mediaDevices.getUserMedia({ video: true });
            video.srcObject = stream;
            console.log('Video stream started.');
        } catch (error) {
            console.error('Error accessing the camera:', error);
            errorMessage.textContent = 'Error accessing the camera. Please allow camera access and try again.';
        }
    };

    /**
     * Function to send recognized user data via Fetch API
     */
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
            // Optionally, display an error message to the user
            errorMessage.textContent = 'Error sending user data. Please check the console for details.';
        }
    };

    /**
     * Function to detect emotions and recognize faces
     */
    const detectAndRecognize = async () => {
        if (video.paused || video.ended) {
            console.log('Video is not playing.');
            return;
        }

        console.log('Detecting faces and expressions...');
        const detections = await faceapi
            .detectAllFaces(video, new faceapi.TinyFaceDetectorOptions())
            .withFaceLandmarks()
            .withFaceExpressions()
            .withFaceDescriptors();

        console.log(`Number of detections: ${detections.length}`);

        if (detections.length > 0) {
            detections.forEach(detection => {
                const { expressions, descriptor } = detection;
                
                // Emotion Detection
                const maxEmotion = Object.keys(expressions).reduce((a, b) =>
                    expressions[a] > expressions[b] ? a : b
                );
                emotionDisplay.textContent = `Detected Emotion: ${maxEmotion}`;
                console.log(`Detected Emotion: ${maxEmotion}`);
                
                // Face Recognition (Optional)
                if (faceMatcher) {
                    const bestMatch = faceMatcher.findBestMatch(descriptor);
                    console.log(`Best match: ${bestMatch.toString()}`);
                    if (bestMatch.label !== 'unknown') {
                        userDisplay.textContent = `User: ${bestMatch.label}`;
                        // Send data to backend
                        sendUserData(bestMatch.label, maxEmotion);
                    } else {
                        userDisplay.textContent = `User: Unknown`;
                    }
                } else {
                    userDisplay.textContent = `User: Recognition not available`;
                }
            });
        } else {
            emotionDisplay.textContent = 'Detected Emotion: None';
            userDisplay.textContent = `User: Unknown`;
        }
    };

    /**
     * Start detection at regular intervals
     */
    const startDetection = () => {
        const detectionInterval = 1000; // 1 second

        setInterval(async () => {
            try {
                await detectAndRecognize();
            } catch (error) {
                console.error('Error during detection:', error);
                errorMessage.textContent = 'Error during detection. Please check the console for details.';
            }
        }, detectionInterval);
    };

    /**
     * Initialize everything
     */
    document.addEventListener('DOMContentLoaded', async () => {
        await loadModels();
        labeledFaceDescriptors = await loadLabeledImages();
        if (labeledFaceDescriptors.length === 0) {
            console.warn('No labeled face descriptors available. Face recognition will not work.');
            userDisplay.textContent = `User: Recognition not available`;
        } else {
            faceMatcher = new faceapi.FaceMatcher(labeledFaceDescriptors, 0.6); // 0.6 is the tolerance
            console.log('FaceMatcher initialized.');
        }
        await startVideo();
    });

    /**
     * Start detection once the video starts playing
     */
    video.addEventListener('play', () => {
        console.log('Video started playing. Starting emotion and face recognition...');
        startDetection();
    });
})();

