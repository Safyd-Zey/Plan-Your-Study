import React from 'react';
import { X } from 'lucide-react';
import { useNotificationStore } from '@/store';

export default function NotificationToasts() {
  const { notifications, dismissNotification } = useNotificationStore();

  return (
    <div className="fixed top-20 right-4 z-50 space-y-2 w-80 max-w-[calc(100vw-2rem)] pointer-events-none">
      {notifications.map((notification) => (
        <div
          key={notification.id}
          className="pointer-events-auto bg-white border border-gray-200 shadow-lg rounded-lg p-3"
        >
          <div className="flex items-start justify-between gap-3">
            <div>
              <p className="text-sm font-semibold text-gray-900">{notification.title}</p>
              <p className="text-sm text-gray-600 mt-1">{notification.message}</p>
            </div>
            <button
              onClick={() => dismissNotification(notification.id)}
              className="text-gray-400 hover:text-gray-700"
            >
              <X size={16} />
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}
