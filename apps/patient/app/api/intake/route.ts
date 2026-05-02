import { db } from "@redmed/db";
import { encryptField, intakeDraftSchema, rateLimit } from "@redmed/shared";
import { requireSession } from "@/lib/auth";
import { audit } from "@/lib/audit";
import { NextResponse } from "next/server";

export async function POST(request: Request) {
  const body = await request.json();
  const parsed = intakeDraftSchema.safeParse(body);
  if (!parsed.success) return NextResponse.json({ error: "invalid" }, { status: 400 });
  const session = await requireSession();
  if (!rateLimit(`intake:${session.authProviderId}`, 20, 60_000)) return NextResponse.json({ error: "rate_limited" }, { status: 429 });

  const user = await db.user.findUnique({ where: { authProviderId: session.authProviderId } });
  if (!user) return NextResponse.json({ error: "unauthorized" }, { status: 401 });
  const profile = await db.patientProfile.findUnique({ where: { userId: user.id } });
  if (!profile) return NextResponse.json({ error: "forbidden" }, { status: 403 });

  const created = await db.intakeQuestionnaire.create({
    data: {
      patientId: profile.id,
      status: parsed.data.status,
      answersJson: parsed.data.answersJson,
      summaryEncrypted: encryptField(JSON.stringify(parsed.data.answersJson))
    }
  });
  await audit(user.id, "intake.saved", "IntakeQuestionnaire", created.id);
  return NextResponse.json({ id: created.id });
}
