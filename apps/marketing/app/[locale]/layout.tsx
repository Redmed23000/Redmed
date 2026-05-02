import "../globals.css";
import { NextIntlClientProvider } from "next-intl";
import { getMessages } from "next-intl/server";
import type { ReactNode } from "react";
import Link from "next/link";
import { useTranslations } from "next-intl";

function Nav({ locale }: { locale: string }) {
  const t = useTranslations("nav");
  return (
    <nav className="flex gap-4 p-4 border-b bg-white" aria-label="Main navigation">
      <Link href={`/${locale}`}>{t("home")}</Link>
      <Link href={`/${locale}/services`}>{t("services")}</Link>
      <Link href={`/${locale}/pricing`}>{t("pricing")}</Link>
      <Link href={`/${locale}/about`}>{t("about")}</Link>
      <Link href={`/${locale}/legal`}>{t("legal")}</Link>
      <Link href={`/${locale}/contact`}>{t("contact")}</Link>
      <a href="/api/auth/login" className="ml-auto">{t("cta")}</a>
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
          <main className="mx-auto max-w-4xl p-6">{children}</main>
        </NextIntlClientProvider>
      </body>
    </html>
  );
}
