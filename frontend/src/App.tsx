import React, { useState } from 'react';
import TextPane from './components/TextPane';
import AnalysisPane from './components/AnalysisPane';
import NavigationBar from './components/NavigationBar';
import { TextData, AnalysisData } from './types';
import { analyzeText } from './services/api';

function App() {
  const [textData, setTextData] = useState<TextData | null>(null);
  const [selectedSentence, setSelectedSentence] = useState<string>('');
  const [analysisData, setAnalysisData] = useState<AnalysisData | null>(null);
  const [currentSentenceIndex, setCurrentSentenceIndex] = useState<number>(-1);
  const [loading, setLoading] = useState<boolean>(false);

  const processText = (rawText: string) => {
    // Simple text processing to split into sentences
    const sentences = rawText
      .split(/[。！？\n]+/)
      .map(s => s.trim())
      .filter(s => s.length > 0);

    const textData: TextData = {
      id: 'user_input',
      title: 'User Input Text',
      content: rawText,
      sentences: sentences
    };

    setTextData(textData);
    setSelectedSentence('');
    setCurrentSentenceIndex(-1);
    setAnalysisData(null);
  };

  const handleSentenceSelect = async (sentence: string, index: number) => {
    setSelectedSentence(sentence);
    setCurrentSentenceIndex(index);
    setLoading(true);

    try {
      const analysis = await analyzeText(sentence);
      setAnalysisData(analysis);
    } catch (error) {
      console.error('Failed to analyze text:', error);
      setAnalysisData(null);
    } finally {
      setLoading(false);
    }
  };

  const handleNextSentence = () => {
    if (textData && currentSentenceIndex < textData.sentences.length - 1) {
      const nextIndex = currentSentenceIndex + 1;
      const nextSentence = textData.sentences[nextIndex];
      handleSentenceSelect(nextSentence, nextIndex);
    }
  };

  const handlePreviousSentence = () => {
    if (textData && currentSentenceIndex > 0) {
      const prevIndex = currentSentenceIndex - 1;
      const prevSentence = textData.sentences[prevIndex];
      handleSentenceSelect(prevSentence, prevIndex);
    }
  };

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
