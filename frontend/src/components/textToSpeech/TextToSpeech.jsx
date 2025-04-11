import RoundButton from "../roundButton/RoundButton.jsx";
import playIcon from "../../assets/images/playIcon.png";
import pauseIcon from "../../assets/images/pauseIcon.png";
import { useState, useRef, useEffect } from "react";

export default function TextToSpeech({ text }) {
  const [audioStatus, setAudioStatus] = useState("not-loaded");
  const playAudioRef = useRef(null);

  useEffect(() => {
    if (playAudioRef.current) {
      playAudioRef.current.pause();
      playAudioRef.current.currentTime = 0;
      setAudioStatus("not-loaded");
    }
  }, [text]);

  const getAudio = async (text) => {
    if (!text) return;

    try {
      const response = await fetch(
        `http://localhost:5000/api/text_to_speech?text=${encodeURIComponent(
          text
        )}`
      );

      const data = await response.json();

      playAudioRef.current.src = data.path;
      playAudioRef.current.onended = () => {
        setAudioStatus("not-loaded");
      };
      playAudioRef.current.onerror = () => {
        setAudioStatus("not-loaded");
      };

      playAudioRef.current.play();
      setAudioStatus("playing");
    } catch (error) {
      console.error("Error playing audio:", error);
      setAudioStatus("not-loaded");
    }
  };

  const handlePlayClick = () => {
    if (audioStatus === "not-loaded" && text) {
      getAudio(text);
    } else if (audioStatus === "playing") {
      playAudioRef.current.pause();
      setAudioStatus("paused");
    } else if (audioStatus === "paused") {
      playAudioRef.current.play();
      setAudioStatus("playing");
    }
  };

  return (
    <div>
      <RoundButton
        src={audioStatus === "playing" ? pauseIcon : playIcon}
        onClick={handlePlayClick}
        disabled={!text}
      />
      <audio ref={playAudioRef} hidden />
    </div>
  );
}
