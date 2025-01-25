import { NextRequest, NextResponse } from "next/server";
import { PrismaClient } from "@prisma/client";
import bcrypt from "bcryptjs";
import { z } from "zod";

const prisma = new PrismaClient();

// Input validation schema
const registerSchema = z.object({
  name: z.string().min(2, "Name must be at least 2 characters"),
  email: z.string().email("Invalid email address"),
  password: z.string().min(6, "Password must be at least 6 characters"),
});

export async function POST(req: NextRequest) {
  try {
    // Ensure request has a body
    if (!req.body) {
      return NextResponse.json(
        { error: "Request body is required" },
        { status: 400 },
      );
    }

    let body;
    try {
      body = await req.json();
    } catch (e) {
      return NextResponse.json(
        { error: "Invalid JSON in request body" },
        { status: 400 },
      );
    }

    // Validate input
    const validationResult = registerSchema.safeParse(body);
    if (!validationResult.success) {
      return NextResponse.json(
        { error: validationResult.error.errors[0].message },
        { status: 400 },
      );
    }

    const validatedData = validationResult.data;

    try {
      // Check if user already exists
      const existingUser = await prisma.user.findUnique({
        where: { email: validatedData.email },
      });

      if (existingUser) {
        return NextResponse.json(
          { error: "User with this email already exists" },
          { status: 400 },
        );
      }

      // Hash password
      const hashedPassword = await bcrypt.hash(validatedData.password, 12);

      // Create user
      const user = await prisma.user.create({
        data: {
          name: validatedData.name,
          email: validatedData.email,
          password: hashedPassword,
          emailVerified: null,
          image: null,
        },
      });

      // Remove password from response
      const { password: _, ...userWithoutPassword } = user;

      return NextResponse.json(
        {
          message: "User registered successfully",
          user: userWithoutPassword,
        },
        { status: 201 },
      );
    } catch (dbError) {
      console.error(
        "Database error:",
        dbError instanceof Error ? dbError.message : dbError,
      );
      return NextResponse.json(
        { error: "Failed to create user" },
        { status: 500 },
      );
    }
  } catch (error) {
    console.error(
      "Registration error:",
      error instanceof Error ? error.message : error,
    );
    return NextResponse.json(
      { error: "An unexpected error occurred during registration" },
      { status: 500 },
    );
  } finally {
    await prisma.$disconnect();
  }
}
