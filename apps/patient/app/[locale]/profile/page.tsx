import { useTranslations } from "next-intl";
export default function ProfilePage(){const t=useTranslations("profile"); return <h1 className="text-2xl font-semibold">{t("title")}</h1>;}
