import "./Details.css";
import ReactPlayer from "react-player";

function DetailsPage({ onBackClicked, url, date }) {
  return (
    <div className="details-page">
      <button onClick={onBackClicked} className="back-btn">
        Back
      </button>
      <h1>Person Motion Detected</h1>
      <div className="player">
        <ReactPlayer url={url} controls={true} />
      </div>
      <h3>{date}</h3>
    </div>
  );
}

export default DetailsPage;
