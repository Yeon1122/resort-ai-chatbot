import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

function MainPage() {
  const navigate = useNavigate();

  useEffect(() => {
    const timer = setTimeout(() => {
      navigate('/chat');
    }, 3000);

    return () => clearTimeout(timer);
  }, [navigate]);

  return (
    <div className="w-screen h-screen flex items-center justify-center bg-gray-100">
      <div className="animate-fade-in p-10 bg-white rounded-xl shadow-xl text-center max-w-md w-full">
        <h1 className="text-3xl font-bold mb-4">♻️ Re:sort</h1>
        <p className="text-gray-600">
          사진과 질문으로 정확한 분리배출 방법을 안내받아보세요.
        </p>
      </div>
    </div>
  );
}

export default MainPage;
