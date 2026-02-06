import { createCipheriv, createDecipheriv, randomBytes } from "node:crypto";

const ALGO = "aes-256-gcm";

function keyBuffer(): Buffer {
  const key = process.env.FIELD_ENCRYPTION_KEY ?? "";
  if (key.length !== 64) {
    throw new Error("FIELD_ENCRYPTION_KEY must be a 64-char hex string");
  }
  return Buffer.from(key, "hex");
}

export function encryptField(plaintext: string): string {
  const iv = randomBytes(12);
  const cipher = createCipheriv(ALGO, keyBuffer(), iv);
  const encrypted = Buffer.concat([cipher.update(plaintext, "utf8"), cipher.final()]);
  const tag = cipher.getAuthTag();
  return `${iv.toString("hex")}.${tag.toString("hex")}.${encrypted.toString("hex")}`;
}

export function decryptField(payload: string): string {
  const [ivHex, tagHex, encryptedHex] = payload.split(".");
  if (!ivHex || !tagHex || !encryptedHex) {
    throw new Error("Invalid encrypted payload");
  }
  const decipher = createDecipheriv(ALGO, keyBuffer(), Buffer.from(ivHex, "hex"));
  decipher.setAuthTag(Buffer.from(tagHex, "hex"));
  const decrypted = Buffer.concat([
    decipher.update(Buffer.from(encryptedHex, "hex")),
    decipher.final()
  ]);
  return decrypted.toString("utf8");
}
