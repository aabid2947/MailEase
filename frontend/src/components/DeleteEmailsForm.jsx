
import React, { useState } from 'react';
import { DeleteEmails } from '../API/APICalls';
import { motion } from 'framer-motion';
import { Switch } from '@headlessui/react';
import { TrashIcon, ExclamationCircleIcon } from '@heroicons/react/24/outline';

const DeleteEmailsForm = () => {
    const [criteria, setCriteria] = useState({
        age: true,
        spam: false,
        sender: false,
        subject: true,
        body: true,
        attachments: false,
        unread: false,
        specific_senders: [],
        message_threshold: 5,
    });
    const [isLoading, setIsLoading] = useState(false);
    const [result, setResult] = useState(null);

    const handleChange = (name, value) => {
        setCriteria(prev => ({
            ...prev,
            [name]: value,
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        try {
            const response = await DeleteEmails(criteria);
            setResult({ success: true, message: 'Emails deleted successfully' });
        } catch (error) {
            console.error('Error deleting emails:', error);
            setResult({ success: false, message: 'Error deleting emails' });
        } finally {
            setIsLoading(false);
        }
    };

    const formFields = [
        { name: 'age', label: 'Delete emails older than 6 months' },
        { name: 'spam', label: 'Delete emails in the Spam folder' },
        { name: 'sender', label: 'Delete emails from suspicious senders' },
        { name: 'subject', label: 'Delete emails with promotional subject keywords' },
        { name: 'body', label: 'Delete emails with promotional body content' },
        { name: 'attachments', label: 'Delete emails with large attachments (greater than 10MB)' },
        { name: 'unread', label: 'Delete unread emails' },
    ];

    return (
        <div className="min-h-screen flex items-center justify-center p-4">
            <motion.div 
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
                className="w-full max-w-2xl bg-transparent backdrop-blur-sm p-8 rounded-2xl shadow-2xl text-white relative overflow-hidden"
            >
                <motion.div
                    className="absolute top-0 left-0 w-full h-full"
                    style={{
                        background: 'linear-gradient(90deg, transparent, rgba(68, 93, 126, 0.8), transparent)',
                        backgroundSize: '200% 100%',
                    }}
                    animate={{
                        backgroundPosition: ['200% 0', '-200% 0'],
                    }}
                    transition={{
                        duration: 5,
                        repeat: Infinity,
                        ease: "easeInOut",
                    }}
                />
                <div className="relative z-10">
                    <h1 className="text-3xl font-bold text-center mb-8">Email Deletion Criteria</h1>
                    <form onSubmit={handleSubmit} className="space-y-6">
                        {formFields.map((field) => (
                            <SwitchField
                                key={field.name}
                                name={field.name}
                                label={field.label}
                                checked={criteria[field.name]}
                                onChange={handleChange}
                            />
                        ))}

                        <div>
                            <label className="block text-sm font-medium mb-1">Message Threshold:</label>
                            <input
                                type="number"
                                name="message_threshold"
                                value={criteria.message_threshold}
                                onChange={(e) => handleChange('message_threshold', e.target.value)}
                                className="mt-1 block w-full px-3 py-2 bg-transparent border border-gray-100 rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                            />
                        </div>

                        <div>
                            <label className="block text-sm font-medium mb-1">Specific Senders (comma-separated):</label>
                            <input
                                type="text"
                                name="specific_senders"
                                value={criteria.specific_senders.join(",")}
                                onChange={(e) => handleChange('specific_senders', e.target.value.split(",").map((item) => item.trim()))}
                                className="mt-1 block w-full px-3 py-2 bg-transparent border border-gray-100 rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                            />
                        </div>

                        <motion.button
                            whileHover={{ scale: 1.05 }}
                            whileTap={{ scale: 0.95 }}
                            type="submit"
                            disabled={isLoading}
                            className="w-full py-3 px-4 border border-transparent rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 font-medium transition-colors duration-300 flex items-center justify-center"
                        >
                            {isLoading ? (
                                <svg className="animate-spin h-5 w-5 mr-3 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                </svg>
                            ) : (
                                <TrashIcon className="h-5 w-5 mr-2" />
                            )}
                            {isLoading ? 'Deleting...' : 'Delete Emails'}
                        </motion.button>
                    </form>

                    {result && (
                        <motion.div 
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.5 }}
                            className={`mt-6 p-4 rounded-md ${result.success ? 'bg-green-800' : 'bg-red-800'}`}
                        >
                            <p className="flex items-center">
                                {result.success ? (
                                    <svg className="h-5 w-5 mr-2 text-green-400" fill="none" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" viewBox="0 0 24 24" stroke="currentColor">
                                        <path d="M5 13l4 4L19 7"></path>
                                    </svg>
                                ) : (
                                    <ExclamationCircleIcon className="h-5 w-5 mr-2 text-red-400" />
                                )}
                                {result.message}
                            </p>
                        </motion.div>
                    )}
                </div>
            </motion.div>
        </div>
    );
};

const SwitchField = ({ name, label, checked, onChange }) => {
    return (
        <Switch.Group>
            <div className="flex items-center justify-between">
                <Switch.Label className="mr-4">{label}</Switch.Label>
                <Switch
                    checked={checked}
                    onChange={(value) => onChange(name, value)}
                    className={`${
                        checked ? 'bg-blue-600' : 'bg-gray-600'
                    } relative inline-flex items-center h-6 rounded-full w-11 transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500`}
                >
                    <span
                        className={`${
                            checked ? 'translate-x-6' : 'translate-x-1'
                        } inline-block w-4 h-4 transform bg-white rounded-full transition-transform`}
                    />
                </Switch>
            </div>
        </Switch.Group>
    );
};

export default DeleteEmailsForm;
