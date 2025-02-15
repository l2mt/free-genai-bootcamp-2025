import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

interface Group {
  id: string;
  name: string;
  wordCount: number;
}

const GroupsIndex: React.FC = () => {
  const [groups, setGroups] = useState<Group[]>([]);
  const [page, setPage] = useState<number>(1);
  const navigate = useNavigate();
  const itemsPerPage = 100;

  useEffect(() => {
    fetch(`/api/groups?page=${page}&limit=${itemsPerPage}`)
      .then(res => res.json())
      .then(data => setGroups(data.groups));
  }, [page]);

  return (
    <div className="p-4">
      <table className="table-auto w-full">
        <thead>
          <tr>
            <th>Grupo</th>
            <th>Cantidad de Palabras</th>
          </tr>
        </thead>
        <tbody>
          {groups.map(group => (
            <tr 
              key={group.id} 
              className="hover:bg-gray-100 cursor-pointer" 
              onClick={() => navigate(`/groups/${group.id}`)}>
              <td>{group.name}</td>
              <td>{group.wordCount}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <div className="flex justify-between mt-4">
        <button disabled={page === 1} onClick={() => setPage(page - 1)} className="btn btn-secondary">Anterior</button>
        <button onClick={() => setPage(page + 1)} className="btn btn-secondary">Siguiente</button>
      </div>
    </div>
  );
};

export default GroupsIndex;
