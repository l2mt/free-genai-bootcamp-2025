import React from 'react';
import { useTheme } from '../../contexts/ThemeContext';

const Settings: React.FC = () => {
  const { theme, setTheme } = useTheme();

  const handleResetHistory = async () => {
    if (confirm('¿Estás seguro de que quieres resetear el historial? Esta acción no se puede deshacer.')) {
      try {
        await fetch('/api/reset_history', { method: 'POST' });
        alert('Historial reiniciado exitosamente');
      } catch (error) {
        alert('Error al resetear el historial');
      }
    }
  };

  const handleFullReset = async () => {
    if (confirm('¿Estás seguro de que quieres resetear toda la aplicación? Esta acción no se puede deshacer.')) {
      try {
        await fetch('/api/full_reset', { method: 'POST' });
        alert('Reset completo realizado exitosamente');
      } catch (error) {
        alert('Error al realizar el reset completo');
      }
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-8">
        Configuración
      </h1>

      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg overflow-hidden">
        <div className="p-6 space-y-6">
          {/* Apariencia */}
          <div>
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
              Apariencia
            </h2>
            <div className="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg">
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Tema
              </label>
              <select 
                value={theme} 
                onChange={e => setTheme(e.target.value as 'light' | 'dark' | 'system')}
                className="block w-full px-4 py-2 text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-600 border border-gray-300 dark:border-gray-500 rounded-md shadow-sm focus:border-blue-500 focus:ring-blue-500"
              >
                <option value="light">Claro</option>
                <option value="dark">Oscuro</option>
                <option value="system">Sistema</option>
              </select>
              <p className="mt-2 text-sm text-gray-500 dark:text-gray-400">
                Selecciona el tema que prefieras para la aplicación
              </p>
            </div>
          </div>

          {/* Datos */}
          <div>
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
              Datos y Privacidad
            </h2>
            <div className="space-y-4">
              <div className="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg">
                <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
                  Resetear Historial
                </h3>
                <p className="text-sm text-gray-500 dark:text-gray-400 mb-4">
                  Elimina todo el historial de estudio manteniendo las palabras y grupos
                </p>
                <button 
                  onClick={handleResetHistory}
                  className="w-full px-4 py-2 text-sm font-medium text-white bg-yellow-600 hover:bg-yellow-700 rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-yellow-500 transition-colors"
                >
                  Resetear Historial
                </button>
              </div>

              <div className="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg">
                <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
                  Resetear Todo
                </h3>
                <p className="text-sm text-gray-500 dark:text-gray-400 mb-4">
                  Elimina todos los datos de la aplicación, incluyendo palabras, grupos e historial
                </p>
                <button 
                  onClick={handleFullReset}
                  className="w-full px-4 py-2 text-sm font-medium text-white bg-red-600 hover:bg-red-700 rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 transition-colors"
                >
                  Resetear Todo
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Settings;
