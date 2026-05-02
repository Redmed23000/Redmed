const bucket = new Map<string, { count: number; resetAt: number }>();

export function rateLimit(key: string, max: number, windowMs: number): boolean {
  const now = Date.now();
  const existing = bucket.get(key);
  if (!existing || now > existing.resetAt) {
    bucket.set(key, { count: 1, resetAt: now + windowMs });
    return true;
  }
  if (existing.count >= max) {
    return false;
  }
  existing.count += 1;
  return true;
}
