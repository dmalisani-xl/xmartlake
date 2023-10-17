import styles from './file-input.module.scss'

type FileInputProps = {
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  file: File | null;
  text: string;
  accept: string;
}

export const FileInput : React.FC<FileInputProps> = ({onChange, text, accept}) => {
  return (
    <div className={styles.fileUpload}>
      <p>{text}</p>
      <span className="material-symbols-outlined">upload</span>
      <input type="file" onChange={onChange} accept={accept}/>
    </div>
  )
}