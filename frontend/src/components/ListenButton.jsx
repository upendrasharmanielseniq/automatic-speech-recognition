// import React, { useState }  from 'react';
// import { triggerListening } from '../services/api';

// const ListenButton = ({ onTxtFileReceived }) => {
//   const [mp3File, setMp3File] = useState(null);
  
//   const handleAudioChange = (e) => {
//     if (e.target.files.length > 0) {
//       setMp3File(e.target.files[0]);
//     }
//   };
  
// const handleListen = async () => {
//     if (!mp3File) return;
//     try {
//       const txtFile = await triggerListening(mp3File);
//       onTxtFileReceived(txtFile);
//     } catch (err) {
//       console.error("Listening failed:", err);
//     }
//   };

//    return (
//     <div className="flex flex-col items-center mb-4">
//       <label className="cursor-pointer bg-gray-200 hover:bg-gray-300 text-gray-800 font-semibold py-2 px-4 rounded">
//         Upload Audio File
//         <input
//           type="file"
//           accept="audio/*"
//           onChange={handleAudioChange}
//           className="hidden"
//         />
//       </label>
//       <button
//         onClick={handleListen}
//         disabled={!mp3File}
//         className="mt-2 bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded disabled:opacity-50"
//       >
//         Listen
//       </button>
//     </div>
//   );
// };

// export default ListenButton;
// ListenButton.jsx
// import React, { useState } from 'react';

const ListenButton = ({ onTxtFileReceived }) => {

  const handleTxtChange = (e) => {
    if (e.target.files.length > 0) {
      const file = e.target.files[0];
      onTxtFileReceived(file); // Immediately pass it to parent
    }
  };

  return (
    <>
    <div className="flex flex-col items-center mb-4">
      <label>
        Upload Transcript (.txt)
      </label>
     
    </div>
    <div>
       <input
          type="file"
          accept=".txt"
          onChange={handleTxtChange}
          className="hidden"
        />
    </div>
    </>
  );
};

export default ListenButton;
