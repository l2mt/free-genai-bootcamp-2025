import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

interface GroupDetail {
  id: string;
  name: string;
  totalWords: number;
}
interface Word {
  id: string;
  japanese: string;
  romaji: string;
  english: string;
}
interface StudySession {
  id: string;
  activityName: string;
  groupName: string;
  startTime: string;
  endTime: string;
  reviewCount: number;
}

const GroupShow: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [group, setGroup] = useState<GroupDetail | null>(null);
  const [words, setWords] = useState<Word[]>([]);
  const [sessions, setSessions] = useState<StudySession[]>([]);

  useEffect(() => {
    fetch(`/api/groups/${id}`).then(res => res.json()).then(setGroup);
    fetch(`/api/groups/${id}/words`).then(res => res.json()).then(data => setWords(data.words));
    fetch(`/api/groups/${id}/study_sessions`).then(res => res.json()).then(data => setSessions(data.sessions));
  }, [id]);

  if (!group) return <p>Cargando...</p>;

  return (
    <div className="p-4 space-y-4">
      <h2 className="text-2xl font-bold">{group.name}</h2>
      <p>Total de Palabras: {group.totalWords}</p>

      <div>
        <h3 className="font-bold mb-2">Palabras en el Grupo</h3>
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
      </div>

      <div>
        <h3 className="font-bold mb-2">Sesiones de Estudio</h3>
        <table className="table-auto w-full">
          <thead>
            <tr>
              <th>ID</th>
              <th>Actividad</th>
              <th>Grupo</th>
              <th>Inicio</th>
              <th>Fin</th>
              <th>Items</th>
            </tr>
          </thead>
          <tbody>
            {sessions.map(session => (
              <tr 
                key={session.id} 
                className="hover:bg-gray-100 cursor-pointer" 
                onClick={() => navigate(`/study_sessions/${session.id}`)}>
                <td>{session.id}</td>
                <td>{session.activityName}</td>
                <td>{session.groupName}</td>
                <td>{session.startTime}</td>
                <td>{session.endTime}</td>
                <td>{session.reviewCount}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default GroupShow;
