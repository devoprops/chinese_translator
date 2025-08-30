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
    <div className="bg-white border-b border-gray-200 px-6 py-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <h1 className="text-xl font-semibold text-gray-800">{title}</h1>
          {currentIndex >= 0 && (
            <span className="text-sm text-gray-600">
              {currentIndex + 1} of {totalSentences}
            </span>
          )}
        </div>
        
        <div className="flex items-center space-x-2">
          <button
            onClick={onPrevious}
            disabled={currentIndex <= 0}
            className="nav-button"
          >
            ← Previous
          </button>
          
          <button
            onClick={onNext}
            disabled={currentIndex >= totalSentences - 1}
            className="nav-button"
          >
            Next →
          </button>
        </div>
      </div>
    </div>
  );
};

export default NavigationBar;



