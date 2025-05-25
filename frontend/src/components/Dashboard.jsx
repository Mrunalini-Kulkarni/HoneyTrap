/* eslint-disable react-hooks/exhaustive-deps */
/* eslint-disable no-unused-vars */
import React, { useState, useEffect } from 'react';
import { Activity, AlertTriangle, Eye, Server, Globe, Clock, Filter, Bug, Crosshair, Zap, Target } from 'lucide-react';
import { PieChart, Pie, Cell, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const HoneyTrapDashboard = () => {
  const [logs, setLogs] = useState([]);
  const [filteredLogs, setFilteredLogs] = useState([]);
  const [selectedService, setSelectedService] = useState('all');
  const [stats, setStats] = useState({
    totalConnections: 0,
    uniqueIPs: 0,
    alerts: 0,
    activeThreats: 0
  });
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activityData, setActivityData] = useState([]);
  const [pieData, setPieData] = useState([]);

  // API Base URL - adjust if your backend runs on different host/port
  const API_BASE_URL = 'http://127.0.0.1:5000';

  // Fetch logs from backend
  const fetchLogs = async (serviceFilter = null) => {
    try {
      const params = serviceFilter && serviceFilter !== 'all' 
        ? `?service=${serviceFilter}` 
        : '';
      const response = await fetch(`${API_BASE_URL}/api/logs${params}`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error fetching logs:', error);
      throw error;
    }
  };

  // Fetch stats from backend
  const fetchStats = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/stats`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error fetching stats:', error);
      throw error;
    }
  };

  // Load data from backend
  const loadData = async () => {
    try {
      setIsLoading(true);
      setError(null);
      
      // Fetch both logs and stats
      const [logsData, statsData] = await Promise.all([
        fetchLogs(selectedService === 'all' ? null : selectedService),
        fetchStats()
      ]);
      
      setLogs(logsData);
      setStats(statsData);
      
      // Process chart data
      const { pieChartData, last24Hours } = processChartData(logsData);
      setPieData(pieChartData);
      setActivityData(last24Hours);
      
    } catch (err) {
      console.error('Error loading data:', err);
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  // Initial load and polling setup
  useEffect(() => {
    loadData();
    
    // Set up polling for real-time updates every 5 seconds
    const interval = setInterval(loadData, 5000);
    return () => clearInterval(interval);
  }, []);

  // Filter logs based on selected service
  useEffect(() => {
    if (selectedService === 'all') {
      setFilteredLogs(logs);
    } else {
      setFilteredLogs(logs.filter(log => log.service === selectedService));
    }
  }, [logs, selectedService]);

  // Process data for charts
  const processChartData = (logs) => {
    // Process pie chart data (attacks by service)
    const serviceAttacks = logs.reduce((acc, log) => {
      const service = log.service || 'Unknown';
      acc[service] = (acc[service] || 0) + 1;
      return acc;
    }, {});

    const pieChartData = Object.entries(serviceAttacks).map(([service, count]) => ({
      name: service,
      value: count,
      color: service === 'SSH' ? '#60A5FA' : service === 'HTTP' ? '#34D399' : service === 'FTP' ? '#FBBF24' : '#A78BFA'
    }));

    // Process line chart data (activity over time - last 24 hours by hour)
    const now = new Date();
    const last24Hours = [];
    
    for (let i = 23; i >= 0; i--) {
      const hourAgo = new Date(now.getTime() - (i * 60 * 60 * 1000));
      const hourKey = hourAgo.getHours();
      const hourLabel = hourAgo.toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        hour12: false 
      });
      
      const connectionsInHour = logs.filter(log => {
        const logTime = new Date(log.timestamp);
        return logTime.getHours() === hourKey && 
               logTime.toDateString() === hourAgo.toDateString();
      }).length;

      last24Hours.push({
        time: hourLabel,
        connections: connectionsInHour,
        fullTime: hourAgo.toLocaleTimeString('en-US', { 
          hour: '2-digit', 
          minute: '2-digit',
          hour12: true 
        })
      });
    }

    return { pieChartData, last24Hours };
  };
  
  // Handle service filter change
  const handleServiceFilterChange = (newService) => {
    setSelectedService(newService);
    // Immediately fetch data with new filter
    fetchLogs(newService === 'all' ? null : newService)
      .then(data => {
        setLogs(data);
        const { pieChartData, last24Hours } = processChartData(data);
        setPieData(pieChartData);
        setActivityData(last24Hours);
      })
      .catch(err => setError(err.message));
  };

  const StatCard = ({ icon: Icon, title, value, trend, color }) => (
    <div className="bg-gray-800/60 border border-gray-600/40 rounded-lg p-6 hover:border-blue-400/60 transition-all duration-300 group backdrop-blur-sm">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-gray-400 text-sm font-medium">{title}</p>
          <p className="text-2xl font-bold text-white mt-1">{value}</p>
          {trend && (
            <p className={`text-sm mt-1 ${trend > 0 ? 'text-red-400' : 'text-emerald-400'}`}>
              {trend > 0 ? '↑' : '↓'} {Math.abs(trend)}% from last hour
            </p>
          )}
        </div>
        <div className={`p-3 rounded-lg ${color} group-hover:scale-110 transition-transform duration-300`}>
          <Icon className="w-6 h-6 text-white" />
        </div>
      </div>
    </div>
  );

  const LogEntry = ({ log, index }) => (
    <div 
      className="bg-gray-800/40 border border-gray-600/30 rounded-lg p-4 hover:border-blue-400/50 transition-all duration-300 backdrop-blur-sm"
      style={{ 
        animation: `fadeIn 0.5s ease-in-out ${index * 0.1}s both`
      }}
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <div className={`w-3 h-3 rounded-full ${
            log.alert 
              ? 'bg-red-400 animate-pulse shadow-lg shadow-red-400/50' 
              : log.service === 'SSH' 
                ? 'bg-blue-400 shadow-lg shadow-blue-400/50' 
                : log.service === 'HTTP' 
                  ? 'bg-emerald-400 shadow-lg shadow-emerald-400/50' 
                  : 'bg-amber-400 shadow-lg shadow-amber-400/50'
          }`}></div>
          <div>
            <p className="text-white font-medium">{log.source_ip}</p>
            <p className="text-gray-300 text-sm">
              {log.service} - {log.protocol} 
              {log.destination_ip && ` → ${log.destination_ip}`}
            </p>
          </div>
        </div>
        <div className="text-right">
          <p className="text-gray-200 text-sm">
            {new Date(log.timestamp).toLocaleString()}
          </p>
          {log.alert && (
            <p className="text-red-400 text-xs mt-1 flex items-center justify-end">
              <AlertTriangle className="w-3 h-3 mr-1" />
              {log.alert}
            </p>
          )}
          {log.length && (
            <p className="text-gray-400 text-xs">
              {log.length} bytes
            </p>
          )}
        </div>
      </div>
    </div>
  );

  // Connection status indicator
  const getConnectionStatus = () => {
    if (error) {
      return { color: 'text-red-400', text: 'Connection Error', dot: 'bg-red-400' };
    }
    if (isLoading) {
      return { color: 'text-amber-400', text: 'Connecting...', dot: 'bg-amber-400' };
    }
    return { color: 'text-emerald-400', text: 'Live Monitoring', dot: 'bg-emerald-400' };
  };

  const status = getConnectionStatus();

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      {/* Background Effects */}
      <div className="fixed inset-0 bg-gradient-to-br from-gray-900 via-slate-800 to-blue-950"></div>
      <div 
        className="fixed inset-0 opacity-30"
        style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%2306b6d4' fill-opacity='0.03'%3E%3Ccircle cx='30' cy='30' r='1'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`
        }}
      ></div>
      
      <div className="relative z-10">
        {/* Header */}
        <header className="border-b border-gray-700/50 bg-gray-800/40 backdrop-blur-md">
          <div className="max-w-7xl mx-auto px-6 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-4">
                <div className="relative p-3 bg-gradient-to-br from-blue-500 via-blue-600 to-cyan-500 rounded-xl shadow-2xl shadow-blue-500/30">
                  <div className="absolute inset-0 bg-gradient-to-br from-blue-400 via-blue-500 to-cyan-400 rounded-xl blur opacity-75 animate-pulse"></div>
                  <div className="relative flex items-center justify-center">
                    {/* Trap Icon - Bear trap style with targeting elements */}
                    <svg className="w-8 h-8" viewBox="0 0 32 32" fill="none">
                      {/* Trap base */}
                      <ellipse cx="16" cy="20" rx="12" ry="3" fill="white" fillOpacity="0.8"/>
                      
                      {/* Trap jaws */}
                      <path d="M6 16 Q16 8 26 16 L24 18 Q16 12 8 18 Z" fill="white" fillOpacity="0.9"/>
                      <path d="M6 16 Q16 24 26 16 L24 14 Q16 20 8 14 Z" fill="white" fillOpacity="0.9"/>
                      
                      {/* Trap teeth */}
                      <path d="M8 16 L10 14 L10 18 M12 16 L14 14 L14 18 M18 16 L20 14 L20 18 M22 16 L24 14 L24 18" 
                            stroke="white" strokeWidth="1" strokeLinecap="round"/>
                      
                      {/* Central targeting crosshair */}
                      <circle cx="16" cy="16" r="4" stroke="white" strokeWidth="1.5" fill="none" opacity="0.7"/>
                      <path d="M16 12 L16 20 M12 16 L20 16" stroke="white" strokeWidth="1.5" strokeLinecap="round" opacity="0.8"/>
                      <circle cx="16" cy="16" r="1" fill="white"/>
                      
                      {/* Danger indicators */}
                      <circle cx="16" cy="8" r="1" fill="white" opacity="0.6">
                        <animate attributeName="opacity" values="0.6;1;0.6" dur="2s" repeatCount="indefinite"/>
                      </circle>
                      <circle cx="8" cy="12" r="0.8" fill="white" opacity="0.5">
                        <animate attributeName="opacity" values="0.5;0.9;0.5" dur="2.5s" repeatCount="indefinite"/>
                      </circle>
                      <circle cx="24" cy="12" r="0.8" fill="white" opacity="0.5">
                        <animate attributeName="opacity" values="0.5;0.9;0.5" dur="1.8s" repeatCount="indefinite"/>
                      </circle>
                    </svg>
                    {/* Pulse rings */}
                    <div className="absolute inset-0 rounded-xl border-2 border-white/20 animate-ping"></div>
                    <div className="absolute inset-0 rounded-xl border border-white/10 animate-pulse"></div>
                  </div>
                </div>
                <div>
                  <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-400 via-cyan-400 to-blue-500 bg-clip-text text-transparent tracking-wide">
                    🍯 HoneyTrap
                  </h1>
                  <p className="text-gray-400 text-sm font-medium">Advanced Threat Intelligence Platform</p>
                </div>
              </div>

              <div className="flex items-center space-x-4">
                <div className={`flex items-center space-x-2 ${status.color}`}>
                  <div className={`w-2 h-2 ${status.dot} rounded-full ${!error ? 'animate-pulse' : ''}`}></div>
                  <span className="text-sm">{status.text}</span>
                </div>
                <div className="text-gray-400 text-sm">
                  <Clock className="w-4 h-4 inline mr-1" />
                  {new Date().toLocaleTimeString()}
                </div>
              </div>
            </div>
          </div>
        </header>

        <main className="max-w-7xl mx-auto px-6 py-8">
          {/* Error Alert */}
          {error && (
            <div className="bg-red-900/20 border border-red-500/50 rounded-lg p-4 mb-6 backdrop-blur-sm">
              <div className="flex items-center space-x-2">
                <AlertTriangle className="w-5 h-5 text-red-400" />
                <div>
                  <p className="text-red-400 font-medium">Connection Error</p>
                  <p className="text-gray-400 text-sm">
                    Failed to connect to backend: {error}
                  </p>
                  <p className="text-gray-500 text-xs mt-1">
                    Make sure your Flask server is running on http://127.0.0.1:5000
                  </p>
                </div>
              </div>
            </div>
          )}

          <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
            {/* Left Column - Main Content (2/3 width) */}
            <div className="xl:col-span-2 space-y-8">
              {/* Stats Grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <StatCard
                  icon={Activity}
                  title="Total Connections"
                  value={stats.totalConnections}
                  color="bg-gradient-to-r from-blue-500 to-cyan-500"
                />
                <StatCard
                  icon={Globe}
                  title="Unique IPs"
                  value={stats.uniqueIPs}
                  color="bg-gradient-to-r from-emerald-500 to-teal-500"
                />
                <StatCard
                  icon={AlertTriangle}
                  title="Security Alerts"
                  value={stats.alerts}
                  color="bg-gradient-to-r from-red-500 to-pink-500"
                />
                <StatCard
                  icon={Eye}
                  title="Active Threats"
                  value={stats.activeThreats}
                  color="bg-gradient-to-r from-blue-600 to-indigo-500"
                />
              </div>

              {/* Services Status */}
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {['SSH', 'HTTP', 'FTP'].map((service, index) => {
                  const serviceConnections = logs.filter(log => log.service === service).length;
                  const colors = {
                    SSH: 'from-blue-500 to-cyan-500',
                    HTTP: 'from-emerald-500 to-teal-500',
                    FTP: 'from-blue-600 to-indigo-500'
                  };
                  return (
                    <div key={service} className="bg-gray-800/60 border border-gray-600/40 rounded-lg p-6 hover:border-blue-400/60 transition-all duration-300 backdrop-blur-sm">
                      <div className="flex items-center justify-between mb-4">
                        <div className="flex items-center space-x-3">
                          <div className={`p-2 bg-gradient-to-r ${colors[service]} rounded-lg`}>
                            <Server className="w-4 h-4 text-white" />
                          </div>
                          <h3 className="text-lg font-semibold text-white">{service} Honeypot</h3>
                        </div>
                        <div className="flex items-center space-x-2">
                          <div className="w-2 h-2 bg-emerald-400 rounded-full animate-pulse"></div>
                          <span className="text-emerald-400 text-sm">Active</span>
                        </div>
                      </div>
                      <div className="space-y-2">
                        <div className="flex justify-between text-sm">
                          <span className="text-gray-400">Port:</span>
                          <span className="text-white">
                            {service === 'SSH' ? '2222' : service === 'HTTP' ? '8080' : '2121'}
                          </span>
                        </div>
                        <div className="flex justify-between text-sm">
                          <span className="text-gray-400">Connections:</span>
                          <span className="text-white">{serviceConnections}</span>
                        </div>
                        <div className="flex justify-between text-sm">
                          <span className="text-gray-400">Status:</span>
                          <span className="text-emerald-400">Listening</span>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>

              {/* Activity Log */}
              <div className="bg-gray-800/60 border border-gray-600/40 rounded-lg backdrop-blur-sm">
                <div className="border-b border-gray-600/40 p-6">
                  <div className="flex items-center justify-between">
                    <h2 className="text-xl font-semibold text-white flex items-center">
                      <Activity className="w-5 h-5 mr-2 text-cyan-400" />
                      Recent Activity
                    </h2>

                    <div className="flex items-center space-x-4">
                      <div className="flex items-center space-x-2">
                        <Filter className="w-4 h-4 text-gray-400" />
                        <select
                          value={selectedService}
                          onChange={(e) => handleServiceFilterChange(e.target.value)}
                          className="bg-gray-700/60 border border-gray-500/40 rounded-md px-3 py-1 text-white text-sm focus:outline-none focus:border-blue-400 backdrop-blur-sm"
                        >
                          <option value="all">All Services</option>
                          <option value="SSH">SSH</option>
                          <option value="HTTP">HTTP</option>
                          <option value="FTP">FTP</option>
                        </select>
                      </div>

                      {isLoading && (
                        <div className="flex items-center space-x-2 text-cyan-400">
                          <div className="w-4 h-4 border-2 border-cyan-400 border-t-transparent rounded-full animate-spin"></div>
                          <span className="text-sm">Loading...</span>
                        </div>
                      )}
                    </div>
                  </div>
                </div>

                <div className="p-6">
                  {filteredLogs.length === 0 ? (
                    <div className="text-center py-12">
                      <Eye className="w-12 h-12 text-gray-500 mx-auto mb-4" />
                      <p className="text-gray-400">
                        {error ? 'Unable to load activity data' : 'No activity detected yet'}
                      </p>
                      <p className="text-gray-500 text-sm mt-1">
                        {error 
                          ? 'Check your backend connection' 
                          : 'Honeypots are actively monitoring for threats'
                        }
                      </p>
                    </div>
                  ) : (
                    <div className="space-y-4 max-h-96 overflow-y-auto">
                      {filteredLogs
                        .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))
                        .map((log, index) => (
                          <LogEntry key={`${log.timestamp}-${log.source_ip}-${index}`} log={log} index={index} />
                        ))
                      }
                    </div>
                  )}
                </div>
              </div>
            </div>

            {/* Right Column - Charts (1/3 width) */}
            <div className="xl:col-span-1 space-y-6">
              {/* Attack Distribution Pie Chart */}
              <div className="bg-gray-800/60 border border-gray-600/40 rounded-lg p-6 backdrop-blur-sm">
                <h3 className="text-lg font-semibold text-white mb-4 flex items-center">
                  <div className="w-3 h-3 bg-gradient-to-r from-blue-400 to-cyan-400 rounded-full mr-2"></div>
                  Attack Distribution
                </h3>
                <div className="h-80">
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie
                        data={pieData}
                        cx="50%"
                        cy="50%"
                        outerRadius={80}
                        fill="#8884d8"
                        dataKey="value"
                        label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                        labelLine={false}
                      >
                        {pieData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={entry.color} />
                        ))}
                      </Pie>
                      <Tooltip 
                        contentStyle={{
                          backgroundColor: '#1F2937',
                          border: '1px solid #4B5563',
                          borderRadius: '8px',
                          color: '#fff'
                        }}
                      />
                    </PieChart>
                  </ResponsiveContainer>
                </div>
                <div className="mt-4 space-y-2">
                  {pieData.map((entry, index) => (
                    <div key={index} className="flex items-center justify-between text-sm">
                      <div className="flex items-center space-x-2">
                        <div 
                          className="w-3 h-3 rounded-full" 
                          style={{ backgroundColor: entry.color }}
                        ></div>
                        <span className="text-gray-300">{entry.name}</span>
                      </div>
                      <span className="text-white font-medium">{entry.value}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Activity Timeline */}
              <div className="bg-gray-800/60 border border-gray-600/40 rounded-lg p-6 backdrop-blur-sm">
                <h3 className="text-lg font-semibold text-white mb-4 flex items-center">
                  <div className="w-3 h-3 bg-gradient-to-r from-cyan-400 to-blue-400 rounded-full mr-2"></div>
                  Activity Timeline
                </h3>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={activityData}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#4B5563" />
                      <XAxis 
                        dataKey="time" 
                        stroke="#9CA3AF"
                        fontSize={12}
                        tick={{ fill: '#9CA3AF' }}
                      />
                      <YAxis 
                        stroke="#9CA3AF"
                        fontSize={12}
                        tick={{ fill: '#9CA3B8' }}
                      />
                      <Tooltip
                        contentStyle={{
                          backgroundColor: '#1E293B',
                          border: '1px solid #475569',
                          borderRadius: '8px',
                          color: '#fff'
                        }}
                        labelFormatter={(value) => `Time: ${value}`}
                        formatter={(value) => [value, 'Connections']}
                      />
                      <Line 
                        type="monotone" 
                        dataKey="connections" 
                        stroke="#3B82F6" 
                        strokeWidth={3}
                        dot={{ fill: '#3B82F6', strokeWidth: 2, r: 4 }}
                        activeDot={{ r: 6, stroke: '#3B82F6', strokeWidth: 2, fill: '#fff' }}
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
                <div className="mt-4 text-center">
                  <p className="text-gray-400 text-xs">Last 24 hours activity</p>
                  <p className="text-white text-sm font-medium">
                    Total: {activityData.reduce((sum, item) => sum + item.connections, 0)} connections
                  </p>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>

      <style jsx>{`
        @keyframes fadeIn {
          from {
            opacity: 0;
            transform: translateY(10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
      `}</style>
    </div>
  );
};

export default HoneyTrapDashboard;