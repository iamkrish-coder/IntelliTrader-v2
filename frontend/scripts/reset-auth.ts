import { PrismaClient } from '@prisma/client';

const resetAuth = async () => {
  const prisma = new PrismaClient();
  
  try {
    // For PostgreSQL
    await prisma.$transaction([
      prisma.$executeRaw`TRUNCATE TABLE "Account" CASCADE;`,
      prisma.$executeRaw`TRUNCATE TABLE "Session" CASCADE;`,
      prisma.$executeRaw`TRUNCATE TABLE "VerificationToken" CASCADE;`,
      prisma.$executeRaw`TRUNCATE TABLE "User" CASCADE;`,
    ]);

    console.log('All Authentication tables truncated successfully');
  } catch (error) {
    console.error('Error truncating Authentication tables:', error);
  } finally {
    await prisma.$disconnect();
  }
};

resetAuth(); 