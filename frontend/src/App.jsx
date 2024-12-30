import React, { useState } from "react";
import "./App.css";

function App() {
  const [trendData, setTrendData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchTrends = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await fetch(
        "http://127.0.0.1:8000/api/get-trending-data/"
      );
      if (!response.ok) {
        throw new Error("Failed to fetch trends");
      }
      const data = await response.json();
      setTrendData(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString();
  };

  return (
    <div className="container">
      <button
        onClick={fetchTrends}
        disabled={isLoading}
        className="fetch-button"
      >
        {isLoading
          ? "Fetching trends..."
          : trendData
          ? "Click here to run the query again"
          : "Fetch Twitter Trends"}
      </button>

      {error && <div className="error">Error: {error}</div>}

      {trendData && (
        <div className="card">
          <p className="timestamp">
            These are the most happening topics as on{" "}
            {formatDate(trendData.timestamp)}
          </p>

          {trendData.topics.map((topic, index) => (
            <p key={index} className="topic">
              - {topic}
            </p>
          ))}

          <p className="ip-address">
            The IP address used for this query was {trendData.ip_address}.
          </p>

          <div className="json-container">
            <p className="json-title">
              Here's a JSON extract of this record from the MongoDB:
            </p>
            <pre className="json-pre">{JSON.stringify(trendData, null, 2)}</pre>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
