import { useTranslations } from "next-intl";
export default function DashboardPage(){const t=useTranslations("dashboard"); return <h1 className="text-2xl font-semibold">{t("title")}</h1>;}
