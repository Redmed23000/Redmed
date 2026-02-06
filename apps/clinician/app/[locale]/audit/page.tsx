import { useTranslations } from "next-intl";
export default function AuditPage(){const t=useTranslations("audit"); return <h1 className="text-2xl font-semibold">{t("title")}</h1>;}
