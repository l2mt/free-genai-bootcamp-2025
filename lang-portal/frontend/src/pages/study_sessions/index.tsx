import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

interface StudySession {
  id: string;
  activityName: string;
  groupName: string;
  startTime: string;
  endTime: string;
  reviewCount: number;
}

const StudySessionsIndex: React.FC = () => {
  const [sessions, setSessions] = useState<StudySession[]>([]);
  const [page, setPage] = useState<number>(1);
  const navigate = useNavigate();
  const itemsPerPage = 100;

  useEffect(() => {
    fetch(`/api/study_sessions?page=${page}&limit=${itemsPerPage}`)
      .then(res => res.json())
      .then(data => setSessions(data.sessions));
  }, [page]);

  return (
    <div className="p-4">
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
      <div className="flex justify-between mt-4">
        <button disabled={page === 1} onClick={() => setPage(page - 1)} className="btn btn-secondary">Anterior</button>
        <button onClick={() => setPage(page + 1)} className="btn btn-secondary">Siguiente</button>
      </div>
    </div>
  );
};

export default StudySessionsIndex;
