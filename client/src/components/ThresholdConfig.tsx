"use client";

import { useState, useEffect } from "react";
import { useTranslations } from 'next-intl';
import { api, ThresholdConfig as ThresholdConfigType } from "@/lib/api";

interface ThresholdConfigProps {
  onUpdate: () => void;
}

export default function ThresholdConfig({ onUpdate }: ThresholdConfigProps) {
  const t = useTranslations('config');
  const tCommon = useTranslations('common');
  const [config, setConfig] = useState<ThresholdConfigType | null>(null);
  const [editing, setEditing] = useState(false);
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState<Partial<ThresholdConfigType>>({});

  useEffect(() => {
    loadConfig();
  }, []);

  const loadConfig = async () => {
    try {
      const data = await api.getThresholds();
      setConfig(data);
      setFormData(data);
    } catch (error) {
      console.error('Failed to load thresholds:', error);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await api.updateThresholds(formData);
      await loadConfig();
      setEditing(false);
      onUpdate();
    } catch (error) {
      alert(`Error: ${error}`);
    } finally {
      setLoading(false);
    }
  };

  if (!config) {
    return <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">{tCommon('loading')}</div>;
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-semibold text-gray-800 dark:text-gray-100">
          {t('thresholdConfig')}
        </h2>
        <button
          onClick={() => setEditing(!editing)}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          {editing ? tCommon('cancel') : tCommon('edit')}
        </button>
      </div>

      {editing ? (
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                {t('soilMoistureLow')}
              </label>
              <input
                type="number"
                step="0.01"
                min="0"
                max="1"
                value={formData.soil_moisture_low || 0}
                onChange={(e) => setFormData({ ...formData, soil_moisture_low: parseFloat(e.target.value) })}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-gray-100"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                {t('soilMoistureHigh')}
              </label>
              <input
                type="number"
                step="0.01"
                min="0"
                max="1"
                value={formData.soil_moisture_high || 0}
                onChange={(e) => setFormData({ ...formData, soil_moisture_high: parseFloat(e.target.value) })}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-gray-100"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                {t('wateringDuration')}
              </label>
              <input
                type="number"
                value={formData.watering_seconds || 0}
                onChange={(e) => setFormData({ ...formData, watering_seconds: parseInt(e.target.value) })}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-gray-100"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                {t('soakMinutes')}
              </label>
              <input
                type="number"
                value={formData.soak_minutes || 0}
                onChange={(e) => setFormData({ ...formData, soak_minutes: parseInt(e.target.value) })}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-gray-100"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                {t('dailyBudget')}
              </label>
              <input
                type="number"
                value={formData.daily_budget_minutes || 0}
                onChange={(e) => setFormData({ ...formData, daily_budget_minutes: parseInt(e.target.value) })}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-gray-100"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                {t('windowHours')}
              </label>
              <div className="flex gap-2">
                <input
                  type="number"
                  min="0"
                  max="23"
                  value={formData.window_start_hour || 0}
                  onChange={(e) => setFormData({ ...formData, window_start_hour: parseInt(e.target.value) })}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-gray-100"
                />
                <input
                  type="number"
                  min="0"
                  max="23"
                  value={formData.window_end_hour || 0}
                  onChange={(e) => setFormData({ ...formData, window_end_hour: parseInt(e.target.value) })}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-gray-100"
                />
              </div>
            </div>
          </div>
          <button
            type="submit"
            disabled={loading}
            className="w-full px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors disabled:opacity-50"
          >
            {loading ? t('saving') : t('saveConfiguration')}
          </button>
        </form>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
          <div className="flex justify-between">
            <span className="text-gray-600 dark:text-gray-400">{t('soilMoistureLow')}:</span>
            <span className="font-semibold">{(config.soil_moisture_low * 100).toFixed(1)}%</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600 dark:text-gray-400">{t('soilMoistureHigh')}:</span>
            <span className="font-semibold">{(config.soil_moisture_high * 100).toFixed(1)}%</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600 dark:text-gray-400">{t('wateringDuration')}:</span>
            <span className="font-semibold">{config.watering_seconds}s</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600 dark:text-gray-400">{t('soakMinutes')}:</span>
            <span className="font-semibold">{config.soak_minutes} min</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600 dark:text-gray-400">{t('dailyBudget')}:</span>
            <span className="font-semibold">{config.daily_budget_minutes} min</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600 dark:text-gray-400">{t('windowHours')}:</span>
            <span className="font-semibold">{config.window_start_hour}:00 - {config.window_end_hour}:00</span>
          </div>
        </div>
      )}
    </div>
  );
}

