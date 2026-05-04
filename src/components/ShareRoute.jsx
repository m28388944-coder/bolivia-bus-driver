import { motion } from 'framer-motion';
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
