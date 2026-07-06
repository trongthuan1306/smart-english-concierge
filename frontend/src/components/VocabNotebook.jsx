import React from 'react';

export default function VocabNotebook() {
  return (
    <div className="w-80 bg-white border-l p-4 h-screen overflow-y-auto">
      <h2 className="text-xl font-bold mb-4">Vocabulary Notebook</h2>
      <div className="space-y-3">
        <div className="p-3 border rounded-lg bg-yellow-50">
          <h3 className="font-semibold">Serendipity</h3>
          <p className="text-sm text-gray-600">The occurrence and development of events by chance in a happy or beneficial way.</p>
        </div>
      </div>
    </div>
  );
}
