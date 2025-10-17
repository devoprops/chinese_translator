import React, { useState } from 'react';
import { TextData, ScriptType } from '../types/index';
import { detectScriptType } from '../services/api';

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
  const [showInput, setShowInput] = useState<boolean>(true);
  const [scriptType, setScriptType] = useState<ScriptType>('auto');
  const [detectedType, setDetectedType] = useState<ScriptType | null>(null);

  const handleLoadText = async () => {
    if (inputText.trim()) {
      const text = inputText.trim();
      
      // Auto-detect script type if set to auto
      if (scriptType === 'auto') {
        try {
          const detected = await detectScriptType(text);
          setDetectedType(detected);
          console.log(`Auto-detected script type: ${detected}`);
        } catch (error) {
          console.error('Failed to detect script type:', error);
          setDetectedType('traditional'); // Default to traditional
        }
      } else {
        setDetectedType(scriptType);
      }
      
      onLoadText(text);
      setInputText('');
      setShowInput(false);
    }
  };

  const handlePasteNewText = () => {
    setInputText('');
    setShowInput(true);
    setScriptType('auto');
    setDetectedType(null);
  };

  const renderTextWithHighlight = () => {
    if (!textData || !selectedSentence) {
      return textData?.content;
    }

    const content = textData.content;
    const sentenceIndex = content.indexOf(selectedSentence);
    
    if (sentenceIndex === -1) {
      // Sentence not found in content, just return content as-is
      return content;
    }

    const beforeText = content.substring(0, sentenceIndex);
    const highlightedText = selectedSentence;
    const afterText = content.substring(sentenceIndex + selectedSentence.length);

    return (
      <>
        {beforeText}
        <span className="bg-yellow-200 border-b-2 border-yellow-500">{highlightedText}</span>
        {afterText}
      </>
    );
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

  const handleDoubleClick = (event: React.MouseEvent) => {
    event.preventDefault(); // Prevent default double-click selection
    event.stopPropagation(); // Stop event bubbling
    
    if (!textData) return;
    
    // Clear any existing selection immediately
    const selection = window.getSelection();
    if (selection) {
      selection.removeAllRanges();
    }
    
    // Use setTimeout to ensure our logic runs after any native selection
    setTimeout(() => {
      // Get the click position using cross-browser method
      let range: Range | null = null;
      
      if (document.caretRangeFromPoint) {
        // WebKit browsers
        range = document.caretRangeFromPoint(event.clientX, event.clientY);
      } else if ((document as any).caretPositionFromPoint) {
        // Firefox
        const caretPosition = (document as any).caretPositionFromPoint(event.clientX, event.clientY);
        if (caretPosition) {
          range = document.createRange();
          range.setStart(caretPosition.offsetNode, caretPosition.offset);
          range.collapse(true);
        }
      }
      
      if (!range) return;
      
      // Find the sentence at this position
      const sentence = findSentenceAtPosition(range);
      if (sentence) {
        // Clear selection again before setting our custom selection
        const sel = window.getSelection();
        if (sel) {
          sel.removeAllRanges();
        }
        
        // Manually select the sentence text
        selectTextInDOM(sentence);
        onSentenceSelect(sentence, -1);
      }
    }, 0); // Run on next tick
  };

  const findSentenceAtPosition = (range: Range): string | null => {
    if (!textData) return null;
    
    // Get the character position in the text
    const textContainer = range.startContainer.parentElement?.closest('.chinese-text');
    if (!textContainer) return null;
    
    // Get all text content and find position
    const fullText = textData.content;
    const beforeRange = document.createRange();
    beforeRange.setStart(textContainer, 0);
    beforeRange.setEnd(range.startContainer, range.startOffset);
    const position = beforeRange.toString().length;
    
    // Find sentence boundaries around this position
    const sentenceStart = findSentenceStart(fullText, position);
    const sentenceEnd = findSentenceEnd(fullText, position);
    const foundSentence = fullText.substring(sentenceStart, sentenceEnd).trim();
    
    // If the found sentence is very short (like just "氣功"), 
    // try to find a longer sentence from the pre-split sentences
    if (foundSentence.length < 6) {
      const textAtPosition = fullText.substring(Math.max(0, position - 2), position + 3);
      for (const sentence of textData.sentences) {
        if (sentence.includes(textAtPosition) && sentence.length > foundSentence.length) {
          return sentence;
        }
      }
    }
    
    return foundSentence;
  };

  const findSentenceStart = (text: string, position: number): number => {
    // Look backward for sentence endings first
    for (let i = position; i >= 0; i--) {
      if (text[i] === '。' || text[i] === '！' || text[i] === '？') {
        return i + 1; // Start after the period
      }
    }
    
    // If no period found, look for paragraph breaks (more generous)
    for (let i = position; i >= 0; i--) {
      if (text.substring(i, i + 2) === '\n\n') {
        return i + 2;
      }
    }
    
    // If no double newline, look for single newline
    for (let i = position; i >= 0; i--) {
      if (text[i] === '\n') {
        return i + 1;
      }
    }
    
    return 0; // Start of text
  };

  const findSentenceEnd = (text: string, position: number): number => {
    // Look forward for sentence endings first
    for (let i = position; i < text.length; i++) {
      if (text[i] === '。' || text[i] === '！' || text[i] === '？') {
        return i + 1; // Include the period
      }
    }
    
    // If no period found, look for paragraph breaks (more generous)
    for (let i = position; i < text.length; i++) {
      if (text.substring(i, i + 2) === '\n\n') {
        return i;
      }
    }
    
    // If no double newline, look for single newline
    for (let i = position; i < text.length; i++) {
      if (text[i] === '\n') {
        return i;
      }
    }
    
    return text.length; // End of text
  };

  const selectTextInDOM = (text: string) => {
    // Find and select the text in the DOM
    const textContainer = document.querySelector('.chinese-text');
    if (!textContainer) return;
    
    const walker = document.createTreeWalker(
      textContainer,
      NodeFilter.SHOW_TEXT
    );
    
    let node;
    while ((node = walker.nextNode())) {
      const nodeText = node.textContent || '';
      const index = nodeText.indexOf(text);
      if (index !== -1) {
        const range = document.createRange();
        range.setStart(node, index);
        range.setEnd(node, index + text.length);
        
        const selection = window.getSelection();
        if (selection) {
          selection.removeAllRanges();
          selection.addRange(range);
        }
        break;
      }
    }
  };



  return (
    <div className="p-6">
      {/* Header with controls */}
      <div className="mb-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-semibold text-gray-800">
            {textData?.title || 'Chinese Learning App'}
          </h2>
          <div className="flex items-center space-x-2">
            <button
              onClick={() => setShowInput(!showInput)}
              className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
            >
              {showInput ? 'Cancel' : 'Process Text'}
            </button>
            
            {/* Script type selector */}
            <div className="flex items-center space-x-2">
              <label className="text-sm text-gray-600">Script:</label>
              <select
                value={scriptType}
                onChange={(e) => setScriptType(e.target.value as ScriptType)}
                className="px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="auto">Auto-detect</option>
                <option value="traditional">Traditional</option>
                <option value="simplified">Simplified</option>
              </select>
              {detectedType && detectedType !== 'auto' && (
                <span className="text-xs text-gray-500">
                  (Detected: {detectedType})
                </span>
              )}
            </div>
            
            {/* Load Sample button - commented out but kept for testing */}
            {/* 
            <button
              onClick={handleLoadSample}
              className="px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600 transition-colors"
            >
              Load Sample
            </button>
            */}
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
                Process Text
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Text content */}
      {textData ? (
        <div>
          <div className="mb-4 flex items-center justify-between">
            <div className="p-2 bg-gray-50 rounded text-sm text-gray-600 flex-1">
              💡 <strong>Tip:</strong> Double-click any Chinese text to analyze the entire sentence
            </div>
            <button
              onClick={handlePasteNewText}
              className="ml-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors whitespace-nowrap"
            >
              Paste New Text
            </button>
          </div>
          
          <div 
            className="chinese-text text-lg leading-relaxed whitespace-pre-wrap select-text cursor-text"
            onMouseUp={handleTextSelection}
            onDoubleClick={handleDoubleClick}
          >
            {renderTextWithHighlight()}
          </div>
        </div>
      ) : (
        <div className="text-center py-12 text-gray-500">
          <div className="mb-4">
            <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <h3 className="text-lg font-medium mb-2">No text loaded</h3>
          <p className="mb-4">Click "Process Text" to paste Chinese text for analysis</p>
          <button
            onClick={() => setShowInput(true)}
            className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
          >
          Process Text
        </button>
      </div>
      )}
    </div>
  );
};

export default TextPane;
