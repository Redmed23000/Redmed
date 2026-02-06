import { useTranslations } from "next-intl";

export default function ContactPage() {
  const t = useTranslations("contact");
  return <h1 className="text-2xl font-semibold">{t("title")}</h1>;
}
