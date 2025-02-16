import React from 'react';
import { useNavigate } from 'react-router-dom';
import { StudyActivity } from '../../types/study-activities';

interface StudyActivityCardProps {
  activity: StudyActivity;
}

const StudyActivityCard: React.FC<StudyActivityCardProps> = ({ activity }) => {
  const navigate = useNavigate();
  
  return (
    <div className="bg-white shadow-lg rounded-lg overflow-hidden">
      <img 
        src={activity.thumbnail_url} 
        alt={activity.name} 
        className="w-full h-48 object-cover"
      />
      <div className="p-4">
        <h3 className="text-xl font-semibold text-gray-800 mb-2">{activity.name}</h3>
        <p className="text-gray-600 mb-4">{activity.description}</p>
        <div className="flex justify-between gap-4">
          <button 
            onClick={() => navigate(`/study-activities/${activity.id}/launch`)} 
            className="flex-1 bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors">
            Launch Activity
          </button>
          <button 
            onClick={() => navigate(`/study-activities/${activity.id}`)} 
            className="flex-1 bg-gray-100 text-gray-700 px-4 py-2 rounded-md hover:bg-gray-200 transition-colors">
            View Details
          </button>
        </div>
      </div>
    </div>
  );
};

export default StudyActivityCard;
