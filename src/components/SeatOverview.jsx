import { motion } from 'framer-motion';
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
