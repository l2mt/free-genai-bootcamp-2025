import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

interface StudyActivityDetail {
  id: string;
  name: string;
}
interface Group {
  id: string;
  name: string;
}

const StudyActivityLaunch: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [activity, setActivity] = useState<StudyActivityDetail | null>(null);
  const [groups, setGroups] = useState<Group[]>([]);
  const [selectedGroup, setSelectedGroup] = useState<string>('');

  useEffect(() => {
    fetch(`/api/study_activities/${id}`).then(res => res.json()).then(setActivity);
    // Se asume endpoint para obtener grupos disponibles
    fetch(`/api/groups`).then(res => res.json()).then(setGroups);
  }, [id]);

  const handleLaunch = async (e: React.FormEvent) => {
    e.preventDefault();
    const res = await fetch('/api/study_activities', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ activityId: id, groupId: selectedGroup })
    });
    const data = await res.json();
    window.open(data.url, '_blank');
    navigate(`/study_sessions/${data.studySessionId}`);
  };

  if (!activity) return <p>Cargando...</p>;

  return (
    <div className="p-4 max-w-md mx-auto">
      <h2 className="text-2xl font-bold mb-4">{activity.name}</h2>
      <form onSubmit={handleLaunch} className="space-y-4">
        <div>
          <label className="block mb-1">Selecciona un grupo</label>
          <select 
            value={selectedGroup} 
            onChange={e => setSelectedGroup(e.target.value)} 
            className="input">
            <option value="">Selecciona...</option>
            {groups.map(group => (
              <option key={group.id} value={group.id}>{group.name}</option>
            ))}
          </select>
        </div>
        <button type="submit" className="btn btn-primary w-full">
          Lanzar Ahora
        </button>
      </form>
    </div>
  );
};

export default StudyActivityLaunch;
