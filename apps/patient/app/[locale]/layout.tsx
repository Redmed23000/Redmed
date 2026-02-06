import "../globals.css";
import { NextIntlClientProvider } from "next-intl";
import { getMessages } from "next-intl/server";
import type { ReactNode } from "react";
import Link from "next/link";
import { useTranslations } from "next-intl";

function Nav({ locale }: { locale: string }) {
  const t = useTranslations("nav");
  return (
    <nav className="flex gap-4 border-b bg-white p-4" aria-label="Patient navigation">
      <Link href={`/${locale}`}>{t("dashboard")}</Link>
      <Link href={`/${locale}/intake`}>{t("intake")}</Link>
      <Link href={`/${locale}/messages`}>{t("messages")}</Link>
      <Link href={`/${locale}/files`}>{t("files")}</Link>
      <Link href={`/${locale}/billing`}>{t("billing")}</Link>
      <Link href={`/${locale}/profile`}>{t("profile")}</Link>
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
