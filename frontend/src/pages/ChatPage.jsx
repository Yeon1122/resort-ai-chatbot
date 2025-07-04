import { useState, useRef, useEffect } from 'react';
import { FaPaperPlane, FaImage } from 'react-icons/fa';
import ReactMarkdown from 'react-markdown';

function ChatPage() {
  const [imageName, setImageName] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);
  const [question, setQuestion] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const chatEndRef = useRef(null);
  const fileInputRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatHistory]);

  const handleSend = async () => {
    if (!question.trim() && !selectedFile) return;

    const formData = new FormData();
    if (selectedFile) formData.append('file', selectedFile);
    if (question.trim()) formData.append('question', question.trim());

    setIsLoading(true);

    try {
    const res = await fetch(`${import.meta.env.VITE_API_URL}/analyze`, {
      method: 'POST',
      body: formData,
    });

      if (!res.ok) throw new Error('서버 응답 오류');

      const data = await res.json();

      setChatHistory((prev) => [
        ...prev,
        {
          userQuestion: question,
          userImage: selectedFile ? URL.createObjectURL(selectedFile) : null,
          botAnswer: data.answer || '응답이 없습니다.',
          botImage: data.image_url || null,
        },
      ]);
    } catch (err) {
      console.error(err);
      alert('서버에서 응답을 받지 못했습니다.');
    }

    setQuestion('');
    setSelectedFile(null);
    fileInputRef.current.value = null;
    setImageName('');
    setIsLoading(false);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

return (
  <div className="w-full h-screen bg-[#f7f7f8] flex items-center justify-center">
    <div className="w-full max-w-3xl h-full flex flex-col border-x bg-white relative">

      {/* 로딩 모달 */}
      {isLoading && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-30 backdrop-blur-sm">
          <div className="bg-white rounded-2xl p-6 shadow-2xl flex flex-col items-center">
            <img
              src="/RESORT_loading.gif"
              alt="로딩 중"
              className="w-32 h-32 object-contain mb-2"
            />
            <p className="text-gray-700 text-sm">잠시만 기다려주세요...</p>
          </div>
        </div>
      )}
      
      {/* 🔝 네비게이션 바 */}
      <div className="absolute top-0 left-0 right-0 h-14 px-4 flex items-center justify-between bg-white border-b z-10">
        {/* 왼쪽: RE:SORT 메인으로 */}
        <a href="/" className="block">
          <img src="/logo.png" alt="RE:SORT logo" className="w-[80px] h-[80px] object-contain" />
        </a>

        {/* 오른쪽: About 페이지 이동 */}
        <button
          onClick={() => setIsModalOpen(true)}
          className="text-gray-600 text-sm hover:underline"
        >
          RE:SORT란?
        </button>
      </div>

      {/* 채팅 영역 (네비게이션 높이 고려하여 패딩 추가) */}
      <div className="flex-1 overflow-y-auto px-6 py-20 space-y-6">
        {chatHistory.map((chat, idx) => (
          <div key={idx} className="space-y-2">
            {/* 사용자 메시지 */}
            <div className="flex justify-end gap-2">
              <div className="flex flex-col items-end max-w-[75%] gap-1">
                {chat.userImage && (
                  <img
                    src={chat.userImage}
                    alt="uploaded"
                    className="w-40 h-auto rounded-xl border"
                  />
                )}
                {chat.userQuestion && (
                  <div className="bg-green-500 text-white px-4 py-2 rounded-2xl rounded-br-sm text-sm shadow">
                    {chat.userQuestion}
                  </div>
                )}
              </div>
            </div>

            {/* 챗봇 메시지 */}
            <div className="flex items-start gap-3">
              <img
                src="/RESORT1.png"
                alt="bot"
                className="w-8 h-8 rounded-full object-cover border"
              />
            <div className="bg-gray-200 text-gray-800 px-4 py-2 rounded-2xl rounded-bl-sm text-sm shadow max-w-[75%]">
              <ReactMarkdown>{chat.botAnswer}</ReactMarkdown>
            </div>
            </div>
          </div>
        ))}
        <div ref={chatEndRef} />
      </div>

      {/* 선택 이미지 미리보기 */}
      {selectedFile && (
        <div className="px-6 pt-2 pb-0 bg-white border-t flex justify-start">
          <div className="relative w-32">
            <img
              src={URL.createObjectURL(selectedFile)}
              alt="preview"
              className="rounded-lg border w-full h-auto"
            />
            <button
              onClick={() => setSelectedFile(null)}
              className="absolute top-1 right-1 bg-red-500 text-white text-xs px-1 rounded-full hover:bg-red-600"
            >
              ✕
            </button>
          </div>
        </div>
      )}

      {/* 하단 입력창 */}
      <div className="p-4 border-t bg-white flex items-center gap-3">
        <label className="cursor-pointer text-gray-600 hover:text-green-500">
          <FaImage size={20} />
        <input
          ref={fileInputRef}
          type="file"
          className="hidden"
          accept="image/*"
          onChange={(e) => {
            const file = e.target.files[0];
            if (file) {
              setSelectedFile(file);
              setImageName(file.name);
            }
          }}
        />
        </label>

        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={handleKeyDown}
          rows={1}
          placeholder="메시지를 입력하세요"
          className="flex-1 resize-none border rounded-2xl px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-green-400"
        />

        <button
          onClick={handleSend}
          className="p-2 text-white bg-green-500 hover:bg-green-600 rounded-2xl"
        >
          <FaPaperPlane />
        </button>
      </div>
      {isModalOpen && (
      <div className="fixed inset-0 z-50 flex items-center justify-center backdrop-blur-sm bg-black/30">
        <div
          className="relative bg-white rounded-2xl shadow-2xl w-[90%] max-w-md px-6 py-8 animate-fadeIn"
          onClick={(e) => e.stopPropagation()}
        >
          {/* 닫기 버튼 */}
          <button
            onClick={() => setIsModalOpen(false)}
            className="absolute top-3 right-3 text-gray-400 hover:text-gray-700 transition"
            aria-label="Close"
          >
            ✕
          </button>

          {/* 헤더 */}
          <div className="flex items-center gap-2 mb-4">
            <span className="text-2xl">♻️</span>
            <h2 className="text-xl font-bold text-gray-800">RE:SORT란?</h2>
          </div>

          {/* 본문 */}
          <div className="text-sm text-gray-700 leading-relaxed space-y-2">
            <p>
              <strong className="text-green-600">RE:SORT</strong>는 질문과 이미지를 바탕으로
              분리수거 방법을 안내하는 친환경 챗봇입니다.
            </p>
            <p>
              AI 분석을 통해 이미지 속 품목을 인식하고, <br />
              적절한 <span className="font-medium">분리배출 방법</span>을 알려드려요.
            </p>
          </div>
        </div>
      </div>
    )}
    </div>
  </div>
);
}

export default ChatPage;
