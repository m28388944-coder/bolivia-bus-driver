import { useState } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import DriverLogin from './components/DriverLogin';
import Dashboard from './components/Dashboard';

export default function App() {
  const [driver, setDriver] = useState(null);

  const handleLogin  = (data) => setDriver(data);
  const handleLogout = () => setDriver(null);

  return (
    <div className="min-h-screen">
      <AnimatePresence mode="wait">
        {!driver ? (
          <motion.div key="login" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
            <DriverLogin onLogin={handleLogin}/>
          </motion.div>
        ) : (
          <motion.div key="dashboard" initial={{ opacity: 0, scale: 0.98 }} animate={{ opacity: 1, scale: 1 }} exit={{ opacity: 0 }}>
            <Dashboard driver={driver} onLogout={handleLogout}/>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
