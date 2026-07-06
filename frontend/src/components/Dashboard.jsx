import React from 'react';
import { BookOpen, CheckCircle, MessageSquare, Flame } from 'lucide-react';

export default function Dashboard() {
  // Mock statistics for display
  const stats = [
    { id: 1, title: "Words Saved", value: "24", icon: BookOpen, color: "text-[#4285F4]", bg: "bg-blue-50" },
    { id: 2, title: "Grammar Checks", value: "18", icon: CheckCircle, color: "text-green-600", bg: "bg-green-50" },
    { id: 3, title: "Total Messages", value: "142", icon: MessageSquare, color: "text-purple-600", bg: "bg-purple-50" },
    { id: 4, title: "Day Streak", value: "5", icon: Flame, color: "text-orange-500", bg: "bg-orange-50" },
  ];

  return (
    <div className="h-full overflow-y-auto p-6 md:p-10 bg-[#F8F9FA]">
      <div className="max-w-5xl mx-auto">
        <header className="mb-10">
          <h2 className="text-3xl font-bold text-gray-800 tracking-tight">Your Progress Dashboard</h2>
          <p className="text-gray-500 mt-2 text-lg">Keep up the great work! Here's your learning summary.</p>
        </header>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {stats.map((stat) => {
            const Icon = stat.icon;
            return (
              <div key={stat.id} className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 flex items-center gap-5 hover:-translate-y-1 transition-transform cursor-default">
                <div className={`${stat.bg} ${stat.color} p-4 rounded-xl`}>
                  <Icon size={28} />
                </div>
                <div>
                  <p className="text-sm font-medium text-gray-500 mb-0.5">{stat.title}</p>
                  <p className="text-3xl font-bold text-gray-800">{stat.value}</p>
                </div>
              </div>
            );
          })}
        </div>

        {/* Placeholder for future expansion */}
        <div className="mt-10 bg-white rounded-2xl p-8 shadow-sm border border-gray-100 text-center flex flex-col items-center justify-center py-20">
          <div className="w-16 h-16 bg-gray-50 rounded-full flex items-center justify-center mb-4">
            <LayoutDashboard size={24} className="text-gray-400" />
          </div>
          <h3 className="text-lg font-bold text-gray-700">Detailed Analytics Coming Soon</h3>
          <p className="text-gray-500 mt-2 max-w-md mx-auto">Future updates will include visual charts for learning progression, skill usage breakdowns, and personalized study recommendations.</p>
        </div>
      </div>
    </div>
  );
}

// Small mock import fix
import { LayoutDashboard } from 'lucide-react';
