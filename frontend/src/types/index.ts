export interface TextData {
  id: string;
  title: string;
  content: string;
  sentences: string[];
}

export interface AnalysisData {
  original: string;
  pinyin: string;
  translation: string;
  character_analysis: CharacterAnalysis[];
}

export interface CharacterAnalysis {
  character: string;
  pinyin: string;
  meaning: string;
  word?: string;
  word_position?: number;
  word_length?: number;
  is_word_start?: boolean;
  is_word_end?: boolean;
}

export interface CharacterInfo {
  character: string;
  pinyin: string;
  meaning: string;
  stroke_count: number;
  common_phrases: string[];
}

export interface ApiResponse<T> {
  data: T;
  error?: string;
}

export type ScriptType = 'auto' | 'traditional' | 'simplified' | 'mixed';

export interface DictionaryStats {
  total_words: number;
  total_entries: number;
  words_with_multiple_pinyin: number;
  simplified_mappings: number;
  traditional_mappings: number;
}



