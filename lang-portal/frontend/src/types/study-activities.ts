export interface StudyActivity {
  id: number;
  name: string;
  thumbnail_url: string;
  description: string;
  launch_url: string;
  study_session_id?: number;
  group_id?: number;
  created_at?: string;
}

export interface StudyActivityResponse {
  study_activities: StudyActivity[];
  pagination: {
    current_page: number;
    total_pages: number;
    total_items: number;
    items_per_page: number;
  };
}
