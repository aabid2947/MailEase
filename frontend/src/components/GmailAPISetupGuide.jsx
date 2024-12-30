import React, { useState } from 'react';

const AccordionItem = ({ title, children }) => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="border-b border-gray-700">
      <button
        className="flex justify-between items-center w-full py-4 px-6 text-left text-white hover:bg-gray-800 focus:outline-none"
        onClick={() => setIsOpen(!isOpen)}
      >
        <span>{title}</span>
        <span className="transform transition-transform duration-200 ease-in-out">
          {isOpen ? '▲' : '▼'}
        </span>
      </button>
      {isOpen && (
        <div className="p-6 bg-gray-800 text-gray-300">
          {children}
        </div>
      )}
    </div>
  );
};

const GmailSetupGuide = () => {
  return (
    <div className="w-full max-w-3xl mx-auto  text-white rounded-lg shadow-xl overflow-hidden">
      <div className="p-6">
        <h2 className="text-2xl font-bold mb-2">Gmail API Setup Guide</h2>
        <p className="text-gray-300">
          Follow these steps to set up the Gmail API and generate OAuth 2.0 credentials
        </p>
      </div>
      <div className="divide-y divide-gray-700">
        <AccordionItem title="Step 1: Enable the Gmail API">
          <ol className="list-decimal list-inside space-y-2">
            <li>Log in to <a href="https://console.cloud.google.com/" target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:underline">Google Cloud Console</a></li>
            <li>Create a new project (e.g., "MailEase")</li>
            <li>Navigate to API & Services &gt; Library</li>
            <li>Search for "Gmail API" and enable it</li>
          </ol>
        </AccordionItem>
        <AccordionItem title="Step 2: Configure OAuth Consent Screen">
          <ol className="list-decimal list-inside space-y-2">
            <li>Go to API & Services &gt; OAuth Consent Screen</li>
            <li>Choose External or Internal user type</li>
            <li>Fill out app information (name, support email, etc.)</li>
            <li>Add the scope: https://mail.google.com/</li>
            <li>Add test users if in testing mode</li>
          </ol>
        </AccordionItem>
        <AccordionItem title="Step 3: Generate OAuth 2.0 Credentials">
          <ol className="list-decimal list-inside space-y-2">
            <li>Go to API & Services &gt; Credentials</li>
            <li>Click "Create Credentials" and select "OAuth Client ID"</li>
            <li>Choose "Web Application" as the application type</li>
            <li>Add authorized redirect URIs:
              <ul className="list-disc list-inside ml-4 mt-1">
                <li>http://localhost:8000/ (for local development)</li>
                <li>https://your-domain.com/auth/callback (for production)</li>
              </ul>
            </li>
            <li>Download the credentials.json file</li>
          </ol>
        </AccordionItem>
      </div>
    </div>
  );
};

export default GmailSetupGuide;
