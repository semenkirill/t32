import React from 'react';
import { useParams } from 'react-router-dom'
const VideoViewer = () => {
    const { uuid_file } = useParams()

    return (
        <div>
            <h2>Video Viewer</h2>
            <p>UUID: {uuid_file}</p>
            <video width="640" height="360" controls>
                <source src={`http://localhost:8000/t32_disk/video/${uuid_file}`} type="video/mp4" />
                Your browser does not support the video tag.
            </video>
        </div>
    );
};

export default VideoViewer;
