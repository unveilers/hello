import React from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Heart, Star, Users, Sparkles } from 'lucide-react'

const About: React.FC = () => {
  return (
    <div className="space-y-12">
      <section className="text-center py-16 bg-gradient-to-r from-purple-100 via-pink-100 to-blue-100 rounded-3xl">
        <div className="max-w-4xl mx-auto px-4">
          <h1 className="text-5xl font-bold text-gray-800 mb-6">
            About <span className="text-purple-600">Ghibli Closet</span>
          </h1>
          <p className="text-xl text-gray-600 leading-relaxed">
            Where magic meets fashion, and every piece tells a story from the enchanting world of Studio Ghibli.
          </p>
        </div>
      </section>

      <section className="max-w-4xl mx-auto space-y-8">
        <div className="text-center">
          <h2 className="text-3xl font-bold text-gray-800 mb-4">Our Story</h2>
          <p className="text-lg text-gray-600 leading-relaxed">
            Born from a deep love for Studio Ghibli's timeless stories and characters, Ghibli Closet was created 
            to bring the magic of these beloved films into your everyday wardrobe. We believe that clothing should 
            be more than just fabric – it should be a way to express your connection to the stories and characters 
            that inspire you.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <Card className="border-0 shadow-lg">
            <CardHeader>
              <div className="flex items-center gap-3">
                <div className="bg-purple-100 rounded-full p-2">
                  <Heart className="h-6 w-6 text-purple-600" />
                </div>
                <CardTitle className="text-xl">Our Mission</CardTitle>
              </div>
            </CardHeader>
            <CardContent>
              <p className="text-gray-600">
                To create high-quality, ethically-made clothing that celebrates the wonder, imagination, 
                and environmental consciousness found in Studio Ghibli films. Every piece is designed 
                with love and attention to detail.
              </p>
            </CardContent>
          </Card>

          <Card className="border-0 shadow-lg">
            <CardHeader>
              <div className="flex items-center gap-3">
                <div className="bg-pink-100 rounded-full p-2">
                  <Sparkles className="h-6 w-6 text-pink-600" />
                </div>
                <CardTitle className="text-xl">Our Vision</CardTitle>
              </div>
            </CardHeader>
            <CardContent>
              <p className="text-gray-600">
                To build a community of dreamers and nature lovers who share our passion for Studio Ghibli's 
                timeless messages of friendship, courage, and respect for the natural world.
              </p>
            </CardContent>
          </Card>
        </div>

        <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-2xl p-8">
          <h3 className="text-2xl font-bold text-gray-800 mb-6 text-center">What Makes Us Special</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="bg-blue-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <Star className="h-8 w-8 text-blue-600" />
              </div>
              <h4 className="font-semibold text-gray-800 mb-2">Authentic Designs</h4>
              <p className="text-gray-600 text-sm">
                Every design is carefully crafted to capture the essence and spirit of beloved Ghibli characters
              </p>
            </div>
            <div className="text-center">
              <div className="bg-green-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <Heart className="h-8 w-8 text-green-600" />
              </div>
              <h4 className="font-semibold text-gray-800 mb-2">Sustainable Materials</h4>
              <p className="text-gray-600 text-sm">
                We use eco-friendly materials and ethical manufacturing processes, honoring Ghibli's environmental values
              </p>
            </div>
            <div className="text-center">
              <div className="bg-purple-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <Users className="h-8 w-8 text-purple-600" />
              </div>
              <h4 className="font-semibold text-gray-800 mb-2">Community Driven</h4>
              <p className="text-gray-600 text-sm">
                Built by fans, for fans – we listen to our community and create what you want to wear
              </p>
            </div>
          </div>
        </div>

        <div className="text-center space-y-6">
          <h3 className="text-2xl font-bold text-gray-800">Our Favorite Characters</h3>
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
            {[
              { name: 'Totoro', color: 'bg-green-100 text-green-700' },
              { name: 'Chihiro', color: 'bg-blue-100 text-blue-700' },
              { name: 'Howl', color: 'bg-purple-100 text-purple-700' },
              { name: 'Kiki', color: 'bg-pink-100 text-pink-700' },
              { name: 'Ponyo', color: 'bg-orange-100 text-orange-700' },
            ].map((character) => (
              <div key={character.name} className={`${character.color} rounded-full py-2 px-4 text-sm font-medium`}>
                {character.name}
              </div>
            ))}
          </div>
        </div>

        <div className="bg-gradient-to-r from-purple-600 to-pink-600 rounded-2xl p-8 text-white text-center">
          <h3 className="text-2xl font-bold mb-4">Join Our Magical Journey</h3>
          <p className="text-lg opacity-90 mb-6">
            Every purchase supports independent artists and helps us create more magical designs. 
            Thank you for being part of our story!
          </p>
          <div className="flex justify-center">
            <Heart className="h-8 w-8" />
          </div>
        </div>
      </section>
    </div>
  )
}

export default About
