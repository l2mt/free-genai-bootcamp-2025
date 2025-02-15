// src/App.tsx
import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import Dashboard from './pages/dashboard';
import StudyActivitiesIndex from './pages/study_activities';
import StudyActivityShow from './pages/study_activities/Show';
import StudyActivityLaunch from './pages/study_activities/Launch';
import WordsIndex from './pages/words';
import WordShow from './pages/words/Show';
import GroupsIndex from './pages/groups';
import GroupShow from './pages/groups/Show';
import StudySessionsIndex from './pages/study_sessions';
import StudySessionShow from './pages/study_sessions/Show';
import Settings from './pages/settings';
import MainLayout from './components/Layout/MainLayout';

const App: React.FC = () => {
  return (
    <Routes>
      <Route element={<MainLayout />}>
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/study_activities" element={<StudyActivitiesIndex />} />
        <Route path="/study_activities/:id" element={<StudyActivityShow />} />
        <Route path="/study_activities/:id/launch" element={<StudyActivityLaunch />} />
        <Route path="/words" element={<WordsIndex />} />
        <Route path="/words/:id" element={<WordShow />} />
        <Route path="/groups" element={<GroupsIndex />} />
        <Route path="/groups/:id" element={<GroupShow />} />
        <Route path="/study_sessions" element={<StudySessionsIndex />} />
        <Route path="/study_sessions/:id" element={<StudySessionShow />} />
        <Route path="/settings" element={<Settings />} />
      </Route>
    </Routes>
  );
};

export default App;
