import React from 'react';
import { useParams } from 'react-router-dom'
const ImageViewer = () => {
    const { uuid_file } = useParams()

    return (
        <div>
            <h2>Image Viewer</h2>
            <p>UUID: {uuid_file}</p>
            {/* Здесь вы можете встроить компонент отображения изображения */}
            <img src={`http://localhost:8000/t32_disk/image/${uuid_file}`} alt={uuid_file} />
        </div>
    );
};

export default ImageViewer;
