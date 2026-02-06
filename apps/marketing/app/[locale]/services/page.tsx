import { useTranslations } from "next-intl";

export default function ServicesPage() {
  const t = useTranslations("services");
  return <h1 className="text-2xl font-semibold">{t("title")}</h1>;
}
