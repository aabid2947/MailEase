import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import Smail from '../assets/smail.png'
import { Bars3Icon, XMarkIcon } from '@heroicons/react/24/outline'

export default function Header() {
  const [isMenuOpen, setIsMenuOpen] = useState(false)

  const navItems = [
    { name: 'Home', href: '/' },
    { name: 'Monitor Email', href: '/monitor-email' },
    { name: 'Delete Email', href: '/delete-email' }

   
  ]

  return (
    <header className=" shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center py-4">
          <div className="flex items-center">
            <Link to="/">
            <img src={Smail} alt="Smail Logo" className="h-20 w-auto" />
           </Link>
          </div>
          
          <nav className="hidden md:flex space-x-8">
            {navItems.map((item) => (
              <Link
                key={item.name}
                to={item.href}
                className="text-gray-300 font-bold hover:bg-gray-100 hover:text-blue-600 px-3 py-2 rounded-md text-lg "
              >
                {item.name}
              </Link>
            ))}
          </nav>

          <div className="hidden md:flex items-center space-x-4">
          <Link to="/authenticate">
            <button className="bg-purple-600 text-white hover:bg-blue-700 px-4 py-2 rounded-md text-lg font-bold transition duration-150 ease-in-out">
              Authenticate
            </button>
           </Link>
          </div>

          <div className="md:hidden flex items-center">
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="text-gray-300 hover:text-white focus:outline-none focus:text-white"
            >
              {isMenuOpen ? (
                <XMarkIcon className="h-6 w-6" aria-hidden="true" />
              ) : (
                <Bars3Icon className="h-6 w-6" aria-hidden="true" />
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile menu, show/hide based on menu state */}
      {isMenuOpen && (
        <div className="md:hidden">
          <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
            {navItems.map((item) => (
              <Link
                key={item.name}
                to={item.href}
                className="text-gray-300 hover:bg-gray-700 hover:text-blue block px-3 py-2 rounded-md text-base font-medium"
              >
                {item.name}
              </Link>
            ))}
          </div>
          <div className="pt-4 pb-3 border-t border-gray-700">
            
            <div className="mt-3 px-2 space-y-1">
              <Link to='/authenticate'>
              <button className="block w-full text-left px-3 py-2 rounded-md text-base font-medium bg-blue-600 text-white hover:bg-blue-700">
                Authenticate
              </button>
              </Link>
            </div>
          </div>
        </div>
      )}
    </header>
  )
}

