import React, { useState } from 'react';
import Sidebar from './components/Sidebar';
import ChatWindow from './components/ChatWindow';
import VocabularyNotebook from './components/VocabularyNotebook';
import Dashboard from './components/Dashboard';

function App() {
  const [activeTab, setActiveTab] = useState('chat');

  return (
    <div className="flex h-screen bg-[#F8F9FA] font-sans antialiased text-gray-900">
      
      {/* Persistent Sidebar Navigation */}
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />
      
      {/* Main Content Area - Renders based on activeTab */}
      <main className="flex-1 overflow-hidden relative">
        {activeTab === 'chat' && <ChatWindow />}
        {activeTab === 'vocabulary' && <VocabularyNotebook />}
        {activeTab === 'dashboard' && <Dashboard />}
      </main>

    </div>
  );
}

export default App;
