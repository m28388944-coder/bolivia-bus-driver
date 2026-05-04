import axios from 'axios';

const API = axios.create({
  baseURL: 'https://bolivia-bus-backend.onrender.com',
  headers: { 'Content-Type': 'application/json' },
});

export const getSchedules  = (placa) => API.get('/schedules/' + (placa ? '?placa=' + placa : ''));
export const getBuses      = ()      => API.get('/schedules/');
export const getPassengers = (id)    => API.get('/bookings/schedule/' + id);
export const getSeatMap    = (id)    => API.get('/schedules/' + id + '/seats');
export const WS_URL = 'ws://localhost:8000/tracking/ws';

export default API;
