import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

interface StudyActivityDetail {
  id: string;
  name: string;
  thumbnail: string;
  description: string;
}
interface StudySession {
  id: string;
  activityName: string;
  groupName: string;
  startTime: string;
  endTime: string;
  reviewCount: number;
}

const StudyActivityShow: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [activity, setActivity] = useState<StudyActivityDetail | null>(null);
  const [sessions, setSessions] = useState<StudySession[]>([]);

  useEffect(() => {
    fetch(`/api/study_activities/${id}`).then(res => res.json()).then(setActivity);
    fetch(`/api/study_activities/${id}/study_sessions`).then(res => res.json()).then(setSessions);
  }, [id]);

  if (!activity) return <p>Cargando...</p>;

  return (
    <div className="p-4 space-y-4">
      <div className="card shadow rounded p-4">
        <img src={activity.thumbnail} alt={activity.name} className="w-full h-32 object-cover rounded"/>
        <h2 className="text-2xl font-bold">{activity.name}</h2>
        <p>{activity.description}</p>
        <button 
          onClick={() => navigate(`/study_activities/${id}/launch`)} 
          className="btn btn-primary mt-2">
          Lanzar Actividad
        </button>
      </div>
      <div>
        <h3 className="text-xl font-bold mb-2">Sesiones de Estudio</h3>
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

export default StudyActivityShow;
