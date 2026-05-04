import os

os.makedirs("src/components", exist_ok=True)

# ── index.css ────────────────────────────────────────────────────────────────
index_css = """@tailwind base;
@tailwind components;
@tailwind utilities;

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

* { font-family: 'Inter', sans-serif; }

body {
  background: #0a0f1e;
  color: white;
  overscroll-behavior: none;
}

.glass {
  background: rgba(255,255,255,0.05);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255,255,255,0.1);
}

.glass-card {
  background: rgba(255,255,255,0.07);
  backdrop-filter: blur(16px);
  border: 1px solid rgba(255,255,255,0.12);
  border-radius: 20px;
}

.gold { color: #D4AF37; }
.bg-gold { background: #D4AF37; }

.seat-available { background: rgba(27,42,107,0.6); border: 1.5px solid #4B6BDB; }
.seat-occupied  { background: rgba(239,68,68,0.3);  border: 1.5px solid #ef4444; }
.seat-free      { background: rgba(34,197,94,0.2);  border: 1.5px solid #22c55e; }

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.15); border-radius: 4px; }
"""

# ── api.js ───────────────────────────────────────────────────────────────────
api_js = """import axios from 'axios';

const API = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  headers: { 'Content-Type': 'application/json' },
});

export const getSchedules       = ()   => API.get('/schedules/');
export const getBuses           = ()   => API.get('/schedules/buses');
export const getPassengers      = (id) => API.get('/bookings/schedule/' + id);
export const getSeatMap         = (id) => API.get('/seats/schedule/' + id);
export const WS_URL = 'ws://localhost:8000/api/v1/tracking/ws/tracking';

export default API;
"""

# ── main.jsx ─────────────────────────────────────────────────────────────────
main_jsx = """import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
"""

# ── DriverLogin.jsx ──────────────────────────────────────────────────────────
login_jsx = r"""import { useState } from 'react';
import { motion } from 'framer-motion';
import { Bus, Shield, ChevronRight, AlertCircle } from 'lucide-react';
import { getBuses, getSchedules } from '../api';

export default function DriverLogin({ onLogin }) {
  const [plate, setPlate]     = useState('');
  const [code, setCode]       = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError]     = useState('');
  const [step, setStep]       = useState(1);

  const DRIVER_CODES = {
    'ABC-123': { name: 'Juan Carlos Mamani',   company: 'Bolivia Bus Express', code: '1234' },
    'XYZ-456': { name: 'Pedro Quispe Condori', company: 'Trans Copacabana',    code: '5678' },
    'DEF-789': { name: 'Luis Flores Tarqui',   company: 'Flota Boliviana',     code: '9012' },
  };

  const handlePlate = async (e) => {
    e.preventDefault();
    const normalized = plate.toUpperCase().trim();
    if (!DRIVER_CODES[normalized]) {
      setError('Placa no registrada en el sistema');
      return;
    }
    setError('');
    setStep(2);
  };

  const handleCode = async (e) => {
    e.preventDefault();
    const normalized = plate.toUpperCase().trim();
    const driver = DRIVER_CODES[normalized];
    if (!driver || code !== driver.code) {
      setError('Codigo incorrecto');
      return;
    }
    setLoading(true);
    try {
      const [schRes, busRes] = await Promise.all([getSchedules(), getBuses()]);
      const schedules = schRes.data.schedules || [];
      const buses = busRes.data.buses || [];
      const bus = buses.find(b => b.plate === normalized);
      const mySchedules = schedules.filter(s => s.plate === normalized);
      onLogin({
        name: driver.name,
        company: driver.company,
        plate: normalized,
        bus,
        schedules: mySchedules,
      });
    } catch {
      setError('Error de conexion. Verifica el backend.');
    } finally {
      setLoading(false);
    }
  };

  const COMPANY_COLORS = {
    'Bolivia Bus Express': '#1B2A6B',
    'Trans Copacabana':    '#C8102E',
    'Flota Boliviana':     '#007A33',
  };

  const driverInfo = DRIVER_CODES[plate.toUpperCase().trim()];

  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-6 relative overflow-hidden">
      {/* Fondo animado */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -left-40 w-96 h-96 rounded-full opacity-10"
          style={{ background: 'radial-gradient(circle, #1B2A6B, transparent)' }}/>
        <div className="absolute -bottom-40 -right-40 w-96 h-96 rounded-full opacity-10"
          style={{ background: 'radial-gradient(circle, #D4AF37, transparent)' }}/>
        {[...Array(20)].map((_, i) => (
          <motion.div key={i}
            className="absolute w-1 h-1 rounded-full bg-white opacity-20"
            style={{ left: Math.random() * 100 + '%', top: Math.random() * 100 + '%' }}
            animate={{ opacity: [0.1, 0.4, 0.1], scale: [1, 1.5, 1] }}
            transition={{ duration: 2 + Math.random() * 3, repeat: Infinity, delay: Math.random() * 2 }}
          />
        ))}
      </div>

      <motion.div initial={{ opacity: 0, y: 40 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6 }}
        className="w-full max-w-sm relative z-10">

        {/* Logo */}
        <div className="text-center mb-10">
          <motion.div
            animate={{ rotate: [0, -5, 5, 0] }}
            transition={{ duration: 3, repeat: Infinity, repeatDelay: 2 }}
            className="w-20 h-20 rounded-3xl flex items-center justify-center mx-auto mb-4 shadow-2xl"
            style={{ background: 'linear-gradient(135deg, #1B2A6B, #2d45a8)' }}>
            <Bus size={40} className="text-[#D4AF37]"/>
          </motion.div>
          <h1 className="text-3xl font-black text-white">Bolivia <span className="text-[#D4AF37]">Bus</span></h1>
          <p className="text-gray-400 text-sm mt-1">Panel del Conductor</p>
        </div>

        {/* Step 1: Placa */}
        {step === 1 && (
          <motion.form onSubmit={handlePlate} initial={{ opacity: 0 }} animate={{ opacity: 1 }}
            className="glass-card p-6">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-10 h-10 rounded-xl bg-[#D4AF37]/20 flex items-center justify-center">
                <Bus size={20} className="text-[#D4AF37]"/>
              </div>
              <div>
                <p className="font-bold text-white">Identificacion del Bus</p>
                <p className="text-xs text-gray-400">Ingresa la placa de tu unidad</p>
              </div>
            </div>

            <div className="mb-4">
              <label className="text-xs font-semibold text-gray-400 uppercase tracking-wider block mb-2">
                Placa del vehiculo
              </label>
              <input
                value={plate}
                onChange={e => { setPlate(e.target.value); setError(''); }}
                placeholder="Ej: ABC-123"
                className="w-full bg-white/10 border border-white/20 rounded-xl px-4 py-4 text-white text-lg font-mono font-bold tracking-widest placeholder-gray-600 focus:outline-none focus:border-[#D4AF37] transition-colors uppercase"
                autoFocus
              />
            </div>

            {error && (
              <motion.div initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }}
                className="flex items-center gap-2 text-red-400 text-sm mb-4 bg-red-500/10 px-3 py-2 rounded-lg">
                <AlertCircle size={14}/> {error}
              </motion.div>
            )}

            <motion.button type="submit"
              whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}
              className="w-full py-4 rounded-xl font-bold text-[#1B2A6B] flex items-center justify-center gap-2 text-lg"
              style={{ background: 'linear-gradient(135deg, #D4AF37, #f0c84a)' }}>
              Continuar <ChevronRight size={20}/>
            </motion.button>

            <p className="text-center text-xs text-gray-600 mt-4">
              Placas de prueba: ABC-123 · XYZ-456 · DEF-789
            </p>
          </motion.form>
        )}

        {/* Step 2: Codigo PIN */}
        {step === 2 && (
          <motion.form onSubmit={handleCode} initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }}
            className="glass-card p-6">
            <button type="button" onClick={() => { setStep(1); setError(''); setCode(''); }}
              className="text-gray-400 text-sm mb-4 flex items-center gap-1 hover:text-white transition-colors">
              Cambiar placa
            </button>

            {driverInfo && (
              <div className="mb-5 p-3 rounded-xl" style={{ background: COMPANY_COLORS[driverInfo.company] + '30', border: '1px solid ' + COMPANY_COLORS[driverInfo.company] + '60' }}>
                <p className="text-xs text-gray-400">Conductor encontrado</p>
                <p className="font-bold text-white">{driverInfo.name}</p>
                <p className="text-sm" style={{ color: '#D4AF37' }}>{driverInfo.company} · {plate.toUpperCase()}</p>
              </div>
            )}

            <div className="flex items-center gap-3 mb-6">
              <div className="w-10 h-10 rounded-xl bg-green-500/20 flex items-center justify-center">
                <Shield size={20} className="text-green-400"/>
              </div>
              <div>
                <p className="font-bold text-white">Codigo de acceso</p>
                <p className="text-xs text-gray-400">Ingresa tu PIN de 4 digitos</p>
              </div>
            </div>

            {/* PIN Inputs */}
            <div className="flex gap-3 justify-center mb-6">
              {[0,1,2,3].map(i => (
                <div key={i}
                  className="w-14 h-14 rounded-xl border-2 flex items-center justify-center text-2xl font-black transition-all"
                  style={{ borderColor: code.length > i ? '#D4AF37' : 'rgba(255,255,255,0.15)', background: code.length > i ? 'rgba(212,175,55,0.15)' : 'rgba(255,255,255,0.05)' }}>
                  {code.length > i ? '●' : ''}
                </div>
              ))}
            </div>

            {/* Teclado numerico */}
            <div className="grid grid-cols-3 gap-3 mb-4">
              {[1,2,3,4,5,6,7,8,9,'',0,'⌫'].map((n, i) => (
                <button key={i} type="button"
                  onClick={() => {
                    if (n === '⌫') setCode(c => c.slice(0,-1));
                    else if (n !== '' && code.length < 4) setCode(c => c + n);
                    setError('');
                  }}
                  className={"h-14 rounded-xl font-bold text-xl transition-all " +
                    (n === '' ? 'invisible' : 'glass hover:bg-white/15 active:scale-95') +
                    (n === '⌫' ? ' text-red-400' : ' text-white')}>
                  {n}
                </button>
              ))}
            </div>

            {error && (
              <motion.div initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }}
                className="flex items-center gap-2 text-red-400 text-sm mb-3 bg-red-500/10 px-3 py-2 rounded-lg">
                <AlertCircle size={14}/> {error}
              </motion.div>
            )}

            <motion.button type="submit" disabled={code.length < 4 || loading}
              whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}
              className="w-full py-4 rounded-xl font-bold text-[#1B2A6B] flex items-center justify-center gap-2 text-lg disabled:opacity-40 transition-opacity"
              style={{ background: 'linear-gradient(135deg, #D4AF37, #f0c84a)' }}>
              {loading ? (
                <><div className="w-5 h-5 border-2 border-[#1B2A6B] border-t-transparent rounded-full animate-spin"/> Verificando...</>
              ) : (
                <><Shield size={18}/> Ingresar al Sistema</>
              )}
            </motion.button>
          </motion.form>
        )}
      </motion.div>
    </div>
  );
}
"""

# ── Dashboard.jsx ────────────────────────────────────────────────────────────
dashboard_jsx = r"""import { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Bus, Users, MapPin, Clock, ChevronRight, Wifi, WifiOff, LogOut, Grid, List, Share2, Bell } from 'lucide-react';
import { getPassengers, getSeatMap, WS_URL } from '../api';
import PassengerList from './PassengerList';
import SeatOverview from './SeatOverview';
import ShareRoute from './ShareRoute';

const COMPANY_COLORS = {
  'Bolivia Bus Express': { primary: '#1B2A6B', accent: '#D4AF37' },
  'Trans Copacabana':    { primary: '#C8102E', accent: '#FFFFFF' },
  'Flota Boliviana':     { primary: '#007A33', accent: '#F4D03F' },
};

export default function Dashboard({ driver, onLogout }) {
  const [tab, setTab]               = useState('passengers');
  const [passengers, setPassengers] = useState([]);
  const [seats, setSeats]           = useState([]);
  const [loading, setLoading]       = useState(true);
  const [connected, setConnected]   = useState(false);
  const [busData, setBusData]       = useState(null);
  const [showShare, setShowShare]   = useState(false);
  const [lastUpdate, setLastUpdate] = useState(null);
  const wsRef = useRef(null);

  const schedule = driver.schedules?.[0];
  const colors   = COMPANY_COLORS[driver.company] || { primary: '#1B2A6B', accent: '#D4AF37' };

  useEffect(() => {
    if (!schedule) { setLoading(false); return; }
    Promise.all([
      getPassengers(schedule.id),
      getSeatMap(schedule.id),
    ]).then(([pRes, sRes]) => {
      setPassengers(pRes.data.bookings || []);
      setSeats(sRes.data.seats || []);
    }).catch(() => {}).finally(() => setLoading(false));

    // WebSocket GPS
    const ws = new WebSocket(WS_URL);
    wsRef.current = ws;
    ws.onopen  = () => setConnected(true);
    ws.onclose = () => setConnected(false);
    ws.onmessage = (e) => {
      const data = JSON.parse(e.data);
      if (data.type === 'location_update' && data.plate === driver.plate) {
        setBusData(data);
        setLastUpdate(new Date());
      }
    };
    return () => ws.close();
  }, [schedule]);

  const confirmed  = passengers.filter(p => p.status === 'confirmed');
  const pending    = passengers.filter(p => p.status === 'pending');
  const totalSeats = seats.length || 40;
  const occupied   = seats.filter(s => s.status === 'occupied').length;
  const available  = seats.filter(s => s.status === 'available').length;
  const occupancy  = totalSeats > 0 ? Math.round((occupied / totalSeats) * 100) : 0;

  const fmt = (dt) => dt ? new Date(dt).toLocaleTimeString('es-BO', { hour: '2-digit', minute: '2-digit' }) : '--:--';

  const TABS = [
    { id: 'passengers', label: 'Pasajeros', icon: Users,  count: passengers.length },
    { id: 'seats',      label: 'Asientos',  icon: Grid,   count: null },
    { id: 'route',      label: 'Mi Ruta',   icon: MapPin, count: null },
  ];

  return (
    <div className="min-h-screen flex flex-col max-w-md mx-auto">
      {/* Header */}
      <div className="relative overflow-hidden px-5 pt-12 pb-6"
        style={{ background: `linear-gradient(135deg, ${colors.primary}, ${colors.primary}dd)` }}>
        {/* Decoracion fondo */}
        <div className="absolute -top-10 -right-10 w-40 h-40 rounded-full opacity-10"
          style={{ background: colors.accent }}/>
        <div className="absolute -bottom-6 -left-6 w-28 h-28 rounded-full opacity-10"
          style={{ background: colors.accent }}/>

        <div className="relative z-10">
          <div className="flex items-center justify-between mb-5">
            <div className="flex items-center gap-3">
              <div className="w-11 h-11 rounded-2xl flex items-center justify-center"
                style={{ background: colors.accent + '30', border: '1.5px solid ' + colors.accent + '60' }}>
                <Bus size={22} style={{ color: colors.accent }}/>
              </div>
              <div>
                <p className="text-white/60 text-xs">Bolivia Bus</p>
                <p className="text-white font-black text-base leading-tight">{driver.company}</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <div className={"flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-bold " +
                (connected ? "bg-green-500/20 text-green-300" : "bg-red-500/20 text-red-300")}>
                {connected ? <Wifi size={11}/> : <WifiOff size={11}/>}
                {connected ? "GPS" : "Sin GPS"}
              </div>
              <button onClick={onLogout}
                className="w-9 h-9 rounded-xl flex items-center justify-center bg-white/10 hover:bg-white/20 transition-all">
                <LogOut size={16} className="text-white/70"/>
              </button>
            </div>
          </div>

          {/* Info del conductor */}
          <div className="mb-5">
            <p className="text-white/50 text-xs mb-0.5">Conductor</p>
            <p className="text-white font-black text-xl">{driver.name}</p>
            <div className="flex items-center gap-3 mt-1">
              <span className="text-xs px-2 py-0.5 rounded-full font-bold" style={{ background: colors.accent + '30', color: colors.accent }}>
                {driver.plate}
              </span>
              {schedule && (
                <span className="text-white/50 text-xs flex items-center gap-1">
                  <Clock size={10}/> {fmt(schedule.departure_time)} → {fmt(schedule.arrival_time)}
                </span>
              )}
            </div>
          </div>

          {/* Ruta */}
          {schedule ? (
            <div className="glass rounded-2xl p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-white/50 text-xs mb-1">Ruta de hoy</p>
                  <div className="flex items-center gap-2">
                    <span className="text-white font-black text-lg">{schedule.origin}</span>
                    <ChevronRight size={16} style={{ color: colors.accent }}/>
                    <span className="text-white font-black text-lg">{schedule.destination}</span>
                  </div>
                </div>
                <button onClick={() => setShowShare(true)}
                  className="w-10 h-10 rounded-xl flex items-center justify-center"
                  style={{ background: colors.accent + '20', border: '1px solid ' + colors.accent + '40' }}>
                  <Share2 size={16} style={{ color: colors.accent }}/>
                </button>
              </div>
            </div>
          ) : (
            <div className="glass rounded-2xl p-4 text-center">
              <p className="text-white/50 text-sm">Sin horario asignado hoy</p>
            </div>
          )}
        </div>
      </div>

      {/* Stats */}
      <div className="px-4 -mt-1 mb-4">
        <div className="grid grid-cols-3 gap-3">
          {[
            { label: 'Pasajeros', value: confirmed.length, sub: pending.length + ' pendientes', color: '#3b82f6' },
            { label: 'Ocupacion', value: occupancy + '%',  sub: occupied + '/' + totalSeats + ' asientos', color: colors.primary },
            { label: 'Disponibles', value: available,      sub: 'asientos libres', color: '#22c55e' },
          ].map((stat, i) => (
            <motion.div key={stat.label}
              initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.1 }}
              className="glass-card p-3 text-center">
              <p className="text-2xl font-black" style={{ color: stat.color }}>{stat.value}</p>
              <p className="text-white text-xs font-semibold">{stat.label}</p>
              <p className="text-white/40 text-[10px] mt-0.5">{stat.sub}</p>
            </motion.div>
          ))}
        </div>
      </div>

      {/* GPS live info */}
      {busData && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}
          className="mx-4 mb-4 glass-card p-3 flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-green-500/20 flex items-center justify-center">
            <MapPin size={16} className="text-green-400"/>
          </div>
          <div className="flex-1">
            <p className="text-white text-xs font-semibold">GPS en vivo</p>
            <p className="text-white/50 text-[10px]">{busData.speed_kmh} km/h · {busData.latitude?.toFixed(4)}, {busData.longitude?.toFixed(4)}</p>
          </div>
          <div className="w-2 h-2 rounded-full bg-green-400 animate-pulse"/>
        </motion.div>
      )}

      {/* Tabs */}
      <div className="px-4 mb-4">
        <div className="glass rounded-2xl p-1 flex gap-1">
          {TABS.map(t => (
            <button key={t.id} onClick={() => setTab(t.id)}
              className={"flex-1 flex items-center justify-center gap-1.5 py-2.5 rounded-xl text-xs font-bold transition-all " +
                (tab === t.id ? "bg-white text-[#1B2A6B]" : "text-white/50 hover:text-white")}>
              <t.icon size={14}/>
              {t.label}
              {t.count !== null && t.count > 0 && (
                <span className={"text-[10px] px-1.5 rounded-full font-black " +
                  (tab === t.id ? "bg-[#1B2A6B] text-white" : "bg-white/20 text-white")}>
                  {t.count}
                </span>
              )}
            </button>
          ))}
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 px-4 pb-8 overflow-y-auto">
        <AnimatePresence mode="wait">
          {tab === 'passengers' && (
            <motion.div key="passengers" initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }}>
              <PassengerList passengers={passengers} loading={loading} colors={colors}/>
            </motion.div>
          )}
          {tab === 'seats' && (
            <motion.div key="seats" initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }}>
              <SeatOverview seats={seats} loading={loading} colors={colors}/>
            </motion.div>
          )}
          {tab === 'route' && (
            <motion.div key="route" initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }}>
              <RouteInfo schedule={schedule} driver={driver} busData={busData} colors={colors}/>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Share Modal */}
      <AnimatePresence>
        {showShare && (
          <ShareRoute schedule={schedule} passengers={passengers} driver={driver} onClose={() => setShowShare(false)}/>
        )}
      </AnimatePresence>
    </div>
  );
}

function RouteInfo({ schedule, driver, busData, colors }) {
  if (!schedule) return (
    <div className="text-center py-12">
      <MapPin size={40} className="text-white/20 mx-auto mb-3"/>
      <p className="text-white/40">Sin ruta asignada hoy</p>
    </div>
  );

  const fmt = (dt) => new Date(dt).toLocaleTimeString('es-BO', { hour: '2-digit', minute: '2-digit' });
  const fmtDate = (dt) => new Date(dt).toLocaleDateString('es-BO', { weekday: 'long', day: 'numeric', month: 'long' });

  return (
    <div className="flex flex-col gap-4">
      <div className="glass-card p-5">
        <p className="text-white/50 text-xs mb-3 uppercase tracking-wider">Informacion del viaje</p>
        <div className="flex items-center gap-4 mb-4">
          <div className="text-center">
            <p className="text-white font-black text-2xl">{fmt(schedule.departure_time)}</p>
            <p className="text-white/50 text-xs mt-0.5">{schedule.origin}</p>
          </div>
          <div className="flex-1 flex flex-col items-center gap-1">
            <div className="w-full h-px bg-white/20 relative">
              <motion.div className="absolute top-0 left-0 h-full"
                style={{ background: colors.accent }}
                initial={{ width: '0%' }} animate={{ width: '60%' }} transition={{ duration: 2, ease: 'easeInOut' }}/>
            </div>
            <p className="text-white/40 text-[10px]">{schedule.duration_hours || '?'}h de viaje</p>
          </div>
          <div className="text-center">
            <p className="text-white font-black text-2xl">{fmt(schedule.arrival_time)}</p>
            <p className="text-white/50 text-xs mt-0.5">{schedule.destination}</p>
          </div>
        </div>
        <p className="text-white/30 text-xs text-center">{fmtDate(schedule.departure_time)}</p>
      </div>

      <div className="glass-card p-5">
        <p className="text-white/50 text-xs mb-3 uppercase tracking-wider">Mi unidad</p>
        <div className="grid grid-cols-2 gap-3">
          {[
            { label: 'Placa',   value: driver.plate },
            { label: 'Tipo',    value: (schedule.bus_type || 'normal').toUpperCase() },
            { label: 'Normal',  value: 'Bs. ' + schedule.price_normal },
            { label: 'Cama',    value: 'Bs. ' + (schedule.price_cama || '-') },
          ].map(item => (
            <div key={item.label} className="bg-white/5 rounded-xl p-3">
              <p className="text-white/40 text-[10px]">{item.label}</p>
              <p className="text-white font-bold text-sm">{item.value}</p>
            </div>
          ))}
        </div>
      </div>

      {busData && (
        <div className="glass-card p-5">
          <p className="text-white/50 text-xs mb-3 uppercase tracking-wider">GPS en tiempo real</p>
          <div className="grid grid-cols-2 gap-3">
            <div className="bg-green-500/10 rounded-xl p-3 border border-green-500/20">
              <p className="text-green-400/60 text-[10px]">Velocidad</p>
              <p className="text-green-400 font-black text-xl">{busData.speed_kmh} <span className="text-sm font-normal">km/h</span></p>
            </div>
            <div className="bg-blue-500/10 rounded-xl p-3 border border-blue-500/20">
              <p className="text-blue-400/60 text-[10px]">Estado</p>
              <p className="text-blue-400 font-bold text-sm capitalize">{busData.status || 'en ruta'}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
"""

# ── PassengerList.jsx ────────────────────────────────────────────────────────
passengers_jsx = r"""import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Users, Search, User, CheckCircle, Clock, ChevronDown, Phone, Hash } from 'lucide-react';

const STATUS_CONFIG = {
  confirmed: { label: 'Confirmado', color: '#22c55e', bg: 'rgba(34,197,94,0.15)', icon: CheckCircle },
  pending:   { label: 'Pendiente',  color: '#f59e0b', bg: 'rgba(245,158,11,0.15)', icon: Clock },
  cancelled: { label: 'Cancelado',  color: '#ef4444', bg: 'rgba(239,68,68,0.15)',  icon: Clock },
};

export default function PassengerList({ passengers, loading, colors }) {
  const [search, setSearch]     = useState('');
  const [filter, setFilter]     = useState('all');
  const [expanded, setExpanded] = useState(null);

  if (loading) return (
    <div className="flex flex-col gap-3">
      {[1,2,3,4].map(i => (
        <div key={i} className="glass-card p-4 animate-pulse">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-white/10"/>
            <div className="flex-1">
              <div className="h-3 bg-white/10 rounded w-32 mb-2"/>
              <div className="h-2 bg-white/10 rounded w-20"/>
            </div>
          </div>
        </div>
      ))}
    </div>
  );

  if (passengers.length === 0) return (
    <div className="text-center py-16">
      <div className="w-16 h-16 rounded-2xl bg-white/5 flex items-center justify-center mx-auto mb-4">
        <Users size={28} className="text-white/20"/>
      </div>
      <p className="text-white/40 font-semibold">Sin pasajeros aun</p>
      <p className="text-white/20 text-sm mt-1">Los pasajeros apareceran aqui</p>
    </div>
  );

  const filtered = passengers.filter(p => {
    const matchSearch = p.passenger_name.toLowerCase().includes(search.toLowerCase()) ||
                        p.passenger_ci?.includes(search) ||
                        p.seat_number?.includes(search);
    const matchFilter = filter === 'all' || p.status === filter;
    return matchSearch && matchFilter;
  });

  return (
    <div>
      {/* Busqueda */}
      <div className="relative mb-3">
        <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-white/30"/>
        <input value={search} onChange={e => setSearch(e.target.value)}
          placeholder="Buscar por nombre, CI o asiento..."
          className="w-full bg-white/5 border border-white/10 rounded-xl pl-9 pr-4 py-3 text-white text-sm placeholder-white/20 focus:outline-none focus:border-white/30 transition-colors"/>
      </div>

      {/* Filtros */}
      <div className="flex gap-2 mb-4">
        {[
          { id: 'all',       label: 'Todos ' + passengers.length },
          { id: 'confirmed', label: 'Confirmados' },
          { id: 'pending',   label: 'Pendientes' },
        ].map(f => (
          <button key={f.id} onClick={() => setFilter(f.id)}
            className={"text-xs px-3 py-1.5 rounded-full font-bold transition-all " +
              (filter === f.id ? "text-[#1B2A6B] bg-[#D4AF37]" : "text-white/50 bg-white/5 hover:bg-white/10")}>
            {f.label}
          </button>
        ))}
      </div>

      {/* Lista */}
      <div className="flex flex-col gap-2">
        <AnimatePresence>
          {filtered.map((p, i) => {
            const cfg = STATUS_CONFIG[p.status] || STATUS_CONFIG.pending;
            const StatusIcon = cfg.icon;
            const isOpen = expanded === p.id;
            return (
              <motion.div key={p.id}
                initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.04 }}
                className="glass-card overflow-hidden cursor-pointer"
                onClick={() => setExpanded(isOpen ? null : p.id)}>
                <div className="p-4 flex items-center gap-3">
                  {/* Avatar */}
                  <div className="w-10 h-10 rounded-xl flex items-center justify-center font-black text-lg shrink-0"
                    style={{ background: colors.primary + '40', color: colors.accent }}>
                    {p.passenger_name.charAt(0)}
                  </div>

                  {/* Info */}
                  <div className="flex-1 min-w-0">
                    <p className="text-white font-bold text-sm truncate">{p.passenger_name}</p>
                    <div className="flex items-center gap-2 mt-0.5">
                      <span className="text-white/40 text-[11px]">Asiento {p.seat_number}</span>
                      <span className="text-white/20 text-[11px]">·</span>
                      <span className="text-white/40 text-[11px]">Piso {p.floor}</span>
                    </div>
                  </div>

                  {/* Status + expand */}
                  <div className="flex items-center gap-2 shrink-0">
                    <div className="flex items-center gap-1 px-2 py-1 rounded-full text-[10px] font-bold"
                      style={{ background: cfg.bg, color: cfg.color }}>
                      <StatusIcon size={10}/>
                      {cfg.label}
                    </div>
                    <motion.div animate={{ rotate: isOpen ? 180 : 0 }} transition={{ duration: 0.2 }}>
                      <ChevronDown size={14} className="text-white/30"/>
                    </motion.div>
                  </div>
                </div>

                {/* Expandido */}
                <AnimatePresence>
                  {isOpen && (
                    <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }}
                      exit={{ height: 0, opacity: 0 }} transition={{ duration: 0.2 }}
                      className="border-t border-white/10 px-4 pb-4 pt-3 bg-white/5">
                      <div className="grid grid-cols-2 gap-3">
                        <div>
                          <p className="text-white/30 text-[10px] flex items-center gap-1"><Hash size={9}/> CI / Carnet</p>
                          <p className="text-white font-semibold text-sm">{p.passenger_ci || '-'}</p>
                        </div>
                        <div>
                          <p className="text-white/30 text-[10px]">Total pagado</p>
                          <p className="text-white font-black text-sm" style={{ color: colors.accent }}>Bs. {p.total_price}</p>
                        </div>
                        <div>
                          <p className="text-white/30 text-[10px]">Reservado el</p>
                          <p className="text-white font-semibold text-xs">{p.created_at ? new Date(p.created_at).toLocaleDateString('es-BO') : '-'}</p>
                        </div>
                        <div>
                          <p className="text-white/30 text-[10px]">Piso</p>
                          <p className="text-white font-semibold text-sm">Piso {p.floor}</p>
                        </div>
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </motion.div>
            );
          })}
        </AnimatePresence>
      </div>
    </div>
  );
}
"""

# ── SeatOverview.jsx ─────────────────────────────────────────────────────────
seats_jsx = r"""import { motion } from 'framer-motion';
import { Grid } from 'lucide-react';

const STATUS_COLORS = {
  available: { body: 'rgba(27,42,107,0.5)',  border: '#4B6BDB', text: '#7B9EFF' },
  occupied:  { body: 'rgba(239,68,68,0.25)', border: '#ef4444', text: '#fca5a5' },
  reserved:  { body: 'rgba(245,158,11,0.2)', border: '#f59e0b', text: '#fcd34d' },
};

function SeatSVG({ status, seatNum }) {
  const c = STATUS_COLORS[status] || STATUS_COLORS.available;
  return (
    <svg width="40" height="44" viewBox="0 0 48 52" xmlns="http://www.w3.org/2000/svg">
      <rect x="6" y="2" width="36" height="24" rx="6" fill={c.body} stroke={c.border} strokeWidth="2"/>
      <rect x="10" y="4" width="28" height="7" rx="3" fill={c.border} opacity="0.2"/>
      <rect x="4" y="24" width="40" height="15" rx="5" fill={c.body} stroke={c.border} strokeWidth="2"/>
      <rect x="1" y="22" width="5" height="17" rx="3" fill={c.border} opacity="0.25"/>
      <rect x="42" y="22" width="5" height="17" rx="3" fill={c.border} opacity="0.25"/>
      <text x="24" y="35" textAnchor="middle" fontSize="8" fontWeight="bold" fill={c.text}>{seatNum}</text>
    </svg>
  );
}

export default function SeatOverview({ seats, loading, colors }) {
  if (loading) return (
    <div className="glass-card p-6 animate-pulse">
      <div className="grid grid-cols-4 gap-2">
        {[...Array(16)].map((_,i) => <div key={i} className="h-12 bg-white/10 rounded-xl"/>)}
      </div>
    </div>
  );

  const available = seats.filter(s => s.status === 'available').length;
  const occupied  = seats.filter(s => s.status === 'occupied').length;
  const reserved  = seats.filter(s => s.status === 'reserved').length;

  const floors = [...new Set(seats.map(s => s.floor))].sort();

  return (
    <div className="flex flex-col gap-4">
      {/* Resumen */}
      <div className="grid grid-cols-3 gap-3">
        {[
          { label: 'Libres',     value: available, color: '#4B6BDB', border: '#4B6BDB' },
          { label: 'Ocupados',   value: occupied,  color: '#ef4444', border: '#ef4444' },
          { label: 'Reservados', value: reserved,  color: '#f59e0b', border: '#f59e0b' },
        ].map(s => (
          <div key={s.label} className="glass-card p-3 text-center" style={{ borderColor: s.border + '40' }}>
            <p className="text-2xl font-black" style={{ color: s.color }}>{s.value}</p>
            <p className="text-white/50 text-[11px]">{s.label}</p>
          </div>
        ))}
      </div>

      {/* Leyenda */}
      <div className="flex gap-3 flex-wrap">
        {[
          { label: 'Disponible', color: '#4B6BDB' },
          { label: 'Ocupado',    color: '#ef4444' },
          { label: 'Reservado',  color: '#f59e0b' },
        ].map(l => (
          <div key={l.label} className="flex items-center gap-1.5 text-xs text-white/50">
            <div className="w-3 h-3 rounded" style={{ background: l.color + '50', border: '1.5px solid ' + l.color }}/>
            {l.label}
          </div>
        ))}
      </div>

      {/* Pisos */}
      {floors.map(floor => {
        const floorSeats = seats.filter(s => s.floor === floor);
        const rows = {};
        floorSeats.forEach(s => { if (!rows[s.row]) rows[s.row] = []; rows[s.row].push(s); });
        return (
          <div key={floor} className="glass-card p-4">
            <div className="text-center text-xs font-bold text-white/40 uppercase tracking-widest mb-4 pb-2 border-b border-white/10">
              Frente del Bus — Piso {floor}
            </div>
            <div className="flex flex-col gap-2">
              {Object.entries(rows).sort((a,b) => +a[0] - +b[0]).map(([row, rowSeats]) => (
                <div key={row} className="flex gap-2 justify-center items-center">
                  <span className="text-white/20 text-[10px] w-3 text-center">{row}</span>
                  {rowSeats.sort((a,b) => a.column - b.column).map((s, i) => (
                    <div key={s.id}>
                      {i === 1 && <div className="w-4"/>}
                      <motion.div whileHover={{ scale: 1.1, y: -2 }} transition={{ type: 'spring', stiffness: 400 }}>
                        <SeatSVG status={s.status} seatNum={s.seat_number}/>
                      </motion.div>
                    </div>
                  ))}
                </div>
              ))}
            </div>
          </div>
        );
      })}

      {seats.length === 0 && (
        <div className="text-center py-12">
          <Grid size={36} className="text-white/20 mx-auto mb-3"/>
          <p className="text-white/30 text-sm">Sin datos de asientos</p>
        </div>
      )}
    </div>
  );
}
"""

# ── ShareRoute.jsx ───────────────────────────────────────────────────────────
share_jsx = r"""import { motion } from 'framer-motion';
import { X, Share2, MessageCircle, Users, Copy, Check } from 'lucide-react';
import { useState } from 'react';

export default function ShareRoute({ schedule, passengers, driver, onClose }) {
  const [copied, setCopied] = useState(false);

  if (!schedule) return null;

  const fmt = (dt) => new Date(dt).toLocaleTimeString('es-BO', { hour: '2-digit', minute: '2-digit' });
  const confirmed = passengers.filter(p => p.status === 'confirmed');

  const routeMsg =
    "Bolivia Bus - Informacion de Viaje\n\n" +
    "Ruta: " + schedule.origin + " -> " + schedule.destination + "\n" +
    "Salida: " + fmt(schedule.departure_time) + "\n" +
    "Llegada estimada: " + fmt(schedule.arrival_time) + "\n" +
    "Empresa: " + driver.company + "\n" +
    "Bus: " + driver.plate + "\n\n" +
    "Pasajeros confirmados: " + confirmed.length + "\n\n" +
    "Rastreo en tiempo real: http://boliviabus.bo/track/" + driver.plate + "\n\n" +
    "Bolivia Bus - Sistema Nacional de Pasajes";

  const handleShareAll = () => {
    const encoded = encodeURIComponent(routeMsg);
    window.open("https://wa.me/?text=" + encoded, "_blank");
  };

  const handleSharePassenger = (p) => {
    const msg =
      "Bolivia Bus - Tu viaje esta confirmado!\n\n" +
      "Pasajero: " + p.passenger_name + "\n" +
      "Ruta: " + schedule.origin + " -> " + schedule.destination + "\n" +
      "Salida: " + fmt(schedule.departure_time) + "\n" +
      "Asiento: " + p.seat_number + " (Piso " + p.floor + ")\n" +
      "Empresa: " + driver.company + "\n\n" +
      "Rastreo: http://boliviabus.bo/track/" + driver.plate + "\n\n" +
      "Buen viaje!";
    window.open("https://wa.me/?text=" + encodeURIComponent(msg), "_blank");
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(routeMsg).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  };

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
      className="fixed inset-0 z-50 flex items-end justify-center"
      style={{ background: 'rgba(0,0,0,0.7)', backdropFilter: 'blur(8px)' }}
      onClick={onClose}>
      <motion.div initial={{ y: 100 }} animate={{ y: 0 }} exit={{ y: 100 }}
        transition={{ type: 'spring', bounce: 0.2 }}
        className="w-full max-w-md glass-card rounded-b-none rounded-t-3xl p-6 pb-10"
        onClick={e => e.stopPropagation()}>

        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-green-500/20 flex items-center justify-center">
              <Share2 size={18} className="text-green-400"/>
            </div>
            <div>
              <p className="text-white font-black">Compartir Ruta</p>
              <p className="text-white/40 text-xs">{schedule.origin} → {schedule.destination}</p>
            </div>
          </div>
          <button onClick={onClose} className="w-8 h-8 rounded-full bg-white/10 flex items-center justify-center">
            <X size={16} className="text-white/60"/>
          </button>
        </div>

        {/* Acciones principales */}
        <div className="flex flex-col gap-3 mb-6">
          <motion.button whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}
            onClick={handleShareAll}
            className="flex items-center gap-3 p-4 rounded-2xl font-bold text-white transition-all"
            style={{ background: 'linear-gradient(135deg, #25D366, #128C7E)' }}>
            <div className="w-10 h-10 rounded-xl bg-white/20 flex items-center justify-center">
              <MessageCircle size={20}/>
            </div>
            <div className="text-left">
              <p className="font-black">WhatsApp — Info de ruta</p>
              <p className="text-white/70 text-xs font-normal">Compartir horario y placa del bus</p>
            </div>
          </motion.button>

          <motion.button whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}
            onClick={handleCopy}
            className="flex items-center gap-3 p-4 rounded-2xl bg-white/10 border border-white/15 font-bold text-white">
            <div className="w-10 h-10 rounded-xl bg-white/10 flex items-center justify-center">
              {copied ? <Check size={20} className="text-green-400"/> : <Copy size={20}/>}
            </div>
            <div className="text-left">
              <p className="font-black">{copied ? 'Copiado!' : 'Copiar mensaje'}</p>
              <p className="text-white/50 text-xs font-normal">Para pegar en cualquier app</p>
            </div>
          </motion.button>
        </div>

        {/* Pasajeros individuales */}
        {confirmed.length > 0 && (
          <div>
            <div className="flex items-center gap-2 mb-3">
              <Users size={14} className="text-white/40"/>
              <p className="text-white/40 text-xs uppercase tracking-wider font-semibold">
                Enviar a pasajero individual
              </p>
            </div>
            <div className="flex flex-col gap-2 max-h-52 overflow-y-auto">
              {confirmed.map(p => (
                <button key={p.id} onClick={() => handleSharePassenger(p)}
                  className="flex items-center gap-3 p-3 rounded-xl bg-white/5 hover:bg-white/10 transition-all text-left">
                  <div className="w-8 h-8 rounded-lg bg-[#1B2A6B]/60 flex items-center justify-center text-[#D4AF37] font-black text-sm shrink-0">
                    {p.passenger_name.charAt(0)}
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-white font-semibold text-sm truncate">{p.passenger_name}</p>
                    <p className="text-white/30 text-[11px]">Asiento {p.seat_number}</p>
                  </div>
                  <MessageCircle size={14} className="text-green-400 shrink-0"/>
                </button>
              ))}
            </div>
          </div>
        )}
      </motion.div>
    </motion.div>
  );
}
"""

# ── App.jsx ──────────────────────────────────────────────────────────────────
app_jsx = r"""import { useState } from 'react';
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
"""

# Escribir todos los archivos
files = {
    "src/index.css":                    index_css,
    "src/api.js":                       api_js,
    "src/main.jsx":                     main_jsx,
    "src/App.jsx":                      app_jsx,
    "src/components/DriverLogin.jsx":   login_jsx,
    "src/components/Dashboard.jsx":     dashboard_jsx,
    "src/components/PassengerList.jsx": passengers_jsx,
    "src/components/SeatOverview.jsx":  seats_jsx,
    "src/components/ShareRoute.jsx":    share_jsx,
}

for path, content in files.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("OK:", path)

print("\nApp del Chofer lista!")