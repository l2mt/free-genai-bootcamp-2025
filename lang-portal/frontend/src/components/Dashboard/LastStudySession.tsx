import React from 'react';
import { useNavigate } from 'react-router-dom';
import { LastStudySessionData } from '../../types/dashboard';

interface Props {
  data: LastStudySessionData;
}

const LastStudySession: React.FC<Props> = ({ data }) => {
  const navigate = useNavigate();

  return (
    <div className="bg-white shadow-lg rounded-lg p-6 mb-6">
      <h2 className="text-2xl font-bold mb-4 text-gray-800">Last Study Session</h2>
      <div className="space-y-3">
        <p className="text-gray-700">
          <span className="font-semibold">Activity:</span> {data.activity_name}
        </p>
        <p className="text-gray-700">
          <span className="font-semibold">Last used:</span> {new Date(data.created_at).toLocaleString()}
        </p>
        <p className="text-gray-700">
          <span className="font-semibold">Correct:</span> {data.correct_count} / 
          <span className="font-semibold ml-2">Incorrect:</span> {data.incorrect_count}
        </p>
        <button 
          onClick={() => navigate(`/groups/${data.group_id}`)}
          className="w-full mt-4 px-4 py-2 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 transition-colors"
        >
          Go to Group: {data.group_name}
        </button>
      </div>
    </div>
  );
};

export default LastStudySession;
