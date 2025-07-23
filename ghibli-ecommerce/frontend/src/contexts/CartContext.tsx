import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react'
import { useAuth } from './AuthContext'

interface CartItem {
  id: string
  user_id: string
  product_id: string
  quantity: number
  size: string
  color: string
  added_at: string
}


interface CartContextType {
  cartItems: CartItem[]
  addToCart: (productId: string, quantity: number, size: string, color: string) => Promise<boolean>
  updateCartItem: (itemId: string, quantity: number) => Promise<boolean>
  removeFromCart: (itemId: string) => Promise<boolean>
  getCartTotal: () => number
  getCartItemCount: () => number
  refreshCart: () => Promise<void>
}

const CartContext = createContext<CartContextType | undefined>(undefined)

export const useCart = () => {
  const context = useContext(CartContext)
  if (context === undefined) {
    throw new Error('useCart must be used within a CartProvider')
  }
  return context
}

interface CartProviderProps {
  children: ReactNode
}

export const CartProvider: React.FC<CartProviderProps> = ({ children }) => {
  const [cartItems, setCartItems] = useState<CartItem[]>([])
  const { token } = useAuth()
  const API_URL = (import.meta as any).env.VITE_API_URL || 'http://localhost:8000'

  const refreshCart = async () => {
    if (!token) {
      setCartItems([])
      return
    }

    try {
      const response = await fetch(`${API_URL}/api/cart`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      })

      if (response.ok) {
        const data = await response.json()
        setCartItems(data)
      }
    } catch (error) {
      console.error('Error fetching cart:', error)
    }
  }

  useEffect(() => {
    refreshCart()
  }, [token])

  const addToCart = async (productId: string, quantity: number, size: string, color: string): Promise<boolean> => {
    if (!token) return false

    try {
      const response = await fetch(`${API_URL}/api/cart`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          product_id: productId,
          quantity,
          size,
          color,
        }),
      })

      if (response.ok) {
        await refreshCart()
        return true
      }
      return false
    } catch (error) {
      console.error('Error adding to cart:', error)
      return false
    }
  }

  const updateCartItem = async (itemId: string, quantity: number): Promise<boolean> => {
    if (!token) return false

    try {
      const response = await fetch(`${API_URL}/api/cart/${itemId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ quantity }),
      })

      if (response.ok) {
        await refreshCart()
        return true
      }
      return false
    } catch (error) {
      console.error('Error updating cart item:', error)
      return false
    }
  }

  const removeFromCart = async (itemId: string): Promise<boolean> => {
    if (!token) return false

    try {
      const response = await fetch(`${API_URL}/api/cart/${itemId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      })

      if (response.ok) {
        await refreshCart()
        return true
      }
      return false
    } catch (error) {
      console.error('Error removing from cart:', error)
      return false
    }
  }

  const getCartTotal = (): number => {
    return cartItems.reduce((total, item) => total + (item.quantity * 0), 0)
  }

  const getCartItemCount = (): number => {
    return cartItems.reduce((total, item) => total + item.quantity, 0)
  }

  const value = {
    cartItems,
    addToCart,
    updateCartItem,
    removeFromCart,
    getCartTotal,
    getCartItemCount,
    refreshCart,
  }

  return <CartContext.Provider value={value}>{children}</CartContext.Provider>
}
