import React from 'react';
import { QuickStatsData } from '../../types/dashboard';

interface Props {
  data: QuickStatsData;
}

const QuickStats: React.FC<Props> = ({ data }) => {
  return (
    <div className="bg-white shadow-lg rounded-lg p-6 mb-6">
      <h2 className="text-2xl font-bold mb-4 text-gray-800">Quick Stats</h2>
      <div className="grid grid-cols-2 gap-4">
        <div className="p-4 bg-blue-50 rounded-lg">
          <p className="text-sm text-gray-600">Success Rate</p>
          <p className="text-2xl font-bold text-blue-600">{data.success_rate}%</p>
        </div>
        <div className="p-4 bg-green-50 rounded-lg">
          <p className="text-sm text-gray-600">Total Sessions</p>
          <p className="text-2xl font-bold text-green-600">{data.total_study_sessions}</p>
        </div>
        <div className="p-4 bg-purple-50 rounded-lg">
          <p className="text-sm text-gray-600">Active Groups</p>
          <p className="text-2xl font-bold text-purple-600">{data.total_active_groups}</p>
        </div>
        <div className="p-4 bg-orange-50 rounded-lg">
          <p className="text-sm text-gray-600">Study Streak</p>
          <p className="text-2xl font-bold text-orange-600">{data.study_streak_days} days</p>
        </div>
      </div>
    </div>
  );
};

export default QuickStats;
