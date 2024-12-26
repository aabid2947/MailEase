import { useState } from 'react'
import AuthenticateForm from './components/AuthenticateUser'
import './App.css'
import Header from './components/Header'
import DeleteEmailsForm from './components/DeleteEmailsForm'
import EmailMonitoringForm from './components/EmailMonitoringForm'
import { BrowserRouter as Router } from 'react-router-dom'


function App() {

  return (
    <>
      <div className='space-y-4 bg-gradient-to-br from-gray-900 to-gray-800'>
      
      <Router>

      <Header/>
      </Router>
      <AuthenticateForm/>
      <EmailMonitoringForm/>
      <DeleteEmailsForm/>
      </div>

    
    </>
  )
}

export default App
