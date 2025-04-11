import { useReactMediaRecorder } from "react-media-recorder";
import { useEffect, useRef } from "react";
import micIcon from "../../assets/images/micIcon.png";
import stopIcon from "../../assets/images/pauseIcon.png";
import RoundButton from "../roundButton/RoundButton.jsx";

export default function Microphone({ setPrompt }) {
  const { status, startRecording, stopRecording, mediaBlobUrl } =
    useReactMediaRecorder({ audio: true });

  useEffect(() => {
    if (mediaBlobUrl) {
      sendAudioToBackend(mediaBlobUrl);
    }
  }, [mediaBlobUrl]);

  const sendAudioToBackend = async (mediaBlobUrl) => {
    const audioResponse = await fetch(mediaBlobUrl);
    const blob = await audioResponse.blob();

    const formData = new FormData();
    formData.append("file", blob);

    console.log("here1");
    const uploadResponse = await fetch(
      "http://localhost:5000/api/speech_to_text",
      {
        method: "POST",
        body: formData,
      }
    );

    console.log("here");
    const data = await uploadResponse.json();
    console.log(data.text);
    setPrompt(data.text);
  };

  return (
    <div>
      {/* <p>{status}</p> */}
      <RoundButton
        src={status === "idle" || status === "stopped" ? micIcon : stopIcon}
        onClick={
          status === "idle" || status === "stopped"
            ? startRecording
            : stopRecording
        }
      />
    </div>
  );
}
