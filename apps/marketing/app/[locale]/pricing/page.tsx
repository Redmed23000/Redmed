import { useTranslations } from "next-intl";

export default function PricingPage() {
  const t = useTranslations("pricing");
  return <h1 className="text-2xl font-semibold">{t("title")}</h1>;
}
