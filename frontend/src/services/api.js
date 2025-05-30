import axios from 'axios';

const API_BASE_GENAI = 'http://localhost:8000';
const API_BASE_CPP = 'http://localhost:5000';
// const TMDB_API_KEY = '452d96cf89416b99843ba59c48a6f076';

export const uploadTranscript = async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return axios.post(`${API_BASE_GENAI}/predictFromUpload`, formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        },
    });
};

export const triggerListening = async (audioFile) => {
    const formData = new FormData();
    formData.append('file', audioFile);
    const response = await axios.post(`${API_BASE_CPP}/transcribe`, formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        },
    });
     return response.data;
};

// export const fetchTmdbMetadata = async (title) => {
//   try {
//     const response = await axios.get(
//       `https://api.themoviedb.org/3/search/multi`,
//       {
//         params: {
//           api_key: TMDB_API_KEY,
//           query: title,
//         },
//       }
//     );

//     const results = response.data.results;
//     if (results && results.length > 0) {
//       const item = results[0];
//       return {
//         posterUrl: `https://image.tmdb.org/t/p/w500${item.poster_path}`,
//       };
//     } else {
//       return null;
//     }
//   } catch (error) {
//     console.error("Error fetching TMDB metadata:", error);
//     return null;
//   }
// };