import React, { useEffect, useState } from 'react';
import apiClient from '@/api';
import { format, startOfWeek, addDays } from 'date-fns';
import { Calendar, Clock } from 'lucide-react';

interface ScheduleDay {
  date: string;
  assignments: any[];
  study_sessions: any[];
}

export default function SchedulePage() {
  const [schedule, setSchedule] = useState<ScheduleDay[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [selectedDate, setSelectedDate] = useState(new Date());

  const fetchWeeklySchedule = async () => {
    setIsLoading(true);
    try {
      const startDate = startOfWeek(selectedDate);
      const response = await apiClient.get('/schedule/weekly?start_date=' + startDate.toISOString().split('T')[0]);

      const days: ScheduleDay[] = [];
      for (let i = 0; i < 7; i++) {
        const date = addDays(startDate, i);
        days.push({
          date: format(date, 'yyyy-MM-dd'),
          assignments: [],
          study_sessions: [],
        });
      }

      // Group assignments and sessions by date
      response.data.assignments.forEach((a: any) => {
        const dateStr = new Date(a.deadline).toISOString().split('T')[0];
        const day = days.find((d) => d.date === dateStr);
        if (day) day.assignments.push(a);
      });

      response.data.study_sessions.forEach((s: any) => {
        const dateStr = new Date(s.start_time).toISOString().split('T')[0];
        const day = days.find((d) => d.date === dateStr);
        if (day) day.study_sessions.push(s);
      });

      setSchedule(days);
    } catch (error) {
      console.error('Error fetching schedule:', error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchWeeklySchedule();
  }, [selectedDate]);

  const priorityColors = {
    high: 'border-l-4 border-red-600 bg-red-50',
    medium: 'border-l-4 border-yellow-600 bg-yellow-50',
    low: 'border-l-4 border-green-600 bg-green-50',
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Weekly Schedule</h1>
          <div className="flex gap-4">
            <button
              onClick={() => setSelectedDate(addDays(selectedDate, -7))}
              className="px-4 py-2 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition"
            >
              ← Previous Week
            </button>
            <button
              onClick={() => setSelectedDate(new Date())}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
            >
              Today
            </button>
            <button
              onClick={() => setSelectedDate(addDays(selectedDate, 7))}
              className="px-4 py-2 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition"
            >
              Next Week →
            </button>
          </div>
        </div>

        {isLoading ? (
          <div className="flex items-center justify-center min-h-96">
            <div className="text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
              <p className="text-gray-600">Loading schedule...</p>
            </div>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-7 gap-4">
            {schedule.map((day) => {
              const dateObj = new Date(day.date);
              const isToday = format(dateObj, 'yyyy-MM-dd') === format(new Date(), 'yyyy-MM-dd');

              return (
                <div
                  key={day.date}
                  className={`rounded-lg p-4 min-h-96 ${isToday ? 'bg-blue-50 border-2 border-blue-600' : 'bg-white border border-gray-200'}`}
                >
                  <div className="mb-4">
                    <p className={`font-semibold ${isToday ? 'text-blue-600' : 'text-gray-900'}`}>
                      {format(dateObj, 'EEE')}
                    </p>
                    <p className="text-sm text-gray-600">{format(dateObj, 'MMM d')}</p>
                  </div>

                  {/* Assignments */}
                  <div className="space-y-2 mb-4">
                    {day.assignments.map((assignment) => (
                      <div key={assignment.id} className={`p-3 rounded-lg text-sm ${priorityColors[assignment.priority]}`}>
                        <p className="font-medium text-gray-900">{assignment.title}</p>
                        <p className="text-xs text-gray-600 mt-1">
                          {format(new Date(assignment.deadline), 'h:mm a')}
                        </p>
                      </div>
                    ))}
                  </div>

                  {/* Study Sessions */}
                  <div className="space-y-2">
                    {day.study_sessions.map((session) => (
                      <div key={session.id} className="p-3 bg-purple-50 border-l-4 border-purple-600 rounded-lg text-sm">
                        <p className="font-medium text-gray-900 flex items-center gap-2">
                          <Clock size={14} /> {session.title}
                        </p>
                        <p className="text-xs text-gray-600 mt-1">
                          {format(new Date(session.start_time), 'h:mm a')} -{' '}
                          {format(new Date(session.end_time), 'h:mm a')}
                        </p>
                      </div>
                    ))}
                  </div>

                  {day.assignments.length === 0 && day.study_sessions.length === 0 && (
                    <p className="text-gray-500 text-center text-sm py-8">No events</p>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
