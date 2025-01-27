# IntelliTrader

A sophisticated algorithmic trading platform built with Next.js 15, FastAPI, and KiteConnect API, designed for the Indian stock market. IntelliTrader empowers traders with automated strategies, real-time market data, and advanced portfolio management.

## Features

- 🚀 **Algorithmic Trading**
  - Custom strategy implementation
  - Real-time market data processing
  - Automated trade execution

- 🔒 **Security**
  - JWT-based authentication
  - Secure API endpoints
  - Environment-based configuration
  - Role-based access control

- 📊 **Trading Capabilities**
  - Custom strategy implementation
  - Real-time market data processing
  - Automated trade execution
  - Handsfree trading
  - Strategy and Portfolio Dashboard

## Tech Stack

### Frontend
- Next.js 15 with App Router
- TypeScript
- TailwindCSS
- Shadcn UI
- NextAuth v5 (Auth.js)
- Prisma ORM

### Backend
- FastAPI
- SQLAlchemy
- PostgreSQL
- Docker
- KiteConnect API

## Project Structure

```
IntelliTrader/
├── frontend/
│   ├── app/                 # Next.js 15 app router
│   ├── components/          # Reusable UI components
│   ├── lib/                 # Utility functions
│   ├── services/           # API services
│   └── types.ts            # TypeScript definitions
│
├── backend/
│   ├── api/                # FastAPI routes
│   ├── services/           # Business logic
│   ├── domain/             # Models and schemas
│   ├── algorithms/         # Trading algorithms
│   └── database/           # DB migrations and functions
```

## Setup and Installation

### Prerequisites
- Node.js 18+
- Python 3.9+
- PostgreSQL
- Docker

### Frontend Setup
```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Database Setup
```bash
docker-compose up -d
```

## Environment Variables

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your-secret
```

### Backend (.env)
```
DATABASE_URL=postgresql://user:password@localhost:5432/intellitrader
KITE_API_KEY=your-kite-api-key
KITE_API_SECRET=your-kite-api-secret
```

## Development Guidelines

### Git Commit Convention
- `fix:` Bug fixes (patch)
- `feat:` New features (minor)
- `feat!:`, `fix!:`, `refactor!:` Breaking changes (major)
- `docs:` Documentation updates
- `revert:` Revert changes

### Code Style
- TypeScript: Follow strict type checking
- Python: Follow PEP 8 guidelines
- Use descriptive variable names
- Implement proper error handling
- Write comprehensive tests

## Architecture Flow

```
Frontend ←→ FastAPI Backend ←→ KiteConnect API
    ↓            ↓
    └────→ PostgreSQL ←────┘
```

## License

MIT License - See LICENSE file for details

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'feat: Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request