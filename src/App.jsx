import React, { useState } from 'react';
import FileUpload from './components/FileUpload';
import OcrResult from './components/OcrResult';

const App = () => {
  const [texts, setTexts] = useState([]);

  const handleFileUpload = async (file) => {
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:5000/upload', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      if (data.texts) {
        setTexts(data.texts);
      } else if (data.text) {
        setTexts([data.text]);
      }
    } catch (error) {
      console.error('Error uploading file:', error);
    }
  };

  return (
    <div>
      <h1>OCR Engine</h1>
      <FileUpload onFileUpload={handleFileUpload} />
      <OcrResult texts={texts} />
    </div>
  );
};

export default App;
