import React from 'react';
import apiClient from '@/api';
import { useNotificationStore } from '@/store';

type ServerNotification = {
  id: number;
  title: string;
  message: string;
  type: string;
  is_read: boolean;
  scheduled_for?: string | null;
  created_at: string;
};

export default function NotificationWatcher() {
  const { pushNotification } = useNotificationStore();
  const isFetchingRef = React.useRef(false);

  const checkForUpdates = React.useCallback(async () => {
    if (isFetchingRef.current) return;
    isFetchingRef.current = true;

    try {
      const response = await apiClient.get('/notifications/unread');
      const unread: ServerNotification[] = response.data || [];

      if (unread.length > 0) {
        unread.forEach((notification) => {
          pushNotification(notification.title, notification.message, `server-${notification.id}`);
        });

        await apiClient.post('/notifications/mark-read', {
          ids: unread.map((n) => n.id),
        });
      }
    } catch (_error) {
      // Keep notification polling best-effort only.
    } finally {
      isFetchingRef.current = false;
    }
  }, [pushNotification]);

  React.useEffect(() => {
    checkForUpdates();
    const intervalId = window.setInterval(checkForUpdates, 10 * 1000);
    return () => window.clearInterval(intervalId);
  }, [checkForUpdates]);

  return null;
}
