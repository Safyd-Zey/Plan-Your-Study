import React, { useState, useEffect } from 'react';
import { parse, format } from 'date-fns';
import { useDataStore } from '@/store';
import { Plus, Trash2, Edit2, Clock, ChevronDown, ChevronUp, Users } from 'lucide-react';
import apiClient from '@/api';
import { useAuthStore } from '@/store';

const DAY_NAMES = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];

interface CourseScheduleSlot {
  id: number;
  course_id: number;
  day_of_week: number;
  start_time: string;
  end_time: string;
  room?: string;
}

interface UserItem {
  id: number;
  username: string;
  email: string;
  role: 'user' | 'admin';
}

export default function CoursesPage() {
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({ name: '', description: '', instructor: '' });
  const [editingId, setEditingId] = useState<number | null>(null);
  const [expandedScheduleCourseId, setExpandedScheduleCourseId] = useState<number | null>(null);
  const [expandedMembersCourseId, setExpandedMembersCourseId] = useState<number | null>(null);
  const [scheduleSlots, setScheduleSlots] = useState<Record<number, CourseScheduleSlot[]>>({});
  const [courseMembers, setCourseMembers] = useState<Record<number, UserItem[]>>({});
  const [allUsers, setAllUsers] = useState<UserItem[]>([]);
  const [selectedUserByCourse, setSelectedUserByCourse] = useState<Record<number, number>>({});
  const [memberSearchByCourse, setMemberSearchByCourse] = useState<Record<number, string>>({});
  const [newSlot, setNewSlot] = useState({ day_of_week: 0, start_time: '', end_time: '', room: '' });
  const [addingSlotFor, setAddingSlotFor] = useState<number | null>(null);

  const { user } = useAuthStore();
  const {
    courses,
    fetchCourses,
    addCourse,
    updateCourse,
    deleteCourse,
    fetchCourseMembers,
    addCourseMember,
    removeCourseMember,
    isLoading,
  } = useDataStore();
  const isAdmin = user?.role === 'admin';

  useEffect(() => {
    fetchCourses();
  }, []);

  useEffect(() => {
    const fetchUsers = async () => {
      if (!isAdmin) return;
      try {
        const res = await apiClient.get('/auth/users');
        setAllUsers((res.data || []).filter((u: UserItem) => u.role === 'user'));
      } catch (e) {
        console.error(e);
      }
    };
    fetchUsers();
  }, [isAdmin]);

  const fetchSlots = async (courseId: number) => {
    try {
      const res = await apiClient.get(`/courses/${courseId}/schedules`);
      setScheduleSlots((prev) => ({ ...prev, [courseId]: res.data }));
    } catch (e) {
      console.error(e);
    }
  };

  const toggleSchedule = (courseId: number) => {
    if (expandedScheduleCourseId === courseId) {
      setExpandedScheduleCourseId(null);
      setAddingSlotFor(null);
      return;
    }
    setExpandedScheduleCourseId(courseId);
    fetchSlots(courseId);
    setAddingSlotFor(null);
  };

  const toggleMembers = (courseId: number) => {
    if (expandedMembersCourseId === courseId) {
      setExpandedMembersCourseId(null);
      return;
    }
    setExpandedMembersCourseId(courseId);
    fetchMembers(courseId);
  };

  const fetchMembers = async (courseId: number) => {
    try {
      const members = await fetchCourseMembers(courseId);
      setCourseMembers((prev) => ({ ...prev, [courseId]: members as UserItem[] }));
    } catch (e) {
      console.error(e);
    }
  };

  const handleAddMember = async (courseId: number) => {
    const selectedUserId = selectedUserByCourse[courseId];
    if (!selectedUserId) return;
    try {
      await addCourseMember(courseId, selectedUserId);
      setSelectedUserByCourse((prev) => ({ ...prev, [courseId]: 0 }));
      await fetchMembers(courseId);
    } catch (e) {
      console.error(e);
    }
  };

  const handleRemoveMember = async (courseId: number, userId: number) => {
    try {
      await removeCourseMember(courseId, userId);
      await fetchMembers(courseId);
    } catch (e) {
      console.error(e);
    }
  };

  const handleAddSlot = async (courseId: number) => {
    try {
      await apiClient.post(`/courses/${courseId}/schedules`, {
        day_of_week: newSlot.day_of_week,
        start_time: newSlot.start_time,
        end_time: newSlot.end_time,
        room: newSlot.room || null,
      });
      setNewSlot({ day_of_week: 0, start_time: '', end_time: '', room: '' });
      setAddingSlotFor(null);
      fetchSlots(courseId);
    } catch (e) {
      console.error(e);
    }
  };

  const handleDeleteSlot = async (courseId: number, slotId: number) => {
    try {
      await apiClient.delete(`/courses/${courseId}/schedules/${slotId}`);
      fetchSlots(courseId);
    } catch (e) {
      console.error(e);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (editingId) {
        await updateCourse(editingId, formData);
        setEditingId(null);
      } else {
        await addCourse(formData);
      }
      setFormData({ name: '', description: '', instructor: '' });
      setShowForm(false);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const handleEdit = (course: any) => {
    setFormData({
      name: course.name,
      description: course.description || '',
      instructor: course.instructor || '',
    });
    setEditingId(course.id);
    setShowForm(true);
  };

  const handleCancel = () => {
    setShowForm(false);
    setEditingId(null);
    setFormData({ name: '', description: '', instructor: '' });
  };

  const getFilteredUsers = (courseId: number) => {
    const query = (memberSearchByCourse[courseId] || '').trim().toLowerCase();
    const terms = query.split(/\s+/).filter(Boolean);

    return allUsers
      .filter((u) => !(courseMembers[courseId] || []).some((m) => m.id === u.id))
      .filter((u) => {
        if (terms.length === 0) return true;
        const haystack = `${u.username} ${u.email}`.toLowerCase();
        return terms.every((term) => haystack.includes(term));
      });
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">My Courses</h1>
          {isAdmin && (
            <button
              onClick={() => setShowForm(true)}
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
            >
              <Plus size={20} />
              New Course
            </button>
          )}
        </div>

        {/* Form */}
        {showForm && isAdmin && (
          <div className="bg-white rounded-lg shadow p-6 mb-8">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">
              {editingId ? 'Edit Course' : 'Add New Course'}
            </h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Course Name *</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  placeholder="e.g., Mathematics 101"
                  required
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
                <textarea
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  placeholder="Course description"
                  rows={3}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                ></textarea>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Instructor</label>
                <input
                  type="text"
                  value={formData.instructor}
                  onChange={(e) => setFormData({ ...formData, instructor: e.target.value })}
                  placeholder="e.g., Dr. John Smith"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div className="flex gap-3">
                <button
                  type="submit"
                  disabled={isLoading}
                  className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition disabled:bg-gray-400"
                >
                  {isLoading ? 'Saving...' : editingId ? 'Update Course' : 'Add Course'}
                </button>
                <button
                  type="button"
                  onClick={handleCancel}
                  className="px-6 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 transition"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        )}

        {/* Courses Grid */}
        {isLoading && courses.length === 0 ? (
          <div className="flex items-center justify-center min-h-96">
            <div className="text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
              <p className="text-gray-600">Loading courses...</p>
            </div>
          </div>
        ) : courses.length === 0 ? (
          <div className="bg-white rounded-lg shadow p-12 text-center">
            <p className="text-gray-600 text-lg">No courses yet. Create your first course to get started!</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {courses.map((course) => (
              <div key={course.id} className="bg-white rounded-2xl shadow border border-gray-100 hover:shadow-lg transition p-6">
                <div className="flex items-start justify-between gap-3 mb-2">
                  <h3 className="text-lg font-bold text-gray-900">{course.name}</h3>
                  {isAdmin && (
                    <span className="px-2 py-1 rounded-full text-xs font-semibold bg-orange-100 text-orange-700">ADMIN COURSE</span>
                  )}
                </div>
                {course.instructor && (
                  <p className="text-sm text-gray-600 mb-3">👨‍🏫 {course.instructor}</p>
                )}
                {course.description && (
                  <p className="text-gray-700 text-sm mb-4 line-clamp-2">{course.description}</p>
                )}
                {isAdmin && (
                  <div className="flex gap-2 justify-end mb-3">
                    <button
                      onClick={() => handleEdit(course)}
                      className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition"
                    >
                      <Edit2 size={18} />
                    </button>
                    <button
                      onClick={() => deleteCourse(course.id)}
                      className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition"
                    >
                      <Trash2 size={18} />
                    </button>
                  </div>
                )}

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 mt-3">
                  <button
                    onClick={() => toggleSchedule(course.id)}
                    className="flex items-center justify-between px-3 py-2 rounded-lg border border-teal-200 bg-teal-50 text-teal-700 text-sm font-medium"
                  >
                    <span className="flex items-center gap-2"><Clock size={14} /> Schedule</span>
                    {expandedScheduleCourseId === course.id ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
                  </button>

                  {isAdmin && (
                    <button
                      onClick={() => toggleMembers(course.id)}
                      className="flex items-center justify-between px-3 py-2 rounded-lg border border-blue-200 bg-blue-50 text-blue-700 text-sm font-medium"
                    >
                      <span className="flex items-center gap-2"><Users size={14} /> Members</span>
                      {expandedMembersCourseId === course.id ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
                    </button>
                  )}
                </div>

                {expandedScheduleCourseId === course.id && (
                  <div className="mt-3 space-y-2">
                    {(scheduleSlots[course.id] || []).length === 0 && (
                      <p className="text-xs text-gray-500">No schedule set.</p>
                    )}
                    {(scheduleSlots[course.id] || []).map((slot) => (
                      <div key={slot.id} className="flex items-center justify-between bg-teal-50 rounded px-3 py-2 text-sm">
                        <span className="font-medium text-teal-800">{DAY_NAMES[slot.day_of_week]}</span>
                        <span className="text-gray-700">{
                          format(parse(slot.start_time, 'HH:mm', new Date()), 'HH:mm')
                        } – {
                          format(parse(slot.end_time, 'HH:mm', new Date()), 'HH:mm')
                        }</span>
                        {slot.room && <span className="text-gray-500 text-xs">{slot.room}</span>}
                        {isAdmin && (
                          <button
                            onClick={() => handleDeleteSlot(course.id, slot.id)}
                            className="text-red-500 hover:text-red-700 ml-2"
                          >
                            <Trash2 size={14} />
                          </button>
                        )}
                      </div>
                    ))}

                    {isAdmin && addingSlotFor === course.id ? (
                      <div className="mt-2 space-y-2 bg-gray-50 rounded p-3">
                        <select
                          value={newSlot.day_of_week}
                          onChange={(e) => setNewSlot({ ...newSlot, day_of_week: Number(e.target.value) })}
                          className="w-full border border-gray-300 rounded px-2 py-1 text-sm"
                        >
                          {DAY_NAMES.map((d, i) => (
                            <option key={i} value={i}>{d}</option>
                          ))}
                        </select>
                        <div className="flex gap-2">
                          <input
                            type="time"
                            value={newSlot.start_time}
                            onChange={(e) => setNewSlot({ ...newSlot, start_time: e.target.value })}
                            className="flex-1 border border-gray-300 rounded px-2 py-1 text-sm"
                          />
                          <input
                            type="time"
                            value={newSlot.end_time}
                            onChange={(e) => setNewSlot({ ...newSlot, end_time: e.target.value })}
                            className="flex-1 border border-gray-300 rounded px-2 py-1 text-sm"
                          />
                        </div>
                        <input
                          type="text"
                          placeholder="Room (optional)"
                          value={newSlot.room}
                          onChange={(e) => setNewSlot({ ...newSlot, room: e.target.value })}
                          className="w-full border border-gray-300 rounded px-2 py-1 text-sm"
                        />
                        <div className="flex gap-2">
                          <button
                            onClick={() => handleAddSlot(course.id)}
                            disabled={!newSlot.start_time || !newSlot.end_time}
                            className="px-3 py-1 bg-teal-600 text-white rounded text-sm hover:bg-teal-700 disabled:bg-gray-300 transition"
                          >
                            Save
                          </button>
                          <button
                            onClick={() => setAddingSlotFor(null)}
                            className="px-3 py-1 bg-gray-200 text-gray-700 rounded text-sm hover:bg-gray-300 transition"
                          >
                            Cancel
                          </button>
                        </div>
                      </div>
                    ) : isAdmin ? (
                      <button
                        onClick={() => setAddingSlotFor(course.id)}
                        className="mt-1 flex items-center gap-1 text-xs text-teal-700 hover:underline"
                      >
                        <Plus size={12} /> Add time slot
                      </button>
                    ) : null}
                  </div>
                )}

                {isAdmin && expandedMembersCourseId === course.id && (
                  <div className="mt-4 border-t border-gray-200 pt-3">
                    <p className="text-sm font-semibold text-gray-800 mb-2">Course Members</p>
                    <div className="space-y-2 mb-3">
                      {(courseMembers[course.id] || []).map((member) => (
                        <div key={member.id} className="flex items-center justify-between bg-gray-50 rounded px-3 py-2 text-sm">
                          <span className="text-gray-800">{member.username} ({member.email})</span>
                          <button
                            onClick={() => handleRemoveMember(course.id, member.id)}
                            className="text-red-500 hover:text-red-700"
                          >
                            <Trash2 size={14} />
                          </button>
                        </div>
                      ))}
                      {(courseMembers[course.id] || []).length === 0 && (
                        <p className="text-xs text-gray-500">No enrolled users yet.</p>
                      )}
                    </div>

                    <div className="space-y-2 min-w-0">
                      <input
                        type="text"
                        value={memberSearchByCourse[course.id] || ''}
                        onChange={(e) => setMemberSearchByCourse((prev) => ({
                          ...prev,
                          [course.id]: e.target.value,
                        }))}
                        placeholder="Search user by username or email..."
                        className="w-full border border-gray-300 rounded px-3 py-2 text-sm"
                      />

                      <div className="border border-gray-300 rounded-lg bg-white max-h-44 overflow-y-auto">
                        {getFilteredUsers(course.id).length === 0 ? (
                          <p className="px-3 py-2 text-xs text-gray-500">No users found</p>
                        ) : (
                          getFilteredUsers(course.id).map((u) => (
                            <button
                              key={u.id}
                              type="button"
                              onClick={() => setSelectedUserByCourse((prev) => ({ ...prev, [course.id]: u.id }))}
                              className={`w-full text-left px-3 py-2 text-sm border-b last:border-b-0 transition ${
                                (selectedUserByCourse[course.id] || 0) === u.id
                                  ? 'bg-blue-50 text-blue-700'
                                  : 'hover:bg-gray-50 text-gray-800'
                              }`}
                            >
                              <p className="font-medium truncate">{u.username}</p>
                              <p className="text-xs text-gray-500 truncate">{u.email}</p>
                            </button>
                          ))
                        )}
                      </div>

                      <div className="flex justify-end">
                        <button
                          onClick={() => handleAddMember(course.id)}
                          disabled={!selectedUserByCourse[course.id]}
                          className="px-3 py-1 bg-blue-600 text-white rounded text-sm hover:bg-blue-700 disabled:bg-gray-300 transition"
                        >
                          Add Selected User
                        </button>
                      </div>
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
