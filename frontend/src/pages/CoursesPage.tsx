import React, { useState, useEffect } from 'react';
import { useDataStore } from '@/store';
import { Plus, Trash2, Edit2 } from 'lucide-react';

export default function CoursesPage() {
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({ name: '', description: '', instructor: '' });
  const [editingId, setEditingId] = useState<number | null>(null);

  const { courses, fetchCourses, addCourse, updateCourse, deleteCourse, isLoading } = useDataStore();

  useEffect(() => {
    fetchCourses();
  }, []);

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

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">My Courses</h1>
          <button
            onClick={() => setShowForm(true)}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
          >
            <Plus size={20} />
            New Course
          </button>
        </div>

        {/* Form */}
        {showForm && (
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
              <div key={course.id} className="bg-white rounded-lg shadow hover:shadow-lg transition p-6">
                <h3 className="text-lg font-bold text-gray-900 mb-2">{course.name}</h3>
                {course.instructor && (
                  <p className="text-sm text-gray-600 mb-3">👨‍🏫 {course.instructor}</p>
                )}
                {course.description && (
                  <p className="text-gray-700 text-sm mb-4 line-clamp-2">{course.description}</p>
                )}
                <div className="flex gap-2 justify-end">
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
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
