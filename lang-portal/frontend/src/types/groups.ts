import { Word } from './words';

export interface Pagination {
  current_page: number;
  total_pages: number;
  total_items: number;
  items_per_page: number;
}

export interface Group {
  id: number;
  name: string;
  word_count: number;
}

export interface GroupDetail extends Group {
  words: Word[];
}

export interface GroupsResponse {
  groups: Group[];
  pagination: Pagination;
}
