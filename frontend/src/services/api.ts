import axios from 'axios';
import { AnalysisData, TextData, CharacterInfo, ScriptType, DictionaryStats } from '../types';
import config from '../config';

// Backend expects /api prefix for all API routes
const API_BASE_URL = `${config.apiUrl}/api`;

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getTextById = async (textId: string): Promise<TextData> => {
  try {
    const response = await api.get(`/text/${textId}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching text:', error);
    throw error;
  }
};

export const analyzeText = async (text: string): Promise<AnalysisData> => {
  try {
    const response = await api.post('/analyze', { text });
    return response.data;
  } catch (error) {
    console.error('Error analyzing text:', error);
    throw error;
  }
};

export const translateText = async (text: string): Promise<string> => {
  try {
    const response = await api.post('/translate', { text });
    return response.data.translation;
  } catch (error) {
    console.error('Error translating text:', error);
    throw error;
  }
};

export const generatePinyin = async (text: string): Promise<string> => {
  try {
    const response = await api.post('/pinyin', { text });
    return response.data.pinyin;
  } catch (error) {
    console.error('Error generating pinyin:', error);
    throw error;
  }
};

export const getCharacterInfo = async (char: string): Promise<CharacterInfo> => {
  try {
    const response = await api.get(`/characters/${encodeURIComponent(char)}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching character info:', error);
    throw error;
  }
};

export const detectScriptType = async (text: string): Promise<ScriptType> => {
  try {
    const response = await api.post('/detect-script', { text });
    return response.data.scriptType;
  } catch (error) {
    console.error('Error detecting script type:', error);
    throw error;
  }
};

export const convertScript = async (text: string, toType: 'simplified' | 'traditional'): Promise<string> => {
  try {
    const response = await api.post('/convert-script', { text, toType });
    return response.data.convertedText;
  } catch (error) {
    console.error('Error converting script:', error);
    throw error;
  }
};

export const getDictionaryStats = async (): Promise<DictionaryStats> => {
  try {
    const response = await api.get('/dictionary/stats');
    return response.data;
  } catch (error) {
    console.error('Error fetching dictionary stats:', error);
    throw error;
  }
};

export default api;



