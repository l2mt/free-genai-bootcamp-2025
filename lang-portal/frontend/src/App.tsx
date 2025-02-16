// src/App.tsx
import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider } from './contexts/ThemeContext';
import Dashboard from './pages/dashboard';
import StudyActivitiesIndex from './pages/study-activities';
import StudyActivityShow from './pages/study-activities/Show';
import StudyActivityLaunch from './pages/study-activities/Launch';
import WordsIndex from './pages/words';
import WordShow from './pages/words/Show';
import GroupsIndex from './pages/groups';
import GroupShow from './pages/groups/Show';
import StudySessionsIndex from './pages/study-sessions';
import StudySessionShow from './pages/study-sessions/Show';
import Settings from './pages/settings';
import MainLayout from './components/Layout/MainLayout';

const App: React.FC = () => {
  return (
    <ThemeProvider>
      <Routes>
        <Route element={<MainLayout />}>
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/study-activities" element={<StudyActivitiesIndex />} />
          <Route path="/study-activities/:id" element={<StudyActivityShow />} />
          <Route path="/study-activities/:id/launch" element={<StudyActivityLaunch />} />
          <Route path="/words" element={<WordsIndex />} />
          <Route path="/words/:id" element={<WordShow />} />
          <Route path="/groups" element={<GroupsIndex />} />
          <Route path="/groups/:id" element={<GroupShow />} />
          <Route path="/study-sessions" element={<StudySessionsIndex />} />
          <Route path="/study-sessions/:id" element={<StudySessionShow />} />
          <Route path="/settings" element={<Settings />} />
        </Route>
      </Routes>
    </ThemeProvider>
  );
};

export default App;
