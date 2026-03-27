import React, { useEffect, useState } from 'react';
import apiClient from '@/api';
import { TrendingUp, CheckCircle, Clock, AlertCircle } from 'lucide-react';

interface ProgressStats {
  total_assignments: number;
  completed_assignments: number;
  in_progress_assignments: number;
  not_started_assignments: number;
  completion_percentage: number;
  upcoming_deadlines: any[];
}

export default function ProgressPage() {
  const [stats, setStats] = useState<ProgressStats | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await apiClient.get('/progress/stats');
        setStats(response.data);
      } catch (error) {
        console.error('Error fetching stats:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchStats();
  }, []);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading progress...</p>
        </div>
      </div>
    );
  }

  if (!stats) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <p className="text-gray-600">Failed to load progress data</p>
      </div>
    );
  }

  const getMotivationalMessage = (percentage: number) => {
    if (percentage === 100) return '🎉 Outstanding! You\'ve completed all assignments!';
    if (percentage >= 75) return '🌟 Great progress! Keep it up!';
    if (percentage >= 50) return '💪 You\'re doing well! Stay focused!';
    if (percentage >= 25) return '📈 Good start! More to go!';
    return '🚀 Get started and make progress!';
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 flex items-center gap-2">
            <TrendingUp size={32} className="text-blue-600" />
            Your Progress
          </h1>
          <p className="text-gray-600 mt-2">{getMotivationalMessage(stats.completion_percentage)}</p>
        </div>

        {/* Main Progress Circle */}
        <div className="bg-white rounded-lg shadow p-8 mb-8">
          <div className="flex flex-col md:flex-row items-center gap-8">
            {/* Circle Chart */}
            <div className="flex-shrink-0">
              <div className="relative w-40 h-40">
                <svg className="w-full h-full transform -rotate-90" viewBox="0 0 160 160">
                  <circle
                    cx="80"
                    cy="80"
                    r="70"
                    stroke="#e5e7eb"
                    strokeWidth="8"
                    fill="none"
                  />
                  <circle
                    cx="80"
                    cy="80"
                    r="70"
                    stroke="#3b82f6"
                    strokeWidth="8"
                    fill="none"
                    strokeDasharray={`${(stats.completion_percentage / 100) * 440} 440`}
                    className="transition-all duration-500"
                  />
                </svg>
                <div className="absolute inset-0 flex items-center justify-center">
                  <div className="text-center">
                    <div className="text-4xl font-bold text-blue-600">{Math.round(stats.completion_percentage)}%</div>
                    <p className="text-gray-600 text-sm mt-1">Complete</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Stats Details */}
            <div className="flex-1 space-y-4">
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="flex items-center gap-2 text-gray-700">
                    <CheckCircle size={20} className="text-green-600" />
                    Completed
                  </span>
                  <span className="text-2xl font-bold text-green-600">{stats.completed_assignments}/{stats.total_assignments}</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-3">
                  <div
                    className="bg-green-600 h-3 rounded-full transition-all duration-300"
                    style={{
                      width: `${stats.total_assignments > 0 ? (stats.completed_assignments / stats.total_assignments) * 100 : 0}%`,
                    }}
                  ></div>
                </div>
              </div>

              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="flex items-center gap-2 text-gray-700">
                    <Clock size={20} className="text-blue-600" />
                    In Progress
                  </span>
                  <span className="text-2xl font-bold text-blue-600">{stats.in_progress_assignments}</span>
                </div>
              </div>

              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="flex items-center gap-2 text-gray-700">
                    <AlertCircle size={20} className="text-gray-600" />
                    Not Started
                  </span>
                  <span className="text-2xl font-bold text-gray-600">{stats.not_started_assignments}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Upcoming Deadlines */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Upcoming Deadlines</h2>
          {stats.upcoming_deadlines.length > 0 ? (
            <div className="space-y-3">
              {stats.upcoming_deadlines.map((assignment, index) => (
                <div key={assignment.id} className="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition">
                  <div className="flex-1">
                    <div className="flex items-center gap-2">
                      <div className="w-2 h-2 rounded-full bg-blue-600"></div>
                      <p className="font-medium text-gray-900">{assignment.title}</p>
                    </div>
                    <p className="text-sm text-gray-600 mt-1 ml-4">
                      {new Date(assignment.deadline).toLocaleDateString('en-US', {
                        weekday: 'short',
                        year: 'numeric',
                        month: 'short',
                        day: 'numeric',
                      })}
                    </p>
                  </div>
                  <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                    assignment.priority === 'high'
                      ? 'bg-red-100 text-red-800'
                      : assignment.priority === 'medium'
                      ? 'bg-yellow-100 text-yellow-800'
                      : 'bg-green-100 text-green-800'
                  }`}>
                    {assignment.priority} priority
                  </span>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-500 text-center py-8">No upcoming deadlines</p>
          )}
        </div>
      </div>
    </div>
  );
}
