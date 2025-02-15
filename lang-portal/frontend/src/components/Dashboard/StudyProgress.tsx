import React from 'react';
import { StudyProgressData } from '../../types/dashboard';

interface Props {
  data: StudyProgressData;
}

const StudyProgress: React.FC<Props> = ({ data }) => {
  return (
    <div className="bg-white shadow-lg rounded-lg p-6 mb-6">
      <h2 className="text-2xl font-bold mb-4 text-gray-800">Study Progress</h2>
      <div className="space-y-4">
        <div>
          <p className="text-gray-700 mb-2">
            <span className="font-semibold">Words Studied:</span> {data.total_words_studied} / {data.total_available_words}
          </p>
          <div className="w-full bg-gray-200 rounded-full h-2.5">
            <div 
              className="bg-blue-600 h-2.5 rounded-full" 
              style={{ width: `${(data.total_words_studied / data.total_available_words) * 100}%` }}
            ></div>
          </div>
        </div>
        
        <div>
          <p className="text-gray-700 mb-2">
            <span className="font-semibold">Mastery Level:</span> {data.mastery_percentage}%
          </p>
          <div className="w-full bg-gray-200 rounded-full h-2.5">
            <div 
              className="bg-green-600 h-2.5 rounded-full" 
              style={{ width: `${data.mastery_percentage}%` }}
            ></div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StudyProgress;
