### Coding Environment
Frameworks & Libraries: NextJS v15, TypeScript, TailwindCSS, Shadcn UI
Database: PostgreSQL (self-hosted on Docker)

### Code Style and Structure
Adhere to best practices; ensure code is correct, bug-free, and fully functional.
Follow the DRY (Don't Repeat Yourself) principle.
Write concise, technical TypeScript/JavaScript code.
Favor iteration and modularization to prevent code duplication.
Use descriptive variable names with auxiliary verbs (e.g., isLoading, hasError).
Prioritize readability and maintainability over performance.
Fully implement all requested features without leaving TODOs or placeholders.
Include all necessary imports and ensure proper naming conventions for key components.
If uncertain about an answer, acknowledge it instead of guessing.

### Naming Conventions
Use lowercase with dashes for directory names (e.g., components/auth-wizard).
Prefer named exports for components.

### TypeScript Usage
Utilize Next.js v15 with the App Router.
Write all code in TypeScript; prefer interfaces over types.
Avoid using enums; opt for maps instead.
Implement functional components with TypeScript interfaces.

### UI and Styling
Utilize Shadcn UI and TailwindCSS for component styling.
Ensure responsive design with Tailwind CSS.
Always apply Tailwind classes for styling HTML elements; avoid inline CSS or tags.

### Database
Use a unified PostgreSQL database for both frontend and backend.
Conduct all database operations using stored procedures or functions.
Refer to the IntelliTrader/backend/database directory for database-related context.
Check table definitions before generating database queries for accurate field names.

### Libraries
Use NextAuth v5 aka Auth.js for authentication.

### Code Implementation Guidelines
Use early returns to enhance code readability.
Prefer class: over the ternary operator in class tags.
Employ descriptive names for variables and functions; prefix event handlers with “handle” (e.g., handleClick, handleKeyDown).
Implement accessibility features on elements (e.g., tabindex="0", aria-label, on:click, on:keydown).
Use const for function declarations, e.g., const toggle = () =>.
