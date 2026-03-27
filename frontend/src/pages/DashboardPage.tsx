import React, { useEffect } from 'react';
import { useAuthStore, useDataStore } from '@/store';
import { CheckCircle, Circle, AlertCircle } from 'lucide-react';
import { format } from 'date-fns';

export default function DashboardPage() {
  const { user } = useAuthStore();
  const { assignments, fetchAssignments, isLoading, error } = useDataStore();

  useEffect(() => {
    fetchAssignments();
  }, []);

  const completed = assignments.filter((a) => a.status === 'completed').length;
  const inProgress = assignments.filter((a) => a.status === 'in_progress').length;
  const notStarted = assignments.filter((a) => a.status === 'not_started').length;
  const total = assignments.length;
  const completionPercentage = total > 0 ? Math.round((completed / total) * 100) : 0;

  // Get upcoming assignments (sorted by deadline)
  const upcomingAssignments = assignments
    .filter((a) => a.status !== 'completed' && new Date(a.deadline) > new Date())
    .sort((a, b) => new Date(a.deadline).getTime() - new Date(b.deadline).getTime())
    .slice(0, 5);

  // Get overdue assignments
  const overdueAssignments = assignments
    .filter((a) => a.status !== 'completed' && new Date(a.deadline) <= new Date())
    .slice(0, 5);

  const priorityColors = {
    high: 'text-red-600 bg-red-50',
    medium: 'text-yellow-600 bg-yellow-50',
    low: 'text-green-600 bg-green-50',
  };

  const statusIcons = {
    not_started: <Circle size={20} className="text-gray-400" />,
    in_progress: <AlertCircle size={20} className="text-blue-600" />,
    completed: <CheckCircle size={20} className="text-green-600" />,
  };

  if (isLoading && total === 0) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading your dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Welcome Section */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900">Welcome back, {user?.username}!</h1>
          <p className="text-gray-600 mt-2">Here's your study overview</p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="text-2xl font-bold text-gray-900">{total}</div>
            <p className="text-gray-600 text-sm mt-1">Total Assignments</p>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <div className="text-2xl font-bold text-green-600">{completed}</div>
            <p className="text-gray-600 text-sm mt-1">Completed</p>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <div className="text-2xl font-bold text-blue-600">{inProgress}</div>
            <p className="text-gray-600 text-sm mt-1">In Progress</p>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <div className="text-2xl font-bold text-gray-600">{notStarted}</div>
            <p className="text-gray-600 text-sm mt-1">Not Started</p>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <div className="text-2xl font-bold text-blue-600">{completionPercentage}%</div>
            <p className="text-gray-600 text-sm mt-1">Completion</p>
          </div>
        </div>

        {/* Progress Bar */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Overall Progress</h2>
          <div className="w-full bg-gray-200 rounded-full h-4">
            <div
              className="bg-blue-600 h-4 rounded-full transition-all duration-300"
              style={{ width: `${completionPercentage}%` }}
            ></div>
          </div>
          <p className="text-sm text-gray-600 mt-2">{completionPercentage}% Complete</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Overdue Assignments */}
          {overdueAssignments.length > 0 && (
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-lg font-semibold text-red-600 mb-4 flex items-center gap-2">
                <AlertCircle size={20} />
                Overdue Assignments
              </h2>
              <div className="space-y-3">
                {overdueAssignments.map((assignment) => (
                  <div key={assignment.id} className="p-4 border border-red-200 rounded-lg bg-red-50">
                    <div className="flex items-start justify-between gap-3">
                      <div className="flex-1">
                        <p className="font-medium text-gray-900">{assignment.title}</p>
                        <p className="text-sm text-gray-600 mt-1">
                          Due: {format(new Date(assignment.deadline), 'MMM d, yyyy')}
                        </p>
                      </div>
                      <span className={`px-3 py-1 rounded-full text-xs font-medium ${priorityColors[assignment.priority]}`}>
                        {assignment.priority}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Upcoming Assignments */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Upcoming Assignments</h2>
            {upcomingAssignments.length > 0 ? (
              <div className="space-y-3">
                {upcomingAssignments.map((assignment) => (
                  <div key={assignment.id} className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition">
                    <div className="flex items-start justify-between gap-3">
                      <div className="flex-1">
                        <p className="font-medium text-gray-900">{assignment.title}</p>
                        <p className="text-sm text-gray-600 mt-1">
                          Due: {format(new Date(assignment.deadline), 'MMM d, yyyy')}
                        </p>
                      </div>
                      <span className={`px-3 py-1 rounded-full text-xs font-medium ${priorityColors[assignment.priority]}`}>
                        {assignment.priority}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-500 text-center py-8">No upcoming assignments</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
