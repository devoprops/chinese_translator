import React from 'react';

interface NavigationBarProps {
  title: string;
  currentIndex: number;
  totalSentences: number;
  onNext: () => void;
  onPrevious: () => void;
}

const NavigationBar: React.FC<NavigationBarProps> = ({
  title,
  currentIndex,
  totalSentences,
  onNext,
  onPrevious,
}) => {
  return (
    <div className="bg-white border-b border-gray-200">
      {/* App Title Bar */}
      <div className="bg-gradient-to-r from-blue-600 to-blue-700 px-6 py-4 shadow-md">
        <h1 className="text-2xl font-bold text-white tracking-wide">
          Chinese: Translate and Study
        </h1>
      </div>
      
      {/* Navigation Bar */}
      <div className="px-6 py-3">
        <div className="flex items-center justify-center">
          <div className="flex items-center space-x-2">
            <button
              onClick={onPrevious}
              disabled={currentIndex <= 0}
              className="nav-button"
            >
              ← Previous Sentence
            </button>
            
            <button
              onClick={onNext}
              disabled={currentIndex < 0 || currentIndex >= totalSentences - 1}
              className="nav-button"
            >
              Next Sentence →
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default NavigationBar;



