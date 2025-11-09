"use client";

import { useState, useEffect } from "react";
import { useTranslations } from 'next-intl';
import { api, Metrics } from "@/lib/api";
import MetricsCard from "@/components/MetricsCard";
import ControlPanel from "@/components/ControlPanel";
import ThresholdConfig from "@/components/ThresholdConfig";
import ScheduleList from "@/components/ScheduleList";
import LanguageSwitcher from "@/components/LanguageSwitcher";

export default function Home() {
  const t = useTranslations();
  const [metrics, setMetrics] = useState<Metrics | null>(null);
  const [error, setError] = useState<string | null>(null);

  const loadMetrics = async () => {
    try {
      const data = await api.getMetrics();
      setMetrics(data);
      setError(null);
    } catch (err) {
      setError(t('errors.connectionFailed'));
      console.error('Failed to load metrics:', err);
    }
  };

  useEffect(() => {
    loadMetrics();
    const interval = setInterval(loadMetrics, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <header className="bg-white dark:bg-gray-800 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl sm:text-3xl font-bold text-gray-900 dark:text-gray-100">
              🌱 {t('common.title')}
            </h1>
            <div className="flex gap-3 items-center">
              <LanguageSwitcher />
              <button
                onClick={loadMetrics}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm sm:text-base"
              >
                🔄 {t('common.refresh')}
              </button>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8">
        {error && (
          <div className="mb-6 p-4 bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-200 rounded-lg">
            {error}
          </div>
        )}

        <div className="space-y-6">
          <MetricsCard metrics={metrics} />

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <ControlPanel
              currentMode={metrics?.mode || "auto"}
              onRefresh={loadMetrics}
            />
            <ThresholdConfig onUpdate={loadMetrics} />
          </div>

          <ScheduleList />
        </div>
      </main>

      <footer className="mt-12 py-6 border-t border-gray-200 dark:border-gray-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-gray-600 dark:text-gray-400 text-sm">
          {t('common.poweredBy')}
        </div>
      </footer>
    </div>
  );
}

