import { db } from "@redmed/db";
import { encryptField, messageSchema, rateLimit } from "@redmed/shared";
import { requireSession } from "@/lib/auth";
import { audit } from "@/lib/audit";
import { NextResponse } from "next/server";

export async function POST(request: Request) {
  const payload = messageSchema.safeParse(await request.json());
  if (!payload.success) return NextResponse.json({ error: "invalid" }, { status: 400 });
  const session = await requireSession();
  if (!rateLimit(`msg:${session.authProviderId}`, 50, 60_000)) return NextResponse.json({ error: "rate_limited" }, { status: 429 });

  const user = await db.user.findUnique({ where: { authProviderId: session.authProviderId } });
  if (!user) return NextResponse.json({ error: "unauthorized" }, { status: 401 });
  const message = await db.message.create({
    data: { threadId: payload.data.threadId, senderUserId: user.id, bodyEncrypted: encryptField(payload.data.body) }
  });
  await audit(user.id, "message.sent", "Message", message.id);
  return NextResponse.json({ id: message.id });
}
