import React, { useState } from 'react';
import { MonitorEmails } from '../API/APICalls';
import { motion } from 'framer-motion';
import { EnvelopeIcon, KeyIcon, ClockIcon, PhoneIcon } from '@heroicons/react/24/outline';

const EmailMonitoringForm = () => {
  const [emailAddresses, setEmailAddresses] = useState('');
  const [keywords, setKeywords] = useState('');
  const [phoneNumber, setPhoneNumber] = useState('');
  const [interval, setInterval] = useState(5);
  const [formSubmitted, setFormSubmitted] = useState(false);
  const [response, setResponse] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    const preferences = {
      email_addresses: emailAddresses.split(',').map((email) => email.trim()),
      keywords: keywords.split(',').map((keyword) => keyword.trim()),
      user_phone_number: phoneNumber,
    };

    try {
      const res = await MonitorEmails(preferences, interval);

      if (res.data.status === 'success') {
        setResponse(res.data.message);
        setFormSubmitted(true);
      } else {
        setResponse(res.data.message);
      }
    } catch (error) {
      setResponse('An error occurred. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const inputClasses = "mt-1 block w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-sm shadow-sm placeholder-gray-400 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 text-gray-200";

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 flex items-center justify-center p-4">
      <motion.div 
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="w-full max-w-2xl bg-gray-800 p-8 rounded-2xl shadow-xl"
      >
        <h2 className="text-3xl font-bold text-center mb-8 text-gray-100">Email Monitoring Setup</h2>
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label htmlFor="emailAddresses" className="block text-sm font-medium text-gray-300 mb-1">
              Email Addresses to Monitor
            </label>
            <div className="relative">
              <EnvelopeIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <input
                type="text"
                id="emailAddresses"
                value={emailAddresses}
                onChange={(e) => setEmailAddresses(e.target.value)}
                className={`${inputClasses} pl-10`}
                placeholder="example@mail.com, another@mail.com"
                required
              />
            </div>
            <p className="mt-1 text-xs text-gray-400">Comma separated list of email addresses</p>
          </div>

          <div>
            <label htmlFor="keywords" className="block text-sm font-medium text-gray-300 mb-1">
              Keywords to Track
            </label>
            <div className="relative">
              <KeyIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <input
                type="text"
                id="keywords"
                value={keywords}
                onChange={(e) => setKeywords(e.target.value)}
                className={`${inputClasses} pl-10`}
                placeholder="important, meeting, urgent"
                required
              />
            </div>
            <p className="mt-1 text-xs text-gray-400">Comma separated list of keywords</p>
          </div>

          <div>
            <label htmlFor="interval" className="block text-sm font-medium text-gray-300 mb-1">
              Monitoring Interval (minutes)
            </label>
            <div className="relative">
              <ClockIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <input
                type="number"
                id="interval"
                value={interval}
                onChange={(e) => setInterval(e.target.value)}
                className={`${inputClasses} pl-10`}
                min="1"
                required
              />
            </div>
            <p className="mt-1 text-xs text-gray-400">How frequently to check for new emails</p>
          </div>

          <div>
            <label htmlFor="phoneNumber" className="block text-sm font-medium text-gray-300 mb-1">
              Your Phone Number
            </label>
            <div className="relative">
              <PhoneIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <input
                type="tel"
                id="phoneNumber"
                value={phoneNumber}
                onChange={(e) => setPhoneNumber(e.target.value)}
                className={`${inputClasses} pl-10`}
                placeholder="+1234567890"
                required
              />
            </div>
            <p className="mt-1 text-xs text-gray-400">Your phone number with country code for notifications</p>
          </div>

          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            type="submit"
            disabled={isLoading}
            className="w-full py-3 px-4 border border-transparent rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 font-medium transition-colors duration-300"
          >
            {isLoading ? 'Setting up...' : 'Start Monitoring'}
          </motion.button>
        </form>

        {formSubmitted && response && (
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="mt-8 p-6 bg-gray-700 rounded-xl border border-gray-600"
          >
            <h3 className="text-xl font-semibold text-green-400 mb-2">Success!</h3>
            <p className="text-gray-300 mb-4">{response}</p>
            <p className="text-blue-400 font-medium">Email monitoring has begun! Check your WhatsApp for updates.</p>
          </motion.div>
        )}

        {!formSubmitted && response && (
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="mt-8 p-6 bg-gray-700 rounded-xl border border-gray-600"
          >
            <h3 className="text-xl font-semibold text-red-400 mb-2">Error</h3>
            <p className="text-gray-300">{response}</p>
          </motion.div>
        )}
      </motion.div>
    </div>
  );
};

export default EmailMonitoringForm;

