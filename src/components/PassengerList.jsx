import { useState } from 'react';
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
