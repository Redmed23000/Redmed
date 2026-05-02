import { useTranslations } from "next-intl";
export default function TriagePage(){const t=useTranslations("triage"); return <h1 className="text-2xl font-semibold">{t("title")}</h1>;}
