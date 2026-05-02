import { useTranslations } from "next-intl";
export default function PatientsPage(){const t=useTranslations("patients"); return <h1 className="text-2xl font-semibold">{t("title")}</h1>;}
