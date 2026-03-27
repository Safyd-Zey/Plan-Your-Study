import React, { useState, useEffect } from 'react';
import { useDataStore } from '@/store';
import { Plus, Trash2, Edit2, ChevronDown } from 'lucide-react';
import { format } from 'date-fns';

export default function AssignmentsPage() {
  const [showForm, setShowForm] = useState(false);
  const [expandedAssignmentId, setExpandedAssignmentId] = useState<number | null>(null);
  const [newSubtaskTitle, setNewSubtaskTitle] = useState<Record<number, string>>({});
  const [editingId, setEditingId] = useState<number | null>(null);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    deadline: '',
    priority: 'medium' as const,
    course_id: 0,
  });

  const {
    courses,
    assignments,
    fetchCourses,
    fetchAssignments,
    addAssignment,
    updateAssignment,
    deleteAssignment,
    addSubtask,
    deleteSubtask,
    updateSubtask,
    isLoading,
  } = useDataStore();

  useEffect(() => {
    fetchCourses();
    fetchAssignments();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (editingId) {
        await updateAssignment(editingId, {
          ...formData,
          deadline: new Date(formData.deadline).toISOString(),
        });
        setEditingId(null);
      } else {
        if (!formData.course_id) {
          alert('Please select a course');
          return;
        }
        await addAssignment({
          ...formData,
          deadline: new Date(formData.deadline).toISOString(),
        });
      }
      setFormData({
        title: '',
        description: '',
        deadline: '',
        priority: 'medium',
        course_id: 0,
      });
      setShowForm(false);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const handleAddSubtask = async (assignmentId: number) => {
    const title = newSubtaskTitle[assignmentId];
    if (!title?.trim()) return;

    try {
      await addSubtask(assignmentId, {
        title,
        description: '',
        status: 'not_started',
      });
      setNewSubtaskTitle({ ...newSubtaskTitle, [assignmentId]: '' });
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const priorityColors = {
    high: 'bg-red-100 text-red-800',
    medium: 'bg-yellow-100 text-yellow-800',
    low: 'bg-green-100 text-green-800',
  };

  const statusBadgeColors = {
    not_started: 'bg-gray-100 text-gray-800',
    in_progress: 'bg-blue-100 text-blue-800',
    completed: 'bg-green-100 text-green-800',
  };

  const getCourseNameById = (courseId: number) => {
    return courses.find((c) => c.id === courseId)?.name || 'Unknown Course';
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Assignments</h1>
          <button
            onClick={() => setShowForm(true)}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
          >
            <Plus size={20} />
            New Assignment
          </button>
        </div>

        {/* Form */}
        {showForm && (
          <div className="bg-white rounded-lg shadow p-6 mb-8">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">
              {editingId ? 'Edit Assignment' : 'Add New Assignment'}
            </h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Course *</label>
                  <select
                    value={formData.course_id}
                    onChange={(e) => setFormData({ ...formData, course_id: Number(e.target.value) })}
                    required
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value={0}>Select a course</option>
                    {courses.map((course) => (
                      <option key={course.id} value={course.id}>
                        {course.name}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Title *</label>
                  <input
                    type="text"
                    value={formData.title}
                    onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                    placeholder="Assignment title"
                    required
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
                <textarea
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  placeholder="Assignment description"
                  rows={3}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                ></textarea>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Deadline *</label>
                  <input
                    type="datetime-local"
                    value={formData.deadline}
                    onChange={(e) => setFormData({ ...formData, deadline: e.target.value })}
                    required
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Priority</label>
                  <select
                    value={formData.priority}
                    onChange={(e) => setFormData({ ...formData, priority: e.target.value as any })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                  </select>
                </div>
              </div>

              <div className="flex gap-3">
                <button
                  type="submit"
                  disabled={isLoading}
                  className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition disabled:bg-gray-400"
                >
                  {isLoading ? 'Saving...' : editingId ? 'Update' : 'Create'}
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setShowForm(false);
                    setEditingId(null);
                    setFormData({
                      title: '',
                      description: '',
                      deadline: '',
                      priority: 'medium',
                      course_id: 0,
                    });
                  }}
                  className="px-6 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 transition"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        )}

        {/* Assignments List */}
        {isLoading && assignments.length === 0 ? (
          <div className="flex items-center justify-center min-h-96">
            <div className="text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
              <p className="text-gray-600">Loading assignments...</p>
            </div>
          </div>
        ) : assignments.length === 0 ? (
          <div className="bg-white rounded-lg shadow p-12 text-center">
            <p className="text-gray-600 text-lg">No assignments yet. Create one to get started!</p>
          </div>
        ) : (
          <div className="space-y-4">
            {assignments
              .sort((a, b) => new Date(b.deadline).getTime() - new Date(a.deadline).getTime())
              .map((assignment) => (
                <div key={assignment.id} className="bg-white rounded-lg shadow overflow-hidden">
                  <div
                    className="p-6 cursor-pointer hover:bg-gray-50 transition flex items-center justify-between"
                    onClick={() =>
                      setExpandedAssignmentId(
                        expandedAssignmentId === assignment.id ? null : assignment.id
                      )
                    }
                  >
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <h3 className="text-lg font-semibold text-gray-900">{assignment.title}</h3>
                        <span className={`px-3 py-1 rounded-full text-xs font-medium ${priorityColors[assignment.priority]}`}>
                          {assignment.priority}
                        </span>
                        <span className={`px-3 py-1 rounded-full text-xs font-medium ${statusBadgeColors[assignment.status]}`}>
                          {assignment.status.replace('_', ' ')}
                        </span>
                      </div>
                      <p className="text-sm text-gray-600">
                        📚 {getCourseNameById(assignment.course_id)} • 📅 {format(new Date(assignment.deadline), 'MMM d, yyyy h:mm a')}
                      </p>
                    </div>
                    <ChevronDown
                      size={24}
                      className={`text-gray-400 transition ${expandedAssignmentId === assignment.id ? 'rotate-180' : ''}`}
                    />
                  </div>

                  {expandedAssignmentId === assignment.id && (
                    <div className="border-t border-gray-200 p-6 bg-gray-50">
                      {assignment.description && (
                        <p className="text-gray-700 mb-4">{assignment.description}</p>
                      )}

                      {/* Subtasks */}
                      <div className="mb-6">
                        <h4 className="font-semibold text-gray-900 mb-3">Subtasks</h4>
                        {assignment.subtasks && assignment.subtasks.length > 0 ? (
                          <div className="space-y-2 mb-4">
                            {assignment.subtasks.map((subtask) => (
                              <div key={subtask.id} className="flex items-center gap-3 p-3 bg-white rounded-lg">
                                <input
                                  type="checkbox"
                                  checked={subtask.status === 'completed'}
                                  onChange={(e) =>
                                    updateSubtask(subtask.id, {
                                      status: e.target.checked ? 'completed' : 'not_started',
                                    })
                                  }
                                  className="w-4 h-4 text-blue-600"
                                />
                                <span className={subtask.status === 'completed' ? 'line-through text-gray-500' : 'text-gray-900'}>
                                  {subtask.title}
                                </span>
                                <button
                                  onClick={() => deleteSubtask(subtask.id)}
                                  className="ml-auto p-1 text-red-600 hover:bg-red-50 rounded transition"
                                >
                                  <Trash2 size={16} />
                                </button>
                              </div>
                            ))}
                          </div>
                        ) : (
                          <p className="text-gray-500 text-sm mb-4">No subtasks yet</p>
                        )}

                        <div className="flex gap-2">
                          <input
                            type="text"
                            value={newSubtaskTitle[assignment.id] || ''}
                            onChange={(e) =>
                              setNewSubtaskTitle({
                                ...newSubtaskTitle,
                                [assignment.id]: e.target.value,
                              })
                            }
                            placeholder="Add a subtask..."
                            className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
                            onKeyPress={(e) => {
                              if (e.key === 'Enter') {
                                handleAddSubtask(assignment.id);
                              }
                            }}
                          />
                          <button
                            onClick={() => handleAddSubtask(assignment.id)}
                            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition text-sm"
                          >
                            Add
                          </button>
                        </div>
                      </div>

                      {/* Action Buttons */}
                      <div className="flex gap-2 justify-end">
                        <button
                          onClick={() => deleteAssignment(assignment.id)}
                          className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition"
                        >
                          <Trash2 size={18} />
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              ))}
          </div>
        )}
      </div>
    </div>
  );
}
