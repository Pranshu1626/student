import React from 'react';
import { BrowserRouter } from 'react-router-dom';

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-50">
        {/* Application routes will go here */}
        <div className="p-4">
          <h1 className="text-2xl font-bold text-center text-blue-600">
            Student Management System
          </h1>
        </div>
      </div>
    </BrowserRouter>
  );
}

export default App;
