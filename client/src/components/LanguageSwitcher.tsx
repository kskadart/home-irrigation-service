"use client";

import { useLocale } from 'next-intl';
import Link from 'next/link';

export default function LanguageSwitcher() {
  const locale = useLocale();
  const nextLocale = locale === 'ru' ? 'en' : 'ru';

  return (
    <Link
      href={`/${nextLocale}`}
      className="px-3 py-1 rounded-lg text-sm font-semibold transition-colors bg-blue-600 text-white hover:bg-blue-700"
    >
      {locale === 'ru' ? 'EN' : 'RU'}
    </Link>
  );
}

