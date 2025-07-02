import styles from './ChatResponse.module.css';

function ChatResponse({ response }) {
  if (!response) return null;

    return (
    <div className={styles.container}>
        <strong>📋 분리배출 안내</strong>
        <p style={{ marginTop: '8px' }}>{response}</p>
    </div>
    );
}

export default ChatResponse;
