import { db } from "@redmed/db";
import { encounterSchema, encryptField, requireRole, rateLimit } from "@redmed/shared";
import { requireSession } from "@/lib/auth";
import { audit } from "@/lib/audit";
import { NextResponse } from "next/server";

export async function POST(request: Request) {
  const payload = encounterSchema.safeParse(await request.json());
  if (!payload.success) return NextResponse.json({ error: "invalid" }, { status: 400 });
  const session = await requireSession();
  requireRole(session.role, "clinician");
  if (!session.mfaVerified) return NextResponse.json({ error: "mfa_required" }, { status: 403 });
  if (!rateLimit(`enc:${session.authProviderId}`, 30, 60_000)) return NextResponse.json({ error: "rate_limited" }, { status: 429 });

  const clinicianUser = await db.user.findUnique({ where: { authProviderId: session.authProviderId }, include: { clinician: true } });
  if (!clinicianUser?.clinician) return NextResponse.json({ error: "forbidden" }, { status: 403 });
  const patient = await db.patientProfile.findUnique({ where: { id: payload.data.patientId } });
  if (!patient || patient.assignedClinicianId !== clinicianUser.clinician.id) return NextResponse.json({ error: "forbidden" }, { status: 403 });

  const encounter = await db.encounter.create({
    data: { patientId: patient.id, clinicianId: clinicianUser.clinician.id, notesEncrypted: encryptField(payload.data.notes) }
  });
  await audit(clinicianUser.id, "encounter.created", "Encounter", encounter.id);
  return NextResponse.json({ id: encounter.id });
}
