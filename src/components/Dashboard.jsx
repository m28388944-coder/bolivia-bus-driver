import { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Bus, MapPin, Grid, LogOut, ChevronRight, Zap, Radio, Shield, X, CheckCircle } from 'lucide-react';
import { getSeatMap, WS_URL } from '../api';
import './Dashboard.css';

const GOLD = '#D4AF37';
const NAVY = '#1B2A6B';

const COMPANY_ACCENT = {
  'Bolivia Bus Express': '#D4AF37',
  'Trans Copacabana':    '#FF4466',
  'Flota Boliviana':     '#4ade80',
  'Flota Bolivar':       '#FB923C',
  'Flota Cosmos':        '#22D3EE',
  'Concordia':           '#A78BFA',
};

function fmt(dt) {
  if (!dt) return '--:--';
  return new Date(dt).toLocaleTimeString('es-BO', { hour: '2-digit', minute: '2-digit', timeZone: 'America/La_Paz' });
}
function fmtDay(dt) {
  if (!dt) return '';
  return new Date(dt).toLocaleDateString('es-BO', { weekday: 'long', day: 'numeric', month: 'long', timeZone: 'America/La_Paz' });
}

export default function Dashboard({ driver, onLogout }) {
  const [tab, setTab] = useState('seats');
  const [seats, setSeats] = useState([]);
  const [loading, setLoading] = useState(true);
  const [connected, setConnected] = useState(false);
  const [busData, setBusData] = useState(null);
  const [seatModal, setSeatModal] = useState(null);
  const wsRef = useRef(null);
  const schedule = driver.schedules?.[0];
  const accent = COMPANY_ACCENT[driver.company] || GOLD;

  useEffect(() => {
    if (!schedule) { setLoading(false); return; }
    getSeatMap(schedule.id)
      .then(res => { const d = res.data; setSeats(Array.isArray(d) ? d : (d.value || d.items || [])); })
      .catch(() => {})
      .finally(() => setLoading(false));
    try {
      const ws = new WebSocket(WS_URL);
      wsRef.current = ws;
      ws.onopen = () => setConnected(true);
      ws.onclose = () => setConnected(false);
      ws.onerror = () => setConnected(false);
      ws.onmessage = (e) => { try { const d = JSON.parse(e.data); if (d.plate === driver.plate) setBusData(d); } catch {} };
    } catch {}
    return () => { try { wsRef.current?.close(); } catch {} };
  }, [schedule]);

  const total    = seats.length || 40;
  const ocupados = seats.filter(s => !s.disponible).length;
  const libres   = seats.filter(s => s.disponible).length;
  const pct      = total > 0 ? Math.round((ocupados / total) * 100) : 0;

  return (
    <div className="dr">
      <div className="hdr">
        <div className="hdr-top">
          <div className="logo-strip">
            <Bus size={20} color={GOLD}/>
            <span className="logo-text">Bolivia<span className="logo-gold">Bus</span></span>
          </div>
          <div style={{ display:'flex', alignItems:'center', gap:8 }}>
            <div className="gps-pill">
              <div className={connected ? 'dot pulse' : 'dot'} style={{ background: connected ? '#22c55e' : '#ddd', boxShadow: connected ? '0 0 6px #22c55e' : 'none' }}/>
              <span style={{ fontSize:11, fontWeight:700, color: connected ? '#22c55e' : '#bbb' }}>{connected ? 'GPS activo' : 'Sin GPS'}</span>
              {connected && <Radio size={10} color="#22c55e"/>}
            </div>
            <button className="logout-btn" onClick={onLogout}><LogOut size={12}/> Salir</button>
          </div>
        </div>
        <div className="conductor-card">
          <div className="avatar">{driver.name.charAt(0)}</div>
          <div style={{ flex:1, minWidth:0 }}>
            <div style={{ fontSize:9, fontWeight:700, letterSpacing:2, textTransform:'uppercase', color:'rgba(255,255,255,0.5)', marginBottom:3 }}>Conductor</div>
            <div style={{ fontSize:16, fontWeight:800, color:'#fff', whiteSpace:'nowrap', overflow:'hidden', textOverflow:'ellipsis' }}>{driver.name}</div>
            <div style={{ fontSize:11, color:'rgba(255,255,255,0.6)', marginTop:1 }}>{driver.company}</div>
          </div>
          <div style={{ textAlign:'right', flexShrink:0 }}>
            <div style={{ fontSize:14, fontWeight:900, color:GOLD, background:'rgba(212,175,55,0.2)', border:'1px solid rgba(212,175,55,0.4)', borderRadius:8, padding:'5px 12px' }}>{driver.plate}</div>
          </div>
        </div>
        {schedule && (
          <div className="sched-strip">
            <Bus size={16} color={NAVY} style={{ flexShrink:0 }}/>
            <div style={{ flex:1 }}>
              <div style={{ display:'flex', alignItems:'baseline', gap:8, marginBottom:3 }}>
                <span style={{ fontSize:22, fontWeight:900, color:NAVY, lineHeight:1 }}>{fmt(schedule.departure_time)}</span>
                <ChevronRight size={14} color="#ddd"/>
                <span style={{ fontSize:18, fontWeight:700, color:'#aaa', lineHeight:1 }}>{fmt(schedule.arrival_time)}</span>
              </div>
              <div style={{ fontSize:11, fontWeight:700, color:NAVY, opacity:0.7 }}>{schedule.origin} - {schedule.destination}</div>
            </div>
            <div style={{ textAlign:'right', flexShrink:0 }}>
              <div style={{ fontSize:9, color:'#ccc', fontWeight:700, letterSpacing:1, textTransform:'uppercase' }}>hoy</div>
              <div style={{ fontSize:10, color:'#aaa', marginTop:2, textTransform:'capitalize' }}>{fmtDay(schedule.departure_time).split(',')[0]}</div>
            </div>
          </div>
        )}
      </div>

      <div className="stats-row">
        {[{l:'Ocupados',v:ocupados,c:'#FF5555'},{l:'Ocupacion',v:pct+'%',c:NAVY},{l:'Libres',v:libres,c:'#22c55e'}].map(s=>(
          <div key={s.l} className="stat" style={{'--c':s.c}}>
            <div className="stat-val" style={{color:s.c}}>{s.v}</div>
            <div className="stat-lbl">{s.l}</div>
          </div>
        ))}
      </div>

      <div className="tabs">
        {[{id:'seats',label:'Asientos',Icon:Grid},{id:'route',label:'Mi Ruta',Icon:MapPin}].map(({id,label,Icon})=>(
          <button key={id} className={tab===id?'tab on':'tab'} onClick={()=>setTab(id)}><Icon size={13}/>{label}</button>
        ))}
      </div>

      <div className="content">
        <AnimatePresence mode="wait">
          {tab==='seats' && (
            <motion.div key="s" initial={{opacity:0,y:8}} animate={{opacity:1,y:0}} exit={{opacity:0,y:-8}} transition={{duration:0.15}}>
              {loading ? <Spinner/> : <SeatGrid seats={seats} onSeatClick={setSeatModal}/>}
            </motion.div>
          )}
          {tab==='route' && (
            <motion.div key="r" initial={{opacity:0,y:8}} animate={{opacity:1,y:0}} exit={{opacity:0,y:-8}} transition={{duration:0.15}}>
              <RouteInfo schedule={schedule} driver={driver} busData={busData} accent={accent}/>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* ── MODAL ASIENTO ── */}
      <AnimatePresence>
        {seatModal && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setSeatModal(null)}
            style={{
              position: 'fixed', inset: 0,
              background: 'rgba(0,0,0,0.75)',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              zIndex: 999, padding: 24,
            }}>
            <motion.div
              initial={{ scale: 0.9, opacity: 0, y: 20 }}
              animate={{ scale: 1, opacity: 1, y: 0 }}
              exit={{ scale: 0.9, opacity: 0 }}
              onClick={e => e.stopPropagation()}
              style={{
                background: 'linear-gradient(135deg, #0f1d56, #1B2A6B)',
                border: '1px solid rgba(212,175,55,0.3)',
                borderRadius: 20, padding: 28, width: '100%', maxWidth: 320,
                boxShadow: '0 24px 60px rgba(0,0,0,0.5)',
              }}>

              {/* Header */}
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                  <div style={{
                    width: 36, height: 36, borderRadius: 10,
                    background: seatModal.disponible ? 'rgba(34,197,94,0.15)' : 'rgba(212,175,55,0.15)',
                    border: `1px solid ${seatModal.disponible ? 'rgba(34,197,94,0.3)' : 'rgba(212,175,55,0.3)'}`,
                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                    fontSize: 16, fontWeight: 900,
                    color: seatModal.disponible ? '#22c55e' : GOLD,
                  }}>
                    {seatModal.numero}
                  </div>
                  <div>
                    <div style={{ color: '#fff', fontWeight: 800, fontSize: 16 }}>
                      Asiento {seatModal.numero}
                    </div>
                    <div style={{
                      fontSize: 11, fontWeight: 700,
                      color: seatModal.disponible ? '#22c55e' : GOLD,
                    }}>
                      {seatModal.disponible ? 'LIBRE' : 'OCUPADO'}
                    </div>
                  </div>
                </div>
                <button onClick={() => setSeatModal(null)} style={{
                  background: 'rgba(255,255,255,0.08)', border: 'none',
                  borderRadius: 8, padding: 8, cursor: 'pointer', color: '#fff',
                  display: 'flex', alignItems: 'center',
                }}>
                  <X size={16}/>
                </button>
              </div>

              {/* Contenido */}
              {seatModal.disponible ? (
                <div style={{ textAlign: 'center', padding: '20px 0' }}>
                  <div style={{ fontSize: 40, marginBottom: 12 }}>💺</div>
                  <p style={{ color: 'rgba(255,255,255,0.6)', fontSize: 14 }}>
                    Este asiento está disponible
                  </p>
                </div>
              ) : seatModal.codigo_reserva ? (
                <>
                  {/* Pasajero */}
                  <div style={{
                    background: "rgba(255,255,255,0.05)",
                    border: "1px solid rgba(255,255,255,0.1)",
                    borderRadius: 14, padding: "16px 18px", marginBottom: 12,
                  }}>
                    <p style={{ color: "rgba(255,255,255,0.4)", fontSize: 10, fontWeight: 700, letterSpacing: 1, textTransform: "uppercase", marginBottom: 10 }}>
                      Pasajero
                    </p>
                    <p style={{ color: "#fff", fontSize: 18, fontWeight: 800, marginBottom: 6 }}>
                      {seatModal.pasajero_nombre || "Sin nombre"}
                    </p>
                    <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                      <span style={{ color: "rgba(255,255,255,0.4)", fontSize: 12 }}>CI:</span>
                      <span style={{ color: GOLD, fontSize: 15, fontWeight: 700, fontFamily: "monospace" }}>
                        {seatModal.pasajero_ci || "—"}
                      </span>
                    </div>
                  </div>
                  {/* Codigo reserva */}
                  <div style={{
                    background: "rgba(212,175,55,0.08)",
                    border: "1px solid rgba(212,175,55,0.2)",
                    borderRadius: 14, padding: "16px 18px", marginBottom: 12,
                    textAlign: "center",
                  }}>
                    <p style={{ color: "rgba(255,255,255,0.4)", fontSize: 10, fontWeight: 700, letterSpacing: 1, textTransform: "uppercase", marginBottom: 8 }}>
                      Código de Reserva
                    </p>
                    <p style={{ color: GOLD, fontSize: 22, fontWeight: 900, letterSpacing: 3, fontFamily: "monospace" }}>
                      {seatModal.codigo_reserva}
                    </p>
                  </div>
                  {/* Verificado */}
                  <div style={{
                    display: "flex", alignItems: "center", gap: 8,
                    background: "rgba(34,197,94,0.08)",
                    border: "1px solid rgba(34,197,94,0.2)",
                    borderRadius: 10, padding: "10px 14px",
                  }}>
                    <CheckCircle size={16} color="#22c55e"/>
                    <p style={{ color: "#86efac", fontSize: 13, fontWeight: 600, margin: 0 }}>
                      Pasaje verificado — puede abordar
                    </p>
                  </div>
                </>
              ) : (
                <div style={{ textAlign: 'center', padding: '20px 0' }}>
                  <p style={{ color: 'rgba(255,255,255,0.4)', fontSize: 13 }}>
                    Sin código de reserva registrado
                  </p>
                </div>
              )}
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

function SeatGrid({ seats, onSeatClick }) {
  const filas = [...new Set(seats.map(s => s.fila))].sort();
  if (!seats.length) return (
    <div style={{textAlign:"center",padding:"48px 0",color:"#ccc"}}>
      <Grid size={32} color="#ddd" style={{display:"block",margin:"0 auto 10px"}}/>
      <p style={{fontSize:13,fontWeight:600}}>Sin asientos cargados</p>
    </div>
  );
  return (
    <>
      <div className="bus-front">
        <div className="divider"/><Bus size={12} color="#ddd"/>
        <span className="front-label">Frente del bus</span>
        <div className="divider"/>
      </div>
      <div style={{display:"flex",flexDirection:"column",alignItems:"center"}}>
        {filas.map((fila,i)=>{
          const row=seats.filter(s=>s.fila===fila).sort((a,b)=>a.columna-b.columna);
          const izq=row.filter(s=>s.columna<=2);
          const der=row.filter(s=>s.columna>2);
          return(
            <motion.div key={fila} className="seat-row"
              initial={{opacity:0,x:-6}} animate={{opacity:1,x:0}}
              transition={{delay:i*0.025,duration:0.18}}>
              <span className="row-num">{fila}</span>
              <div className="seats-side">{izq.map(s=><SeatSVG key={s.id} s={s} onClick={()=>onSeatClick(s)}/>)}</div>
              <div className="aisle"/>
              <div className="seats-side">{der.map(s=><SeatSVG key={s.id} s={s} onClick={()=>onSeatClick(s)}/>)}</div>
            </motion.div>
          );
        })}
      </div>
      <div style={{ textAlign:'center', marginTop: 12, color:'rgba(255,255,255,0.3)', fontSize:11 }}>
        Toca un asiento para ver detalles
      </div>
      <div className="legend">
        <div className="legend-item"><SeatSVG s={{disponible:true,numero:""}} mini/> Libre</div>
        <div className="legend-item"><SeatSVG s={{disponible:false,numero:""}} mini/> Ocupado</div>
      </div>
    </>
  );
}

function SeatSVG({ s, mini, onClick }) {
  const libre = s.disponible;
  const size = mini ? 16 : 34;
  const headBg = libre ? "#D4AF37" : "#2d45a8";
  const bodyBg = libre ? "#FDE68A" : "#243580";
  const legBg  = libre ? "#D4AF37" : "#1B2A6B";
  const border = libre ? "#D4AF37" : "#1B2A6B";
  const txtCol = libre ? "#1B2A6B" : "rgba(255,255,255,0.7)";
  return (
    <div
      onClick={onClick}
      style={{
        width:size, height:size, position:"relative",
        cursor: onClick ? "pointer" : "default",
        transition: "transform 0.15s",
      }}
      title={s.numero}
      onMouseEnter={e => { if (onClick) e.currentTarget.style.transform = "scale(1.15)"; }}
      onMouseLeave={e => { e.currentTarget.style.transform = "scale(1)"; }}
    >
      <svg width={size} height={size} viewBox="0 0 34 34" xmlns="http://www.w3.org/2000/svg">
        <rect x="5" y="2" width="24" height="9" rx="4" fill={headBg}/>
        <rect x="5" y="10" width="24" height="13" rx="2" fill={bodyBg}/>
        <rect x="3" y="22" width="28" height="8" rx="3" fill={legBg}/>
        <rect x="5" y="29" width="4" height="3" rx="1" fill={legBg}/>
        <rect x="25" y="29" width="4" height="3" rx="1" fill={legBg}/>
        <rect x="1" y="1" width="32" height="32" rx="5" fill="none" stroke={border} strokeWidth="1.5"/>
      </svg>
      {!mini && s.numero && (
        <div style={{
          position:"absolute", top:"50%", left:"50%",
          transform:"translate(-50%,-50%)",
          fontSize:8, fontWeight:900, color:txtCol,
          letterSpacing:-0.3, pointerEvents:"none",
        }}>
          {s.numero}
        </div>
      )}
    </div>
  );
}

function RouteInfo({ schedule, driver, busData, accent }) {
  if (!schedule) return (
    <div style={{textAlign:'center',padding:'48px 0',color:'#ccc'}}>
      <MapPin size={32} color="#ddd" style={{display:'block',margin:'0 auto 10px'}}/>
      <p style={{fontSize:13,fontWeight:700}}>Sin ruta asignada hoy</p>
    </div>
  );
  return (
    <div>
      <div className="route-card">
        <div className="card-label">Informacion del viaje</div>
        <div style={{display:'flex',alignItems:'center',gap:10}}>
          <div style={{flex:1}}>
            <div style={{fontSize:34,fontWeight:900,color:NAVY,letterSpacing:-1,lineHeight:1}}>{fmt(schedule.departure_time)}</div>
            <div style={{fontSize:12,fontWeight:700,color:GOLD,marginTop:5}}>{schedule.origin}</div>
          </div>
          <ChevronRight size={18} color="#ddd"/>
          <div style={{flex:1,textAlign:'right'}}>
            <div style={{fontSize:34,fontWeight:900,color:'#bbb',letterSpacing:-1,lineHeight:1}}>{fmt(schedule.arrival_time)}</div>
            <div style={{fontSize:12,fontWeight:700,color:'#bbb',marginTop:5}}>{schedule.destination}</div>
          </div>
        </div>
      </div>
      <div className="detail-grid">
        {[
          {l:'Placa',v:driver.plate,c:NAVY},
          {l:'Tipo Bus',v:(schedule.bus_type||'Normal').toUpperCase(),c:'#6366f1'},
          {l:'Precio',v:'Bs. '+schedule.price_normal,c:'#22c55e'},
          {l:'Duracion',v:schedule.duration_hours+' horas',c:'#f59e0b'},
        ].map(item=>(
          <div key={item.l} className="detail-cell">
            <div className="detail-lbl">{item.l}</div>
            <div className="detail-val" style={{color:item.c}}>{item.v}</div>
          </div>
        ))}
      </div>
      {busData && (
        <motion.div className="gps-live" initial={{opacity:0,scale:0.98}} animate={{opacity:1,scale:1}}>
          <div className="gps-header">
            <div style={{width:6,height:6,borderRadius:'50%',background:'#4ade80',boxShadow:'0 0 8px #4ade80',flexShrink:0}}/>
            <span style={{fontSize:9,fontWeight:700,letterSpacing:2,textTransform:'uppercase',color:GOLD}}>GPS en vivo</span>
            <Zap size={10} color={GOLD}/>
          </div>
          <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:10}}>
            <div>
              <div style={{fontSize:9,color:'rgba(255,255,255,0.5)',fontWeight:700,letterSpacing:1,textTransform:'uppercase',marginBottom:3}}>Velocidad</div>
              <div style={{fontSize:34,fontWeight:900,color:'#fff',letterSpacing:-1,lineHeight:1}}>{busData.speed_kmh}<span style={{fontSize:12,fontWeight:500,color:'rgba(255,255,255,0.5)'}}> km/h</span></div>
            </div>
            <div>
              <div style={{fontSize:9,color:'rgba(255,255,255,0.5)',fontWeight:700,letterSpacing:1,textTransform:'uppercase',marginBottom:3}}>Estado</div>
              <div style={{fontSize:16,fontWeight:800,color:'#fff',textTransform:'capitalize',lineHeight:1.3}}>{busData.status||'En ruta'}</div>
            </div>
          </div>
        </motion.div>
      )}
      <div className="verified-strip">
        <Shield size={12} color={GOLD}/>
        <span>Sistema verificado Bolivia Bus</span>
      </div>
    </div>
  );
}

function Spinner() {
  return (
    <div style={{textAlign:'center',padding:'48px 0'}}>
      <div className="spin" style={{width:26,height:26,border:'2.5px solid #eef0f5',borderTopColor:NAVY,borderRadius:'50%',margin:'0 auto 10px'}}/>
      <p style={{fontSize:10,color:'#ccc',fontWeight:700,letterSpacing:2}}>CARGANDO...</p>
    </div>
  );
}

