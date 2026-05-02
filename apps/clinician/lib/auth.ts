import { getSession } from "@auth0/nextjs-auth0";
import type { UserRole } from "@prisma/client";

export async function requireSession() {
  const session = await getSession();
  if (!session?.user.sub || !session.user.email) {
    throw new Error("unauthorized");
  }
  const role = (session.user["https://redmed.example/role"] as UserRole | undefined) ?? "patient";
  const mfa = session.user["https://redmed.example/mfa"] as boolean | undefined;
  return {
    authProviderId: session.user.sub,
    email: session.user.email,
    role,
    mfaVerified: mfa === true
  };
}
