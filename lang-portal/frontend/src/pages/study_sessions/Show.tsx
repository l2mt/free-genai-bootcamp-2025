import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

interface StudySessionDetail {
  id: string;
  activityName: string;
  groupName: string;
  startTime: string;
  endTime: string;
  reviewCount: number;
}
interface Word {
  id: string;
  japanese: string;
  romaji: string;
  english: string;
}

const StudySessionShow: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [session, setSession] = useState<StudySessionDetail | null>(null);
  const [words, setWords] = useState<Word[]>([]);
  const [page, setPage] = useState<number>(1);
  const itemsPerPage = 100;

  useEffect(() => {
    fetch(`/api/study_sessions/${id}`)
      .then(res => res.json())
      .then(setSession);
    fetch(`/api/study_sessions/${id}/words?page=${page}&limit=${itemsPerPage}`)
      .then(res => res.json())
      .then(data => setWords(data.words));
  }, [id, page]);

  if (!session) return <p>Cargando...</p>;

  return (
    <div className="p-4 space-y-4">
      <div className="shadow rounded p-4">
        <h2 className="text-2xl font-bold">{session.activityName}</h2>
        <p>Grupo: {session.groupName}</p>
        <p>Inicio: {session.startTime}</p>
        <p>Fin: {session.endTime}</p>
        <p>Items: {session.reviewCount}</p>
      </div>
      <div>
        <h3 className="font-bold mb-2">Palabras Revisadas</h3>
        <table className="table-auto w-full">
          <thead>
            <tr>
              <th>Japonés</th>
              <th>Romaji</th>
              <th>Inglés</th>
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
              </tr>
            ))}
          </tbody>
        </table>
        <div className="flex justify-between mt-4">
          <button disabled={page === 1} onClick={() => setPage(page - 1)} className="btn btn-secondary">Anterior</button>
          <button onClick={() => setPage(page + 1)} className="btn btn-secondary">Siguiente</button>
        </div>
      </div>
    </div>
  );
};

export default StudySessionShow;
