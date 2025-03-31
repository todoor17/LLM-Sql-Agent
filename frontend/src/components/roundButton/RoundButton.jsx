import styles from "./roundButton.module.css";

export default function RoundButton({ src, onClick }) {
  return (
    <button className={styles.button} onClick={onClick}>
      <img src={src} className={styles.buttonIcon}></img>
    </button>
  );
}
