import { useTranslations } from "next-intl";
export default function BillingPage(){const t=useTranslations("billing"); return <h1 className="text-2xl font-semibold">{t("title")}</h1>;}
