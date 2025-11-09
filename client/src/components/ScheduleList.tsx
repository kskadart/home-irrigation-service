"use client";

import { useState, useEffect } from "react";
import { useTranslations } from 'next-intl';
import { api, Schedule, ScheduleCreate } from "@/lib/api";

export default function ScheduleList() {
  const t = useTranslations('schedule');
  const tCommon = useTranslations('common');
  const [schedules, setSchedules] = useState<Schedule[]>([]);
  const [loading, setLoading] = useState(false);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState<ScheduleCreate>({
    name: "",
    schedule_date: "",
    schedule_time: "",
    duration_seconds: 90,
    enabled: true,
  });

  useEffect(() => {
    loadSchedules();
  }, []);

  const loadSchedules = async () => {
    try {
      const data = await api.listSchedules();
      setSchedules(data);
    } catch (error) {
      console.error('Failed to load schedules:', error);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await api.createSchedule(formData);
      await loadSchedules();
      setShowForm(false);
      setFormData({
        name: "",
        schedule_date: "",
        schedule_time: "",
        duration_seconds: 90,
        enabled: true,
      });
    } catch (error) {
      alert(`Error: ${error}`);
    } finally {
      setLoading(false);
    }
  };

  const handleToggle = async (id: number) => {
    try {
      await api.toggleSchedule(id);
      await loadSchedules();
    } catch (error) {
      alert(`Error: ${error}`);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Are you sure you want to delete this schedule?')) return;
    try {
      await api.deleteSchedule(id);
      await loadSchedules();
    } catch (error) {
      alert(`Error: ${error}`);
    }
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-semibold text-gray-800 dark:text-gray-100">
          {t('wateringSchedules')}
        </h2>
        <button
          onClick={() => setShowForm(!showForm)}
          className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
        >
          {showForm ? tCommon('cancel') : t('addSchedule')}
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleSubmit} className="mb-6 p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                {t('name')}
              </label>
              <input
                type="text"
                required
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-800 dark:text-gray-100"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                {t('duration')}
              </label>
              <input
                type="number"
                required
                value={formData.duration_seconds}
                onChange={(e) => setFormData({ ...formData, duration_seconds: parseInt(e.target.value) })}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-800 dark:text-gray-100"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                {t('date')}
              </label>
              <input
                type="date"
                required
                value={formData.schedule_date}
                onChange={(e) => setFormData({ ...formData, schedule_date: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-800 dark:text-gray-100"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                {t('time')}
              </label>
              <input
                type="time"
                required
                value={formData.schedule_time}
                onChange={(e) => setFormData({ ...formData, schedule_time: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-800 dark:text-gray-100"
              />
            </div>
          </div>
          <button
            type="submit"
            disabled={loading}
            className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50"
          >
            {loading ? t('creating') : t('createSchedule')}
          </button>
        </form>
      )}

      <div className="space-y-3">
        {schedules.length === 0 ? (
          <p className="text-gray-500 text-center py-4">{t('noSchedules')}</p>
        ) : (
          schedules.map((schedule) => (
            <div
              key={schedule.id}
              className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700 rounded-lg"
            >
              <div className="flex-1">
                <h3 className="font-semibold text-gray-800 dark:text-gray-100">
                  {schedule.name}
                </h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  {schedule.schedule_date} at {schedule.schedule_time} - {schedule.duration_seconds}s
                </p>
              </div>
              <div className="flex gap-2">
                <button
                  onClick={() => handleToggle(schedule.id)}
                  className={`px-3 py-1 rounded-lg text-sm font-semibold transition-colors ${
                    schedule.enabled
                      ? "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200"
                      : "bg-gray-200 text-gray-600 dark:bg-gray-600 dark:text-gray-300"
                  }`}
                >
                  {schedule.enabled ? t('enabled') : t('disabled')}
                </button>
                <button
                  onClick={() => handleDelete(schedule.id)}
                  className="px-3 py-1 bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200 rounded-lg text-sm font-semibold hover:bg-red-200 dark:hover:bg-red-800 transition-colors"
                >
                  {tCommon('delete')}
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

