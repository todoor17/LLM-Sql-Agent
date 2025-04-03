import style from "./mediaRecorder.module.css";
import RoundButton from "../roundButton/RoundButton.jsx";
import { useReactMediaRecorder } from "react-media-recorder";
import micIcon from "../../assets/images/micIcon.png";
import stopIcon from "../../assets/images/stopIcon.png";
import { useEffect, useRef } from "react";

export default function MediaRecorder() {
  const { status, startRecording, stopRecording, mediaBlobUrl } =
    useReactMediaRecorder({ audio: true });

  const audioRef = useRef(null);

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

      // const uploadResponse = await fetch(
      //   "http://localhost:5000/get_audio?prompt=which%20is%20the%20most%20sold%20product"
      // );
      const data = await uploadResponse.json();
      console.log(data.path);

      setTimeout(() => {
        audioRef.current.src = "/public/audio/response.wav";
        audioRef.current.play();
      }, 1000);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div>
      <RoundButton
        src={status === "idle" || status === "stopped" ? micIcon : stopIcon}
        onClick={
          status === "idle" || status === "stopped"
            ? startRecording
            : stopRecording
        }
      />
      <audio ref={audioRef} hidden></audio>
    </div>
  );
}
