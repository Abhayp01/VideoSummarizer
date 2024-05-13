import React, { useState } from 'react';
function App() {
  const [url, setUrl] = useState('');
  const [transcript, setTranscript] = useState('');
  const [summary, setSummary] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  


  const fetchTranscript = async () => {
    setIsLoading(true);
    setError('');

    try {
      const response = await fetch('http://localhost:5000/transcript', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url }),
      });

      if (response.ok) {
        const data = await response.json();
        setTranscript(data.transcript);
        setSummary(data.summary);
      } else {
        setTranscript('');
        setError('Failed to fetch transcript. Please enter a valid YouTube URL.');
      }
    } catch (error) {
      setTranscript('');
      setError('An error occurred while fetching the transcript.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="App max-w-xl mx-auto p-4">
      <div className='text-center'>
        <h1 className='text-2xl font-bold my-4'>YouTube Caption Viewer</h1>
      </div>
      <div className='flex flex-col sm:flex-row items-center gap-2'>
        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="Enter YouTube Video URL"
          className="flex-1 p-2 border rounded-full"
        />
        <button
          className={`btn ${isLoading ? 'bg-gray-500' : 'bg-blue-500 hover:bg-blue-700'} text-white font-bold py-2 px-4 rounded-full`}
          onClick={fetchTranscript}
          disabled={isLoading}
        >
          {isLoading ? 'Loading...' : 'Get Transcript'}
        </button>
      </div>
      {error && <div className="mt-4 p-2 bg-red-100 text-red-700 border border-red-400 rounded">{error}</div>}
      {summary && (
        <div className="mt-4 p-2 border rounded">
          <h2 className="font-bold">Transcript:</h2>
          <p>{summary}</p>
        </div>
      )}
    </div>
  );
}

export default App;
