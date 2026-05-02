import { useTranslations } from "next-intl";

export default function AboutPage() {
  const t = useTranslations("about");
  return <h1 className="text-2xl font-semibold">{t("title")}</h1>;
}
