# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Architecture

Platziflix is a multi-platform online course platform:

- **Backend**: FastAPI + PostgreSQL 15, containerized via Docker Compose, managed with UV
- **Frontend**: Next.js 15 (App Router) + TypeScript + SCSS Modules
- **Mobile**: Android (Kotlin + Jetpack Compose) and iOS (Swift + SwiftUI) — placeholder structure

The frontend and mobile apps consume the backend REST API as their sole data source. The backend runs at `http://localhost:8000`, frontend at `http://localhost:3000`.

## Backend Commands

All backend commands run from `Backend/`. Docker must be running first.

```bash
make start            # Start Docker Compose (API + DB)
make stop             # Stop containers
make logs             # Follow container logs
make migrate          # Apply Alembic migrations
make create-migration # Prompt for a message, then autogenerate a migration
make seed             # Seed demo data
make seed-fresh       # Clear and re-seed
make clean            # Remove containers, volumes, and images
```

Before running any `docker-compose exec` command, verify the `api` container is up (`make logs`).

**Run backend tests** (inside the api container):
```bash
docker-compose exec api bash -c "cd /app && uv run pytest"
# Single test file:
docker-compose exec api bash -c "cd /app && uv run pytest app/tests/test_rating_endpoints.py"
# Single test by name:
docker-compose exec api bash -c "cd /app && uv run pytest -k test_create_rating"
```

## Frontend Commands

All frontend commands run from `Frontend/`. Node 18 is required (see `.npmrc`).

```bash
npm run dev    # Dev server with Turbopack
npm run build  # Production build
npm run lint   # ESLint
npm run test   # Vitest (watch mode off in CI)
```

**Run a single test file:**
```bash
npx vitest run src/components/StarRating/StarRating.test.tsx
```

## Data Model

- **Course** — has a URL-friendly `slug`, many-to-many with Teacher via `course_teachers`
- **Teacher** — associated with one or more courses
- **Lesson** — belongs to a Course (one-to-many)
- **Class** — belongs to a Lesson (one-to-many); carries the video URL
- **CourseRating** — per-user rating for a course (1–5 stars)

## API Endpoints

```
GET  /health                                    # Health check + DB connectivity
GET  /courses                                   # List all courses
GET  /courses/{slug}                            # Course detail (teachers, lessons, classes)
GET  /classes/{class_id}                        # Class/video detail
POST /courses/{course_id}/ratings               # Create or update a rating
GET  /courses/{course_id}/ratings               # List ratings for a course
GET  /courses/{course_id}/ratings/stats         # Aggregate rating stats
GET  /courses/{course_id}/ratings/user/{user_id}
PUT  /courses/{course_id}/ratings/{user_id}
DELETE /courses/{course_id}/ratings/{user_id}
```

Swagger UI is available at `http://localhost:8000/docs`.

## Backend Patterns

- **Service Layer**: business logic lives in `app/services/` (e.g., `course_service.py`)
- **Schemas**: Pydantic v2 models in `app/schemas/` — use these for all input/output
- **Models**: SQLAlchemy 2.0 ORM in `app/models/`
- **Migrations**: `app/alembic/versions/` — always autogenerate, never hand-write SQL
- Use `def` for sync routes, `async def` for async I/O operations
- Handle errors with early returns / guard clauses; raise `HTTPException` for expected errors
- Use FastAPI dependency injection for DB sessions

## Frontend Patterns

- **Routing**: App Router — dynamic routes at `app/course/[slug]/` and `app/classes/[class_id]/`
- **Data fetching**: Server Components with `fetch` — no client-side data fetching layer
- **Styling**: CSS Modules (`.module.scss`) per component; global vars in `src/styles/vars.scss`
- **Testing**: Vitest + React Testing Library; test files colocated as `ComponentName.test.tsx`
- Path alias `@/*` resolves to `src/*`

## Naming Conventions

| Context | Convention |
|---|---|
| Python (backend) | `snake_case` |
| TypeScript/JavaScript | `camelCase` variables, `PascalCase` components/types |
| Swift | `camelCase` / `PascalCase` |
| Kotlin | `camelCase` / `PascalCase` |

## Database

Docker Compose DB credentials (development only):

- User: `platziflix_user` / Password: `platziflix_password` / DB: `platziflix_db` / Port: `5432`

Schema changes require a migration: `make create-migration` → `make migrate`.
