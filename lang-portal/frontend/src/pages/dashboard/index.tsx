import React from 'react';
import { useDashboard } from '../../hooks/useDashboard';
import LastStudySession from '../../components/Dashboard/LastStudySession';
import StudyProgress from '../../components/Dashboard/StudyProgress';
import QuickStats from '../../components/Dashboard/QuickStats';
import { useNavigate } from 'react-router-dom';

const Dashboard: React.FC = () => {
  const { lastSession, progress, stats } = useDashboard();
  const navigate = useNavigate();

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Welcome to Your Spanish Learning Journey</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {lastSession ? (
          <LastStudySession data={lastSession} />
        ) : (
          <div className="bg-white shadow-lg rounded-lg p-6 mb-6 animate-pulse">
            <div className="h-8 bg-gray-200 rounded w-3/4 mb-4"></div>
            <div className="space-y-3">
              <div className="h-4 bg-gray-200 rounded w-1/2"></div>
              <div className="h-4 bg-gray-200 rounded w-2/3"></div>
              <div className="h-4 bg-gray-200 rounded w-1/2"></div>
              <div className="h-10 bg-gray-200 rounded w-full mt-4"></div>
            </div>
          </div>
        )}

        {progress ? (
          <StudyProgress data={progress} />
        ) : (
          <div className="bg-white shadow-lg rounded-lg p-6 mb-6 animate-pulse">
            <div className="h-8 bg-gray-200 rounded w-3/4 mb-4"></div>
            <div className="space-y-4">
              <div className="h-4 bg-gray-200 rounded w-full"></div>
              <div className="h-2 bg-gray-200 rounded-full w-full"></div>
              <div className="h-4 bg-gray-200 rounded w-full"></div>
              <div className="h-2 bg-gray-200 rounded-full w-full"></div>
            </div>
          </div>
        )}
      </div>

      {stats ? (
        <QuickStats data={stats} />
      ) : (
        <div className="bg-white shadow-lg rounded-lg p-6 mb-6 animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-3/4 mb-4"></div>
          <div className="grid grid-cols-2 gap-4">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="p-4 bg-gray-50 rounded-lg">
                <div className="h-4 bg-gray-200 rounded w-1/2 mb-2"></div>
                <div className="h-8 bg-gray-200 rounded w-3/4"></div>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="text-center mt-8">
        <button
          onClick={() => navigate('/study_activities')}
          className="px-8 py-3 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 transition-colors shadow-md"
        >
          Start Learning Spanish
        </button>
      </div>
    </div>
  );
};

export default Dashboard;
