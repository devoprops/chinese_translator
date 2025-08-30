import React, { useState } from 'react';
import { AnalysisData } from '../types';

interface AnalysisPaneProps {
  selectedSentence: string;
  analysisData: AnalysisData | null;
  loading: boolean;
}

interface CharacterAnalysisSectionProps {
  analysisData: AnalysisData;
}

const CharacterAnalysisSection: React.FC<CharacterAnalysisSectionProps> = ({ analysisData }) => {
  const [translations, setTranslations] = useState<{[key: string]: string}>({});
  const [loading, setLoading] = useState(true);
  const [isTranslating, setIsTranslating] = useState(false);

  // Group characters by words
  const wordGroups: Array<typeof analysisData.character_analysis> = [];
  let currentGroup: typeof analysisData.character_analysis = [];
  
  analysisData.character_analysis.forEach((char, index) => {
    // Skip punctuation characters
    const isPunctuation = /[、，。！？；：""''（）【】《》〈〉「」『』\s]/.test(char.character);
    
    if (!isPunctuation) {
      currentGroup.push(char);
    }
    
    if (char.is_word_end || index === analysisData.character_analysis.length - 1) {
      if (currentGroup.length > 0) {
        wordGroups.push([...currentGroup]);
        currentGroup = [];
      }
    }
  });

  // Fetch batch translations when component mounts
  React.useEffect(() => {
    // Prevent multiple simultaneous requests
    if (isTranslating) {
      console.log('Translation already in progress, skipping...');
      return;
    }

    console.log('CharacterAnalysisSection useEffect triggered');
    console.log('wordGroups.length:', wordGroups.length);
    
    const fetchBatchTranslations = async () => {
      setIsTranslating(true);
      setLoading(true);
      
      // Collect all unique words and characters to translate
      const itemsToTranslate = new Set<string>();
      
      // Add word groups
      wordGroups.forEach(wordGroup => {
        const word = wordGroup[0]?.word || wordGroup.map(c => c.character).join('');
        if (word && word.trim().length > 0) {
          itemsToTranslate.add(word.trim());
        }
      });
      
      // Add individual characters (excluding punctuation)
      analysisData.character_analysis.forEach(char => {
        const isPunctuation = /[、，。！？；：""''（）【】《》〈〉「」『』\s]/.test(char.character);
        if (char.character && char.character >= '\u4e00' && char.character <= '\u9fff' && !isPunctuation) {
          itemsToTranslate.add(char.character);
        }
      });
      
      // Remove any items we already have translations for
      const itemsArray = Array.from(itemsToTranslate).filter(item => !translations[item]);
      
      if (itemsArray.length === 0) {
        console.log('All items already translated, skipping API call');
        setLoading(false);
        setIsTranslating(false);
        return;
      }
      
      try {
        console.log('Sending batch translation request for', itemsArray.length, 'new items:', itemsArray);
        
        const response = await fetch('/api/translate-batch', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ items: itemsArray })
        });
        
        if (response.ok) {
          const data = await response.json();
          console.log('Batch translation response:', data);
          // Merge with existing translations
          setTranslations(prev => ({ ...prev, ...data.translations }));
        } else {
          console.error('Batch translation failed with status:', response.status);
          const errorText = await response.text();
          console.error('Error response:', errorText);
        }
      } catch (error) {
        console.error('Error fetching batch translations:', error);
      } finally {
        setLoading(false);
        setIsTranslating(false);
      }
    };

    if (wordGroups.length > 0) {
      console.log('Calling fetchBatchTranslations...');
      fetchBatchTranslations();
    } else {
      console.log('No word groups found, skipping batch translation');
      setLoading(false);
    }
  }, [analysisData, isTranslating, translations]);

  return (
    <div>
      <h2 className="text-xl font-semibold mb-3 text-gray-800">Character Analysis</h2>
      <div className="p-4 bg-gray-50 rounded-lg">
        <div className="space-y-4">
          {loading ? (
            <div className="flex items-center justify-center py-8">
              <div className="text-gray-500">Loading translations...</div>
            </div>
          ) : (
            wordGroups.map((wordGroup, groupIndex) => {
              const word = wordGroup[0]?.word || wordGroup.map(c => c.character).join('');
              const pinyin = wordGroup.map(c => c.pinyin).join(' ');
              // Use the batch translation, fallback to first character's meaning
              const translation = translations[word] || wordGroup[0]?.meaning || 'Unknown';
            
            return (
              <div key={groupIndex} className="flex gap-4 overflow-x-auto">
                {/* Word Group */}
                <div className="flex flex-col items-center p-3 bg-blue-50 border border-blue-200 rounded-lg min-w-[120px] flex-shrink-0">
                  {/* Row 1: Characters */}
                  <div className="chinese-character mb-1">
                    {word}
                  </div>
                  {/* Row 2: Pinyin */}
                  <div className="text-sm text-gray-600 mb-1 text-center">
                    {pinyin}
                  </div>
                  {/* Row 3: Translation */}
                  <div className="text-xs text-blue-600 text-center max-w-[120px] break-words">
                    {translation}
                  </div>
                </div>

                {/* Individual Characters for this group */}
                {wordGroup.map((char, charIndex) => (
                  <div key={`${groupIndex}-${charIndex}`} className="flex flex-col items-center p-3 bg-green-50 border border-green-200 rounded-lg min-w-[100px] flex-shrink-0">
                    {/* Row 1: Character */}
                    <div className="chinese-character mb-1">
                      {char.character}
                    </div>
                    {/* Row 2: Pinyin */}
                    <div className="text-sm text-gray-600 mb-1 text-center">
                      {char.pinyin}
                    </div>
                    {/* Row 3: Meaning */}
                    <div className="text-xs text-green-600 text-center max-w-[100px] break-words">
                      {translations[char.character] || char.meaning}
                    </div>
                  </div>
                ))}
              </div>
            );
          })
          )}
        </div>
      </div>
    </div>
  );
};

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
      {/* Original Sentence */}
      <div>
        <h2 className="text-xl font-semibold mb-3 text-gray-800">Original Sentence</h2>
        <div className="p-4 bg-gray-50 rounded-lg">
          <p className="chinese-text text-lg leading-relaxed">{analysisData.original}</p>
        </div>
      </div>

      {/* Translation */}
      <div>
        <h2 className="text-xl font-semibold mb-3 text-gray-800">Translation</h2>
        <div className="p-4 bg-blue-50 rounded-lg">
          <p className="text-gray-800 leading-relaxed">{analysisData.translation}</p>
        </div>
      </div>

      {/* Chinese Text with Pinyin */}
      <div>
        <h2 className="text-xl font-semibold mb-3 text-gray-800">Chinese Text with Pinyin</h2>
        <div className="p-4 bg-gray-50 rounded-lg">
          <div className="flex flex-wrap gap-6">
            {(() => {
              // Group characters by words
              const wordGroups: Array<typeof analysisData.character_analysis> = [];
              let currentGroup: typeof analysisData.character_analysis = [];
              
              analysisData.character_analysis.forEach((char, index) => {
                currentGroup.push(char);
                if (char.is_word_end || index === analysisData.character_analysis.length - 1) {
                  wordGroups.push([...currentGroup]);
                  currentGroup = [];
                }
              });
              
              return wordGroups.map((wordGroup, groupIndex) => (
                <div key={groupIndex} className="flex flex-col items-center">
                  {/* Row 1: Chinese characters in tight horizontal layout */}
                  <div className="flex gap-1 mb-1">
                    {wordGroup.map((char, charIndex) => (
                      <div key={charIndex} className="chinese-character text-3xl">
                        {char.character}
                      </div>
                    ))}
                  </div>
                  
                  {/* Row 2: Pinyin in tight horizontal layout */}
                  <div className="flex gap-1 mb-2">
                    {wordGroup.map((char, charIndex) => (
                      <div key={charIndex} className="pinyin-text text-sm text-gray-600 text-center min-w-[2rem]">
                        {char.pinyin}
                      </div>
                    ))}
                  </div>
                  
                  {/* Row 3: Complete word (grouped characters) */}
                  <div className="text-xs text-blue-500 opacity-70 text-center">
                    {wordGroup[0]?.word || wordGroup.map(c => c.character).join('')}
                  </div>
                </div>
              ));
            })()}
          </div>
        </div>
      </div>

      {/* Character Analysis - Two Pane Layout */}
      <CharacterAnalysisSection analysisData={analysisData} />
    </div>
  );
};

export default AnalysisPane;
