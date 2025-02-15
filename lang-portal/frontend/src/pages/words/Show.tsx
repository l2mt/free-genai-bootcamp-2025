import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

interface WordDetail {
  id: string;
  japanese: string;
  romaji: string;
  english: string;
  correctCount: number;
  wrongCount: number;
  groups: { id: string; name: string }[];
}

const WordShow: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [word, setWord] = useState<WordDetail | null>(null);

  useEffect(() => {
    fetch(`/api/words/${id}`).then(res => res.json()).then(setWord);
  }, [id]);

  if (!word) return <p>Loading...</p>;

  return (
    <div className="p-4 space-y-4">
      <h2 className="text-2xl font-bold">{word.japanese}</h2>
      <p><strong>Romaji:</strong> {word.romaji}</p>
      <p><strong>English:</strong> {word.english}</p>
      <div>
        <h3 className="font-bold">Study Statistics</h3>
        <p>Correct: {word.correctCount} - Incorrect: {word.wrongCount}</p>
      </div>
      <div>
        <h3 className="font-bold">Groups</h3>
        <div className="flex flex-wrap gap-2">
          {word.groups.map(group => (
            <span 
              key={group.id} 
              onClick={() => navigate(`/groups/${group.id}`)} 
              className="cursor-pointer badge">
              {group.name}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
};

export default WordShow;
