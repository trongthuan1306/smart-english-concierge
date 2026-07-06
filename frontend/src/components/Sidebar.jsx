import React from 'react';
import { MessageSquare, BookOpen, LayoutDashboard, Bot } from 'lucide-react';

export default function Sidebar({ activeTab, setActiveTab }) {
  const navItems = [
    { id: 'chat', label: 'Chat', icon: MessageSquare },
    { id: 'vocabulary', label: 'Vocabulary Notebook', icon: BookOpen },
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
  ];

  return (
    <div className="w-64 bg-white border-r border-gray-200 flex flex-col h-full shadow-sm z-20 hidden md:flex">
      
      {/* Brand Header */}
      <div className="p-6 flex items-center gap-3 border-b border-gray-100">
        <div className="bg-[#4285F4] p-2 rounded-lg text-white shadow-sm flex-shrink-0">
          <Bot size={24} />
        </div>
        <h1 className="font-bold text-gray-800 text-lg leading-tight tracking-tight">
          Smart English<br/>
          <span className="text-[#4285F4]">Concierge</span>
        </h1>
      </div>
      
      {/* Navigation Links */}
      <nav className="flex-1 p-4 space-y-2">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 font-medium ${
                isActive 
                  ? 'bg-[#E8F0FE] text-[#4285F4]' 
                  : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
              }`}
            >
              <Icon size={20} className={isActive ? 'text-[#4285F4]' : 'text-gray-500'} />
              {item.label}
            </button>
          );
        })}
      </nav>

      {/* Footer Info */}
      <div className="p-6 border-t border-gray-100">
        <div className="bg-gray-50 rounded-lg p-3 text-xs text-gray-500 text-center">
          Kaggle AI Agents Capstone
        </div>
      </div>
    </div>
  );
}
