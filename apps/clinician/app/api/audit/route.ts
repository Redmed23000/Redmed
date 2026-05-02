import { db } from "@redmed/db";
import { requireRole } from "@redmed/shared";
import { requireSession } from "@/lib/auth";
import { NextResponse } from "next/server";

export async function GET() {
  const session = await requireSession();
  requireRole(session.role, "clinician");
  if (!session.mfaVerified) return NextResponse.json({ error: "mfa_required" }, { status: 403 });

  const user = await db.user.findUnique({ where: { authProviderId: session.authProviderId }, include: { clinician: true } });
  if (!user) return NextResponse.json({ error: "unauthorized" }, { status: 401 });

  const logs = await db.auditLog.findMany({ where: { actorUserId: user.id }, orderBy: { createdAt: "desc" }, take: 100 });
  return NextResponse.json({ logs });
}
