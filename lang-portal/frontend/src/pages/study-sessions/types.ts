export interface StudySession {
  id: string;
  activity_name: string;
  group_name: string;
  start_time: string;
  end_time: string | null;
  review_items_count: number;
}

export interface StudySessionDetail extends StudySession {
  words?: WordReview[];
}

export interface WordReview {
  id: string;
  spanish: string;
  english: string;
  correct: boolean;
  review_time: string;
}

export interface PaginationInfo {
  current_page: number;
  total_pages: number;
  total_items: number;
  items_per_page: number;
}

export interface StudySessionsResponse {
  study_sessions: StudySession[];
  pagination: PaginationInfo;
}

export interface WordReviewResponse {
  words: WordReview[];
  pagination: PaginationInfo;
}
