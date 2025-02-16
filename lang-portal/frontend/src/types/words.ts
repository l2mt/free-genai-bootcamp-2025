import { Pagination } from './groups';

export interface Word {
  id: number;
  spanish: string;
  english: string;
  correct_count: number;
  wrong_count: number;
}

export interface WordsResponse {
  items: Word[];
  pagination: Pagination;
}
