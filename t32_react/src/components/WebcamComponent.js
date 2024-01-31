import React, { useRef } from 'react';
import Webcam from 'react-webcam';

const WebcamVideo = () => {
    const webcamRef = useRef(null);

    return (
        <div>
            <Webcam
                audio={false}
                height={480}
                ref={webcamRef}
                screenshotFormat="image/jpeg"
                width={640}
            />
        </div>
    );
};

export default WebcamVideo;
