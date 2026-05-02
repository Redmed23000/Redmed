import { PrismaClient } from "@prisma/client";

declare global {
  // eslint-disable-next-line no-var
  var prismaClientSingleton: PrismaClient | undefined;
}

export const db = global.prismaClientSingleton ?? new PrismaClient();

if (process.env.NODE_ENV !== "production") {
  global.prismaClientSingleton = db;
}
