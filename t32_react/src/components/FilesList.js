import React, { useState, useEffect, useContext } from 'react';
import axios from '../api/axios';
import AuthContext from '../context/AuthProvider';
import {Link} from "react-router-dom";

const FileList = () => {
    const { auth } = useContext(AuthContext);
    const [files, setFiles] = useState([]);
    const [selectedFiles, setSelectedFiles] = useState([]);

    useEffect(() => {
        fetchFileList();
    }, [auth]);

    const fetchFileList = async () => {
        try {
            const response = await axios.get('t32_disk/user_files', {
                headers: {
                    Authorization: `Bearer ${auth.accessToken}`,
                },
            });

            // Используем Set для уникальных идентификаторов файлов
            const uniqueFiles = Array.from(new Set(response.data.map(file => file.uuid)));

            // Обновляем состояние files
            setFiles(uniqueFiles.map(uuid => response.data.find(file => file.uuid === uuid)));
            // Очищаем выбранные файлы после успешной загрузки
            setSelectedFiles([]);
        } catch (error) {
            console.error('Error fetching file list:', error);
        }
    };

    const handleUpload = async () => {
        const formData = new FormData();

        for (let i = 0; i < selectedFiles.length; i++) {
            formData.append('files', selectedFiles[i]);
        }

        try {
            await axios.post('t32_disk/upload_files', formData, {
                headers: {
                    Authorization: `Bearer ${auth.accessToken}`,
                    'Content-Type': 'multipart/form-data',
                },
            });
            fetchFileList();
        } catch (error) {
            console.error('Error uploading files:', error);
        }
    };

    const handleFileChange = (event) => {
        setSelectedFiles(event.target.files);
    };

    const handleDelete = async (uuid) => {
        try {
            await axios.delete(`t32_disk/delete_files/${uuid}`, {
                headers: {
                    Authorization: `Bearer ${auth.accessToken}`,
                },
            });
            fetchFileList();
        } catch (error) {
            console.error('Error deleting file:', error);
        }
    };

    const handleShow = (filename) => {
        console.log(`Playing file: ${filename}`);
    };

    const handleDownload = async (uuid) => {
        try {
            const response = await axios.get(`t32_disk/download_file/${uuid}`, {
                headers: {
                    Authorization: `Bearer ${auth.accessToken}`,
                },
                responseType: 'blob',  // Указываем тип ответа как blob
            });

            // Создаем ссылку для скачивания и эмулируем клик для запуска скачивания
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', 'file.txt');  // Укажите имя файла для скачивания
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        } catch (error) {
            console.error('Error downloading file:', error);
        }
    };

    return (
        <section>
            <h1>File List</h1>
            <br />
            <input type="file" onChange={handleFileChange} multiple />
            <button onClick={handleUpload}>Upload</button>
            <br />
            <table>
                <thead>
                <tr>
                    <th>Filename</th>
                    <th>Action</th>
                </tr>
                </thead>
                <tbody>
                {files.map((file) => (
                    <tr key={file.filename}>
                        <td>{file.filename}</td>
                        <td>
                            <button onClick={() => handleDelete(file.uuid)}>Delete</button>
                            <Link to={`/video/${file.uuid}`}>
                                <button>Show Video</button>
                            </Link>
                            <Link to={`/image/${file.uuid}`}>
                                <button>Show Image</button>
                            </Link>

                            <button onClick={() => handleDownload(file.uuid)}>Download</button>
                        </td>
                    </tr>
                ))}
                </tbody>
            </table>
        </section>
    );
};

export default FileList;
