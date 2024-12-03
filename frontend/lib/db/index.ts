import { drizzle } from 'drizzle-orm/node-postgres';
import { Pool } from 'pg';

if (!process.env.DB_HOST) throw new Error('DB_HOST is required');
if (!process.env.DB_USER) throw new Error('DB_USER is required');
if (!process.env.DB_PASSWORD) throw new Error('DB_PASSWORD is required');
if (!process.env.DB_NAME) throw new Error('DB_NAME is required');

const pool = new Pool({
  host: process.env.DB_HOST,
  port: parseInt(process.env.DB_PORT || '5432'),
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
  ssl: process.env.NODE_ENV === 'production' ? { rejectUnauthorized: false } : false,
});

export const db = drizzle(pool);
