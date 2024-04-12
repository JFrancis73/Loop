import React, { useState } from 'react';
import axios from 'axios';

const HomePage = () => {
  const [reportData, setReportData] = useState(null);
  const [reportId, setReportId] = useState('');

  const triggerReport = async () => {
    try {
      const response = await axios.get('http://localhost:8000/trigger_report');
      console.log(response.data); // for debugging
      setReportData(response.data);
    } catch (error) {
      console.error('Error triggering report:', error);
    }
  };

  const handleViewReport = async () => {
    if (!reportId) {
      alert('Please enter a report ID');
      return;
    }

    try {
      const response = await axios.get(`http://localhost:8000/get_report/${reportId}`);
	const data = response.data;

    // Check if response contains file data (assuming presence of a 'data' property)
    if (response.headers['content-type']?.startsWith('text/csv')) {
      const blob = new Blob([response.data], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);

    const link = document.createElement('a');
    link.href = url;
    link.download = reportId+'.csv';
    link.click();

    // Revoke the temporary URL after download (optional)
    window.URL.revokeObjectURL(url);
	setReportData({"status":"complete"})
    } else {
      setReportData(data); // Update report data if not a file download
    }
    /*const blob = new Blob([response.data], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);

    const link = document.createElement('a');
    link.href = url;
    link.download = reportId+'.csv';
    link.click();

    // Revoke the temporary URL after download (optional)
    window.URL.revokeObjectURL(url);*/
    } catch (error) {
      console.error('Error fetching report:', error);
    }
  };

  const handleChange = (event) => {
    setReportId(event.target.value);
  };

  return (
    <div>
      <h1>Report Generator</h1>
      <button onClick={triggerReport}>Generate Report</button>
      <button onClick={handleViewReport}>View Report</button>
      <br />
      <input type="text" value={reportId} onChange={handleChange} placeholder="Enter Report ID" />
      <br />
      {reportData && <pre>{JSON.stringify(reportData, null, 2)}</pre>}
    </div>
  );
};

export default HomePage;