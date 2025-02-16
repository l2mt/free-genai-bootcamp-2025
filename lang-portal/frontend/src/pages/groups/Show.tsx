import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Group } from '../../types/groups';
import { Word } from '../../types/words';

interface GroupWithWords extends Group {
  words: Word[];
}

const GroupShow: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [group, setGroup] = useState<GroupWithWords | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchGroupAndWords = async () => {
      try {
        setLoading(true);
        
        // Fetch group details
        const groupResponse = await fetch(`http://localhost:8000/api/groups/${id}`);
        if (!groupResponse.ok) {
          throw new Error('Failed to fetch group details');
        }
        const groupData = await groupResponse.json();
        
        // Fetch group words
        const wordsResponse = await fetch(`http://localhost:8000/api/groups/${id}/words`);
        if (!wordsResponse.ok) {
          throw new Error('Failed to fetch group words');
        }
        const wordsData = await wordsResponse.json();
        
        // Combine the data
        setGroup({
          id: groupData.id,
          name: groupData.name,
          word_count: groupData.word_count,
          words: wordsData.items || []
        });
        
        setError(null);
      } catch (err) {
        console.error('Error fetching group data:', err);
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setLoading(false);
      }
    };

    fetchGroupAndWords();
  }, [id]);

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/4 mb-8"></div>
          <div className="h-16 bg-gray-200 rounded mb-8"></div>
          <div className="space-y-4">
            {[...Array(10)].map((_, index) => (
              <div key={index} className="h-12 bg-gray-200 rounded"></div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-8">
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

  if (!group) {
    return null;
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900">{group.name}</h1>
        <Link
          to="/groups"
          className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
        >
          Back to Groups
        </Link>
      </div>

      <div className="bg-gray-50 rounded-lg p-6 mb-8">
        <h2 className="text-lg font-medium text-gray-700 mb-2">Group Statistics</h2>
        <div className="text-4xl font-bold text-blue-600">
          {group.word_count}
          <span className="text-base font-normal text-gray-500 ml-2">Total Words</span>
        </div>
      </div>

      <div className="bg-white shadow-md rounded-lg overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-200">
          <h2 className="text-lg font-medium text-gray-900">Words in Group</h2>
        </div>
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Spanish
              </th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                English
              </th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Correct
              </th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Wrong
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {group.words.map((word) => (
              <tr key={word.id}>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  {word.spanish}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {word.english}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-green-600">
                  {word.correct_count}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-red-600">
                  {word.wrong_count}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default GroupShow;
