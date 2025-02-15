import { useState, useEffect } from 'react';
import { LastStudySessionData, StudyProgressData, QuickStatsData } from '../types/dashboard';

export const useDashboard = () => {
  const [lastSession, setLastSession] = useState<LastStudySessionData | null>(null);
  const [progress, setProgress] = useState<StudyProgressData | null>(null);
  const [stats, setStats] = useState<QuickStatsData | null>(null);

  useEffect(() => {
    const BASE_URL = 'http://localhost:8000/api/dashboard';

    fetch(`${BASE_URL}/last_study_session`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    })
      .then(res => {
        if (!res.ok) {
          throw new Error(`HTTP error! status: ${res.status}`);
        }
        return res.json();
      })
      .then(setLastSession)
      .catch(error => console.error('Error fetching last study session:', error));
    
    fetch(`${BASE_URL}/study_progress`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    })
      .then(res => {
        if (!res.ok) {
          throw new Error(`HTTP error! status: ${res.status}`);
        }
        return res.json();
      })
      .then(setProgress)
      .catch(error => console.error('Error fetching study progress:', error));
    
    fetch(`${BASE_URL}/quick_stats`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    })
      .then(res => {
        if (!res.ok) {
          throw new Error(`HTTP error! status: ${res.status}`);
        }
        return res.json();
      })
      .then(setStats)
      .catch(error => console.error('Error fetching quick stats:', error));
  }, []);

  return { lastSession, progress, stats };
};
