"use client";

import { useTranslations } from 'next-intl';
import { Metrics } from "@/lib/api";

interface MetricsCardProps {
  metrics: Metrics | null;
}

export default function MetricsCard({ metrics }: MetricsCardProps) {
  const t = useTranslations('metrics');
  const tModes = useTranslations('modes');
  const tStates = useTranslations('states');
  
  if (!metrics) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
        <p className="text-gray-500">{t('loadingMetrics')}</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold mb-4 text-gray-800 dark:text-gray-100">
          {t('airConditions')}
        </h2>
        {metrics.air ? (
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-gray-600 dark:text-gray-300">{t('temperature')}:</span>
              <span className="text-2xl font-bold text-blue-600">
                {metrics.air.temperature_c.toFixed(1)}°C
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600 dark:text-gray-300">{t('humidity')}:</span>
              <span className="text-2xl font-bold text-green-600">
                {metrics.air.humidity_rel.toFixed(1)}%
              </span>
            </div>
          </div>
        ) : (
          <p className="text-gray-500">{t('noAirData')}</p>
        )}
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold mb-4 text-gray-800 dark:text-gray-100">
          {t('soilConditions')}
        </h2>
        {metrics.soil ? (
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-gray-600 dark:text-gray-300">{t('temperature')}:</span>
              <span className="text-2xl font-bold text-orange-600">
                {metrics.soil.temperature_c.toFixed(1)}°C
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600 dark:text-gray-300">{t('moisture')}:</span>
              <span className="text-2xl font-bold text-cyan-600">
                {(metrics.soil.moisture_rel * 100).toFixed(1)}%
              </span>
            </div>
          </div>
        ) : (
          <p className="text-gray-500">{t('noSoilData')}</p>
        )}
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 md:col-span-2">
        <h2 className="text-xl font-semibold mb-4 text-gray-800 dark:text-gray-100">
          {t('systemStatus')}
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div className="flex flex-col items-center">
            <span className="text-gray-600 dark:text-gray-300 mb-2">{t('valve')}</span>
            <span
              className={`px-4 py-2 rounded-full font-semibold ${
                metrics.valve_open
                  ? "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200"
                  : "bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300"
              }`}
            >
              {metrics.valve_open ? t('open') : t('closed')}
            </span>
          </div>
          <div className="flex flex-col items-center">
            <span className="text-gray-600 dark:text-gray-300 mb-2">{t('mode')}</span>
            <span className="px-4 py-2 rounded-full font-semibold bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200">
              {tModes(metrics.mode)}
            </span>
          </div>
          <div className="flex flex-col items-center">
            <span className="text-gray-600 dark:text-gray-300 mb-2">{t('state')}</span>
            <span className="px-4 py-2 rounded-full font-semibold bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200">
              {tStates(metrics.state)}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}

