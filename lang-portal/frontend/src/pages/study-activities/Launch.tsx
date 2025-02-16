import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

interface StudyActivityDetail {
  id: string;
  name: string;
  description: string;
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
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [activityRes, groupsRes] = await Promise.all([
          fetch(`http://localhost:8000/api/study-activities/${id}`),
          fetch('http://localhost:8000/api/groups')
        ]);

        if (!activityRes.ok || !groupsRes.ok) {
          throw new Error('Failed to fetch required data');
        }

        const [activityData, groupsData] = await Promise.all([
          activityRes.json(),
          groupsRes.json()
        ]);

        setActivity(activityData);
        setGroups(groupsData.groups);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [id]);

  const handleLaunch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedGroup) {
      setError('Please select a group');
      return;
    }

    setSubmitting(true);
    setError(null);

    try {
      const res = await fetch('http://localhost:8000/api/study-activities', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          study_activity_id: Number(id), 
          group_id: Number(selectedGroup) 
        })
      });

      if (!res.ok) {
        throw new Error('Failed to launch study activity');
      }

      const data = await res.json();
      if (data.launch_url) {
        window.open(data.launch_url, '_blank');
      }
      navigate(`/study-sessions/${data.id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to launch activity');
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="max-w-xl mx-auto px-4 py-8">
        <div className="animate-pulse space-y-6">
          <div className="h-8 bg-gray-200 rounded w-1/2"/>
          <div className="h-4 bg-gray-200 rounded w-3/4"/>
          <div className="h-12 bg-gray-200 rounded w-full"/>
          <div className="h-12 bg-gray-200 rounded w-full"/>
        </div>
      </div>
    );
  }

  if (error && !activity) {
    return (
      <div className="max-w-xl mx-auto px-4 py-8">
        <div className="bg-red-50 border-l-4 border-red-400 p-4">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <p className="text-sm text-red-700">{error}</p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (!activity) {
    return (
      <div className="max-w-xl mx-auto px-4 py-8">
        <div className="bg-red-50 border-l-4 border-red-400 p-4">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <p className="text-sm text-red-700">Activity not found</p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-xl mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold text-gray-900 mb-4">{activity.name}</h1>
      {activity.description && (
        <p className="text-lg text-gray-600 mb-8">{activity.description}</p>
      )}
      
      <form onSubmit={handleLaunch} className="space-y-6">
        <div>
          <label htmlFor="group" className="block text-base font-medium text-gray-900 mb-2">
            Select a Group
          </label>
          <select 
            id="group"
            value={selectedGroup} 
            onChange={e => setSelectedGroup(e.target.value)}
            className="block w-full px-4 py-3 bg-black text-white border-0 focus:ring-2 focus:ring-blue-500 rounded-lg"
            disabled={submitting}
          >
            <option value="">Choose a group...</option>
            {groups.map(group => (
              <option key={group.id} value={group.id}>
                {group.name}
              </option>
            ))}
          </select>
        </div>

        {error && (
          <div className="bg-red-50 border-l-4 border-red-400 p-4">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <p className="text-sm text-red-700">{error}</p>
              </div>
            </div>
          </div>
        )}

        <button
          type="submit"
          disabled={submitting || !selectedGroup}
          className={`w-full py-3 px-4 text-center text-white text-base font-medium rounded-lg bg-blue-500 hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 ${
            (submitting || !selectedGroup) ? 'opacity-50 cursor-not-allowed' : ''
          }`}
        >
          {submitting ? 'Launching...' : 'Launch Activity'}
        </button>
      </form>
    </div>
  );
};

export default StudyActivityLaunch;
