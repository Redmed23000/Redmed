import { z } from "zod";

export const intakeDraftSchema = z.object({
  status: z.enum(["draft", "submitted"]),
  answersJson: z.record(z.string(), z.string().min(1))
});

export const messageSchema = z.object({
  threadId: z.string().min(1),
  body: z.string().min(1).max(5000)
});

export const encounterSchema = z.object({
  patientId: z.string().min(1),
  notes: z.string().min(1).max(10000)
});
