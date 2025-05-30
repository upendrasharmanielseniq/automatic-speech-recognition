import axios from 'axios';

const API_BASE = 'http://localhost:8000';

export const uploadTranscript = async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return axios.post(`${API_BASE}/predictFromUpload`, formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        },
    });
};