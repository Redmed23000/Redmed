import "../globals.css";
import { NextIntlClientProvider } from "next-intl";
import { getMessages } from "next-intl/server";
import type { ReactNode } from "react";
import Link from "next/link";
import { useTranslations } from "next-intl";

function Nav({ locale }: { locale: string }) {
  const t = useTranslations("nav");
  return (
    <nav className="flex gap-4 border-b bg-white p-4" aria-label="Clinician navigation">
      <Link href={`/${locale}`}>{t("dashboard")}</Link>
      <Link href={`/${locale}/patients`}>{t("patients")}</Link>
      <Link href={`/${locale}/triage`}>{t("triage")}</Link>
      <Link href={`/${locale}/audit`}>{t("audit")}</Link>
    </nav>
  );
}

export default async function RootLayout({ children, params }: { children: ReactNode; params: { locale: string } }) {
  const messages = await getMessages();
  return (
    <html lang={params.locale}>
      <body>
        <NextIntlClientProvider messages={messages}>
          <Nav locale={params.locale} />
          <main className="mx-auto max-w-5xl p-6">{children}</main>
        </NextIntlClientProvider>
      </body>
    </html>
  );
}
