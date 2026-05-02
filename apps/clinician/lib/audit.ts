import { db } from "@redmed/db";

export async function audit(actorUserId: string, action: string, resourceType: string, resourceId: string) {
  await db.auditLog.create({ data: { actorUserId, action, resourceType, resourceId } });
}
