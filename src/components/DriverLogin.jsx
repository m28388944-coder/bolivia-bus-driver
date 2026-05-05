import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Bus, Shield, ChevronRight, AlertCircle, Star } from 'lucide-react';
import API from '../api';

const DRIVER_CODES = {
  'B-1234': { name: 'Juan Carlos Mamani',   company: 'Flota Bolivar',       pin: '1234', color: '#E63946' },
  'B-5678': { name: 'Pedro Quispe Condori', company: 'Trans Copacabana',    pin: '5678', color: '#1D3557' },
  'B-9012': { name: 'Luis Flores Tarqui',   company: 'Flota Cosmos',        pin: '9012', color: '#2A9D8F' },
  'B-2468': { name: 'Mario Condori Ticona', company: 'Flota Bolivar',       pin: '2468', color: '#E63946' },
  'B-3456': { name: 'Carlos Mamani Lima',   company: 'Concordia',           pin: '3456', color: '#E9C46A' },
  'B-7890': { name: 'Roberto Flores Paz',   company: 'Bolivia Bus Express', pin: '7890', color: '#6A0572' },
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
    if (!DRIVER_CODES[normalized]) { setError('Placa no registrada en el sistema'); return; }
    setError(''); setStep(2);
  };

  const handleCode = async (e) => {
    e.preventDefault();
    const normalized = plate.toUpperCase().trim();
    const driver = DRIVER_CODES[normalized];
    if (!driver || code !== driver.pin) { setError('PIN incorrecto'); return; }
    setLoading(true);
    try {
      const today = new Date().toISOString().split('T')[0];
      const res = await API.get('/schedules/?fecha=' + today);
      const data = res.data;
      const lista = Array.isArray(data) ? data : (data.value || data.items || []);
      const today = new Date().toISOString().split('T')[0];
      const mySchedules = lista.filter(s =>
        s.bus?.placa === normalized && s.hora_salida?.startsWith(today)
      ).map(s => ({
        id: s.id,
        departure_time:  s.hora_salida,
        arrival_time:    s.hora_llegada_est,
        origin:          s.ruta?.origen || '',
        destination:     s.ruta?.destino || '',
        duration_hours:  s.ruta?.duracion_min ? (s.ruta.duracion_min / 60).toFixed(1) : '?',
        price_normal:    s.precio_base,
        bus_type:        s.bus?.tipo || 'normal',
        available_seats: s.asientos_disponibles,
        _raw: s,
      }));
      onLogin({ name: driver.name, company: driver.company, plate: normalized, color: driver.color, schedules: mySchedules });
    } catch {
      setError('Error de conexion. Verifica el backend.');
    } finally {
      setLoading(false);
    }
  };

  const driverInfo = DRIVER_CODES[plate.toUpperCase().trim()];
  const addDigit = (n) => { if (code.length < 4) { setCode(c => c + n); setError(''); } };
  const delDigit = () => setCode(c => c.slice(0, -1));

  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-6 relative overflow-hidden"
      style={{ background: 'linear-gradient(135deg, #060d1f 0%, #0d1a3a 60%, #060d1f 100%)' }}>

      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <motion.div className="absolute top-1/4 left-1/4 w-96 h-96 rounded-full"
          style={{ background: 'radial-gradient(circle, rgba(27,42,107,0.3), transparent 70%)' }}
          animate={{ scale: [1, 1.2, 1], opacity: [0.3, 0.5, 0.3] }}
          transition={{ duration: 6, repeat: Infinity }}/>
        <motion.div className="absolute bottom-1/4 right-1/4 w-80 h-80 rounded-full"
          style={{ background: 'radial-gradient(circle, rgba(212,175,55,0.15), transparent 70%)' }}
          animate={{ scale: [1.2, 1, 1.2], opacity: [0.2, 0.4, 0.2] }}
          transition={{ duration: 8, repeat: Infinity }}/>
        {[...Array(20)].map((_, i) => (
          <motion.div key={i} className="absolute rounded-full"
            style={{ width: 2+(i%3), height: 2+(i%3), left: (i*37)%100+'%', top: (i*23)%100+'%',
              background: i%3===0 ? '#D4AF37' : 'white', opacity: 0.15 }}
            animate={{ opacity: [0.05, 0.3, 0.05], y: [-5, 5, -5] }}
            transition={{ duration: 3+(i%4), repeat: Infinity, delay: i*0.2 }}/>
        ))}
      </div>

      <motion.div initial={{ opacity: 0, y: 40 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.7 }}
        className="w-full max-w-sm relative z-10">

        <div className="text-center mb-8">
          <motion.div animate={{ y: [0, -8, 0] }} transition={{ duration: 3, repeat: Infinity, ease: 'easeInOut' }}
            className="relative inline-block mb-5">
            <div className="w-24 h-24 rounded-3xl flex items-center justify-center mx-auto shadow-2xl"
              style={{ background: 'linear-gradient(135deg, #1B2A6B, #2d45a8)' }}>
              <Bus size={44} color="#D4AF37"/>
            </div>
            <motion.div className="absolute -top-1 -right-1 w-7 h-7 rounded-full flex items-center justify-center"
              style={{ background: 'linear-gradient(135deg, #D4AF37, #f0c84a)' }}
              animate={{ rotate: 360 }} transition={{ duration: 8, repeat: Infinity, ease: 'linear' }}>
              <Star size={14} color="#1B2A6B" fill="#1B2A6B"/>
            </motion.div>
          </motion.div>
          <h1 className="text-4xl font-black text-white mb-1">Bolivia <span style={{ color: '#D4AF37' }}>Bus</span></h1>
          <p className="text-sm font-semibold" style={{ color: 'rgba(255,255,255,0.4)' }}>Panel del Conductor</p>
          <div className="flex items-center justify-center gap-2 mt-2">
            <div className="h-px w-12" style={{ background: 'linear-gradient(to right, transparent, rgba(212,175,55,0.5))' }}/>
            <span className="text-xs" style={{ color: 'rgba(212,175,55,0.6)' }}>ACCESO SEGURO</span>
            <div className="h-px w-12" style={{ background: 'linear-gradient(to left, transparent, rgba(212,175,55,0.5))' }}/>
          </div>
        </div>

        <AnimatePresence mode="wait">
          {step === 1 && (
            <motion.form key="step1" onSubmit={handlePlate}
              initial={{ opacity: 0, x: -30 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: 30 }}
              className="p-7 rounded-3xl"
              style={{ background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.1)', boxShadow: '0 25px 60px rgba(0,0,0,0.5)' }}>

              <div className="flex items-center gap-3 mb-6">
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
                className="w-full rounded-2xl px-5 py-4 text-white text-xl font-black tracking-widest placeholder-white/20 focus:outline-none transition-all uppercase mb-3"
                style={{ background: 'rgba(255,255,255,0.07)', border: plate ? '2px solid #D4AF37' : '2px solid rgba(255,255,255,0.1)' }}
                autoFocus/>

              <AnimatePresence>
                {error && (
                  <motion.div initial={{ opacity: 0, y: -5 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }}
                    className="flex items-center gap-2 text-sm mb-3 px-4 py-2.5 rounded-xl"
                    style={{ background: 'rgba(239,68,68,0.12)', color: '#fca5a5', border: '1px solid rgba(239,68,68,0.2)' }}>
                    <AlertCircle size={14}/> {error}
                  </motion.div>
                )}
              </AnimatePresence>

              <motion.button type="submit" whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.97 }}
                className="w-full py-4 rounded-2xl font-black text-lg flex items-center justify-center gap-2 mt-2"
                style={{ background: 'linear-gradient(135deg, #D4AF37, #f0c84a)', color: '#1B2A6B', boxShadow: '0 8px 30px rgba(212,175,55,0.3)' }}>
                Continuar <ChevronRight size={20}/>
              </motion.button>

              <div className="mt-5 p-3 rounded-xl"
                style={{ background: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.06)' }}>
                <p className="text-xs mb-2 text-center" style={{ color: 'rgba(255,255,255,0.25)' }}>Placas disponibles</p>
                <div className="flex flex-wrap justify-center gap-2">
                  {Object.keys(DRIVER_CODES).map(p => (
                    <button key={p} type="button" onClick={() => setPlate(p)}
                      className="text-xs px-2.5 py-1.5 rounded-lg font-mono font-bold transition-all hover:scale-105"
                      style={{ background: 'rgba(212,175,55,0.1)', color: '#D4AF37', border: '1px solid rgba(212,175,55,0.2)' }}>
                      {p}
                    </button>
                  ))}
                </div>
              </div>
            </motion.form>
          )}

          {step === 2 && (
            <motion.form key="step2" onSubmit={handleCode}
              initial={{ opacity: 0, x: 30 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -30 }}
              className="p-7 rounded-3xl"
              style={{ background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.1)', boxShadow: '0 25px 60px rgba(0,0,0,0.5)' }}>

              <button type="button" onClick={() => { setStep(1); setError(''); setCode(''); }}
                className="text-xs font-semibold mb-4 flex items-center gap-1 hover:text-white transition-colors"
                style={{ color: 'rgba(255,255,255,0.35)' }}>
                &larr; Cambiar placa
              </button>

              {driverInfo && (
                <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }}
                  className="mb-5 p-4 rounded-2xl"
                  style={{ background: driverInfo.color + '20', border: '1px solid ' + driverInfo.color + '40' }}>
                  <div className="flex items-center gap-3">
                    <div className="w-11 h-11 rounded-xl flex items-center justify-center font-black text-lg text-white"
                      style={{ background: driverInfo.color }}>
                      {driverInfo.name.charAt(0)}
                    </div>
                    <div>
                      <p className="font-black text-white text-sm">{driverInfo.name}</p>
                      <p className="text-xs" style={{ color: '#D4AF37' }}>{driverInfo.company} &bull; {plate.toUpperCase()}</p>
                    </div>
                  </div>
                </motion.div>
              )}

              <div className="flex items-center gap-3 mb-5">
                <div className="w-12 h-12 rounded-2xl flex items-center justify-center"
                  style={{ background: 'rgba(34,197,94,0.15)', border: '1px solid rgba(34,197,94,0.3)' }}>
                  <Shield size={24} color="#22c55e"/>
                </div>
                <div>
                  <p className="font-black text-white">Codigo PIN</p>
                  <p className="text-xs" style={{ color: 'rgba(255,255,255,0.4)' }}>4 digitos de seguridad</p>
                </div>
              </div>

              <div className="flex gap-3 justify-center mb-6">
                {[0,1,2,3].map(i => (
                  <motion.div key={i}
                    animate={{ scale: code.length === i ? [1, 1.15, 1] : 1 }}
                    transition={{ duration: 0.2 }}
                    className="w-14 h-14 rounded-2xl flex items-center justify-center"
                    style={{
                      background: code.length > i ? 'rgba(212,175,55,0.2)' : 'rgba(255,255,255,0.05)',
                      border: code.length > i ? '2px solid #D4AF37' : '2px solid rgba(255,255,255,0.1)',
                    }}>
                    {code.length > i && (
                      <motion.div initial={{ scale: 0 }} animate={{ scale: 1 }}
                        className="w-4 h-4 rounded-full" style={{ background: '#D4AF37' }}/>
                    )}
                  </motion.div>
                ))}
              </div>

              <div className="grid grid-cols-3 gap-3 mb-4">
                {[1,2,3,4,5,6,7,8,9].map(n => (
                  <motion.button key={n} type="button"
                    whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.92 }}
                    onClick={() => addDigit(String(n))}
                    className="h-14 rounded-2xl font-black text-2xl text-white"
                    style={{ background: 'rgba(255,255,255,0.06)', border: '1px solid rgba(255,255,255,0.08)' }}>
                    {n}
                  </motion.button>
                ))}
                <div/>
                <motion.button type="button" whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.92 }}
                  onClick={() => addDigit('0')}
                  className="h-14 rounded-2xl font-black text-2xl text-white"
                  style={{ background: 'rgba(255,255,255,0.06)', border: '1px solid rgba(255,255,255,0.08)' }}>
                  0
                </motion.button>
                <motion.button type="button" whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.92 }}
                  onClick={delDigit}
                  className="h-14 rounded-2xl font-black text-xl"
                  style={{ background: 'rgba(239,68,68,0.1)', border: '1px solid rgba(239,68,68,0.2)', color: '#ef4444' }}>
                  &larr;
                </motion.button>
              </div>

              <AnimatePresence>
                {error && (
                  <motion.div initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0 }}
                    className="flex items-center gap-2 text-sm mb-3 px-4 py-2.5 rounded-xl"
                    style={{ background: 'rgba(239,68,68,0.12)', color: '#fca5a5', border: '1px solid rgba(239,68,68,0.2)' }}>
                    <AlertCircle size={14}/> {error}
                  </motion.div>
                )}
              </AnimatePresence>

              <motion.button type="submit" disabled={code.length < 4 || loading}
                whileHover={{ scale: code.length === 4 ? 1.02 : 1 }}
                whileTap={{ scale: code.length === 4 ? 0.97 : 1 }}
                className="w-full py-4 rounded-2xl font-black text-lg flex items-center justify-center gap-2 transition-all"
                style={{
                  background: code.length === 4 ? 'linear-gradient(135deg, #D4AF37, #f0c84a)' : 'rgba(255,255,255,0.05)',
                  color: code.length === 4 ? '#1B2A6B' : 'rgba(255,255,255,0.2)',
                  boxShadow: code.length === 4 ? '0 8px 30px rgba(212,175,55,0.3)' : 'none',
                }}>
                {loading
                  ? <><div className="w-5 h-5 border-2 border-current border-t-transparent rounded-full animate-spin"/> Verificando...</>
                  : <><Shield size={18}/> Ingresar al Sistema</>
                }
              </motion.button>
            </motion.form>
          )}
        </AnimatePresence>
      </motion.div>
    </div>
  );
}
