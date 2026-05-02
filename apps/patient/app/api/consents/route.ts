import { db } from "@redmed/db";
import { requireSession } from "@/lib/auth";
import { NextResponse } from "next/server";
import { z } from "zod";

const schema = z.object({ type: z.string().min(1) });

export async function POST(request: Request) {
  const parsed = schema.safeParse(await request.json());
  if (!parsed.success) return NextResponse.json({ error: "invalid" }, { status: 400 });
  const session = await requireSession();
  const user = await db.user.findUnique({ where: { authProviderId: session.authProviderId } });
  if (!user) return NextResponse.json({ error: "unauthorized" }, { status: 401 });
  const profile = await db.patientProfile.findUnique({ where: { userId: user.id } });
  if (!profile) return NextResponse.json({ error: "forbidden" }, { status: 403 });
  const consent = await db.consent.create({ data: { patientId: profile.id, type: parsed.data.type, acceptedAt: new Date() } });
  return NextResponse.json({ id: consent.id });
}
