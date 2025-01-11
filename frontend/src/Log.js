import "./Log.css"; // Import styles for the Log component
import { useRef, useEffect } from "react"; // React hooks for references and lifecycle effects

function Log({ onClick, url, date }) {
  const videoRef = useRef(null); // Reference to the hidden video element
  const canvasRef = useRef(null); // Reference to the canvas for displaying a frame

  useEffect(() => {
    const video = videoRef.current;

    // Event to set the video time to capture a frame
    video.addEventListener("loadeddata", () => {
      video.currentTime = 1; // Adjust if a different frame is needed
    });

    // Event to draw the selected frame on the canvas
    video.addEventListener("seeked", () => {
      const canvas = canvasRef.current;
      const ctx = canvas.getContext("2d");
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height); // Draw video frame on canvas
    });
  }, [url]); // Re-run effect when the video URL changes

  return (
    <div onClick={onClick} className="log">
      {/* Hidden video element used to load video frames */}
      <video ref={videoRef} src={url} style={{ display: "none" }}></video>

      {/* Canvas for displaying the thumbnail of the video */}
      <canvas ref={canvasRef} width="100" height="100"></canvas>

      {/* Log details */}
      <div className="details">
        <h3>Person Motion Detected</h3>
        <h4>{date}</h4>
      </div>
    </div>
  );
}

export default Log;
