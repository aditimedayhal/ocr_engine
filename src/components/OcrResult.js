import React from 'react';

const OcrResult = ({ texts }) => {
  return (
    <div>
      <h2>Extracted Texts</h2>
      {texts.length > 0 ? (
        texts.map((text, index) => (
          <div key={index}>
            <h3>Page {index + 1}</h3>
            <p>{text}</p>
          </div>
        ))
      ) : (
        <p>No texts available</p>
      )}
    </div>
  );
};

export default OcrResult;
