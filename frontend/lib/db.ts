declare global {
  var pool: Pool | undefined;
}

import { Pool } from "pg";

let pool: Pool;

if (!global.pool) {
  global.pool = new Pool({
    host: process.env.DATABASE_HOST,
    port: parseInt(process.env.DATABASE_PORT || "5432"),
    database: process.env.DATABASE_NAME,
    user: process.env.DATABASE_USER,
    password: process.env.DATABASE_PASSWORD,
  });
} else {
  pool = global.pool;
}

export { pool };
