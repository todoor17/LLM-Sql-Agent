import style from "./mediaRecorder.module.css";
import RoundButton from "../roundButton/RoundButton.jsx";
import { useReactMediaRecorder } from "react-media-recorder";
import micIcon from "../../assets/images/micIcon.png";
import stopIcon from "../../assets/images/stopIcon.png";
import { useEffect } from "react";

export default function MediaRecorder() {
  const { status, startRecording, stopRecording, mediaBlobUrl } =
    useReactMediaRecorder({ audio: true });

  useEffect(() => {
    if (mediaBlobUrl) {
      sendAudioToBackend(mediaBlobUrl);
    }
  }, [mediaBlobUrl]);

  const sendAudioToBackend = async (blobUrl) => {
    if (!blobUrl) return;
    try {
      const response = await fetch(blobUrl);
      const blob = await response.blob();
      const formData = new FormData();
      formData.append("file", blob);

      const uploadReponse = await fetch("http://localhost:5000/get_audio", {
        method: "POST",
        body: formData,
      });
      const data = await uploadReponse.json();
      console.log(data.answer);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div>
      <p>{status}</p>
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
