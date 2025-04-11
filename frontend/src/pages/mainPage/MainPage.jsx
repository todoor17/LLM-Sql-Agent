import styles from "./mainPage.module.css";
import Sidebar from "../../components/sidebar/Sidebar.jsx";
import Hello from "../../components/hello/Hello.jsx";
import MainInput from "../../components/mainInput/MainInput.jsx";
import TextToSpeech from "../../components/textToSpeech/TextToSpeech.jsx";

export default function MainPage() {
  return (
    <div className={styles.pageContainer}>
      <div className={styles.left}>
        <Sidebar />
      </div>
      <div className={styles.right}>
        <Hello name={"Todor"} />
        <MainInput />
      </div>
    </div>
  );
}
