import styles from "./hello.module.css";
import logo from "../../assets/images/queryMateLogo.png";

export default function Hello({ name }) {
  return (
    <div className={styles.componentContainer}>
      <img className={styles.image} src={logo}></img>
      <div className={styles.firstRowContainer}>
        <p className={styles.text1}>
          {name
            ? `Hello, ${name}! QueryMate here!`
            : `Hello, user! I am Lawgic!`}
        </p>
      </div>
      <p className={styles.text2}>What can I assist you with today?</p>
    </div>
  );
}
