import { motion } from "motion/react";
import { Card } from "../components/ui/card";
import { Badge } from "../components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "../components/ui/tabs";
import { Network, GitBranch, TrendingUp, ArrowRight } from "lucide-react";
import { Progress } from "../components/ui/progress";
import { useState } from "react";

export function PatternMining() {
  const [selectedRule, setSelectedRule] = useState<number | null>(null);

  const associationRules = [
    {
      antecedent: ["AI Tools", "Machine Learning"],
      consequent: ["Python Development"],
      support: 0.35,
      confidence: 0.85,
      lift: 3.2,
      platforms: ["Reddit", "Twitter"],
    },
    {
      antecedent: ["Climate Change"],
      consequent: ["Renewable Energy", "Policy"],
      support: 0.28,
      confidence: 0.78,
      lift: 2.8,
      platforms: ["Google", "YouTube"],
    },
    {
      antecedent: ["Web Development", "React"],
      consequent: ["TypeScript"],
      support: 0.42,
      confidence: 0.92,
      lift: 4.1,
      platforms: ["Reddit", "YouTube"],
    },
    {
      antecedent: ["Cryptocurrency"],
      consequent: ["Blockchain", "NFTs"],
      support: 0.31,
      confidence: 0.71,
      lift: 2.5,
      platforms: ["Twitter", "Reddit"],
    },
    {
      antecedent: ["Space Exploration", "NASA"],
      consequent: ["Mars Mission"],
      support: 0.24,
      confidence: 0.88,
      lift: 3.6,
      platforms: ["YouTube", "Google"],
    },
  ];

  const frequentItemsets = [
    { items: ["AI", "ML", "Python"], support: 0.45, count: 2345 },
    { items: ["React", "JavaScript", "Web Dev"], support: 0.38, count: 1987 },
    { items: ["Climate", "Environment", "Sustainability"], support: 0.32, count: 1678 },
    { items: ["Crypto", "Bitcoin", "Trading"], support: 0.29, count: 1523 },
    { items: ["Space", "NASA", "Science"], support: 0.26, count: 1367 },
    { items: ["Gaming", "Esports"], support: 0.22, count: 1156 },
  ];

  const sequentialPatterns = [
    {
      sequence: ["AI Announcement", "Tutorial Videos", "Community Discussion"],
      support: 0.41,
      avgDuration: "3-5 days",
    },
    {
      sequence: ["Product Launch", "Reviews", "Comparisons"],
      support: 0.36,
      avgDuration: "1-2 weeks",
    },
    {
      sequence: ["Breaking News", "Analysis", "Opinion Pieces"],
      support: 0.52,
      avgDuration: "24-48 hours",
    },
    {
      sequence: ["Research Paper", "Explainer Content", "Debates"],
      support: 0.28,
      avgDuration: "1-3 weeks",
    },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-pink-50 to-blue-50 relative overflow-hidden">
      {/* Colorful background elements */}
      <div className="absolute top-10 left-10 w-96 h-96 bg-gradient-to-br from-pink-400 to-rose-400 opacity-20 rounded-full blur-3xl" />
      <div className="absolute bottom-10 right-10 w-80 h-80 bg-gradient-to-br from-violet-400 to-purple-400 opacity-20 rounded-full blur-3xl animate-pulse" />
      <div className="absolute top-1/2 left-1/2 w-72 h-72 bg-gradient-to-br from-blue-400 to-cyan-400 opacity-15 rounded-full blur-3xl" />
      
      <div className="max-w-7xl mx-auto px-6 py-8 relative z-10">
        {/* Header */}
        <motion.div
          className="mb-8"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <h1 className="mb-2 text-slate-900">Pattern Mining</h1>
          <p className="text-xl text-slate-600">
            Discover hidden relationships and patterns in trending topics
          </p>
        </motion.div>

        {/* Algorithm Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          {[
            { label: "Apriori Algorithm", value: "1,247 Rules", icon: Network },
            { label: "FP-Growth", value: "892 Itemsets", icon: GitBranch },
            { label: "Sequential Mining", value: "345 Patterns", icon: TrendingUp },
          ].map((stat, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
            >
              <Card className="bg-gradient-to-br from-white to-purple-50 border-2 border-purple-200 p-6 hover:border-purple-400 hover:shadow-xl transition-all shadow-lg group">
                <div className="flex items-center gap-4">
                  <div className="relative">
                    <div className="absolute inset-0 bg-purple-400 opacity-30 blur-xl rounded-xl" />
                    <div className="relative w-12 h-12 bg-gradient-to-br from-purple-500 to-pink-500 rounded-xl flex items-center justify-center shadow-lg group-hover:scale-110 transition-transform">
                      <stat.icon className="w-6 h-6 text-white" />
                    </div>
                  </div>
                  <div>
                    <div className="text-2xl bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">{stat.value}</div>
                    <div className="text-sm text-slate-600">{stat.label}</div>
                  </div>
                </div>
              </Card>
            </motion.div>
          ))}
        </div>

        {/* Main Content */}
        <Tabs defaultValue="association" className="w-full">
          <TabsList className="bg-white border border-slate-200 mb-6">
            <TabsTrigger value="association">Association Rules</TabsTrigger>
            <TabsTrigger value="frequent">Frequent Itemsets</TabsTrigger>
            <TabsTrigger value="sequential">Sequential Patterns</TabsTrigger>
          </TabsList>

          {/* Association Rules */}
          <TabsContent value="association">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Rules List */}
              <div className="space-y-4">
                {associationRules.map((rule, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.1 }}
                    onClick={() => setSelectedRule(index)}
                  >
                    <Card
                      className={`bg-white border-slate-200 p-6 cursor-pointer transition-all hover:border-purple-400 shadow-md ${
                        selectedRule === index ? "border-purple-500 shadow-lg" : ""
                      }`}
                    >
                      <div className="flex items-center gap-3 mb-4">
                        <div className="flex flex-wrap gap-2">
                          {rule.antecedent.map((item, i) => (
                            <Badge
                              key={i}
                              className="bg-gradient-to-r from-blue-500 to-cyan-500 text-white border-0 shadow-md hover:shadow-lg transition-shadow"
                            >
                              {item}
                            </Badge>
                          ))}
                        </div>
                        <ArrowRight className="w-5 h-5 text-purple-500 flex-shrink-0" />
                        <div className="flex flex-wrap gap-2">
                          {rule.consequent.map((item, i) => (
                            <Badge
                              key={i}
                              className="bg-gradient-to-r from-purple-500 to-pink-500 text-white border-0 shadow-md hover:shadow-lg transition-shadow"
                            >
                              {item}
                            </Badge>
                          ))}
                        </div>
                      </div>

                      <div className="grid grid-cols-3 gap-4 text-sm">
                        <div>
                          <div className="text-slate-500 mb-1">Support</div>
                          <div className="text-slate-900">{(rule.support * 100).toFixed(0)}%</div>
                        </div>
                        <div>
                          <div className="text-slate-500 mb-1">Confidence</div>
                          <div className="text-slate-900">{(rule.confidence * 100).toFixed(0)}%</div>
                        </div>
                        <div>
                          <div className="text-slate-500 mb-1">Lift</div>
                          <div className="text-slate-900">{rule.lift.toFixed(1)}x</div>
                        </div>
                      </div>
                    </Card>
                  </motion.div>
                ))}
              </div>

              {/* Rule Details */}
              <div className="sticky top-24">
                <Card className="bg-white border-slate-200 p-6 shadow-md">
                  {selectedRule !== null ? (
                    <>
                      <h3 className="text-slate-900 mb-4">Rule Details</h3>
                      <div className="space-y-4">
                        <div>
                          <div className="text-sm text-slate-600 mb-2">Support</div>
                          <Progress
                            value={associationRules[selectedRule].support * 100}
                            className="h-3"
                          />
                          <div className="text-xs text-slate-500 mt-1">
                            Appears in {(associationRules[selectedRule].support * 100).toFixed(1)}%
                            of transactions
                          </div>
                        </div>

                        <div>
                          <div className="text-sm text-slate-600 mb-2">Confidence</div>
                          <Progress
                            value={associationRules[selectedRule].confidence * 100}
                            className="h-3"
                          />
                          <div className="text-xs text-slate-500 mt-1">
                            {(associationRules[selectedRule].confidence * 100).toFixed(1)}%
                            probability of consequent given antecedent
                          </div>
                        </div>

                        <div>
                          <div className="text-sm text-slate-600 mb-2">Lift</div>
                          <div className="text-2xl text-slate-900 mb-1">
                            {associationRules[selectedRule].lift.toFixed(2)}x
                          </div>
                          <div className="text-xs text-slate-500">
                            {associationRules[selectedRule].lift > 1
                              ? "Strong positive correlation"
                              : "Weak or negative correlation"}
                          </div>
                        </div>

                        <div>
                          <div className="text-sm text-slate-600 mb-2">Active Platforms</div>
                          <div className="flex gap-2">
                            {associationRules[selectedRule].platforms.map((platform, i) => (
                              <Badge key={i} variant="outline" className="border-slate-300">
                                {platform}
                              </Badge>
                            ))}
                          </div>
                        </div>

                        <div className="pt-4 border-t border-slate-200">
                          <div className="text-sm text-slate-700">
                            <strong>Interpretation:</strong> When users engage with content about{" "}
                            {associationRules[selectedRule].antecedent.join(" and ")}, they are{" "}
                            {associationRules[selectedRule].lift.toFixed(1)}x more likely to also
                            engage with content about{" "}
                            {associationRules[selectedRule].consequent.join(" and ")}.
                          </div>
                        </div>
                      </div>
                    </>
                  ) : (
                    <div className="text-center py-12 text-slate-500">
                      <Network className="w-12 h-12 mx-auto mb-4 opacity-50" />
                      <p>Select a rule to view details</p>
                    </div>
                  )}
                </Card>
              </div>
            </div>
          </TabsContent>

          {/* Frequent Itemsets */}
          <TabsContent value="frequent">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {frequentItemsets.map((itemset, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: index * 0.1 }}
                >
                  <Card className="bg-white border-slate-200 p-6 hover:border-purple-300 transition-colors shadow-md">
                    <div className="flex flex-wrap gap-2 mb-4">
                      {itemset.items.map((item, i) => (
                        <Badge
                          key={i}
                          className="bg-gradient-to-r from-purple-400 to-pink-400 text-white border-0 shadow-md hover:shadow-lg transition-shadow"
                        >
                          {item}
                        </Badge>
                      ))}
                    </div>

                    <div className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <span className="text-slate-600">Support</span>
                        <span className="text-slate-900">{(itemset.support * 100).toFixed(1)}%</span>
                      </div>
                      <Progress value={itemset.support * 100} className="h-2" />

                      <div className="flex justify-between text-sm pt-2">
                        <span className="text-slate-600">Co-occurrences</span>
                        <span className="text-slate-900">{itemset.count.toLocaleString()}</span>
                      </div>
                    </div>
                  </Card>
                </motion.div>
              ))}
            </div>
          </TabsContent>

          {/* Sequential Patterns */}
          <TabsContent value="sequential">
            <div className="space-y-4">
              {sequentialPatterns.map((pattern, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                >
                  <Card className="bg-white border-slate-200 p-6 shadow-md">
                    <div className="flex items-center justify-between mb-4">
                      <h3 className="text-slate-900">Pattern {index + 1}</h3>
                      <Badge className="bg-purple-100 text-purple-700 border-purple-300">
                        {pattern.avgDuration}
                      </Badge>
                    </div>

                    <div className="flex items-center gap-4 mb-4">
                      {pattern.sequence.map((step, i) => (
                        <div key={i} className="flex items-center gap-4">
                          <div className="flex-1">
                            <div className="bg-gradient-to-r from-purple-100 to-pink-100 border border-purple-300 rounded-lg px-4 py-3 text-center">
                              <div className="text-sm text-purple-700">{step}</div>
                            </div>
                          </div>
                          {i < pattern.sequence.length - 1 && (
                            <ArrowRight className="w-5 h-5 text-slate-400 flex-shrink-0" />
                          )}
                        </div>
                      ))}
                    </div>

                    <div className="flex items-center justify-between text-sm">
                      <span className="text-slate-600">Support: {(pattern.support * 100).toFixed(1)}%</span>
                      <span className="text-slate-600">
                        Found in {Math.round(pattern.support * 5234)} trend sequences
                      </span>
                    </div>
                  </Card>
                </motion.div>
              ))}
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}
