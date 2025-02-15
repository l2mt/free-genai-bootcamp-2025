export interface LastStudySessionData {
  id: number;
  activity_name: string;
  group_name: string;
  created_at: string;
  study_activity_id: number;
  group_id: number;
  correct_count: number;
  incorrect_count: number;
  total_items: number;
}

export interface StudyProgressData {
  total_words_studied: number;
  total_available_words: number;
  mastery_percentage: number;
}

export interface QuickStatsData {
  success_rate: number;
  total_study_sessions: number;
  total_active_groups: number;
  study_streak_days: number;
}