"use client";

import { useState } from "react";
import { useTranslations } from 'next-intl';
import { api } from "@/lib/api";

interface ControlPanelProps {
  currentMode: string;
  onRefresh: () => void;
}

export default function ControlPanel({ currentMode, onRefresh }: ControlPanelProps) {
  const t = useTranslations('control');
  const [loading, setLoading] = useState(false);

  const handleModeChange = async (mode: string) => {
    setLoading(true);
    try {
      await api.setMode(mode);
      onRefresh();
    } catch (error) {
      alert(`Error: ${error}`);
    } finally {
      setLoading(false);
    }
  };

  const handleValveControl = async (action: string) => {
    setLoading(true);
    try {
      await api.controlValve(action);
      onRefresh();
    } catch (error) {
      alert(`Error: ${error}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
      <h2 className="text-xl font-semibold mb-4 text-gray-800 dark:text-gray-100">
        {t('manualControl')}
      </h2>
      
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            {t('operationMode')}
          </label>
          <div className="flex gap-2">
            <button
              onClick={() => handleModeChange("auto")}
              disabled={loading || currentMode === "auto"}
              className={`flex-1 px-4 py-2 rounded-lg font-semibold transition-colors ${
                currentMode === "auto"
                  ? "bg-blue-600 text-white"
                  : "bg-gray-200 text-gray-800 hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-200 dark:hover:bg-gray-600"
              } disabled:opacity-50`}
            >
              {t('auto')}
            </button>
            <button
              onClick={() => handleModeChange("manual")}
              disabled={loading || currentMode === "manual"}
              className={`flex-1 px-4 py-2 rounded-lg font-semibold transition-colors ${
                currentMode === "manual"
                  ? "bg-blue-600 text-white"
                  : "bg-gray-200 text-gray-800 hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-200 dark:hover:bg-gray-600"
              } disabled:opacity-50`}
            >
              {t('manual')}
            </button>
          </div>
        </div>

        {currentMode === "manual" && (
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              {t('valveControl')}
            </label>
            <div className="flex gap-2">
              <button
                onClick={() => handleValveControl("open")}
                disabled={loading}
                className="flex-1 px-4 py-3 bg-green-600 text-white rounded-lg font-semibold hover:bg-green-700 transition-colors disabled:opacity-50"
              >
                {t('openValve')}
              </button>
              <button
                onClick={() => handleValveControl("close")}
                disabled={loading}
                className="flex-1 px-4 py-3 bg-red-600 text-white rounded-lg font-semibold hover:bg-red-700 transition-colors disabled:opacity-50"
              >
                {t('closeValve')}
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

