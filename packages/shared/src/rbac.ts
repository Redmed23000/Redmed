import type { UserRole } from "@prisma/client";

const hierarchy: Record<UserRole, number> = {
  patient: 1,
  clinician: 2,
  admin: 3
};

export function requireRole(currentRole: UserRole, minimum: UserRole): void {
  if (hierarchy[currentRole] < hierarchy[minimum]) {
    throw new Error("forbidden");
  }
}

export function canAccessPatient(currentRole: UserRole, actorId: string, patientUserId: string): boolean {
  return currentRole === "admin" || (currentRole === "patient" && actorId === patientUserId) || currentRole === "clinician";
}
