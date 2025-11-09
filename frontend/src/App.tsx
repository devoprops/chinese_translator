import React, { useState, useEffect } from 'react';
import TextPane from './components/TextPane';
import AnalysisPane from './components/AnalysisPane';
import NavigationBar from './components/NavigationBar';
import { TextData, AnalysisData } from './types';
import { analyzeText } from './services/api';

function App() {
  const [textData, setTextData] = useState<TextData | null>(null);
  const [selectedSentence, setSelectedSentence] = useState<string>('');
  const [selectedSentencePosition, setSelectedSentencePosition] = useState<number>(-1);
  const [analysisData, setAnalysisData] = useState<AnalysisData | null>(null);
  const [currentSentenceIndex, setCurrentSentenceIndex] = useState<number>(-1);
  const [loading, setLoading] = useState<boolean>(false);

  const processText = async (rawText: string) => {
    // Split into sentences by:
    // 1. Punctuation marks (。！？)
    // 2. Line breaks (for headings and paragraphs)
    const sentences = rawText
      .split(/(?<=[。！？])|(?:\n\s*\n)/)  // Split on punctuation OR double line breaks
      .flatMap(segment => {
        // Further split segments by single line breaks if they don't end with punctuation
        return segment.split(/\n+/)
          .map(s => s.trim())
          .filter(s => s.length > 0);
      });

    const textData: TextData = {
      id: 'user_input',
      title: 'User Input Text',
      content: rawText,
      sentences: sentences
    };

    setTextData(textData);
    
    // Auto-start with the first sentence if available
    if (sentences.length > 0) {
      const firstSentence = sentences[0];
      // Clean the sentence: remove extra whitespace and newlines
      const cleanSentence = firstSentence.trim().replace(/\s+/g, ' ');
      
      // Find position of first sentence in the content
      const position = rawText.indexOf(firstSentence);
      
      setSelectedSentence(firstSentence);
      setSelectedSentencePosition(position);
      setCurrentSentenceIndex(0);
      setLoading(true);
      
      try {
        // Send cleaned sentence to backend
        const analysis = await analyzeText(cleanSentence);
        setAnalysisData(analysis);
      } catch (error) {
        console.error('Failed to analyze first sentence:', error);
        setAnalysisData(null);
      } finally {
        setLoading(false);
      }
    } else {
      setSelectedSentence('');
      setSelectedSentencePosition(-1);
      setCurrentSentenceIndex(-1);
      setAnalysisData(null);
    }
  };

  const handleSentenceSelect = async (sentence: string, index: number, position: number = -1) => {
    // Clean the sentence: remove extra whitespace and newlines
    const cleanSentence = sentence.trim().replace(/\s+/g, ' ');
    
    setSelectedSentence(sentence); // Keep original for display
    setSelectedSentencePosition(position);
    setCurrentSentenceIndex(index);
    setLoading(true);

    try {
      // Send cleaned sentence to backend
      const analysis = await analyzeText(cleanSentence);
      setAnalysisData(analysis);
    } catch (error) {
      console.error('Failed to analyze text:', error);
      setAnalysisData(null);
    } finally {
      setLoading(false);
    }
  };

  const handleNextSentence = () => {
    if (textData && currentSentenceIndex >= 0 && currentSentenceIndex < textData.sentences.length - 1) {
      const nextIndex = currentSentenceIndex + 1;
      const nextSentence = textData.sentences[nextIndex];
      const position = textData.content.indexOf(nextSentence, selectedSentencePosition + 1);
      handleSentenceSelect(nextSentence, nextIndex, position);
    }
  };

  const handlePreviousSentence = () => {
    if (textData && currentSentenceIndex > 0) {
      const prevIndex = currentSentenceIndex - 1;
      const prevSentence = textData.sentences[prevIndex];
      // Find from beginning since we're going backwards
      let position = 0;
      for (let i = 0; i < prevIndex; i++) {
        const pos = textData.content.indexOf(textData.sentences[i], position);
        if (pos !== -1) {
          position = pos + textData.sentences[i].length;
        }
      }
      position = textData.content.indexOf(prevSentence, position);
      handleSentenceSelect(prevSentence, prevIndex, position);
    }
  };

  // Keyboard navigation: Left/Right arrow keys
  // Uses the same handleNextSentence/handlePreviousSentence functions as the buttons
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      // Only handle arrow keys if not typing in an input/textarea
      if (event.target instanceof HTMLInputElement || event.target instanceof HTMLTextAreaElement) {
        return;
      }
      
      if (event.key === 'ArrowLeft') {
        event.preventDefault();
        handlePreviousSentence(); // Same function as Previous button
      } else if (event.key === 'ArrowRight') {
        event.preventDefault();
        handleNextSentence(); // Same function as Next button
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [handlePreviousSentence, handleNextSentence]); // Re-bind when handler functions change

  return (
    <div className="h-screen flex flex-col">
      <NavigationBar 
        title={textData?.title || 'Chinese Learning App'}
        currentIndex={currentSentenceIndex}
        totalSentences={textData?.sentences.length || 0}
        onNext={handleNextSentence}
        onPrevious={handlePreviousSentence}
      />
      
      <div className="split-pane">
        <div className="left-pane">
          <TextPane
            textData={textData}
            selectedSentence={selectedSentence}
            selectedSentencePosition={selectedSentencePosition}
            currentIndex={currentSentenceIndex}
            onSentenceSelect={handleSentenceSelect}
            onLoadText={processText}
          />
        </div>
        
        <div className="right-pane">
          <AnalysisPane
            selectedSentence={selectedSentence}
            analysisData={analysisData}
            loading={loading}
          />
        </div>
      </div>
    </div>
  );
}

export default App;
