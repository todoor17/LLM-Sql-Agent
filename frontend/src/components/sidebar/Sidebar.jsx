import qm from "../../assets/images/QM.png";
import styles from "./sidebar.module.css";

export default function Sidebar({}) {
  return (
    <div className={styles.sidebarContainer}>
      <img className={styles.image} src={qm}></img>
    </div>
  );
}
