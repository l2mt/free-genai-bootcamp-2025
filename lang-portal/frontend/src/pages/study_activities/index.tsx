import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

interface StudyActivity {
  id: string;
  name: string;
  thumbnail: string;
}

const StudyActivityCard: React.FC<{ activity: StudyActivity }> = ({ activity }) => {
  const navigate = useNavigate();
  return (
    <div className="card shadow rounded p-4">
      <img src={activity.thumbnail} alt={activity.name} className="w-full h-32 object-cover rounded"/>
      <h3 className="font-bold mt-2">{activity.name}</h3>
      <div className="flex justify-between mt-2">
        <button 
          onClick={() => navigate(`/study_activities/${activity.id}/launch`)} 
          className="btn btn-primary">
          Lanzar
        </button>
        <button 
          onClick={() => navigate(`/study_activities/${activity.id}`)} 
          className="btn btn-secondary">
          Ver
        </button>
      </div>
    </div>
  );
};

const StudyActivitiesIndex: React.FC = () => {
  const [activities, setActivities] = useState<StudyActivity[]>([]);

  useEffect(() => {
    fetch('/api/study_activities').then(res => res.json()).then(setActivities);
  }, []);

  return (
    <div className="p-4 grid grid-cols-1 md:grid-cols-3 gap-4">
      {activities.map(activity => (
        <StudyActivityCard key={activity.id} activity={activity} />
      ))}
    </div>
  );
};

export default StudyActivitiesIndex;
