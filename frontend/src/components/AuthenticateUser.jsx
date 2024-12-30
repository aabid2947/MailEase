'use client'

import React, { useState } from 'react'
import { AutheticateUser } from '../API/APICalls'
import { motion } from 'framer-motion'

const AuthenticateForm = () => {
    const [file, setFile] = useState(null)
    const [error, setError] = useState('')
    const [message, setMessage] = useState('')
    const [isLoading, setIsLoading] = useState(false)

    const handleFileChange = (e) => {
        const selectedFile = e.target.files[0]
        if (selectedFile) {
            setFile(selectedFile)
            setError('')
        }
    }

    const handleSubmit = async (e) => {
        e.preventDefault()
        if (!file) {
            setError('Please upload a JSON file.')
            return
        }

        const formData = new FormData()
        formData.append('file', file)

        setIsLoading(true)
        try {
            const response = await AutheticateUser(formData)
            if (response.data.message) {
                setMessage(response.data.message)
            } else {
                setError('Authentication failed: ' + response.data.error)
            }
        } catch (error) {
            setError('An error occurred during authentication.', error)
        } finally {
            setIsLoading(false)
        }
    }

    return (
        <div className=" flex items-center justify-center p-4">
            <motion.div 
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
                className="w-full max-w-2xl bg-transparent backdrop-blur-sm p-8 rounded-2xl shadow-2xl relative overflow-hidden"
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
                <div className="relative z-20">
                    <h1 className="text-4xl font-extrabold text-center mb-8 text-white tracking-tight">
                        Authenticate with Gmail
                    </h1>


                    <form onSubmit={handleSubmit} className="space-y-6">
                        <div>
                            <label htmlFor="file" className="block text-sm font-medium text-gray-200 mb-2">
                                Upload Your JSON Credentials File:
                            </label>
                            <div className="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-500 border-dashed rounded-md hover:border-blue-500 transition-colors duration-300">
                                <div className="space-y-1 text-center">
                                    <svg className="mx-auto h-12 w-12 text-gray-300" stroke="currentColor" fill="none" viewBox="0 0 48 48" aria-hidden="true">
                                        <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                                    </svg>
                                    <div className="flex text-sm text-gray-300">
                                        <label htmlFor="file" className="relative cursor-pointer bg-gray-700 bg-opacity-50 rounded-md font-medium text-blue-300 hover:text-blue-400 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-blue-500">
                                            <span>Upload a file</span>
                                            <input id="file" name="file" type="file" accept=".json" onChange={handleFileChange} className="sr-only" />
                                        </label>
                                        <p className="pl-1">or drag and drop</p>
                                    </div>
                                    <p className="text-xs text-gray-300">JSON up to 10MB</p>
                                </div>
                            </div>
                        </div>

                        {error && (
                            <motion.p 
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                className="text-red-400 bg-red-900 bg-opacity-50 p-3 rounded-md"
                            >
                                {error}
                            </motion.p>
                        )}

                        <div>
                            <motion.button
                                whileHover={{ scale: 1.05 }}
                                whileTap={{ scale: 0.95 }}
                                type="submit"
                                disabled={isLoading}
                                className="w-full py-3 px-4 border border-transparent rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 font-medium transition-colors duration-300"
                            >
                                {isLoading ? 'Authenticating...' : 'Authenticate'}
                            </motion.button>
                        </div>
                    </form>

                    {message && (
                        <motion.div 
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            className="mt-8 bg-gray-800 bg-opacity-50 p-6 rounded-xl border border-gray-600"
                        >
                            <p className="text-green-300 font-semibold mb-4">{message}</p>
                        </motion.div>
                    )}
                </div>
            </motion.div>
        </div>
    )
}

export default AuthenticateForm

