
import React from 'react';
import Dashboard from './Dashboard';
import './App.css';


function App({data = []}) {
  return (
    <div className="Dashboard">
      <Dashboard data={data}/>
    </div>
  );
}

export default App;
