import { create } from 'zustand';
import apiClient from './api';

interface User {
  id: number;
  email: string;
  username: string;
  role: 'user' | 'admin';
  created_at: string;
  updated_at: string;
}

interface Course {
  id: number;
  user_id: number;
  name: string;
  description?: string;
  instructor?: string;
  created_at: string;
  updated_at: string;
}

interface Subtask {
  id: number;
  assignment_id: number;
  title: string;
  description?: string;
  status: 'not_started' | 'in_progress' | 'completed';
  order: number;
  created_at: string;
  updated_at: string;
}

export interface Assignment {
  id: number;
  user_id: number;
  course_id: number;
  title: string;
  description?: string;
  deadline: string;
  priority: 'low' | 'medium' | 'high';
  status: 'not_started' | 'in_progress' | 'completed';
  created_at: string;
  updated_at: string;
  subtasks: Subtask[];
  course?: Course;
  user?: User;
}

interface AuthStore {
  user: User | null;
  authChecked: boolean;
  isLoading: boolean;
  error: string | null;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, username: string, password: string, role: 'user' | 'admin') => Promise<void>;
  logout: () => Promise<void>;
  initializeAuth: () => Promise<void>;
  setUser: (user: User | null) => void;
}

export interface InAppNotification {
  id: string;
  title: string;
  message: string;
  createdAt: number;
}

interface NotificationStore {
  notifications: InAppNotification[];
  pushNotification: (title: string, message: string, id?: string) => void;
  dismissNotification: (id: string) => void;
}

interface DataStore {
  courses: Course[];
  assignments: Assignment[];
  selectedCourse: Course | null;
  upcomingAssignments: Assignment[];
  overdueAssignments: Assignment[];
  calendar: Array<{ date: string; assignments: Assignment[]; study_sessions: any[] }>;
  isLoading: boolean;
  error: string | null;
  
  // Courses
  fetchCourses: () => Promise<void>;
  addCourse: (course: Omit<Course, 'id' | 'user_id' | 'created_at' | 'updated_at'>) => Promise<void>;
  updateCourse: (id: number, course: Partial<Course>) => Promise<void>;
  deleteCourse: (id: number) => Promise<void>;
  fetchCourseMembers: (courseId: number) => Promise<User[]>;
  addCourseMember: (courseId: number, userId: number) => Promise<User>;
  removeCourseMember: (courseId: number, userId: number) => Promise<void>;
  
  // Assignments
  fetchAssignments: () => Promise<void>;
  addAssignment: (assignment: Omit<Assignment, 'id' | 'user_id' | 'created_at' | 'updated_at' | 'subtasks'>) => Promise<void>;
  updateAssignment: (id: number, assignment: Partial<Assignment>) => Promise<void>;
  deleteAssignment: (id: number) => Promise<void>;
  fetchUpcomingAssignments: () => Promise<void>;
  fetchOverdueAssignments: () => Promise<void>;
  fetchCalendarMonth: (month: string) => Promise<{ month: string; days: Array<{ date: string; assignments: Assignment[]; study_sessions: any[] }>; assignments: Assignment[]; study_sessions: any[] }>;
  
  // Subtasks
  addSubtask: (assignmentId: number, subtask: Omit<Subtask, 'id' | 'assignment_id' | 'created_at' | 'updated_at' | 'order'>) => Promise<void>;
  updateSubtask: (subtaskId: number, subtask: Partial<Subtask>) => Promise<void>;
  deleteSubtask: (subtaskId: number) => Promise<void>;
}

export const useAuthStore = create<AuthStore>((set) => ({
  user: localStorage.getItem('user') ? JSON.parse(localStorage.getItem('user')!) : null,
  authChecked: false,
  isLoading: false,
  error: null,
  
  login: async (email: string, password: string) => {
    set({ isLoading: true, error: null });
    try {
      const response = await apiClient.post('/auth/login', { email, password });
      const { user } = response.data;
      localStorage.setItem('user', JSON.stringify(user));
      set({ user, authChecked: true });
    } catch (error: any) {
      const message = error.response?.data?.detail || 'Login failed';
      set({ error: message });
      throw error;
    } finally {
      set({ isLoading: false });
    }
  },
  
  register: async (email: string, username: string, password: string, role: 'user' | 'admin') => {
    set({ isLoading: true, error: null });
    try {
      const response = await apiClient.post('/auth/register', { email, username, password, role });
      const { user } = response.data;
      localStorage.setItem('user', JSON.stringify(user));
      set({ user, authChecked: true });
    } catch (error: any) {
      const message = error.response?.data?.detail || 'Registration failed';
      set({ error: message });
      throw error;
    } finally {
      set({ isLoading: false });
    }
  },
  
  logout: async () => {
    try {
      await apiClient.post('/auth/logout');
    } catch (_error) {
      // If backend session is already invalid, local cleanup is still enough.
    }
    localStorage.removeItem('user');
    set({ user: null, authChecked: true });
  },

  initializeAuth: async () => {
    try {
      const response = await apiClient.get('/auth/me');
      localStorage.setItem('user', JSON.stringify(response.data));
      set({ user: response.data, authChecked: true });
    } catch (_error) {
      localStorage.removeItem('user');
      set({ user: null, authChecked: true });
    }
  },
  
  setUser: (user: User | null) => set({ user }),
}));

export const useNotificationStore = create<NotificationStore>((set, get) => ({
  notifications: [],
  pushNotification: (title: string, message: string, id?: string) => {
    const notificationId = id || `${Date.now()}-${Math.random().toString(36).slice(2, 10)}`;
    if (get().notifications.some((n) => n.id === notificationId)) {
      return;
    }

    set((state) => ({
      notifications: [
        ...state.notifications,
        {
          id: notificationId,
          title,
          message,
          createdAt: Date.now(),
        },
      ],
    }));

    window.setTimeout(() => {
      get().dismissNotification(notificationId);
    }, 7000);
  },
  dismissNotification: (id: string) => {
    set((state) => ({
      notifications: state.notifications.filter((n) => n.id !== id),
    }));
  },
}));

export const useDataStore = create<DataStore>((set, get) => ({
  courses: [],
  assignments: [],
  upcomingAssignments: [],
  overdueAssignments: [],
  calendar: [] as any[],
  selectedCourse: null,
  isLoading: false,
  error: null,
  
  // Courses
  fetchCourses: async () => {
    set({ isLoading: true, error: null });
    try {
      const response = await apiClient.get('/courses/');
      set({ courses: response.data });
    } catch (error: any) {
      set({ error: error.message });
    } finally {
      set({ isLoading: false });
    }
  },
  
  addCourse: async (course) => {
    set({ isLoading: true, error: null });
    try {
      const response = await apiClient.post('/courses/', course);
      set((state) => ({ courses: [...state.courses, response.data] }));
    } catch (error: any) {
      set({ error: error.message });
      throw error;
    } finally {
      set({ isLoading: false });
    }
  },
  
  updateCourse: async (id, course) => {
    set({ isLoading: true, error: null });
    try {
      const response = await apiClient.put(`/courses/${id}`, course);
      set((state) => ({
        courses: state.courses.map((c) => (c.id === id ? response.data : c)),
      }));
    } catch (error: any) {
      set({ error: error.message });
      throw error;
    } finally {
      set({ isLoading: false });
    }
  },
  
  deleteCourse: async (id) => {
    set({ isLoading: true, error: null });
    try {
      await apiClient.delete(`/courses/${id}`);
      set((state) => ({ courses: state.courses.filter((c) => c.id !== id) }));
    } catch (error: any) {
      set({ error: error.message });
      throw error;
    } finally {
      set({ isLoading: false });
    }
  },

  fetchCourseMembers: async (courseId) => {
    try {
      const response = await apiClient.get(`/courses/${courseId}/members`);
      return response.data;
    } catch (error: any) {
      set({ error: error.message });
      throw error;
    }
  },

  addCourseMember: async (courseId, userId) => {
    try {
      const response = await apiClient.post(`/courses/${courseId}/members`, { user_id: userId });
      return response.data;
    } catch (error: any) {
      set({ error: error.message });
      throw error;
    }
  },

  removeCourseMember: async (courseId, userId) => {
    try {
      await apiClient.delete(`/courses/${courseId}/members/${userId}`);
    } catch (error: any) {
      set({ error: error.message });
      throw error;
    }
  },
  
  // Assignments
  fetchAssignments: async () => {
    set({ isLoading: true, error: null });
    try {
      const response = await apiClient.get('/assignments/');
      set({ assignments: response.data });
    } catch (error: any) {
      set({ error: error.message });
    } finally {
      set({ isLoading: false });
    }
  },
  
  addAssignment: async (assignment) => {
    set({ isLoading: true, error: null });
    try {
      const response = await apiClient.post('/assignments/', assignment);
      // Admin assignment creation can return a broadcast payload.
      if (response.data?.assignment_ids) {
        const refreshed = await apiClient.get('/assignments/');
        set({ assignments: refreshed.data });
      } else {
        set((state) => ({ assignments: [...state.assignments, response.data] }));
      }
    } catch (error: any) {
      set({ error: error.message });
      throw error;
    } finally {
      set({ isLoading: false });
    }
  },
  
  updateAssignment: async (id, assignment) => {
    set({ isLoading: true, error: null });
    try {
      const response = await apiClient.put(`/assignments/${id}`, assignment);
      set((state) => ({
        assignments: state.assignments.map((a) => (a.id === id ? response.data : a)),
      }));
    } catch (error: any) {
      set({ error: error.message });
      throw error;
    } finally {
      set({ isLoading: false });
    }
  },
  
  deleteAssignment: async (id) => {
    set({ isLoading: true, error: null });
    try {
      await apiClient.delete(`/assignments/${id}`);
      set((state) => ({ assignments: state.assignments.filter((a) => a.id !== id) }));
    } catch (error: any) {
      set({ error: error.message });
      throw error;
    } finally {
      set({ isLoading: false });
    }
  },

  fetchUpcomingAssignments: async () => {
    set({ isLoading: true, error: null });
    try {
      const response = await apiClient.get('/assignments/upcoming');
      set({ upcomingAssignments: response.data });
    } catch (error: any) {
      set({ error: error.message });
    } finally {
      set({ isLoading: false });
    }
  },

  fetchOverdueAssignments: async () => {
    set({ isLoading: true, error: null });
    try {
      const response = await apiClient.get('/assignments/overdue');
      set({ overdueAssignments: response.data });
    } catch (error: any) {
      set({ error: error.message });
    } finally {
      set({ isLoading: false });
    }
  },

  fetchCalendarMonth: async (month: string) => {
    set({ isLoading: true, error: null });
    try {
      const response = await apiClient.get(`/schedule/calendar?month=${month}`);
      set({ calendar: response.data.days });
      return response.data;
    } catch (error: any) {
      set({ error: error.message });
      throw error;
    } finally {
      set({ isLoading: false });
    }
  },
  
  // Subtasks
  addSubtask: async (assignmentId, subtask) => {
    set({ isLoading: true, error: null });
    try {
      const response = await apiClient.post(`/subtasks/${assignmentId}`, subtask);
      set((state) => ({
        assignments: state.assignments.map((a) =>
          a.id === assignmentId
            ? { ...a, subtasks: [...(a.subtasks || []), response.data] }
            : a
        ),
      }));
    } catch (error: any) {
      set({ error: error.message });
      throw error;
    } finally {
      set({ isLoading: false });
    }
  },
  
  updateSubtask: async (subtaskId, subtask) => {
    set({ isLoading: true, error: null });
    try {
      const response = await apiClient.put(`/subtasks/${subtaskId}`, subtask);
      set((state) => ({
        assignments: state.assignments.map((a) => ({
          ...a,
          subtasks: a.subtasks.map((s) => (s.id === subtaskId ? response.data : s)),
        })),
      }));
    } catch (error: any) {
      set({ error: error.message });
      throw error;
    } finally {
      set({ isLoading: false });
    }
  },
  
  deleteSubtask: async (subtaskId) => {
    set({ isLoading: true, error: null });
    try {
      await apiClient.delete(`/subtasks/${subtaskId}`);
      set((state) => ({
        assignments: state.assignments.map((a) => ({
          ...a,
          subtasks: a.subtasks.filter((s) => s.id !== subtaskId),
        })),
      }));
    } catch (error: any) {
      set({ error: error.message });
      throw error;
    } finally {
      set({ isLoading: false });
    }
  },
}));
