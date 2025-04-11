import styles from "./mainInput.module.css";
import sendIcon from "../../assets/images/sendIcon.png";
import { useRef, useEffect, useState } from "react";
import RoundButton from "../roundButton/RoundButton.jsx";
import Microphone from "../microphone/Microphone.jsx";
import TextToSpeech from "../textToSpeech/TextToSpeech.jsx";

export default function MainInput(
  {
    //   setResponse,
    //   setPrompt,
    //   isLoading,
    //   setIsLoading,
    //   responses,
    //   setResponses,
    //   rightContainer,
  }
) {
  const [prompt, setPrompt] = useState("");

  const textAreaRef = useRef(null);
  const inputContainerRef = useRef(null);

  const handleHeight = () => {
    if (textAreaRef.current && inputContainerRef.current) {
      textAreaRef.current.style.height = "auto";
      inputContainerRef.current.style.height = "auto";

      textAreaRef.current.style.height = `${textAreaRef.current.scrollHeight}px`;
      inputContainerRef.current.style.height = `${textAreaRef.current.style.height}px`;
    }
  };

  useEffect(() => {
    handleHeight();
  }, [prompt]);

  const sendPromptToBackend = async (text) => {
    try {
      const response = await fetch(
        `http://localhost:5000/api/trigger_graph?text=${encodeURIComponent(
          text
        )}`
      );

      const data = await response.json();
      console.log(data);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div
      ref={inputContainerRef}
      className={styles.inputContainer}
      //   style={
      //     isLoading || responses.length
      //       ? { position: "absolute", bottom: "20px" }
      //       : {}
      //   }
    >
      <textarea
        ref={textAreaRef}
        className={
          prompt?.length < 56 || prompt?.length == 0
            ? `${styles.input}`
            : `${styles.input} ${styles.paddingBottom}`
        }
        placeholder="Ask me anything"
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
      ></textarea>
      <div className={styles.buttonsContainer}>
        <Microphone setPrompt={setPrompt} />
        <TextToSpeech text={prompt} />
        <RoundButton
          src={sendIcon}
          onClick={() => {
            sendPromptToBackend(prompt);
          }}
        />
      </div>
    </div>
  );
}
