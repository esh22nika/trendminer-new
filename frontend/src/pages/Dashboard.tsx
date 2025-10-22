import { motion } from "motion/react";
import { TrendCard } from "../components/TrendCard";
import { Card } from "../components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "../components/ui/tabs";
import { Sparkles, Clock, Star, Filter } from "lucide-react";
import { Button } from "../components/ui/button";

export function Dashboard() {
  const personalizedTrends = [
    {
      topic: "AI Image Generation Tools",
      platform: "YouTube",
      likes: 234000,
      dislikes: 8900,
      shares: 45600,
      comments: 34500,
      sentiment: "positive" as const,
      trend: "rising" as const,
      relevanceScore: 95,
      tags: ["AI", "Creative", "Technology"],
      platformColor: "#FF0000",
    },
    {
      topic: "React 19 Features Discussion",
      platform: "Reddit",
      likes: 89000,
      dislikes: 3200,
      shares: 12400,
      comments: 23100,
      sentiment: "positive" as const,
      trend: "rising" as const,
      relevanceScore: 92,
      tags: ["React", "Web Dev", "JavaScript"],
      platformColor: "#FF4500",
    },
    {
      topic: "Climate Tech Innovations",
      platform: "Twitter",
      likes: 156000,
      dislikes: 12300,
      shares: 67800,
      comments: 45200,
      sentiment: "neutral" as const,
      trend: "stable" as const,
      relevanceScore: 88,
      tags: ["Climate", "Technology", "Innovation"],
      platformColor: "#1DA1F2",
    },
    {
      topic: "Machine Learning Frameworks",
      platform: "Google",
      likes: 45200,
      dislikes: 2100,
      shares: 8900,
      comments: 12300,
      sentiment: "positive" as const,
      trend: "rising" as const,
      relevanceScore: 85,
      tags: ["ML", "AI", "Development"],
      platformColor: "#4285F4",
    },
    {
      topic: "Cryptocurrency Market Analysis",
      platform: "Twitter",
      likes: 201000,
      dislikes: 45600,
      shares: 89000,
      comments: 67800,
      sentiment: "negative" as const,
      trend: "falling" as const,
      relevanceScore: 78,
      tags: ["Crypto", "Finance", "Trading"],
      platformColor: "#1DA1F2",
    },
    {
      topic: "Space Exploration Updates",
      platform: "YouTube",
      likes: 345000,
      dislikes: 6700,
      shares: 78900,
      comments: 56700,
      sentiment: "positive" as const,
      trend: "rising" as const,
      relevanceScore: 82,
      tags: ["Space", "Science", "NASA"],
      platformColor: "#FF0000",
    },
  ];

  const userInterests = [
    { name: "AI & Machine Learning", count: 245, color: "#8B5CF6" },
    { name: "Web Development", count: 189, color: "#3B82F6" },
    { name: "Climate & Environment", count: 156, color: "#10B981" },
    { name: "Space & Science", count: 134, color: "#F59E0B" },
    { name: "Cryptocurrency", count: 98, color: "#EF4444" },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 relative overflow-hidden">
      {/* Animated background elements */}
      <div className="absolute top-20 right-10 w-72 h-72 bg-gradient-to-br from-yellow-300 to-orange-300 opacity-20 rounded-full blur-3xl animate-pulse" />
      <div className="absolute bottom-20 left-10 w-96 h-96 bg-gradient-to-br from-cyan-300 to-blue-300 opacity-20 rounded-full blur-3xl" />
      
      <div className="max-w-7xl mx-auto px-6 py-8 relative z-10">
        {/* Header */}
        <motion.div
          className="mb-8"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <h1 className="mb-2 text-slate-900">Your Personalized Dashboard</h1>
          <p className="text-xl text-slate-600">
            Discover trends tailored to your interests
          </p>
        </motion.div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          {[
            { label: "Trends Tracked", value: "1,247", icon: Sparkles, color: "blue" },
            { label: "Active Topics", value: "342", icon: Star, color: "purple" },
            { label: "Updates Today", value: "89", icon: Clock, color: "green" },
            { label: "Relevance Score", value: "92%", icon: Filter, color: "pink" },
          ].map((stat, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
            >
              <Card className="bg-gradient-to-br from-white to-slate-50 border-2 p-6 shadow-lg hover:shadow-xl transition-all group" style={{
                borderColor: `var(--${stat.color}-400)`
              }}>
                <div className="flex items-center justify-between mb-2">
                  <div className={`p-2 rounded-lg bg-gradient-to-br from-${stat.color}-400 to-${stat.color}-500 shadow-md`}>
                    <stat.icon className="w-5 h-5 text-white" />
                  </div>
                  <span className={`text-2xl bg-gradient-to-br from-${stat.color}-600 to-${stat.color}-500 bg-clip-text text-transparent`}>
                    {stat.value}
                  </span>
                </div>
                <p className="text-sm text-slate-600">{stat.label}</p>
              </Card>
            </motion.div>
          ))}
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Trends Feed */}
          <div className="lg:col-span-2">
            <Tabs defaultValue="foryou" className="w-full">
              <TabsList className="bg-white border border-slate-200 mb-6">
                <TabsTrigger value="foryou">For You</TabsTrigger>
                <TabsTrigger value="trending">Trending</TabsTrigger>
                <TabsTrigger value="following">Following</TabsTrigger>
              </TabsList>

              <TabsContent value="foryou" className="space-y-4">
                {personalizedTrends.map((trend, index) => (
                  <TrendCard key={index} {...trend} />
                ))}
              </TabsContent>

              <TabsContent value="trending" className="space-y-4">
                {personalizedTrends
                  .filter((t) => t.trend === "rising")
                  .map((trend, index) => (
                    <TrendCard key={index} {...trend} />
                  ))}
              </TabsContent>

              <TabsContent value="following" className="space-y-4">
                <div className="text-center py-12 text-slate-500">
                  <p>Follow topics to see them here</p>
                </div>
              </TabsContent>
            </Tabs>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Your Interests */}
            <Card className="bg-white border-slate-200 p-6 shadow-md">
              <h3 className="text-slate-900 mb-4">Your Interests</h3>
              <div className="space-y-3">
                {userInterests.map((interest, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.1 }}
                  >
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-sm text-slate-700">{interest.name}</span>
                      <span className="text-xs px-2 py-0.5 rounded-full text-white shadow-sm" style={{ backgroundColor: interest.color }}>
                        {interest.count}
                      </span>
                    </div>
                    <div className="h-2 bg-gradient-to-r from-slate-100 to-slate-200 rounded-full overflow-hidden shadow-inner">
                      <motion.div
                        className="h-full rounded-full shadow-sm"
                        style={{ 
                          background: `linear-gradient(90deg, ${interest.color}, ${interest.color}dd)`
                        }}
                        initial={{ width: 0 }}
                        animate={{ width: `${(interest.count / 245) * 100}%` }}
                        transition={{ duration: 1, delay: 0.3 + index * 0.1 }}
                      />
                    </div>
                  </motion.div>
                ))}
              </div>
              <Button variant="outline" className="w-full mt-4 border-slate-300 text-slate-700">
                Manage Interests
              </Button>
            </Card>

            {/* Quick Actions */}
            <Card className="bg-white border-slate-200 p-6 shadow-md">
              <h3 className="text-slate-900 mb-4">Quick Actions</h3>
              <div className="space-y-2">
                <Button
                  variant="outline"
                  className="w-full justify-start border-slate-300 text-slate-700"
                >
                  <Sparkles className="w-4 h-4 mr-2" />
                  Discover New Topics
                </Button>
                <Button
                  variant="outline"
                  className="w-full justify-start border-slate-300 text-slate-700"
                >
                  <Filter className="w-4 h-4 mr-2" />
                  Refine Preferences
                </Button>
              </div>
            </Card>

            {/* Platform Distribution */}
            <Card className="bg-white border-slate-200 p-6 shadow-md">
              <h3 className="text-slate-900 mb-4">Platform Distribution</h3>
              <div className="space-y-2">
                {[
                  { name: "YouTube", percentage: 35, color: "#FF0000" },
                  { name: "Twitter", percentage: 28, color: "#1DA1F2" },
                  { name: "Reddit", percentage: 22, color: "#FF4500" },
                  { name: "Google", percentage: 15, color: "#4285F4" },
                ].map((platform, index) => (
                  <div key={index}>
                    <div className="flex items-center justify-between mb-1 text-sm">
                      <span className="text-slate-700">{platform.name}</span>
                      <span className="text-slate-500">{platform.percentage}%</span>
                    </div>
                    <div className="h-2 bg-slate-200 rounded-full overflow-hidden">
                      <motion.div
                        className="h-full"
                        style={{ backgroundColor: platform.color }}
                        initial={{ width: 0 }}
                        animate={{ width: `${platform.percentage}%` }}
                        transition={{ duration: 1, delay: 0.5 + index * 0.1 }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}
