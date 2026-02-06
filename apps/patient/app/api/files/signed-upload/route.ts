import { PutObjectCommand, S3Client } from "@aws-sdk/client-s3";
import { getSignedUrl } from "@aws-sdk/s3-request-presigner";
import { db } from "@redmed/db";
import { requireSession } from "@/lib/auth";
import { audit } from "@/lib/audit";
import { NextResponse } from "next/server";
import { z } from "zod";

const schema = z.object({ mimeType: z.literal("application/pdf"), fileName: z.string().min(1) });

export async function POST(request: Request) {
  const parsed = schema.safeParse(await request.json());
  if (!parsed.success) return NextResponse.json({ error: "invalid" }, { status: 400 });
  const session = await requireSession();
  const user = await db.user.findUnique({ where: { authProviderId: session.authProviderId } });
  if (!user) return NextResponse.json({ error: "unauthorized" }, { status: 401 });

  const key = `${user.id}/${Date.now()}-${parsed.data.fileName}`;
  const client = new S3Client({ endpoint: process.env.S3_ENDPOINT, region: process.env.S3_REGION, forcePathStyle: true });
  const command = new PutObjectCommand({ Bucket: process.env.S3_BUCKET, Key: key, ContentType: parsed.data.mimeType });
  const url = await getSignedUrl(client, command, { expiresIn: 300 });

  const asset = await db.fileAsset.create({ data: { ownerUserId: user.id, storageKey: key, mimeType: parsed.data.mimeType } });
  await audit(user.id, "file.upload_url.created", "FileAsset", asset.id);
  return NextResponse.json({ url, assetId: asset.id });
}
