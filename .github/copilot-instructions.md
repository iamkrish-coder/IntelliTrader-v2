### Coding Environment

- Frameworks & Libraries: NextJS v15, TypeScript, TailwindCSS, Shadcn UI
- Database: PostgreSQL (self-hosted on Docker)
- Python Backend: FastAPI, SQLAlchemy
- Trading API: KiteConnect

### Project Structure

Backend:

- Use FastAPI for REST API endpoints
- Organize code in domain-driven structure (controllers, services, models)
- Place trading algorithms in algorithms/ directory
- Keep database migrations in database/ directory
- Store configurations in configurations/ directory

Frontend:

- Follow Next.js 15 App Router structure
- Keep reusable components in components/ directory
- Store utility functions in lib/ directory
- Maintain types in types.ts
- Use Prisma for database access for authentication

### Code Style and Structure

- Adhere to best practices; ensure code is correct, bug-free, and fully functional
- Follow the DRY (Don't Repeat Yourself) principle
- Write concise, technical TypeScript/JavaScript and Python code
- Favor iteration and modularization to prevent code duplication
- Use descriptive variable names with auxiliary verbs (e.g., isLoading, hasError)
- Prioritize readability and maintainability over performance
- Fully implement all requested features without leaving TODOs or placeholders
- Include all necessary imports and ensure proper naming conventions for key components
- If uncertain about an answer, acknowledge it instead of guessing

### Trading-Specific Guidelines

- Utilize KiteConnect API for trading
- India Stock Market
- Use proper error handling for all API calls to KiteConnect
- Implement proper logging for all trading operations
- Handle historical data limits as per API specifications

### Naming Conventions

- Use lowercase with dashes for directory names (e.g., components/auth-wizard)
- Prefer named exports for components
- Python files: Use snake_case
- TypeScript/JavaScript files: Use camelCase
- Class names: Use PascalCase
- Component names: Use lowercase & kebab-case
- Database tables: Use snake_case

### TypeScript Usage

- Utilize Next.js v15 with the App Router
- Write all code in TypeScript; prefer interfaces over types
- Avoid using enums; opt for maps instead
- Implement functional components with TypeScript interfaces

### Python Usage

- Use type hints consistently
- Follow PEP 8 style guide
- Use dataclasses for data models
- Use async/await for I/O operations

### UI and Styling

- Utilize Shadcn UI and TailwindCSS for component styling
- Ensure responsive design with Tailwind CSS
- Always apply Tailwind classes for styling HTML elements; avoid inline CSS or tags
- Implement dark mode support using Tailwind's dark: prefix

### Database

- PostgreSQL running on Docker
- Use a unified PostgreSQL database for both frontend and backend
- Conduct all database operations using stored procedures or functions
- Refer to the IntelliTrader/backend/database directory for database-related context
- Check table definitions before generating database queries for accurate field names
- Use Prisma for frontend database access

### Authentication & Security

- Use NextAuth v5 aka Auth.js for frontend authentication
- Implement proper JWT token handling
- Store sensitive credentials in .env files
- Never commit sensitive data to version control

### Code Implementation Guidelines

- Use early returns to enhance code readability
- Prefer class: over the ternary operator in class tags
- Employ descriptive names for variables and functions; prefix event handlers with "handle" (e.g., handleClick, handleKeyDown)
- Implement accessibility features on elements (e.g., tabindex="0", aria-label, on:click, on:keydown)
- Use const for function declarations, e.g., const toggle = () =>

### Git Workflow

Follow conventional commits:

- fix: for bug fixes (patch)
- feat: for new features (minor)
- feat!, fix!, refactor!: for breaking changes (major)
- docs: for documentation updates
- revert: for reverting changes

### Application Flow and Architecture

Frontend to Backend Flow:

- Frontend NextJS routes make API calls to FastAPI endpoints in `/api/v1/routes.py`
- All API endpoints follow RESTful conventions
- API responses use consistent schema defined in `/domain/schemas/`
- Each endpoint has proper error handling and logging
- API Flow: Frontend -> Backend (routes) -> Domain (schema) -> (service) -> (model) -> (repository) -> Database (stored procedure/function)
- When creating a new route, please refer to the other routes in routes.py for consistency
- We should have a definition of table created as {table_name}.sql (/backend/database/definitions)
- We should have a schema (/backend/domain/schemas) file
- We should have a service (/backend/services) file
- We should have a model (/backend/domain/models) file for the building the domain model
- We should have a repository (/backend/domain/repositories) file for to call Stored Procedure or Function
- We should have a Stored Procedure (/backend/database/stored_procedures) or Function (/backend/database/functions) created for the database operations

Backend Architecture Layers:

Routes Layer (`/api/v1/routes.py`):

- Handles HTTP requests and responses
- Validates request data using Pydantic schemas
- Delegates business logic to service layer
- Implements proper error handling and logging

Service Layer (`/services/`):

- Implements business logic
- Coordinates between multiple domains
- Handles data transformation
- Calls appropriate database functions/procedures

Domain Layer (`/domain/`):

- Contains data models and schemas
- Defines business rules and validations
- Uses Pydantic for schema validation
- Maintains type safety with TypeScript interfaces

Database Layer:

- Uses stored procedures for write operations
- Uses functions for read operations
- Implements proper error handling and returns appropriate data
- Follows naming convention: `it_[module]_[operation]_[sp/fn]`

Data Flow Example (Preferences):

- Refer DEVELOPMENT_RULES.md for more details
