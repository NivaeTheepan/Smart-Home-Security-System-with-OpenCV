import "./Main.css"; // Importing styles
import { useEffect, useState } from "react"; // React hooks for state and effects
import Log from "./Log"; // Component for displaying individual logs

const API_BASE = "http://127.0.0.1:5000"; // API base URL

function MainPage({ onLogClicked }) {
  const [armed, setArmed] = useState(false); // Security system status
  const [logs, setLogs] = useState([]); // Logs for video recordings
  const [daysOffset, setDaysOffset] = useState(0); // Day offset for log filtering

  // Fetch armed status on component load
  useEffect(() => {
    fetch(API_BASE + "/get-armed")
      .then((res) => res.json())
      .then((data) => setArmed(data["armed"]))
      .catch(() => alert("Error retrieving armed status from camera."));
  }, []);

  // Fetch logs when daysOffset changes
  useEffect(() => {
    const startDate = getDateXDaysAgo(daysOffset);
    const endDate = getDateXDaysAgo(daysOffset - 1);

    console.log(`Fetching logs from ${startDate} to ${endDate}`); // Debugging
    fetch(API_BASE + `/get-logs?startDate=${startDate}&endDate=${endDate}`)
      .then((res) => res.json())
      .then((data) => setLogs(data["logs"]))
      .catch((error) => console.error("Error fetching logs:", error));
  }, [daysOffset]);

  // Get date in 'yyyy-mm-dd' format for a given offset in days
  const getDateXDaysAgo = (x) => {
    const pastDate = new Date();
    pastDate.setUTCDate(pastDate.getUTCDate() - x); // Handles UTC date calculation
    const yyyy = pastDate.getUTCFullYear();
    const mm = String(pastDate.getUTCMonth() + 1).padStart(2, "0");
    const dd = String(pastDate.getUTCDate()).padStart(2, "0");
    return `${yyyy}-${mm}-${dd}`;
  };

  // Toggle the armed state of the system
  const toggleArmed = () => {
    const options = { method: "POST" };
    setArmed(!armed);

    if (armed) fetch(API_BASE + "/disarm", options);
    else fetch(API_BASE + "/arm", options);
  };

  return (
    <div className="main">
      {/* Header section */}
      <div className="header">
        <h1>Home Security Hub</h1>
        <div className="toggle-container">
          <h2>
            Security Camera:{" "}
            {armed ? (
              <span style={{ color: "green" }}>On</span>
            ) : (
              <span style={{ color: "red" }}>Off</span>
            )}
          </h2>
          <label className="switch">
            <input type="checkbox" id="togBtn" onClick={toggleArmed} />
            <div className="slider round"></div>
          </label>
        </div>
      </div>

      {/* Logs section */}
      <div className="logs-container">
        <div className="logs-header">
          <h3>All Recordings:</h3>
          <div className="pages">
            {/* Navigate through log days */}
            <button
              className="prev"
              onClick={() => setDaysOffset(daysOffset + 1)}
            >
              ← Yesterday
            </button>
            <p>{getDateXDaysAgo(daysOffset)}</p>
            <button
              className="next"
              onClick={() => {
                if (daysOffset > 0) setDaysOffset(daysOffset - 1);
              }}
            >
              Tomorrow →
            </button>
          </div>
        </div>

        {/* Display logs */}
        <div className="logs">
          {logs.map((log, i) => (
            <Log
              key={i}
              url={log.url}
              date={log.date}
              onClick={() => onLogClicked(log.url, log.date)}
            />
          ))}
          {logs.length === 0 && <p>Number of Events: 0</p>}
        </div>
      </div>
    </div>
  );
}

export default MainPage;
