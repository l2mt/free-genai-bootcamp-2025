import React, { useState } from 'react';

const Settings: React.FC = () => {
  const [theme, setTheme] = useState<string>('system');

  const handleResetHistory = async () => {
    await fetch('/api/reset_history', { method: 'POST' });
    alert('Historial reiniciado');
  };

  const handleFullReset = async () => {
    await fetch('/api/full_reset', { method: 'POST' });
    alert('Reset completo realizado');
  };

  return (
    <div className="p-4 max-w-md mx-auto space-y-4">
      <div>
        <label className="block mb-1 font-bold">Tema</label>
        <select 
          value={theme} 
          onChange={e => setTheme(e.target.value)} 
          className="input">
          <option value="light">Claro</option>
          <option value="dark">Oscuro</option>
          <option value="system">Sistema</option>
        </select>
      </div>
      <button onClick={handleResetHistory} className="btn btn-secondary w-full">
        Resetear Historial
      </button>
      <button onClick={handleFullReset} className="btn btn-danger w-full">
        Resetear Todo
      </button>
    </div>
  );
};

export default Settings;
