import { useTranslations } from "next-intl";
export default function FilesPage(){const t=useTranslations("files"); return <h1 className="text-2xl font-semibold">{t("title")}</h1>;}
