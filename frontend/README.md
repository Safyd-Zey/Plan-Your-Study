# Plan Your Study - Frontend

## Overview
Modern React frontend for "Plan Your Study" - a comprehensive study planning and task management application for students.

## Features
- 🔐 User authentication with JWT
- 📚 Course management
- ✅ Assignment and subtask management
- 📅 Weekly and daily schedule views
- 📊 Progress tracking and statistics
- 🎯 Priority-based task organization
- 📱 Responsive design for all devices

## Tech Stack
- **Framework**: React 18
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Routing**: React Router v6
- **State Management**: Zustand
- **HTTP Client**: Axios
- **Build Tool**: Vite
- **Date Handling**: date-fns
- **Icons**: Lucide React

## Installation

### Prerequisites
- Node.js 16+
- npm or yarn

### Setup Steps

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Setup environment variables**
   ```bash
   cp .env.example .env.local
   # Edit .env.local if needed (usually defaults work for development)
   ```

4. **Start development server**
   ```bash
   npm run dev
   ```
   The app will be available at `http://localhost:3000`

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run type-check` - Run TypeScript type checking

## Project Structure

```
src/
├── pages/              # Page components
│   ├── DashboardPage   # Main dashboard
│   ├── LoginPage       # Login UI
│   ├── RegisterPage    # Registration UI
│   ├── CoursesPage     # Course management
│   ├── AssignmentsPage # Assignment management
│   ├── SchedulePage    # Calendar/schedule view
│   └── ProgressPage    # Progress tracking
├── components/         # Reusable components
│   └── Navigation      # Navigation bar
├── App.tsx            # Main app component
├── api.ts             # API client configuration
├── store.ts           # Zustand store (state management)
├── main.tsx           # Entry point
└── index.css          # Global styles
```

## Key Components

### Pages

**DashboardPage**
- Overview of all assignments
- Completion statistics
- Upcoming and overdue assignments

**CoursesPage**
- View all courses
- Create, edit, delete courses
- Course details with instructor info

**AssignmentsPage**
- List all assignments
- Create and manage assignments
- Add and manage subtasks for each assignment
- Priority and status indicators

**SchedulePage**
- Weekly calendar view
- Daily schedule view
- Navigation between weeks
- Assignment deadlines and study sessions

**ProgressPage**
- Overall completion percentage
- Statistics (completed, in progress, not started)
- Upcoming deadlines overview
- Motivational messages based on progress

### Components

**Navigation**
- Header with logo
- Navigation menu
- User info and logout
- Mobile responsive menu

## State Management

Using Zustand for minimal, efficient state management:

### AuthStore
- User authentication state
- Login/register/logout functions
- Token management

### DataStore
- Courses, assignments, and subtasks data
- CRUD operations for all entities
- Loading and error states
- Data persistence via localStorage

## API Integration

Axios client with:
- Automatic token injection in headers
- Automatic logout on 401 responses
- Base URL configuration
- Error handling

## Styling

Tailwind CSS with customization:
- Custom color scheme
- Responsive design patterns
- Component utilities
- Dark mode ready (can be extended)

## Authentication Flow

1. User registers or logs in
2. JWT token received and stored in localStorage
3. Token automatically included in all API requests
4. Token validated on app load
5. Redirect to login if token invalid

## Key Features Implementation

### Course Management
- Create courses with name, description, instructor
- View all user's courses
- Edit and delete courses

### Assignment Management
- Create assignments with deadlines, priorities
- Break down into subtasks
- Track status (not started, in progress, completed)
- Filter by course and priority

### Subtask Management
- Add subtasks to assignments
- Mark subtasks complete/incomplete
- Delete subtasks
- Visual progress indicator

### Schedule
- Weekly calendar view
- Color-coded assignments by priority
- Study session scheduling
- Easy date navigation

### Progress Tracking
- Completion percentage with visual circle
- Stats breakdown
- Upcoming deadlines list
- Motivational feedback

## Browser Support
- Chrome/Edge 90+
- Firefox 88+
- Safari 14+

## Environment Variables

```
VITE_API_URL=http://localhost:8000/api
```

## Performance Notes

- Images can take up to 2 seconds to load with slow connection
- API response time optimized to <1 second
- Bundle size optimized with code splitting

## Common Issues & Solutions

**CORS Errors**: Backend CORS is configured to accept requests. Ensure backend is running.

**API Not Found (404)**: Verify backend is running on port 8000

**Token Invalid**: Clear localStorage and log in again

**Styling Not Loading**: Ensure Tailwind CSS processes are running

## Development Tips

- Use React DevTools extension for debugging
- Check browser console for API errors
- Use network tab to inspect API calls
- TypeScript provides great IDE autocomplete

## Production Build

```bash
npm run build
```

Creates optimized production build in `dist/` folder.

Deploy to static hosting (Netlify, Vercel, AWS S3, etc.)

## Deployment Example (Netlify)

```bash
npm run build
# Deploy the dist folder
```

## Contributing

Follow the established patterns:
- Use functional components with hooks
- Implement proper TypeScript typing
- Follow Tailwind CSS conventions
- Keep components modular and reusable

## Support & Contact

For issues or questions, please refer to the project documentation or create an issue in the repository.
