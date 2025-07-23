import React, { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Trash2, Plus, Minus, ShoppingBag, ArrowLeft } from 'lucide-react'
import { useAuth } from '../contexts/AuthContext'
import { useCart } from '../contexts/CartContext'
import { useToast } from '@/hooks/use-toast'

interface CartItemWithProduct {
  id: string
  user_id: string
  product_id: string
  quantity: number
  size: string
  color: string
  added_at: string
  product?: {
    id: string
    name: string
    price: number
    image_url: string
    stock: number
  }
}

const Cart: React.FC = () => {
  const { user } = useAuth()
  const { cartItems, updateCartItem, removeFromCart, refreshCart } = useCart()
  const { toast } = useToast()
  const navigate = useNavigate()
  const [cartWithProducts, setCartWithProducts] = useState<CartItemWithProduct[]>([])
  const [isLoading, setIsLoading] = useState(true)

  const API_URL = (import.meta as any).env.VITE_API_URL || 'http://localhost:8000'

  useEffect(() => {
    const fetchProductDetails = async () => {
      if (!cartItems.length) {
        setCartWithProducts([])
        setIsLoading(false)
        return
      }

      try {
        const itemsWithProducts = await Promise.all(
          cartItems.map(async (item) => {
            try {
              const response = await fetch(`${API_URL}/api/products/${item.product_id}`)
              if (response.ok) {
                const product = await response.json()
                return { ...item, product }
              }
              return item
            } catch (error) {
              console.error('Error fetching product:', error)
              return item
            }
          })
        )
        setCartWithProducts(itemsWithProducts)
      } catch (error) {
        console.error('Error fetching cart products:', error)
      } finally {
        setIsLoading(false)
      }
    }

    fetchProductDetails()
  }, [cartItems])

  const handleUpdateQuantity = async (itemId: string, newQuantity: number) => {
    const success = await updateCartItem(itemId, newQuantity)
    if (success) {
      toast({
        title: "Cart updated",
        description: "Item quantity has been updated",
      })
    } else {
      toast({
        title: "Error",
        description: "Failed to update item quantity",
        variant: "destructive",
      })
    }
  }

  const handleRemoveItem = async (itemId: string) => {
    const success = await removeFromCart(itemId)
    if (success) {
      toast({
        title: "Item removed",
        description: "Item has been removed from your cart",
      })
    } else {
      toast({
        title: "Error",
        description: "Failed to remove item from cart",
        variant: "destructive",
      })
    }
  }

  const calculateTotal = () => {
    return cartWithProducts.reduce((total, item) => {
      return total + (item.product?.price || 0) * item.quantity
    }, 0)
  }

  if (!user) {
    return (
      <div className="text-center py-12">
        <ShoppingBag className="h-16 w-16 text-gray-400 mx-auto mb-4" />
        <h1 className="text-2xl font-bold text-gray-800 mb-4">Please Log In</h1>
        <p className="text-gray-600 mb-6">You need to be logged in to view your cart</p>
        <Link to="/login">
          <Button className="bg-purple-600 hover:bg-purple-700">
            Log In
          </Button>
        </Link>
      </div>
    )
  }

  if (isLoading) {
    return (
      <div className="space-y-6">
        <h1 className="text-3xl font-bold text-gray-800">Shopping Cart</h1>
        <div className="space-y-4">
          {[1, 2, 3].map((i) => (
            <Card key={i} className="animate-pulse">
              <CardContent className="p-6">
                <div className="flex gap-4">
                  <div className="h-20 w-20 bg-gray-200 rounded"></div>
                  <div className="flex-1 space-y-2">
                    <div className="h-4 bg-gray-200 rounded w-1/2"></div>
                    <div className="h-4 bg-gray-200 rounded w-1/4"></div>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    )
  }

  if (cartWithProducts.length === 0) {
    return (
      <div className="text-center py-12">
        <ShoppingBag className="h-16 w-16 text-gray-400 mx-auto mb-4" />
        <h1 className="text-2xl font-bold text-gray-800 mb-4">Your Cart is Empty</h1>
        <p className="text-gray-600 mb-6">Looks like you haven't added any magical items yet!</p>
        <Link to="/products">
          <Button className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700">
            Start Shopping
          </Button>
        </Link>
      </div>
    )
  }

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-gray-800">Shopping Cart</h1>
        <Button
          variant="ghost"
          onClick={() => navigate('/products')}
        >
          <ArrowLeft className="mr-2 h-4 w-4" />
          Continue Shopping
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-4">
          {cartWithProducts.map((item) => (
            <Card key={item.id} className="overflow-hidden">
              <CardContent className="p-6">
                <div className="flex gap-4">
                  <div className="flex-shrink-0">
                    <img
                      src={item.product?.image_url || '/placeholder.jpg'}
                      alt={item.product?.name || 'Product'}
                      className="h-20 w-20 object-cover rounded-lg"
                    />
                  </div>
                  
                  <div className="flex-1 space-y-2">
                    <h3 className="font-semibold text-gray-800">
                      {item.product?.name || 'Unknown Product'}
                    </h3>
                    <div className="flex gap-4 text-sm text-gray-600">
                      <span>Size: {item.size}</span>
                      <span>Color: {item.color}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-lg font-bold text-purple-600">
                        ${item.product?.price || 0}
                      </span>
                      <div className="flex items-center gap-2">
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => handleUpdateQuantity(item.id, Math.max(1, item.quantity - 1))}
                          disabled={item.quantity <= 1}
                        >
                          <Minus className="h-3 w-3" />
                        </Button>
                        <span className="w-8 text-center">{item.quantity}</span>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => handleUpdateQuantity(item.id, item.quantity + 1)}
                          disabled={item.quantity >= (item.product?.stock || 0)}
                        >
                          <Plus className="h-3 w-3" />
                        </Button>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => handleRemoveItem(item.id)}
                          className="text-red-600 hover:text-red-700 hover:bg-red-50"
                        >
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </div>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        <div className="lg:col-span-1">
          <Card className="sticky top-4">
            <CardHeader>
              <CardTitle>Order Summary</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span>Subtotal</span>
                  <span>${calculateTotal().toFixed(2)}</span>
                </div>
                <div className="flex justify-between">
                  <span>Shipping</span>
                  <span>Free</span>
                </div>
                <div className="border-t pt-2">
                  <div className="flex justify-between font-bold text-lg">
                    <span>Total</span>
                    <span className="text-purple-600">${calculateTotal().toFixed(2)}</span>
                  </div>
                </div>
              </div>
              
              <Button className="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white">
                Proceed to Checkout
              </Button>
              
              <div className="text-center">
                <Link to="/products" className="text-sm text-purple-600 hover:text-purple-700">
                  Continue Shopping
                </Link>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}

export default Cart
