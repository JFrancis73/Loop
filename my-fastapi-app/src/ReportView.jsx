import React from 'react';

const ReportView = ({ reportId, onSubmit, onInputChange }) => {
  return (
    <div>
      <h2>Report ID:</h2>
      <input type="text" value={reportId} onChange={onInputChange} />
      <button onClick={onSubmit}>Submit</button>
    </div>
  );
};

export default ReportView;
