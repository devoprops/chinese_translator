import React, { useState } from 'react';
import { TextData, ScriptType } from '../types/index';
import { detectScriptType } from '../services/api';

interface TextPaneProps {
  textData: TextData | null;
  selectedSentence: string;
  selectedSentencePosition: number;
  currentIndex: number;
  onSentenceSelect: (sentence: string, index: number, position?: number) => void;
  onLoadText: (text: string) => void;
}

const TextPane: React.FC<TextPaneProps> = ({
  textData,
  selectedSentence,
  selectedSentencePosition,
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
    
    // Use the provided position if available, otherwise try to find it
    let sentenceIndex = selectedSentencePosition >= 0 ? selectedSentencePosition : content.indexOf(selectedSentence);
    
    // Validate the position matches the sentence
    if (sentenceIndex >= 0) {
      const sentenceAtPosition = content.substring(sentenceIndex, sentenceIndex + selectedSentence.length);
      if (sentenceAtPosition !== selectedSentence) {
        // Position doesn't match, fall back to indexOf
        sentenceIndex = content.indexOf(selectedSentence);
      }
    }
    
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
        // Try to find the index of this sentence in the sentences array
        // Normalize both strings by replacing all whitespace with single spaces
        const normalizedSelection = selectedText.trim().replace(/\s+/g, ' ');
        const index = textData?.sentences.findIndex(s => s.trim().replace(/\s+/g, ' ') === normalizedSelection) ?? -1;
        
        console.log('Mouse selection: Selected text:', selectedText);
        console.log('Mouse selection: Normalized:', normalizedSelection);
        console.log('Mouse selection: Found index:', index);
        
        onSentenceSelect(selectedText, index); // Use found index or -1 if not found
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
      
      // Find the sentence at this position and get its position in the content
      const result = findSentenceAtPosition(range);
      if (result) {
        const { sentence, position } = result;
        
        // Clear selection again before setting our custom selection
        const sel = window.getSelection();
        if (sel) {
          sel.removeAllRanges();
        }
        
        // Try to find the index of this sentence in the sentences array
        // Normalize both strings by replacing all whitespace with single spaces
        const normalizedSentence = sentence.trim().replace(/\s+/g, ' ');
        const index = textData.sentences.findIndex(s => s.trim().replace(/\s+/g, ' ') === normalizedSentence);
        
        console.log('Double-click: Found sentence:', sentence);
        console.log('Double-click: Position in content:', position);
        console.log('Double-click: Normalized:', normalizedSentence);
        console.log('Double-click: Found index:', index);
        
        // Manually select the sentence text using the position
        selectTextInDOM(sentence, position);
        onSentenceSelect(sentence, index, position); // Pass the position
      }
    }, 0); // Run on next tick
  };

  const findSentenceAtPosition = (range: Range): { sentence: string; position: number } | null => {
    if (!textData) return null;
    
    // Get the text container
    const textContainer = range.startContainer.parentElement?.closest('.chinese-text');
    if (!textContainer) return null;
    
    // Get the full raw text content (ignoring any HTML elements)
    const fullText = textData.content;
    
    // Get text content up to the click position, stripping all HTML
    const beforeRange = document.createRange();
    beforeRange.setStart(textContainer, 0);
    beforeRange.setEnd(range.startContainer, range.startOffset);
    const textBeforeClick = beforeRange.toString();
    
    // Find the position in the original content by searching for the surrounding context
    // This is more robust than character counting when there are nested elements
    let clickPosition = textBeforeClick.length;
    
    // Adjust position if we're clicking near the end to ensure we get a valid match
    clickPosition = Math.min(clickPosition, fullText.length - 1);
    
    // Find sentence boundaries around this position
    const sentenceStart = findSentenceStart(fullText, clickPosition);
    const sentenceEnd = findSentenceEnd(fullText, clickPosition);
    let foundSentence = fullText.substring(sentenceStart, sentenceEnd).trim();
    let actualStart = sentenceStart;
    
    // If the found sentence is very short or empty, try to match against pre-split sentences
    if (foundSentence.length < 3) {
      // Get a wider context around the click
      const contextStart = Math.max(0, sentenceStart - 10);
      const contextEnd = Math.min(fullText.length, sentenceEnd + 10);
      const context = fullText.substring(contextStart, contextEnd);
      
      // Find the best matching sentence from the pre-split sentences
      for (const sentence of textData.sentences) {
        if (sentence.trim().length > 0 && context.includes(sentence.trim())) {
          // Find the position of this sentence in the full text
          // Search around the click position to find the right occurrence
          const searchStart = Math.max(0, clickPosition - 200);
          const searchEnd = Math.min(fullText.length, clickPosition + 200);
          const searchArea = fullText.substring(searchStart, searchEnd);
          const localPos = searchArea.indexOf(sentence.trim());
          if (localPos !== -1) {
            actualStart = searchStart + localPos;
            return { sentence, position: actualStart };
          }
        }
      }
    }
    
    // Try to find exact match in pre-split sentences for better accuracy
    const normalizedFound = foundSentence.trim().replace(/\s+/g, ' ');
    for (const sentence of textData.sentences) {
      const normalizedSentence = sentence.trim().replace(/\s+/g, ' ');
      if (normalizedSentence === normalizedFound) {
        // Find the position of this sentence near the click position
        const searchStart = Math.max(0, clickPosition - 200);
        const searchEnd = Math.min(fullText.length, clickPosition + 200);
        const searchArea = fullText.substring(searchStart, searchEnd);
        const localPos = searchArea.indexOf(sentence.trim());
        if (localPos !== -1) {
          actualStart = searchStart + localPos;
          return { sentence, position: actualStart };
        }
        // Fallback: search in entire text
        const globalPos = fullText.indexOf(sentence);
        if (globalPos !== -1) {
          return { sentence, position: globalPos };
        }
      }
    }
    
    return { sentence: foundSentence, position: actualStart };
  };

  const findSentenceStart = (text: string, position: number): number => {
    // Look backward for sentence boundaries (punctuation OR newlines)
    for (let i = position; i >= 0; i--) {
      // Check for punctuation marks
      if (text[i] === '。' || text[i] === '！' || text[i] === '？') {
        return i + 1; // Start after the punctuation
      }
      // Check for newline (paragraph/heading boundary)
      if (text[i] === '\n') {
        return i + 1; // Start after the newline
      }
    }
    
    return 0; // Start of text
  };

  const findSentenceEnd = (text: string, position: number): number => {
    // Look forward for sentence boundaries (punctuation OR newlines)
    for (let i = position; i < text.length; i++) {
      // Check for punctuation marks
      if (text[i] === '。' || text[i] === '！' || text[i] === '？') {
        return i + 1; // Include the punctuation
      }
      // Check for newline (paragraph/heading boundary) - stop here for headings
      if (text[i] === '\n') {
        return i; // Don't include the newline in the sentence
      }
    }
    
    return text.length; // End of text
  };

  const selectTextInDOM = (text: string, targetPosition: number = -1) => {
    // Find and select the text in the DOM at the specific position
    const textContainer = document.querySelector('.chinese-text');
    if (!textContainer) return;
    
    if (targetPosition < 0) {
      // Fallback to old behavior if no position specified
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
      return;
    }
    
    // Use position-based selection
    const walker = document.createTreeWalker(
      textContainer,
      NodeFilter.SHOW_TEXT
    );
    
    let currentPosition = 0;
    let node;
    
    while ((node = walker.nextNode())) {
      const nodeText = node.textContent || '';
      const nodeLength = nodeText.length;
      
      // Check if target position falls within this text node
      if (currentPosition <= targetPosition && targetPosition < currentPosition + nodeLength) {
        // The target text starts in this node
        const offsetInNode = targetPosition - currentPosition;
        const endPosition = Math.min(offsetInNode + text.length, nodeLength);
        
        try {
          const range = document.createRange();
          range.setStart(node, offsetInNode);
          
          // Check if the entire text fits in this node
          if (offsetInNode + text.length <= nodeLength) {
            range.setEnd(node, offsetInNode + text.length);
          } else {
            // Text spans multiple nodes, just select what we can
            range.setEnd(node, nodeLength);
          }
          
          const selection = window.getSelection();
          if (selection) {
            selection.removeAllRanges();
            selection.addRange(range);
          }
        } catch (e) {
          console.error('Error selecting text:', e);
        }
        break;
      }
      
      currentPosition += nodeLength;
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
