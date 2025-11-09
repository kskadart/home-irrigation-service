const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface AirReading {
  temperature_c: number;
  humidity_rel: number;
  timestamp: string;
}

export interface SoilReading {
  temperature_c: number;
  moisture_rel: number;
  timestamp: string;
}

export interface Metrics {
  air: AirReading | null;
  soil: SoilReading | null;
  valve_open: boolean;
  mode: string;
  state: string;
}

export interface ThresholdConfig {
  id: number;
  soil_moisture_low: number;
  soil_moisture_high: number;
  air_temp_min: number | null;
  air_temp_max: number | null;
  air_humidity_min: number | null;
  air_humidity_max: number | null;
  watering_seconds: number;
  soak_minutes: number;
  daily_budget_minutes: number;
  window_start_hour: number;
  window_end_hour: number;
}

export interface Schedule {
  id: number;
  name: string;
  schedule_date: string;
  schedule_time: string;
  duration_seconds: number;
  enabled: boolean;
}

export interface ScheduleCreate {
  name: string;
  schedule_date: string;
  schedule_time: string;
  duration_seconds: number;
  enabled: boolean;
}

export const api = {
  async getMetrics(): Promise<Metrics> {
    const res = await fetch(`${API_URL}/status/metrics`);
    if (!res.ok) throw new Error('Failed to fetch metrics');
    return res.json();
  },

  async setMode(mode: string): Promise<void> {
    const res = await fetch(`${API_URL}/control/mode`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ mode }),
    });
    if (!res.ok) throw new Error('Failed to set mode');
  },

  async controlValve(action: string, seconds?: number): Promise<void> {
    const res = await fetch(`${API_URL}/control/valve`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ action, seconds }),
    });
    if (!res.ok) throw new Error('Failed to control valve');
  },

  async getThresholds(): Promise<ThresholdConfig> {
    const res = await fetch(`${API_URL}/config/thresholds`);
    if (!res.ok) throw new Error('Failed to fetch thresholds');
    return res.json();
  },

  async updateThresholds(data: Partial<ThresholdConfig>): Promise<ThresholdConfig> {
    const res = await fetch(`${API_URL}/config/thresholds`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error('Failed to update thresholds');
    return res.json();
  },

  async listSchedules(): Promise<Schedule[]> {
    const res = await fetch(`${API_URL}/schedule/list`);
    if (!res.ok) throw new Error('Failed to fetch schedules');
    return res.json();
  },

  async createSchedule(data: ScheduleCreate): Promise<Schedule> {
    const res = await fetch(`${API_URL}/schedule/create`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error('Failed to create schedule');
    return res.json();
  },

  async updateSchedule(id: number, data: Partial<ScheduleCreate>): Promise<Schedule> {
    const res = await fetch(`${API_URL}/schedule/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error('Failed to update schedule');
    return res.json();
  },

  async deleteSchedule(id: number): Promise<void> {
    const res = await fetch(`${API_URL}/schedule/${id}`, {
      method: 'DELETE',
    });
    if (!res.ok) throw new Error('Failed to delete schedule');
  },

  async toggleSchedule(id: number): Promise<Schedule> {
    const res = await fetch(`${API_URL}/schedule/${id}/toggle`, {
      method: 'POST',
    });
    if (!res.ok) throw new Error('Failed to toggle schedule');
    return res.json();
  },
};

