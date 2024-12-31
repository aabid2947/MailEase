



import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";
import App from './App'
import EmailMonitoringPage from './pages/EmailMonitoringPage.jsx';
import AutheticatePage from './pages/AuthenticatePage.jsx';

import DeleteEmailPage from './pages/DeleteEmailPage.jsx';
import PrivacyPolicy from './components/Policy.jsx';


const router = createBrowserRouter([
  {
    path: "/",
    element: <App/>,
   
  },
  {
    path:"/delete-email",
    element:<DeleteEmailPage/>
  },
  {
    path:"/monitor-email",
    element:<EmailMonitoringPage/>
  },
  {
    path:"/authenticate",
    element:<AutheticatePage/>
  },
  {
    path:"/policy",
    element:<PrivacyPolicy/>
  },



  
  
]);

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
  

     <RouterProvider router={router} />
   
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals

