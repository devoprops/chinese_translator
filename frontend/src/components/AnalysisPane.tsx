import React from 'react';
import { AnalysisData } from '../types';

interface AnalysisPaneProps {
  selectedSentence: string;
  analysisData: AnalysisData | null;
  loading: boolean;
}

const AnalysisPane: React.FC<AnalysisPaneProps> = ({
  selectedSentence,
  analysisData,
  loading,
}) => {
  if (!selectedSentence) {
    return (
      <div className="flex items-center justify-center h-full text-gray-500">
        <div className="text-center">
          <h2 className="text-xl font-semibold mb-2">Text Analysis</h2>
          <p>Select a sentence from the left panel to see its analysis</p>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-gray-600">Analyzing text...</p>
        </div>
      </div>
    );
  }

  if (!analysisData) {
    return (
      <div className="flex items-center justify-center h-full text-red-500">
        <div className="text-center">
          <h2 className="text-xl font-semibold mb-2">Analysis Error</h2>
          <p>Failed to analyze the selected text</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Chinese Text with Pinyin */}
      <div>
        <h2 className="text-xl font-semibold mb-3 text-gray-800">Chinese Text with Pinyin</h2>
        <div className="p-4 bg-gray-50 rounded-lg">
          <div className="flex flex-wrap gap-2">
            {analysisData.character_analysis.map((char, index) => (
              <div key={index} className="flex flex-col items-center">
                <div className="chinese-character text-3xl mb-1">{char.character}</div>
                <div className="pinyin-text text-sm text-gray-600">{char.pinyin}</div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Translation */}
      <div>
        <h2 className="text-xl font-semibold mb-3 text-gray-800">Translation</h2>
        <div className="p-4 bg-green-50 rounded-lg">
          <p className="text-lg">{analysisData.translation}</p>
        </div>
      </div>

      {/* Character Analysis */}
      <div>
        <h2 className="text-xl font-semibold mb-3 text-gray-800">Character Analysis</h2>
        <div className="character-analysis">
          {analysisData.character_analysis.map((char, index) => (
            <div key={index} className="character-item">
              <div className="character-char">{char.character}</div>
              <div className="character-info">
                <div className="character-pinyin">{char.pinyin}</div>
                <div className="character-meaning">{char.meaning}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default AnalysisPane;
