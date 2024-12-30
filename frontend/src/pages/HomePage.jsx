
import React, { useState, useEffect } from 'react'
import { motion, useAnimation } from 'framer-motion'
import {
  BellIcon,
  TrashIcon,
  CogIcon,
  MagnifyingGlassIcon,
  UserCircleIcon,
  ChartPieIcon,
  Squares2X2Icon,
  ClockIcon,
  InboxIcon,
  ShieldCheckIcon,
} from '@heroicons/react/24/outline';

import { Link } from 'react-router-dom'


const HomePage = () => {
  return (
    <div className="min-h-screen">
      <main className="container mx-auto px-4 py-12">
        <HeroSection />
        <FeaturesSection />
      </main>
    </div>
  )
}

const HeroSection = () => {
  return (
    <motion.section
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.8 }}
      className="text-center py-20"
    >
      <h1 className="text-5xl md:text-6xl font-bold text-white mb-6">
        <TypewriterText text="MailEase: Simplify Your Email Management" />
      </h1>
      <p className="text-xl text-gray-300 mb-8">
        Effortlessly monitor, notify, and clean up your inbox with our intelligent email assistant.
      </p>
      
      <motion.button
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        className="bg-blue-600 text-white font-semibold py-3 px-8 rounded-full text-lg shadow-lg hover:bg-blue-700 transition duration-300"
      >
        <Link to='/authenticate'>
        Get Started
        </Link>
      </motion.button>
  
    </motion.section>
  )
}

const TypewriterText = ({ text }) => {
  const [displayText, setDisplayText] = useState('')
  const [index, setIndex] = useState(0)

  useEffect(() => {
    if (index < text.length) {
      const timeout = setTimeout(() => {
        setDisplayText((prev) => prev + text[index])
        setIndex((prev) => prev + 1)
      }, 100)
      return () => clearTimeout(timeout)
    } else {
      const timeout = setTimeout(() => {
        setDisplayText('')
        setIndex(0)
      }, 2000)
      return () => clearTimeout(timeout)
    }
  }, [index, text])

  return <span>{displayText}</span>
}

const FeaturesSection = () => {
  const features = [
    {
      title: "Email Monitoring and Notifications",
      description: "Stay on top of important emails with customizable monitoring and instant WhatsApp notifications.",
      icon: <BellIcon className="h-12 w-12 text-blue-400" />,
    },
    {
      title: "Smart Email Deletion",
      description: "Effortlessly clean up your inbox by deleting old, spam, or unwanted emails based on your criteria.",
      icon: <TrashIcon className="h-12 w-12 text-blue-400" />,
    },
    {
      title: "Customizable Settings",
      description: "Tailor MailEase to your needs with flexible configuration options for both monitoring and deletion.",
      icon: <CogIcon className="h-12 w-12 text-blue-400" />,
    },
    {
      title: "Advanced Keyword Matching",
      description: "Identify important emails using advanced keyword matching in both subject and body for greater accuracy.",
      icon: <MagnifyingGlassIcon className="h-12 w-12 text-blue-400" />,
    },
    {
      title: "Sender Priority Lists",
      description: "Create a priority list of email addresses to ensure critical emails are always noticed.",
      icon: <UserCircleIcon className="h-12 w-12 text-blue-400" />,
    },
    {
      title: "Email Activity Dashboard",
      description: "View a comprehensive dashboard summarizing email activity, including received, deleted, and monitored emails.",
      icon: <ChartPieIcon className="h-12 w-12 text-blue-400" />,
    },
    {
      title: "Batch Email Processing",
      description: "Process emails in batches to clean up your inbox efficiently with just one click.",
      icon: <Squares2X2Icon className="h-12 w-12 text-blue-400" />,
    },
    {
      title: "Notification Scheduling",
      description: "Set specific times to receive notifications to avoid unnecessary disruptions.",
      icon: <ClockIcon className="h-12 w-12 text-blue-400" />,
    },
    {
      title: "Multi-Account Support",
      description: "Monitor and manage multiple email accounts from a single interface seamlessly.",
      icon: <InboxIcon className="h-12 w-12 text-blue-400" />,
    },
   
  ];
  

  return (
    <section className="py-20">
      <h2 className="text-3xl md:text-4xl font-bold text-center text-white mb-12">
        Powerful Features to Manage Your Inbox
      </h2>
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-8 max-w-6xl mx-auto">
        {features.map((feature, index) => (
          <FeatureCard key={index} {...feature} index={index} />
        ))}
      </div>
    </section>
  )
}

const FeatureCard = ({ title, description, icon, index }) => {
  const controls = useAnimation()

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: index * 0.2 }}
      className="bg-gray-800 bg-opacity-50 rounded-lg p-6 shadow-xl backdrop-blur-sm hover:cursor-pointer"
      whileHover={{
        scale: 1.05,
        rotateY: 5,
        rotateX: -5,
        y: -10,
        transition: { duration: 0.3 }
      }}
      onHoverStart={() => controls.start({ y: -10, scale: 1.05 })}
      onHoverEnd={() => controls.start({ y: 0, scale: 1 })}
    >
      <motion.div animate={controls} className="flex items-center justify-center mb-4">
        {icon}
      </motion.div>
      <h3 className="text-xl font-semibold text-white mb-2">{title}</h3>
      <p className="text-gray-300">{description}</p>
    </motion.div>
  )
}

export default HomePage

