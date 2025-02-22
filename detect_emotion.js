(async function() {
    // Select the display elements by ID
    // const video = document.getElementById('video'); // Webcam element not used in manual mode
    const emotionDisplay = document.getElementById('emotion');
    const userDisplay = document.getElementById('user_identified');
    const errorMessage = document.getElementById('error-message'); // Ensure this element exists in your HTML

    // -------------------------------
    // Unused code for webcam and face detection:
    // -------------------------------
    /*
    // Array to hold labeled face descriptors
    let labeledFaceDescriptors = [];

    // Initialize face matcher
    let faceMatcher;

    // Function to load face-api.js models
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

    // Function to load labeled images and create descriptors
    const loadLabeledImages = async () => {
        const labels = ['Alice', 'Bob']; // Replace with your known names
        const imagesPerLabel = {
            'Alice': 5,
            'Bob': 4
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
                    return null;
                }
                console.log(`Loaded ${descriptions.length} descriptors for label: ${label}`);
                return new faceapi.LabeledFaceDescriptors(label, descriptions);
            })
        );

        console.log('Labeled face descriptors loaded:', labeledDescriptors);
        return labeledDescriptors.filter(ld => ld !== null);
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
            errorMessage.textContent = 'Error accessing the camera. Please allow camera access and try again.';
        }
    };

    // Function to detect emotions and recognize faces
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
                const maxEmotion = Object.keys(expressions).reduce((a, b) =>
                    expressions[a] > expressions[b] ? a : b
                );
                emotionDisplay.textContent = `Detected Emotion: ${maxEmotion}`;
                console.log(`Detected Emotion: ${maxEmotion}`);
                if (faceMatcher) {
                    const bestMatch = faceMatcher.findBestMatch(descriptor);
                    console.log(`Best match: ${bestMatch.toString()}`);
                    if (bestMatch.label !== 'unknown') {
                        userDisplay.textContent = `User: ${bestMatch.label}`;
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

    // Start detection at regular intervals
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

    // Initialize everything
    document.addEventListener('DOMContentLoaded', async () => {
        await loadModels();
        labeledFaceDescriptors = await loadLabeledImages();
        if (labeledFaceDescriptors.length === 0) {
            console.warn('No labeled face descriptors available. Face recognition will not work.');
            userDisplay.textContent = `User: Recognition not available`;
        } else {
            faceMatcher = new faceapi.FaceMatcher(labeledFaceDescriptors, 0.6);
            console.log('FaceMatcher initialized.');
        }
        await startVideo();
    });

    // Start detection when the video starts playing
    video.addEventListener('play', () => {
        console.log('Video started playing. Starting emotion and face recognition...');
        startDetection();
    });
    */
    // -------------------------------
    // End of webcam/face detection code.
    // -------------------------------

    // -------------------------------
    // New: Polling functions for manual updates:
    // -------------------------------

    // Function to poll the backend for the current emotion
    const updateEmotion = async () => {
        try {
            const response = await fetch('http://localhost:5000/get_emotion');
            const data = await response.json();
            emotionDisplay.textContent = `Detected Emotion: ${data.emotion}`;
            console.log(`Updated emotion: ${data.emotion}`);
        } catch (error) {
            console.error('Error fetching emotion:', error);
            if (errorMessage) {
                errorMessage.textContent = 'Error fetching emotion from server.';
            }
        }
    };

    // Function to poll the backend for the current user
    const updateUser = async () => {
        try {
            const response = await fetch('http://localhost:5000/get_user');
            const data = await response.json();
            userDisplay.textContent = `User: ${data.user}`;
            console.log(`Updated user: ${data.user}`);
        } catch (error) {
            console.error('Error fetching user:', error);
            if (errorMessage) {
                errorMessage.textContent = 'Error fetching user from server.';
            }
        }
    };

    // Poll for emotion updates every second
    setInterval(updateEmotion, 1000);

    // Poll for user updates every second
    setInterval(updateUser, 1000);

})();
