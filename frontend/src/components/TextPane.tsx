import React, { useState } from 'react';
import { TextData } from '../types';

interface TextPaneProps {
  textData: TextData | null;
  selectedSentence: string;
  currentIndex: number;
  onSentenceSelect: (sentence: string, index: number) => void;
  onLoadText: (text: string) => void;
}

const TextPane: React.FC<TextPaneProps> = ({
  textData,
  selectedSentence,
  currentIndex,
  onSentenceSelect,
  onLoadText,
}) => {
  const [inputText, setInputText] = useState<string>('');
  const [showInput, setShowInput] = useState<boolean>(false);

  const handleLoadText = () => {
    if (inputText.trim()) {
      onLoadText(inputText.trim());
      setInputText('');
      setShowInput(false);
    }
  };

  const handleLoadSample = () => {
    const sampleText = `轉法輪
李洪志

目錄

論語

第一講
真正往高層次上帶人
不同層次有不同層次的法
真、善、忍是衡量好壞人的唯一標準
氣功是史前文化
氣功就是修煉
煉功為甚麼不長功
法輪大法的特點`;
    onLoadText(sampleText);
  };

  const handleTextSelection = () => {
    const selection = window.getSelection();
    if (selection && selection.toString().trim()) {
      const selectedText = selection.toString().trim();
      // Only process if it contains Chinese characters
      if (/[\u4e00-\u9fff]/.test(selectedText)) {
        onSentenceSelect(selectedText, -1); // Use -1 to indicate user selection
      }
    }
  };

  return (
    <div className="p-6">
      {/* Header with controls */}
      <div className="mb-6">
        <div className="flex items-center justify-between mb-4">
          <h1 className="text-2xl font-bold text-gray-800 chinese-text">
            {textData?.title || 'Chinese Learning App'}
          </h1>
          <div className="flex space-x-2">
            <button
              onClick={() => setShowInput(!showInput)}
              className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
            >
              {showInput ? 'Cancel' : 'Load Text'}
            </button>
            <button
              onClick={handleLoadSample}
              className="px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600 transition-colors"
            >
              Load Sample
            </button>
          </div>
        </div>

        {/* Text input area */}
        {showInput && (
          <div className="mb-6 p-4 bg-gray-50 rounded-lg border">
            <div className="mb-2">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Copy and paste Chinese text here:
              </label>
              <textarea
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                placeholder="Paste your Chinese text here..."
                className="w-full h-32 p-3 border border-gray-300 rounded-md resize-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <div className="flex justify-between items-center">
              <p className="text-sm text-gray-600">
                Copy text from any source and paste it here for analysis
              </p>
              <button
                onClick={handleLoadText}
                disabled={!inputText.trim()}
                className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
              >
                Load Text
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Text content */}
      {textData ? (
        <div className="mb-4 p-2 bg-gray-50 rounded text-sm text-gray-600">
          💡 <strong>Tip:</strong> Select any Chinese text with your mouse to analyze it
        </div>
        
        <div 
          className="chinese-text text-lg leading-relaxed whitespace-pre-wrap select-text cursor-text"
          onMouseUp={handleTextSelection}
        >
          {textData.content}
          
          {/* Show selected text for analysis */}
          {selectedSentence && (
            <div className="mt-6 p-3 bg-green-50 border-l-4 border-green-500 rounded-r">
              <div className="flex items-center justify-between mb-2">
                <span className="font-medium text-gray-700">Selected for analysis:</span>
                <span className="text-sm text-gray-500">
                  {selectedSentence.length} characters
                </span>
              </div>
              <div className="text-green-800 font-medium chinese-text text-lg">
                "{selectedSentence}"
              </div>
            </div>
          )}
        </div>
      ) : (
        <div className="text-center py-12 text-gray-500">
          <div className="mb-4">
            <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <h3 className="text-lg font-medium mb-2">No text loaded</h3>
          <p className="mb-4">Click "Load Text" to paste Chinese text for analysis</p>
          <button
            onClick={() => setShowInput(true)}
            className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
          >
            Load Text
          </button>
        </div>
      )}

      {/* Selected sentence display */}
      {selectedSentence && (
        <div className="mt-6 p-4 bg-blue-50 rounded-lg border-l-4 border-blue-500">
          <h3 className="font-semibold text-gray-700 mb-2">Selected:</h3>
          <p className="chinese-text text-lg">{selectedSentence}</p>
        </div>
      )}
    </div>
  );
};

export default TextPane;
