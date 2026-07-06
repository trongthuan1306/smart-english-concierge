import React, { useEffect, useState } from 'react';
import { BookMarked, Loader2 } from 'lucide-react';
import { getVocabulary } from '../services/api';

export default function VocabularyNotebook() {
  const [vocabList, setVocabList] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchVocab = async () => {
      try {
        const response = await getVocabulary();
        if (response.status === 'success') {
          setVocabList(response.words || []);
        } else {
          setError('Failed to fetch vocabulary.');
        }
      } catch (err) {
        setError('Error connecting to the server. Is FastAPI running?');
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchVocab();
  }, []);

  // Format date nicely
  const formatDate = (isoString) => {
    if (!isoString) return 'Unknown date';
    const date = new Date(isoString);
    return date.toLocaleDateString(undefined, { 
      year: 'numeric', 
      month: 'short', 
      day: 'numeric' 
    });
  };

  return (
    <div className="h-full overflow-y-auto p-6 md:p-10 bg-[#F8F9FA]">
      <div className="max-w-5xl mx-auto">
        <header className="mb-10 flex items-center gap-4">
          <div className="p-3 bg-white shadow-sm border border-gray-100 rounded-xl text-[#4285F4]">
            <BookMarked size={32} />
          </div>
          <div>
            <h2 className="text-3xl font-bold text-gray-800 tracking-tight">Vocabulary Notebook</h2>
            <p className="text-gray-500 mt-1">Review words you've saved during your chat sessions.</p>
          </div>
        </header>

        {isLoading && (
          <div className="flex flex-col items-center justify-center py-20 text-gray-500">
            <Loader2 size={40} className="animate-spin text-[#4285F4] mb-4" />
            <p>Loading your vocabulary...</p>
          </div>
        )}

        {error && !isLoading && (
          <div className="bg-red-50 text-red-600 p-4 rounded-xl border border-red-100 text-center">
            {error}
          </div>
        )}

        {!isLoading && !error && vocabList.length === 0 && (
          <div className="bg-white rounded-2xl p-10 shadow-sm border border-gray-100 text-center">
            <p className="text-gray-500 text-lg">No saved vocabulary yet.</p>
            <p className="text-gray-400 mt-2">Chat with the agent and ask to save a word to see it here.</p>
          </div>
        )}

        {!isLoading && !error && vocabList.length > 0 && (
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
            {vocabList.map((vocab, index) => (
              <div key={index} className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 hover:shadow-md transition-shadow relative overflow-hidden group">
                {/* Decorative side border */}
                <div className="absolute top-0 left-0 w-1.5 h-full bg-[#4285F4] opacity-0 group-hover:opacity-100 transition-opacity"></div>
                
                <div className="flex justify-between items-start mb-5">
                  <h3 className="text-xl font-bold text-gray-800 capitalize">{vocab.word}</h3>
                  <span className="text-xs font-medium text-gray-400 bg-gray-50 px-2.5 py-1 rounded-full border border-gray-100 whitespace-nowrap ml-2">
                    {formatDate(vocab.saved_at)}
                  </span>
                </div>
                
                <div className="space-y-4">
                  <div>
                    <p className="text-xs text-gray-400 font-bold uppercase tracking-wider mb-1.5">Meaning</p>
                    <p className="text-gray-700 bg-blue-50/50 p-2.5 rounded-lg border border-blue-50">{vocab.meaning}</p>
                  </div>
                  
                  {vocab.example && (
                    <div>
                      <p className="text-xs text-gray-400 font-bold uppercase tracking-wider mb-1.5">Example</p>
                      <p className="text-gray-600 italic border-l-2 border-[#4285F4]/30 pl-3 py-1">"{vocab.example}"</p>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
