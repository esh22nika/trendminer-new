import { motion } from "motion/react";
import { TrendCard } from "../components/TrendCard";
import { Card } from "../components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "../components/ui/tabs";
import { Sparkles, Clock, Star, Filter } from "lucide-react";
import { Button } from "../components/ui/button";
import { useEffect, useState } from "react";

interface DashboardSummary {
  tracked_trends_count: number;
  active_topics_count: number;
  updated_recently_count: number;
  platform_breakdown: Record<string, number>;
  top_topics: Array<{
    topic: string;
    mentions: number;
    last_updated: string;
  }>;
}

interface ForYouData {
  relevance_score: number;
  for_you: Array<any>;
  trending: Array<any>;
  following: Array<any>;
}

const platformColors: Record<string, string> = {
  Twitter: "#1DA1F2",
  YouTube: "#FF0000",
  Reddit: "#FF4500",
  Google: "#4285F4",
  Youtube: "#FF0000",
};

export function Dashboard() {
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [forYouData, setForYouData] = useState<ForYouData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [summaryRes, forYouRes] = await Promise.all([
          fetch("/api/dashboard/summary"),
          fetch("/api/dashboard/for-you?interests=ai,technology,web development,climate,space&limit=20"),
        ]);

        const summaryData = await summaryRes.json();
        const forYouDataRes = await forYouRes.json();

        setSummary(summaryData);
        setForYouData(forYouDataRes);
      } catch (error) {
        console.error("Error fetching dashboard data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const formatTrendData = (post: any) => {
    const engagement = (post.likes || 0) + (post.shares || 0) + (post.comments || 0);
    const platformColor = platformColors[post.platform] || "#4285F4";
    
    const sentiment = (post.sentiment || "neutral").toLowerCase() as "positive" | "negative" | "neutral";
    
    const relevanceScore = post.relevance_score || 0;
    const trend = relevanceScore > 70 ? "rising" : relevanceScore < 40 ? "falling" : "stable";
    
    const tags = post.hashtags 
      ? post.hashtags.split(",").map((tag: string) => tag.trim().replace("#", "")).filter((tag: string) => tag).slice(0, 3)
      : [];
    
    return {
      topic: post.topic || post.content?.substring(0, 50) || "Unknown Topic",
      platform: post.platform,
      likes: post.likes || 0,
      dislikes: 0,
      shares: post.shares || 0,
      comments: post.comments || 0,
      sentiment,
      trend: trend as "rising" | "falling" | "stable",
      relevanceScore: Math.round(relevanceScore),
      tags,
      platformColor,
    };
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-slate-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  const platformBreakdown = summary?.platform_breakdown || {};
  const totalPosts = Object.values(platformBreakdown).reduce((a, b) => a + b, 0);
  const platformDistribution = Object.entries(platformBreakdown).map(([name, count]) => ({
    name,
    percentage: totalPosts > 0 ? Math.round((count / totalPosts) * 100) : 0,
    color: platformColors[name] || "#4285F4",
  }));

  const topInterests = (summary?.top_topics || []).slice(0, 5).map((topic, index) => {
    const colors = ["#8B5CF6", "#3B82F6", "#10B981", "#F59E0B", "#EF4444"];
    return {
      name: topic.topic,
      count: topic.mentions,
      color: colors[index % colors.length],
    };
  });

  const forYouTrends = (forYouData?.for_you || []).map(formatTrendData);
  const trendingPosts = (forYouData?.trending || []).map(formatTrendData);
  const followingPosts = (forYouData?.following || []).map(formatTrendData);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 relative overflow-hidden">
      <div className="absolute top-20 right-10 w-72 h-72 bg-gradient-to-br from-yellow-300 to-orange-300 opacity-20 rounded-full blur-3xl animate-pulse" />
      <div className="absolute bottom-20 left-10 w-96 h-96 bg-gradient-to-br from-cyan-300 to-blue-300 opacity-20 rounded-full blur-3xl" />
      
      <div className="max-w-7xl mx-auto px-6 py-8 relative z-10">
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

        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          {[
            { label: "Trends Tracked", value: summary?.tracked_trends_count?.toString() || "0", icon: Sparkles, color: "blue" },
            { label: "Active Topics", value: summary?.active_topics_count?.toString() || "0", icon: Star, color: "purple" },
            { label: "Updates Today", value: summary?.updated_recently_count?.toString() || "0", icon: Clock, color: "green" },
            { label: "Relevance Score", value: `${Math.round(forYouData?.relevance_score || 0)}%`, icon: Filter, color: "pink" },
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

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2">
            <Tabs defaultValue="foryou" className="w-full">
              <TabsList className="bg-white border border-slate-200 mb-6">
                <TabsTrigger value="foryou">For You</TabsTrigger>
                <TabsTrigger value="trending">Trending</TabsTrigger>
                <TabsTrigger value="following">Following</TabsTrigger>
              </TabsList>

              <TabsContent value="foryou" className="space-y-4">
                {forYouTrends.length > 0 ? (
                  forYouTrends.map((trend, index) => (
                    <TrendCard key={index} {...trend} />
                  ))
                ) : (
                  <div className="text-center py-12 text-slate-500">
                    <p>No personalized trends available</p>
                  </div>
                )}
              </TabsContent>

              <TabsContent value="trending" className="space-y-4">
                {trendingPosts.length > 0 ? (
                  trendingPosts.map((trend, index) => (
                    <TrendCard key={index} {...trend} />
                  ))
                ) : (
                  <div className="text-center py-12 text-slate-500">
                    <p>No trending posts available</p>
                  </div>
                )}
              </TabsContent>

              <TabsContent value="following" className="space-y-4">
                {followingPosts.length > 0 ? (
                  followingPosts.map((trend, index) => (
                    <TrendCard key={index} {...trend} />
                  ))
                ) : (
                  <div className="text-center py-12 text-slate-500">
                    <p>Follow topics to see them here</p>
                  </div>
                )}
              </TabsContent>
            </Tabs>
          </div>

          <div className="space-y-6">
            <Card className="bg-white border-slate-200 p-6 shadow-md">
              <h3 className="text-slate-900 mb-4">Your Interests</h3>
              <div className="space-y-3">
                {topInterests.map((interest, index) => (
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
                        animate={{ width: `${Math.min((interest.count / (topInterests[0]?.count || 1)) * 100, 100)}%` }}
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

            <Card className="bg-white border-slate-200 p-6 shadow-md">
              <h3 className="text-slate-900 mb-4">Platform Distribution</h3>
              <div className="space-y-2">
                {platformDistribution.map((platform, index) => (
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
