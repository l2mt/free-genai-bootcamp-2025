import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

interface Word {
  id: string;
  japanese: string;
  romaji: string;
  english: string;
  correctCount: number;
  wrongCount: number;
}

const WordsIndex: React.FC = () => {
  const [words, setWords] = useState<Word[]>([]);
  const [page, setPage] = useState<number>(1);
  const navigate = useNavigate();
  const itemsPerPage = 100;

  useEffect(() => {
    fetch(`/api/words?page=${page}&limit=${itemsPerPage}`)
      .then(res => res.json())
      .then(data => setWords(data.words));
  }, [page]);

  return (
    <div className="p-4">
      <table className="table-auto w-full">
        <thead>
          <tr>
            <th>Japonés</th>
            <th>Romaji</th>
            <th>Inglés</th>
            <th>Correctas</th>
            <th>Incorrectas</th>
          </tr>
        </thead>
        <tbody>
          {words.map(word => (
            <tr 
              key={word.id} 
              className="hover:bg-gray-100 cursor-pointer" 
              onClick={() => navigate(`/words/${word.id}`)}>
              <td>{word.japanese}</td>
              <td>{word.romaji}</td>
              <td>{word.english}</td>
              <td>{word.correctCount}</td>
              <td>{word.wrongCount}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <div className="flex justify-between mt-4">
        <button disabled={page === 1} onClick={() => setPage(page - 1)} className="btn btn-secondary">Anterior</button>
        <button onClick={() => setPage(page + 1)} className="btn btn-secondary">Siguiente</button>
      </div>
    </div>
  );
};

export default WordsIndex;
