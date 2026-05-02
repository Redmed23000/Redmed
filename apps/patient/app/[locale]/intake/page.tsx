import { useTranslations } from "next-intl";
export default function IntakePage(){const t=useTranslations("intake"); return <h1 className="text-2xl font-semibold">{t("title")}</h1>;}
