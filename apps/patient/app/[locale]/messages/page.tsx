import { useTranslations } from "next-intl";
export default function MessagesPage(){const t=useTranslations("messages"); return <h1 className="text-2xl font-semibold">{t("title")}</h1>;}
