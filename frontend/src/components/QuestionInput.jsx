import styles from './QuestionInput.module.css';

function QuestionInput({ question, setQuestion }) {
  return (
   <div className={styles.wrapper}>
    <label className={styles.label}>💬 질문을 입력하세요</label>
      <textarea
        className={styles.textarea}
        placeholder="예: 김치국물 묻은 플라스틱 용기 어떻게 버려요?"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />
    </div>
  );
}

export default QuestionInput;
