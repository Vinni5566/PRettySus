import { PRRequest, PRResponse } from '../types';

const API_BASE_URL = 'http://localhost:8000/api';

export const analyzePR = async (data: PRRequest): Promise<PRResponse> => {
  const response = await fetch(`${API_BASE_URL}/analyze`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    throw new Error('Failed to analyze PR');
  }

  return response.json();
};

export const getMarkdownReport = async (data: PRRequest): Promise<{ markdown: string }> => {
  const response = await fetch(`${API_BASE_URL}/analyze/report`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    throw new Error('Failed to generate markdown report');
  }

  return response.json();
};
