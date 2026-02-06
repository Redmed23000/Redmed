import { useTranslations } from "next-intl";

export default function LegalPage() {
  const t = useTranslations("legal");
  return <h1 className="text-2xl font-semibold">{t("title")}</h1>;
}
