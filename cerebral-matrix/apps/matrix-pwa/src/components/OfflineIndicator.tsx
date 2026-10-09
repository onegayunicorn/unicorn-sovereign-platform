import React, { useEffect, useState } from 'react';
// Offline status indicator — PWA runs fully offline after first install.
const OfflineIndicator: React.FC = () => {
  const [online, setOnline] = useState(navigator.onLine);
  useEffect(() => {
    const on = () => setOnline(true);
    const off = () => setOnline(false);
    window.addEventListener('online', on);
    window.addEventListener('offline', off);
    return () => { window.removeEventListener('online', on); window.removeEventListener('offline', off); };
  }, []);
  return (
    <div className={`offline-indicator ${online ? 'online' : 'offline'}`}>
      {online ? 'Online' : 'Offline — running in sovereign mode'}
    </div>
  );
};
export default OfflineIndicator;
