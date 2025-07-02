import { useState } from 'react';
import styles from './ImageUpload.module.css';

function ImageUpload({ setImageName }) {
  const [preview, setPreview] = useState(null);

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setImageName(file.name);

    const previewURL = URL.createObjectURL(file);
    setPreview(previewURL);
  };

  return (
    <div className={styles.wrapper}>
      <label className={styles.label}>📷 이미지 업로드</label>
      <input type="file" onChange={handleImageChange} style={{ width: '100%' }} />
      {preview && <img src={preview} className={styles.previewImage} alt="preview" />}
    </div>
  );
}

export default ImageUpload;
