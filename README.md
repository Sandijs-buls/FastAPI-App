# Databate

A RESTful post platform API built with FastAPI. Enable users to sign up, post, vote on other posts.

---

## Tech Stack

**Backend Framework**
- **FastAPI:** Modern Python web framework for building fast APIs
- **SQLAlchemy:** Object-relational mapper for database abstraction
- **Alembic:** Database schema versioning and migrations

**Database & Authentication**
- **PostgreSQL:** Robust relational database for data persistence
- **JWT (JSON Web Tokens):** Secure token-based authentication
- **Passlib + Bcrypt:** Industry-standard password hashing and security

**Deployment & Infrastructure**
- **Docker & Docker Compose:** Containerization for consistent environments
- **Heroku:** Cloud platform for production hosting
- **GitHub Actions:** Automated CI/CD pipeline for testing and deployment
- **Uvicorn:** ASGI server for running the application

**Testing & Development**
- **Pytest:** Comprehensive testing framework with fixtures and parametrization
- **Python 3.12+:** Latest Python runtime with modern language features

---

## Features

### User Management
- **Account Registration:** Create new user accounts with email validation
- **Secure Authentication:** Password hashing with bcrypt and JWT token generation
- **User Profiles:** Retrieve and manage user account information
- **Access Control:** Role-based permissions preventing unauthorized modifications

### Post Management
- **Create Posts:** Authenticated users can publish discussion content
- **Search & Filter:** Find posts by title with flexible pagination controls
- **Update Posts:** Edit your own posts with ownership enforcement
- **Delete Posts:** Remove posts with automatic cleanup of related data
- **Post Ownership:** Only creators can modify or delete their content

### Community Voting
- **Upvote System:** Users can upvote posts once to show appreciation
- **Vote Tracking:** Prevent duplicate votes on the same post
- **Remove Votes:** Allow users to change their voting decisions
- **Conflict Prevention:** Automatic handling of edge cases and duplicate attempts

### Database Design
- **Normalized Schema:** Three-table design (users, posts, votes) preventing data redundancy
- **Referential Integrity:** Foreign key constraints maintaining data consistency
- **Cascading Deletes:** Automatic cleanup of related records when parents are removed
- **Migration Support:** Version-controlled schema changes with Alembic

### Developer Experience
- **Interactive API Docs:** Auto-generated Swagger UI at `/docs` endpoint
- **Comprehensive Testing:** Isolated test database with fixture support
- **Docker Support:** Pre-configured dev and production environments
- **CI/CD Pipeline:** Automated testing, building, and deployment workflow

---

## Project Structure

```
databate/
├── app/                          # Application core
│   ├── main.py                  # FastAPI application initialization
│   ├── database.py              # Database connection setup
│   ├── models.py                # SQLAlchemy ORM models
│   ├── schemas.py               # Pydantic request/response schemas
│   ├── config.py                # Configuration management
│   ├── oauth2.py                # JWT authentication logic
│   ├── utils.py                 # Helper functions
│   ├── calculations.py          # Business logic utilities
│   └── routers/                 # Endpoint route handlers
│       ├── user.py              # User management endpoints
│       ├── auth.py              # Authentication endpoints
│       ├── post.py              # Post CRUD endpoints
│       └── vote.py              # Voting endpoints
├── tests/                        # Test suite
│   ├── conftest.py              # Pytest configuration and fixtures
│   ├── database.py              # Test database setup
│   ├── test_users.py            # User endpoint tests
│   ├── test_posts.py            # Post endpoint tests
│   ├── test_votes.py            # Voting tests
│   └── my_test.py               # Additional test cases
├── alembic/                      # Database migrations
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Container image definition
├── docker-compose-dev.yml        # Development container stack
├── docker-compose-prod.yml       # Production container stack
├── Procfile                      # Heroku deployment configuration
└── alembic.ini                   # Alembic configuration
```

---

## Getting Started

### Prerequisites
- Python 3.12 or later
- PostgreSQL database server
- Docker & Docker Compose (optional, for containerized setup)

### Local Development Setup

**1. Clone and navigate to project:**
```bash
git clone https://github.com/Sandijs-buls/DataBate.git
cd DataBate
```

**2. Create Python virtual environment:**
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

**3. Install project dependencies:**
```bash
pip install -r requirements.txt
```

**4. Configure environment variables:**

Create a `.env` file in the project root:
```env
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_NAME=your_database_name
DATABASE_USERNAME=your_postgres_user
DATABASE_PASSWORD=your_postgres_password
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Generate a secure SECRET_KEY:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

**5. Initialize the database:**
```bash
alembic upgrade head
```

**6. Start the development server:**
```bash
uvicorn app.main:app --reload
```

Visit `http://localhost:8000` and explore interactive docs at `http://localhost:8000/docs`.

---

## Containerized Deployment

### Using Pre-built Image

Pull the latest image from Docker Hub:
```bash
docker pull sandijsbuls/fastapi
```

### Build Locally with Docker Compose

**1. Create `.env.docker` file with PostgreSQL hostname:**
```env
DATABASE_HOSTNAME=postgres
DATABASE_PORT=5432
DATABASE_NAME=your_database_name
DATABASE_USERNAME=your_postgres_user
DATABASE_PASSWORD=your_postgres_password
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**2. Start development environment (with hot reload):**
```bash
docker-compose -f docker-compose-dev.yml up -d
```

**3. Run database migrations:**
```bash
docker-compose -f docker-compose-dev.yml exec api alembic upgrade head
```

For production deployment without live reload capabilities, use `docker-compose-prod.yml` instead.

---

## API Reference

The platform exposes the following endpoints:

| Method | Path | Auth Required | Description |
|--------|------|---------------|-------------|
| POST | `/users/` | ❌ | Register new user account |
| GET | `/users/{id}` | ❌ | Retrieve user by ID |
| POST | `/login` | ❌ | Authenticate and receive JWT token |
| GET | `/posts/` | ❌ | List posts with search and pagination |
| POST | `/posts/` | ✅ | Create new post (authenticated users) |
| GET | `/posts/{id}` | ❌ | Get specific post |
| PUT | `/posts/{id}` | ✅ | Update post (owner only) |
| DELETE | `/posts/{id}` | ✅ | Delete post (owner only) |
| POST | `/vote/` | ✅ | Add or remove vote on post |

---

## Testing

The test suite provides comprehensive coverage using pytest with an isolated test database for each run.

**Test Coverage:**
- User registration and authentication flows
- JWT token generation and validation
- Complete post CRUD operations with permission checks
- Vote management and conflict resolution
- Error handling for unauthorized access (401, 403)
- Edge cases like non-existent resources (404)

**Setup and Run Tests:**

Create a test database named `{DATABASE_NAME}_test`, then execute:
```bash
pytest -v -s
```

---

## Automated CI/CD Pipeline

GitHub Actions automates the entire deployment workflow (`.github/workflows/build-deploy.yml`) on every push to main:

**Stage 1: Test**
- Spins up PostgreSQL service container
- Installs dependencies from requirements.txt
- Runs complete pytest suite against fresh test database
- Fails fast if any tests don't pass

**Stage 2: Build**
- Constructs Docker image from Dockerfile
- Pushes image to Docker Hub registry
- Only executes after tests pass successfully

**Stage 3: Deploy**
- Releases new image to Heroku platform
- Automatically runs Alembic migrations via Procfile release phase
- Makes latest version live in production

The pipeline ensures broken code never reaches production by requiring successful testing before any build or deployment steps.

---

## Database Schema

The application uses a normalized three-table design:

**users:** User account information with hashed passwords and metadata
**posts:** User-generated discussion content with timestamps and ownership tracking
**votes:** Upvote records linking users to posts with uniqueness constraints

All tables include foreign key relationships with cascading delete behavior for data integrity.

---
