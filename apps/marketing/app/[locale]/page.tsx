import { useTranslations } from "next-intl";

export default function HomePage() {
  const t = useTranslations("home");
  return (
    <section className="space-y-4">
      <h1 className="text-3xl font-semibold">{t("title")}</h1>
      <p>{t("subtitle")}</p>
      <p className="rounded bg-amber-100 p-3 text-sm">{t("disclaimer")}</p>
    </section>
  );
}
