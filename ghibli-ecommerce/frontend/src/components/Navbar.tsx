import React from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { ShoppingCart, User, LogOut, Heart } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { useAuth } from '../contexts/AuthContext'
import { useCart } from '../contexts/CartContext'

const Navbar: React.FC = () => {
  const { user, logout } = useAuth()
  const { getCartItemCount } = useCart()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/')
  }

  return (
    <nav className="bg-gradient-to-r from-purple-600 via-blue-600 to-pink-600 shadow-lg sticky top-0 z-50">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center py-4">
          <Link to="/" className="flex items-center space-x-2">
            <Heart className="h-8 w-8 text-white" />
            <span className="text-2xl font-bold text-white">Ghibli Closet</span>
          </Link>

          <div className="hidden md:flex items-center space-x-6">
            <Link to="/" className="text-white hover:text-pink-200 transition-colors font-medium">
              Home
            </Link>
            <Link to="/products" className="text-white hover:text-pink-200 transition-colors font-medium">
              Products
            </Link>
            <Link to="/about" className="text-white hover:text-pink-200 transition-colors font-medium">
              About Us
            </Link>
            <Link to="/contact" className="text-white hover:text-pink-200 transition-colors font-medium">
              Contact
            </Link>
          </div>

          <div className="flex items-center space-x-4">
            <Link to="/cart" className="relative">
              <Button variant="ghost" size="sm" className="text-white hover:text-pink-200 hover:bg-white/10">
                <ShoppingCart className="h-5 w-5" />
                {getCartItemCount() > 0 && (
                  <span className="absolute -top-2 -right-2 bg-pink-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">
                    {getCartItemCount()}
                  </span>
                )}
              </Button>
            </Link>

            {user ? (
              <div className="flex items-center space-x-2">
                <span className="text-white text-sm">Hello, {user.username}!</span>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={handleLogout}
                  className="text-white hover:text-pink-200 hover:bg-white/10"
                >
                  <LogOut className="h-4 w-4" />
                </Button>
              </div>
            ) : (
              <div className="flex items-center space-x-2">
                <Link to="/login">
                  <Button variant="ghost" size="sm" className="text-white hover:text-pink-200 hover:bg-white/10">
                    <User className="h-4 w-4 mr-1" />
                    Login
                  </Button>
                </Link>
                <Link to="/register">
                  <Button size="sm" className="bg-white text-purple-600 hover:bg-pink-100">
                    Sign Up
                  </Button>
                </Link>
              </div>
            )}
          </div>
        </div>
      </div>
    </nav>
  )
}

export default Navbar
