import os

# ── index.css completo con Tailwind v4 ──────────────────────────────────────
index_css = """@import "tailwindcss";

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

* { font-family: 'Inter', sans-serif; box-sizing: border-box; }

body {
  background: #060d1f;
  color: white;
  overscroll-behavior: none;
  min-height: 100vh;
}

#root {
  min-height: 100vh;
  background: linear-gradient(135deg, #060d1f 0%, #0d1a3a 50%, #060d1f 100%);
}

.glass {
  background: rgba(255,255,255,0.06);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255,255,255,0.12);
}

.glass-card {
  background: rgba(255,255,255,0.07);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 20px;
}

.glass-dark {
  background: rgba(0,0,0,0.3);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 16px;
}

.gold { color: #D4AF37; }
.bg-gold { background: #D4AF37; }

.glow-blue { box-shadow: 0 0 30px rgba(27,42,107,0.4); }
.glow-gold { box-shadow: 0 0 20px rgba(212,175,55,0.3); }

::-webkit-scrollbar { width: 3px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 4px; }
"""

# ── DriverLogin mejorado ─────────────────────────────────────────────────────
login_jsx = r"""import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Bus, Shield, ChevronRight, AlertCircle, Star } from 'lucide-react';
import { getBuses, getSchedules } from '../api';

const DRIVER_CODES = {
  'B-1234': { name: 'Juan Carlos Mamani',   company: 'Bolivia Bus Express', code: '1234', color: '#1B2A6B' },
  'B-5678': { name: 'Pedro Quispe Condori', company: 'Trans Copacabana',    code: '5678', color: '#C8102E' },
  'B-9012': { name: 'Luis Flores Tarqui',   company: 'Flota Boliviana',     code: '9012', color: '#007A33' },
};

export default function DriverLogin({ onLogin }) {
  const [plate, setPlate]     = useState('');
  const [code, setCode]       = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError]     = useState('');
  const [step, setStep]       = useState(1);

  const handlePlate = (e) => {
    e.preventDefault();
    const normalized = plate.toUpperCase().trim();
    if (!DRIVER_CODES[normalized]) { setError('Placa no registrada'); return; }
    setError(''); setStep(2);
  };

  const handleCode = async (e) => {
    e.preventDefault();
    const normalized = plate.toUpperCase().trim();
    const driver = DRIVER_CODES[normalized];
    if (!driver || code !== driver.code) { setError('PIN incorrecto'); return; }
    setLoading(true);
    try {
      const [schRes, busRes] = await Promise.all([getSchedules(), getBuses()]);
      const schedules = schRes.data.schedules || [];
      const buses     = busRes.data.buses || [];
      const bus       = buses.find(b => b.plate === normalized);
      const mySchedules = schedules.filter(s => s.plate === normalized);
      onLogin({ name: driver.name, company: driver.company, plate: normalized, bus, schedules: mySchedules });
    } catch { setError('Error de conexion. Verifica el backend.'); }
    finally { setLoading(false); }
  };

  const driverInfo = DRIVER_CODES[plate.toUpperCase().trim()];

  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-6 relative overflow-hidden"
      style={{ background: 'linear-gradient(135deg, #060d1f 0%, #0d1a3a 60%, #060d1f 100%)' }}>

      {/* Fondo decorativo */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <motion.div className="absolute top-1/4 left-1/4 w-96 h-96 rounded-full"
          style={{ background: 'radial-gradient(circle, rgba(27,42,107,0.3), transparent 70%)' }}
          animate={{ scale: [1, 1.2, 1], opacity: [0.3, 0.5, 0.3] }}
          transition={{ duration: 6, repeat: Infinity }}/>
        <motion.div className="absolute bottom-1/4 right-1/4 w-80 h-80 rounded-full"
          style={{ background: 'radial-gradient(circle, rgba(212,175,55,0.15), transparent 70%)' }}
          animate={{ scale: [1.2, 1, 1.2], opacity: [0.2, 0.4, 0.2] }}
          transition={{ duration: 8, repeat: Infinity }}/>
        {[...Array(30)].map((_, i) => (
          <motion.div key={i}
            className="absolute rounded-full"
            style={{ width: 2 + (i%3), height: 2 + (i%3), left: (i*37)%100+'%', top: (i*23)%100+'%', background: i%3===0 ? '#D4AF37' : 'white', opacity: 0.15 }}
            animate={{ opacity: [0.05, 0.3, 0.05], y: [-5, 5, -5] }}
            transition={{ duration: 3 + (i%4), repeat: Infinity, delay: i*0.2 }}/>
        ))}
        {/* Lineas decorativas */}
        <svg className="absolute inset-0 w-full h-full opacity-5" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <pattern id="grid" width="60" height="60" patternUnits="userSpaceOnUse">
              <path d="M 60 0 L 0 0 0 60" fill="none" stroke="white" strokeWidth="0.5"/>
            </pattern>
          </defs>
          <rect width="100%" height="100%" fill="url(#grid)"/>
        </svg>
      </div>

      <motion.div initial={{ opacity: 0, y: 40 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.7 }}
        className="w-full max-w-sm relative z-10">

        {/* Logo */}
        <div className="text-center mb-10">
          <motion.div
            animate={{ y: [0, -8, 0] }}
            transition={{ duration: 3, repeat: Infinity, ease: 'easeInOut' }}
            className="relative inline-block mb-5">
            <div className="w-24 h-24 rounded-3xl flex items-center justify-center mx-auto shadow-2xl glow-blue"
              style={{ background: 'linear-gradient(135deg, #1B2A6B, #2d45a8)' }}>
              <Bus size={44} color="#D4AF37"/>
            </div>
            <motion.div className="absolute -top-1 -right-1 w-7 h-7 rounded-full flex items-center justify-center"
              style={{ background: 'linear-gradient(135deg, #D4AF37, #f0c84a)' }}
              animate={{ rotate: 360 }} transition={{ duration: 8, repeat: Infinity, ease: 'linear' }}>
              <Star size={14} color="#1B2A6B" fill="#1B2A6B"/>
            </motion.div>
          </motion.div>
          <h1 className="text-4xl font-black text-white mb-1">
            Bolivia <span style={{ color: '#D4AF37' }}>Bus</span>
          </h1>
          <p className="text-sm font-semibold" style={{ color: 'rgba(255,255,255,0.4)' }}>Panel del Conductor</p>
          <div className="flex items-center justify-center gap-2 mt-3">
            <div className="h-px w-12" style={{ background: 'linear-gradient(to right, transparent, rgba(212,175,55,0.5))' }}/>
            <span className="text-xs" style={{ color: 'rgba(212,175,55,0.6)' }}>ACCESO SEGURO</span>
            <div className="h-px w-12" style={{ background: 'linear-gradient(to left, transparent, rgba(212,175,55,0.5))' }}/>
          </div>
        </div>

        <AnimatePresence mode="wait">
          {/* Step 1: Placa */}
          {step === 1 && (
            <motion.form key="step1" onSubmit={handlePlate}
              initial={{ opacity: 0, x: -30 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: 30 }}
              className="glass-card p-7" style={{ boxShadow: '0 25px 60px rgba(0,0,0,0.5)' }}>

              <div className="flex items-center gap-3 mb-7">
                <div className="w-12 h-12 rounded-2xl flex items-center justify-center"
                  style={{ background: 'rgba(212,175,55,0.15)', border: '1px solid rgba(212,175,55,0.3)' }}>
                  <Bus size={24} color="#D4AF37"/>
                </div>
                <div>
                  <p className="font-black text-white text-base">Identificacion</p>
                  <p className="text-xs" style={{ color: 'rgba(255,255,255,0.4)' }}>Ingresa la placa de tu unidad</p>
                </div>
              </div>

              <label className="text-xs font-bold uppercase tracking-widest block mb-2"
                style={{ color: 'rgba(255,255,255,0.35)' }}>Placa del vehiculo</label>
              <input value={plate} onChange={e => { setPlate(e.target.value); setError(''); }}
                placeholder="Ej: B-1234"
                className="w-full rounded-2xl px-5 py-4 text-white text-xl font-black tracking-widest placeholder-white/20 focus:outline-none transition-all uppercase mb-2"
                style={{ background: 'rgba(255,255,255,0.07)', border: plate ? '2px solid #D4AF37' : '2px solid rgba(255,255,255,0.1)', letterSpacing: '0.15em' }}
                autoFocus/>

              {error && (
                <motion.div initial={{ opacity: 0, y: -5 }} animate={{ opacity: 1, y: 0 }}
                  className="flex items-center gap-2 text-sm mb-4 px-4 py-2.5 rounded-xl"
                  style={{ background: 'rgba(239,68,68,0.12)', color: '#fca5a5', border: '1px solid rgba(239,68,68,0.2)' }}>
                  <AlertCircle size={14}/> {error}
                </motion.div>
              )}

              <motion.button type="submit" whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.97 }}
                className="w-full py-4 rounded-2xl font-black text-lg flex items-center justify-center gap-2 mt-4"
                style={{ background: 'linear-gradient(135deg, #D4AF37, #f0c84a)', color: '#1B2A6B', boxShadow: '0 8px 30px rgba(212,175,55,0.3)' }}>
                Continuar <ChevronRight size={20}/>
              </motion.button>

              <div className="mt-5 p-3 rounded-xl text-center" style={{ background: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.06)' }}>
                <p className="text-xs mb-1" style={{ color: 'rgba(255,255,255,0.25)' }}>Placas de prueba</p>
                <div className="flex justify-center gap-3">
                  {Object.keys(DRIVER_CODES).map(p => (
                    <button key={p} type="button" onClick={() => setPlate(p)}
                      className="text-xs px-2 py-1 rounded-lg font-mono font-bold transition-all hover:scale-105"
                      style={{ background: 'rgba(212,175,55,0.1)', color: '#D4AF37', border: '1px solid rgba(212,175,55,0.2)' }}>
                      {p}
                    </button>
                  ))}
                </div>
              </div>
            </motion.form>
          )}

          {/* Step 2: PIN */}
          {step === 2 && (
            <motion.form key="step2" onSubmit={handleCode}
              initial={{ opacity: 0, x: 30 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -30 }}
              className="glass-card p-7" style={{ boxShadow: '0 25px 60px rgba(0,0,0,0.5)' }}>

              <button type="button" onClick={() => { setStep(1); setError(''); setCode(''); }}
                className="text-xs font-semibold mb-5 flex items-center gap-1 transition-all hover:gap-2"
                style={{ color: 'rgba(255,255,255,0.35)' }}>
                ← Cambiar placa
              </button>

              {driverInfo && (
                <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }}
                  className="mb-6 p-4 rounded-2xl"
                  style={{ background: driverInfo.color + '20', border: '1px solid ' + driverInfo.color + '40' }}>
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-xl flex items-center justify-center font-black text-lg"
                      style={{ background: driverInfo.color, color: '#fff' }}>
                      {driverInfo.name.charAt(0)}
                    </div>
                    <div>
                      <p className="font-black text-white text-sm">{driverInfo.name}</p>
                      <p className="text-xs" style={{ color: '#D4AF37' }}>{driverInfo.company} · {plate.toUpperCase()}</p>
                    </div>
                  </div>
                </motion.div>
              )}

              <div className="flex items-center gap-3 mb-6">
                <div className="w-12 h-12 rounded-2xl flex items-center justify-center"
                  style={{ background: 'rgba(34,197,94,0.15)', border: '1px solid rgba(34,197,94,0.3)' }}>
                  <Shield size={24} color="#22c55e"/>
                </div>
                <div>
                  <p className="font-black text-white">Codigo PIN</p>
                  <p className="text-xs" style={{ color: 'rgba(255,255,255,0.4)' }}>4 digitos de seguridad</p>
                </div>
              </div>

              {/* Dots PIN */}
              <div className="flex gap-4 justify-center mb-7">
                {[0,1,2,3].map(i => (
                  <motion.div key={i}
                    animate={{ scale: code.length === i ? [1, 1.2, 1] : 1 }}
                    transition={{ duration: 0.2 }}
                    className="w-16 h-16 rounded-2xl flex items-center justify-center text-3xl"
                    style={{
                      background: code.length > i ? 'rgba(212,175,55,0.2)' : 'rgba(255,255,255,0.05)',
                      border: code.length > i ? '2px solid #D4AF37' : '2px solid rgba(255,255,255,0.1)',
                    }}>
                    {code.length > i ? (
                      <motion.div initial={{ scale: 0 }} animate={{ scale: 1 }}
                        className="w-4 h-4 rounded-full" style={{ background: '#D4AF37' }}/>
                    ) : ''}
                  </motion.div>
                ))}
              </div>

              {/* Teclado */}
              <div className="grid grid-cols-3 gap-3 mb-5">
                {[1,2,3,4,5,6,7,8,9,'',0,'⌫'].map((n, i) => (
                  <motion.button key={i} type="button"
                    whileHover={n !== '' ? { scale: 1.05 } : {}}
                    whileTap={n !== '' ? { scale: 0.92 } : {}}
                    onClick={() => {
                      if (n === '⌫') setCode(c => c.slice(0,-1));
                      else if (n !== '' && code.length < 4) setCode(c => c + n);
                      setError('');
                    }}
                    className={"h-16 rounded-2xl font-black text-2xl transition-all " + (n === '' ? 'invisible' : '')}
                    style={{
                      background: n === '⌫' ? 'rgba(239,68,68,0.1)' : 'rgba(255,255,255,0.06)',
                      border: '1px solid rgba(255,255,255,0.08)',
                      color: n === '⌫' ? '#ef4444' : 'white',
                    }}>
                    {n}
                  </motion.button>
                ))}
              </div>

              {error && (
                <motion.div initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }}
                  className="flex items-center gap-2 text-sm mb-4 px-4 py-2.5 rounded-xl"
                  style={{ background: 'rgba(239,68,68,0.12)', color: '#fca5a5', border: '1px solid rgba(239,68,68,0.2)' }}>
                  <AlertCircle size={14}/> {error}
                </motion.div>
              )}

              <motion.button type="submit" disabled={code.length < 4 || loading}
                whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.97 }}
                className="w-full py-4 rounded-2xl font-black text-lg flex items-center justify-center gap-2 transition-all"
                style={{
                  background: code.length === 4 ? 'linear-gradient(135deg, #D4AF37, #f0c84a)' : 'rgba(255,255,255,0.05)',
                  color: code.length === 4 ? '#1B2A6B' : 'rgba(255,255,255,0.2)',
                  boxShadow: code.length === 4 ? '0 8px 30px rgba(212,175,55,0.3)' : 'none',
                }}>
                {loading ? (
                  <><div className="w-5 h-5 border-2 border-current border-t-transparent rounded-full animate-spin"/> Verificando...</>
                ) : (
                  <><Shield size={18}/> Ingresar al Sistema</>
                )}
              </motion.button>
            </motion.form>
          )}
        </AnimatePresence>
      </motion.div>
    </div>
  );
}
"""

# ── Dashboard mejorado ───────────────────────────────────────────────────────
dashboard_jsx = r"""import { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Bus, Users, MapPin, Clock, ChevronRight, Wifi, WifiOff, LogOut, Grid, Share2, TrendingUp, AlertCircle } from 'lucide-react';
import { getPassengers, getSeatMap, WS_URL } from '../api';
import PassengerList from './PassengerList';
import SeatOverview from './SeatOverview';
import ShareRoute from './ShareRoute';

const COMPANY_COLORS = {
  'Bolivia Bus Express': { primary: '#1B2A6B', accent: '#D4AF37', gradient: 'linear-gradient(135deg, #1B2A6B, #2d45a8)' },
  'Trans Copacabana':    { primary: '#C8102E', accent: '#FFFFFF', gradient: 'linear-gradient(135deg, #C8102E, #e8314a)' },
  'Flota Boliviana':     { primary: '#007A33', accent: '#F4D03F', gradient: 'linear-gradient(135deg, #007A33, #00a344)' },
};

export default function Dashboard({ driver, onLogout }) {
  const [tab, setTab]               = useState('passengers');
  const [passengers, setPassengers] = useState([]);
  const [seats, setSeats]           = useState([]);
  const [loading, setLoading]       = useState(true);
  const [connected, setConnected]   = useState(false);
  const [busData, setBusData]       = useState(null);
  const [showShare, setShowShare]   = useState(false);
  const wsRef = useRef(null);

  const schedule = driver.schedules?.[0];
  const colors   = COMPANY_COLORS[driver.company] || COMPANY_COLORS['Bolivia Bus Express'];

  useEffect(() => {
    if (!schedule) { setLoading(false); return; }
    Promise.all([
      getPassengers(schedule.id),
      getSeatMap(schedule.id),
    ]).then(([pRes, sRes]) => {
      setPassengers(pRes.data.bookings || []);
      setSeats(sRes.data.seats || []);
    }).catch(() => {}).finally(() => setLoading(false));

    const ws = new WebSocket(WS_URL);
    wsRef.current = ws;
    ws.onopen  = () => setConnected(true);
    ws.onclose = () => setConnected(false);
    ws.onmessage = (e) => {
      const data = JSON.parse(e.data);
      if (data.type === 'location_update' && data.plate === driver.plate)
        setBusData(data);
    };
    return () => ws.close();
  }, [schedule]);

  const confirmed  = passengers.filter(p => p.status === 'confirmed');
  const totalSeats = seats.length || 40;
  const occupied   = seats.filter(s => s.status !== 'available').length;
  const available  = seats.filter(s => s.status === 'available').length;
  const occupancy  = totalSeats > 0 ? Math.round((occupied / totalSeats) * 100) : 0;

  const fmt     = (dt) => dt ? new Date(dt).toLocaleTimeString('es-BO', { hour:'2-digit', minute:'2-digit' }) : '--:--';
  const fmtDate = (dt) => dt ? new Date(dt).toLocaleDateString('es-BO', { weekday:'long', day:'numeric', month:'long' }) : '';

  const TABS = [
    { id: 'passengers', label: 'Pasajeros', icon: Users,  count: passengers.length },
    { id: 'seats',      label: 'Asientos',  icon: Grid,   count: null },
    { id: 'route',      label: 'Mi Ruta',   icon: MapPin, count: null },
  ];

  return (
    <div className="min-h-screen flex flex-col" style={{ maxWidth: 480, margin: '0 auto', background: 'transparent' }}>

      {/* HEADER */}
      <div className="relative overflow-hidden" style={{ background: colors.gradient, paddingTop: 52, paddingBottom: 28, paddingLeft: 20, paddingRight: 20 }}>
        {/* Decoracion */}
        <div className="absolute -top-16 -right-16 w-48 h-48 rounded-full opacity-15" style={{ background: colors.accent }}/>
        <div className="absolute top-1/2 -left-10 w-32 h-32 rounded-full opacity-10" style={{ background: 'white' }}/>
        <svg className="absolute bottom-0 left-0 right-0 opacity-5" viewBox="0 0 480 30" xmlns="http://www.w3.org/2000/svg">
          <path d="M0,20 Q120,0 240,15 T480,10 L480,30 L0,30 Z" fill="white"/>
        </svg>

        <div className="relative z-10">
          {/* Top bar */}
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 rounded-2xl flex items-center justify-center" style={{ background: 'rgba(255,255,255,0.15)', border: '1px solid rgba(255,255,255,0.25)' }}>
                <Bus size={24} color={colors.accent}/>
              </div>
              <div>
                <p className="text-xs font-semibold" style={{ color: 'rgba(255,255,255,0.55)' }}>Bolivia Bus</p>
                <p className="font-black text-white text-sm leading-tight">{driver.company}</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <motion.div
                animate={connected ? { scale: [1, 1.05, 1] } : {}}
                transition={{ repeat: Infinity, duration: 2 }}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-bold"
                style={{ background: connected ? 'rgba(34,197,94,0.2)' : 'rgba(239,68,68,0.2)', color: connected ? '#4ade80' : '#f87171', border: '1px solid ' + (connected ? 'rgba(34,197,94,0.3)' : 'rgba(239,68,68,0.3)') }}>
                {connected ? <Wifi size={11}/> : <WifiOff size={11}/>}
                {connected ? 'GPS' : 'Sin GPS'}
              </motion.div>
              <motion.button whileHover={{ scale: 1.1 }} whileTap={{ scale: 0.9 }} onClick={onLogout}
                className="w-9 h-9 rounded-xl flex items-center justify-center"
                style={{ background: 'rgba(255,255,255,0.1)', border: '1px solid rgba(255,255,255,0.15)' }}>
                <LogOut size={16} color="rgba(255,255,255,0.6)"/>
              </motion.button>
            </div>
          </div>

          {/* Conductor */}
          <div className="mb-5">
            <p className="text-xs font-semibold mb-0.5" style={{ color: 'rgba(255,255,255,0.45)' }}>CONDUCTOR</p>
            <p className="text-2xl font-black text-white">{driver.name}</p>
            <div className="flex items-center gap-3 mt-2 flex-wrap">
              <span className="text-xs font-black px-3 py-1 rounded-full" style={{ background: 'rgba(255,255,255,0.15)', color: colors.accent, border: '1px solid rgba(255,255,255,0.2)' }}>
                {driver.plate}
              </span>
              {schedule && (
                <span className="text-xs flex items-center gap-1.5" style={{ color: 'rgba(255,255,255,0.55)' }}>
                  <Clock size={11}/>
                  {fmt(schedule.departure_time)} → {fmt(schedule.arrival_time)}
                </span>
              )}
              {schedule && (
                <span className="text-xs" style={{ color: 'rgba(255,255,255,0.4)' }}>
                  {fmtDate(schedule.departure_time)}
                </span>
              )}
            </div>
          </div>

          {/* Ruta card */}
          {schedule ? (
            <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
              className="rounded-2xl p-4 flex items-center justify-between"
              style={{ background: 'rgba(255,255,255,0.12)', border: '1px solid rgba(255,255,255,0.2)', backdropFilter: 'blur(10px)' }}>
              <div>
                <p className="text-xs mb-1" style={{ color: 'rgba(255,255,255,0.45)' }}>RUTA DE HOY</p>
                <div className="flex items-center gap-2">
                  <span className="text-white font-black text-xl">{schedule.origin}</span>
                  <ChevronRight size={18} color={colors.accent}/>
                  <span className="text-white font-black text-xl">{schedule.destination}</span>
                </div>
              </div>
              <motion.button whileHover={{ scale: 1.1 }} whileTap={{ scale: 0.9 }}
                onClick={() => setShowShare(true)}
                className="w-12 h-12 rounded-2xl flex items-center justify-center"
                style={{ background: 'rgba(255,255,255,0.15)', border: '1px solid rgba(255,255,255,0.25)' }}>
                <Share2 size={18} color={colors.accent}/>
              </motion.button>
            </motion.div>
          ) : (
            <div className="rounded-2xl p-4 flex items-center gap-3"
              style={{ background: 'rgba(255,255,255,0.08)', border: '1px solid rgba(255,255,255,0.12)' }}>
              <AlertCircle size={18} color="rgba(255,255,255,0.4)"/>
              <p className="text-sm" style={{ color: 'rgba(255,255,255,0.45)' }}>Sin horario asignado para hoy</p>
            </div>
          )}
        </div>
      </div>

      {/* STATS */}
      <div style={{ padding: '0 16px', marginTop: -16, marginBottom: 16 }}>
        <div className="grid grid-cols-3 gap-3">
          {[
            { label: 'Pasajeros', value: confirmed.length, sub: passengers.length - confirmed.length + ' pendientes', color: '#60a5fa', icon: Users },
            { label: 'Ocupacion', value: occupancy + '%',  sub: occupied + '/' + totalSeats + ' asientos',            color: colors.accent, icon: TrendingUp },
            { label: 'Libres',    value: available,        sub: 'asientos disp.',                                      color: '#4ade80', icon: Grid },
          ].map((s, i) => (
            <motion.div key={s.label}
              initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 + i * 0.08 }}
              className="rounded-2xl p-3 text-center"
              style={{ background: 'rgba(255,255,255,0.06)', border: '1px solid rgba(255,255,255,0.1)', backdropFilter: 'blur(10px)', boxShadow: '0 8px 24px rgba(0,0,0,0.3)' }}>
              <p className="text-2xl font-black" style={{ color: s.color }}>{s.value}</p>
              <p className="text-white font-bold text-xs mt-0.5">{s.label}</p>
              <p className="text-xs mt-0.5" style={{ color: 'rgba(255,255,255,0.3)', fontSize: 10 }}>{s.sub}</p>
            </motion.div>
          ))}
        </div>
      </div>

      {/* GPS LIVE */}
      <AnimatePresence>
        {busData && (
          <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: 'auto' }} exit={{ opacity: 0, height: 0 }}
            style={{ margin: '0 16px 12px' }}>
            <div className="rounded-2xl p-3 flex items-center gap-3"
              style={{ background: 'rgba(34,197,94,0.08)', border: '1px solid rgba(34,197,94,0.2)' }}>
              <div className="w-8 h-8 rounded-xl flex items-center justify-center" style={{ background: 'rgba(34,197,94,0.15)' }}>
                <MapPin size={16} color="#4ade80"/>
              </div>
              <div className="flex-1">
                <p className="text-white text-xs font-bold">GPS en vivo</p>
                <p className="text-xs" style={{ color: 'rgba(255,255,255,0.4)' }}>{busData.speed_kmh} km/h</p>
              </div>
              <div className="w-2 h-2 rounded-full bg-green-400" style={{ boxShadow: '0 0 8px #4ade80', animation: 'pulse 2s infinite' }}/>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* TABS */}
      <div style={{ padding: '0 16px', marginBottom: 16 }}>
        <div className="flex gap-1 p-1 rounded-2xl" style={{ background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.08)' }}>
          {TABS.map(t => (
            <button key={t.id} onClick={() => setTab(t.id)}
              className="flex-1 flex items-center justify-center gap-1.5 py-3 rounded-xl text-xs font-black transition-all"
              style={{
                background: tab === t.id ? 'rgba(255,255,255,0.95)' : 'transparent',
                color: tab === t.id ? '#1B2A6B' : 'rgba(255,255,255,0.4)',
                boxShadow: tab === t.id ? '0 4px 12px rgba(0,0,0,0.3)' : 'none',
              }}>
              <t.icon size={14}/>
              {t.label}
              {t.count !== null && t.count > 0 && (
                <span className="text-[10px] px-1.5 rounded-full font-black"
                  style={{ background: tab === t.id ? colors.primary : 'rgba(255,255,255,0.15)', color: tab === t.id ? 'white' : 'white' }}>
                  {t.count}
                </span>
              )}
            </button>
          ))}
        </div>
      </div>

      {/* CONTENT */}
      <div style={{ flex: 1, padding: '0 16px 32px', overflowY: 'auto' }}>
        <AnimatePresence mode="wait">
          {tab === 'passengers' && (
            <motion.div key="p" initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }}>
              <PassengerList passengers={passengers} loading={loading} colors={colors}/>
            </motion.div>
          )}
          {tab === 'seats' && (
            <motion.div key="s" initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }}>
              <SeatOverview seats={seats} loading={loading} colors={colors}/>
            </motion.div>
          )}
          {tab === 'route' && (
            <motion.div key="r" initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }}>
              <RouteInfo schedule={schedule} driver={driver} busData={busData} colors={colors}/>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      <AnimatePresence>
        {showShare && <ShareRoute schedule={schedule} passengers={passengers} driver={driver} onClose={() => setShowShare(false)}/>}
      </AnimatePresence>
    </div>
  );
}

function RouteInfo({ schedule, driver, busData, colors }) {
  const fmt     = (dt) => dt ? new Date(dt).toLocaleTimeString('es-BO', { hour:'2-digit', minute:'2-digit' }) : '--:--';
  const fmtDate = (dt) => dt ? new Date(dt).toLocaleDateString('es-BO', { weekday:'long', day:'numeric', month:'long' }) : '';

  if (!schedule) return (
    <div className="text-center py-16">
      <div className="w-20 h-20 rounded-3xl flex items-center justify-center mx-auto mb-4" style={{ background: 'rgba(255,255,255,0.05)' }}>
        <MapPin size={36} color="rgba(255,255,255,0.15)"/>
      </div>
      <p className="font-bold" style={{ color: 'rgba(255,255,255,0.3)' }}>Sin ruta asignada hoy</p>
    </div>
  );

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
      <div className="rounded-2xl p-5" style={{ background: 'rgba(255,255,255,0.06)', border: '1px solid rgba(255,255,255,0.1)' }}>
        <p className="text-xs font-bold uppercase tracking-widest mb-4" style={{ color: 'rgba(255,255,255,0.3)' }}>Informacion del viaje</p>
        <div className="flex items-center gap-3 mb-4">
          <div className="text-center flex-1">
            <p className="text-3xl font-black text-white">{fmt(schedule.departure_time)}</p>
            <p className="text-xs mt-1 font-semibold" style={{ color: colors.accent }}>{schedule.origin}</p>
          </div>
          <div className="flex flex-col items-center gap-1">
            <div className="w-16 h-px" style={{ background: 'rgba(255,255,255,0.2)' }}/>
            <p className="text-xs" style={{ color: 'rgba(255,255,255,0.3)' }}>{schedule.duration_hours}h</p>
            <div className="w-16 h-px" style={{ background: 'rgba(255,255,255,0.2)' }}/>
          </div>
          <div className="text-center flex-1">
            <p className="text-3xl font-black text-white">{fmt(schedule.arrival_time)}</p>
            <p className="text-xs mt-1 font-semibold" style={{ color: 'rgba(255,255,255,0.5)' }}>{schedule.destination}</p>
          </div>
        </div>
        <p className="text-center text-xs" style={{ color: 'rgba(255,255,255,0.25)' }}>{fmtDate(schedule.departure_time)}</p>
      </div>

      <div className="grid grid-cols-2 gap-3">
        {[
          { label: 'Placa',    value: driver.plate,                              color: colors.accent },
          { label: 'Tipo Bus', value: (schedule.bus_type||'normal').toUpperCase(), color: '#60a5fa' },
          { label: 'Bs. Normal',  value: 'Bs. ' + schedule.price_normal,         color: '#4ade80' },
          { label: 'Bs. Cama',    value: 'Bs. ' + (schedule.price_cama||'-'),    color: '#f59e0b' },
        ].map(item => (
          <div key={item.label} className="rounded-2xl p-4"
            style={{ background: 'rgba(255,255,255,0.04)', border: '1px solid rgba(255,255,255,0.08)' }}>
            <p className="text-xs mb-1" style={{ color: 'rgba(255,255,255,0.3)' }}>{item.label}</p>
            <p className="font-black text-base" style={{ color: item.color }}>{item.value}</p>
          </div>
        ))}
      </div>

      {busData && (
        <div className="rounded-2xl p-4" style={{ background: 'rgba(34,197,94,0.07)', border: '1px solid rgba(34,197,94,0.2)' }}>
          <p className="text-xs font-bold uppercase tracking-widest mb-3" style={{ color: 'rgba(74,222,128,0.6)' }}>GPS Tiempo Real</p>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <p className="text-xs" style={{ color: 'rgba(255,255,255,0.3)' }}>Velocidad</p>
              <p className="text-2xl font-black" style={{ color: '#4ade80' }}>{busData.speed_kmh} <span className="text-sm font-normal">km/h</span></p>
            </div>
            <div>
              <p className="text-xs" style={{ color: 'rgba(255,255,255,0.3)' }}>Estado</p>
              <p className="font-black text-sm capitalize" style={{ color: '#4ade80' }}>{busData.status || 'en ruta'}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
"""

files = {
    "src/index.css":                    index_css,
    "src/components/DriverLogin.jsx":   login_jsx,
    "src/components/Dashboard.jsx":     dashboard_jsx,
}

for path, content in files.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("OK:", path)

print("\nMejoras aplicadas!")