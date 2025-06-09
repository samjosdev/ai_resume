# Technical Design Document: Fantasy Cricket Web Application

## 1. Introduction

### 1.1 Purpose
This document provides a detailed technical design and architectural blueprint for the development of the Fantasy Cricket Web Application. It translates the business requirements outlined in the BRD into a set of technical specifications for the engineering team. The goal is to create a scalable, maintainable, and performant system.

### 1.2 Scope
This document covers the system architecture, technology stack, data models, API design, module breakdown, and implementation plan for the core features, including user management, team creation, leagues, scoring, and administration. The initial implementation will use mocked data, but the architecture is designed for future integration with live data APIs.

---

## 2. System Architecture

### 2.1 Architectural Style: Modular Monolith
For the initial version of the application, we will adopt a **Modular Monolith** architecture.

**Justification:**
*   **Speed of Development:** A monolithic approach reduces the initial operational and deployment complexity compared to a microservices architecture, allowing the team to build and launch the core product faster.
*   **Simplicity:** Managing a single codebase, a single build process, and a single deployment is more straightforward, especially for a new project.
*   **Performance:** In-process communication between modules is significantly faster than network calls required in a microservices setup.
*   **Future-Proofing (Modularity):** By strictly enforcing separation of concerns and clear boundaries between modules (e.g., `User`, `League`, `Team`), we design the application to be easily broken apart into microservices in the future if scalability demands it. This directly addresses NFR 3.4.1.

### 2.2 High-Level System Diagram

```mermaid
graph TD
    subgraph "User's Browser (Desktop/Mobile)"
        A[React/Next.js Frontend]
    end

    subgraph "Cloud Infrastructure (AWS)"
        LB[Load Balancer]
        subgraph "Application Server (EC2/ECS)"
            B[Node.js/NestJS API Server]
            B -- REST API & WebSocket --> LB
        end

        subgraph "Data Tier"
            C[PostgreSQL Database (RDS)]
            D[Redis (ElastiCache)]
        end

        subgraph "Background Processing"
            E[Job Queue - BullMQ]
            F[Worker Process]
        end

        G[Admin Frontend - React]

        A -- HTTPS --> LB
        G -- HTTPS --> LB
        B -- CRUD Operations --> C
        B -- Caching, Leaderboards, Sessions --> D
        B -- Enqueues Jobs --> E
        F -- Listens for Jobs --> E
        F -- Processes Data --> C & D
    end

    LB --> B
    style A fill:#cde4ff
    style G fill:#d5e8d4
    style B fill:#f8cecc
    style C fill:#dae8fc
    style D fill:#e1d5e7
```

### 2.3 Technology Stack

| Component         | Technology                | Justification                                                                                                                                                    |
| ----------------- | ------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Frontend**      | **React (with Next.js)**  | **React:** Component-based architecture is ideal for the UI. **Next.js:** Provides Server-Side Rendering (SSR) for fast initial loads (NFR 3.1.1) and better SEO. |
| **Backend**       | **Node.js (with NestJS)** | **Node.js:** Excellent for I/O-intensive, real-time applications. **NestJS:** Enforces a modular, scalable architecture with TypeScript for type safety.      |
| **Database**      | **PostgreSQL**            | Robust, open-source relational database ideal for the structured, relational data of the application (Users, Teams, Leagues). Supports complex queries.          |
| **In-Memory Store**| **Redis**                 | Used for caching frequently accessed data (player lists), session management, real-time leaderboards (using sorted sets), and as a message broker for background jobs. |
| **Real-time Comms** | **Socket.IO**             | A reliable WebSocket library for Node.js that enables real-time score and leaderboard updates (NFR 3.1.2) with fallback support.                                 |
| **Job Queue**     | **BullMQ**                | A robust, Redis-based job queue for Node.js. Essential for offloading long-running tasks like point calculation and price updates.                               |
| **Deployment**    | **Docker, AWS (ECS, RDS)** | **Docker:** Containerization ensures consistency across environments. **AWS:** Provides managed services (ECS for containers, RDS for PostgreSQL) for scalability and reliability. |
| **Authentication**| **JWT (JSON Web Tokens)** | A stateless, secure method for handling user authentication across API requests. Tokens will be stored securely on the client.                                    |

---

## 3. Data Model (Database Schema)

The database schema will be built around the entities defined in the BRD. We will use PostgreSQL.

**Key Tables:**

**`users`**
- `id` (UUID, PK)
- `email` (VARCHAR(255), UNIQUE, NOT NULL)
- `password_hash` (VARCHAR(255), NOT NULL)
- `display_name` (VARCHAR(50), UNIQUE, NOT NULL)
- `favorite_team` (VARCHAR(100))
- `experience_level` (ENUM('Beginner', 'Intermediate', 'Expert'))
- `role` (ENUM('User', 'Admin'), DEFAULT 'User')
- `created_at` (TIMESTAMPTZ, NOT NULL)

**`friendships`**
- `id` (UUID, PK)
- `requester_id` (UUID, FK to `users.id`)
- `addressee_id` (UUID, FK to `users.id`)
- `status` (ENUM('Pending', 'Accepted', 'Declined', 'Blocked'), NOT NULL)
- `created_at` (TIMESTAMPTZ, NOT NULL)
- `UNIQUE` (`requester_id`, `addressee_id`)

**`players`**
- `id` (UUID, PK)
- `full_name` (VARCHAR(100), NOT NULL)
- `real_team_name` (VARCHAR(100), NOT NULL)
- `role` (ENUM('Batsman', 'Bowler', 'All-Rounder', 'Wicket-Keeper'), NOT NULL)
- `price` (DECIMAL(5, 2), NOT NULL)
- `injury_status` (ENUM('Active', 'Injured', 'Doubtful'), DEFAULT 'Active')
- `photo_url` (VARCHAR(255))

**`matches`**
- `id` (UUID, PK)
- `gameweek` (INT, NOT NULL)
- `home_team_name` (VARCHAR(100), NOT NULL)
- `away_team_name` (VARCHAR(100), NOT NULL)
- `match_date` (TIMESTAMPTZ, NOT NULL)
- `status` (ENUM('Scheduled', 'Live', 'Completed', 'Cancelled'), NOT NULL)

**`player_match_stats`**
- `id` (UUID, PK)
- `player_id` (UUID, FK to `players.id`)
- `match_id` (UUID, FK to `matches.id`)
- `runs_scored` (INT, DEFAULT 0)
- `balls_faced` (INT, DEFAULT 0)
- `fours` (INT, DEFAULT 0)
- `sixes` (INT, DEFAULT 0)
- `wickets_taken` (INT, DEFAULT 0)
- `overs_bowled` (DECIMAL(3, 1), DEFAULT 0.0)
- `runs_conceded` (INT, DEFAULT 0)
- `maidens_bowled` (INT, DEFAULT 0)
- `catches` (INT, DEFAULT 0)
- `stumpings` (INT, DEFAULT 0)
- `run_outs` (INT, DEFAULT 0)
- `points` (INT, DEFAULT 0) -- Calculated and stored here
- `UNIQUE` (`player_id`, `match_id`)

**`fantasy_teams`**
- `id` (UUID, PK)
- `user_id` (UUID, FK to `users.id`, UNIQUE) -- One team per user for classic mode
- `team_name` (VARCHAR(100), NOT NULL)
- `logo_url` (VARCHAR(255))
- `bank_balance` (DECIMAL(5, 2), DEFAULT 0.0)
- `wildcard_used` (BOOLEAN, DEFAULT false)
- `created_at` (TIMESTAMPTZ, NOT NULL)

**`fantasy_squad_players`**
- `id` (UUID, PK)
- `fantasy_team_id` (UUID, FK to `fantasy_teams.id`)
- `player_id` (UUID, FK to `players.id`)
- `purchase_price` (DECIMAL(5, 2), NOT NULL) -- Price at which the player was bought
- `UNIQUE` (`fantasy_team_id`, `player_id`)

**`gameweek_data`**
- `id` (UUID, PK)
- `fantasy_team_id` (UUID, FK to `fantasy_teams.id`)
- `gameweek` (INT, NOT NULL)
- `captain_id` (UUID, FK to `players.id`)
- `vice_captain_id` (UUID, FK to `players.id`)
- `points` (INT, DEFAULT 0)
- `transfers_made` (INT, DEFAULT 0)
- `UNIQUE` (`fantasy_team_id`, `gameweek`)

**`leagues`**
- `id` (UUID, PK)
- `name` (VARCHAR(100), NOT NULL)
- `type` (ENUM('Public', 'Private'), NOT NULL)
- `invite_code` (VARCHAR(10), UNIQUE) -- Only for private leagues
- `creator_user_id` (UUID, FK to `users.id`)
- `start_gameweek` (INT, NOT NULL)

**`league_memberships`**
- `id` (UUID, PK)
- `league_id` (UUID, FK to `leagues.id`)
- `fantasy_team_id` (UUID, FK to `fantasy_teams.id`)
- `total_points` (INT, DEFAULT 0) -- Denormalized for fast leaderboard queries
- `rank` (INT)
- `UNIQUE` (`league_id`, `fantasy_team_id`)

---

## 4. Module Breakdown & Technical Implementation

### 4.1 User Management Module
- **Components:** `AuthController`, `UsersController`, `UsersService`, `User` Entity.
- **Authentication:**
    1.  **Register (`POST /api/auth/register`):** Receives email, password, displayName. Hashes the password using `bcrypt`. Creates a new user record. Returns a JWT.
    2.  **Login (`POST /api/auth/login`):** Receives email, password. Validates credentials against the `password_hash`. If valid, generates a JWT signed with a secret key.
    3.  **JWT Strategy:** The JWT will contain `userId` and `role`. It will have a short expiry (e.g., 1 hour) and be sent with a refresh token (longer expiry, e.g., 7 days) stored in an HttpOnly cookie for security.
- **Friends System:**
    - `POST /api/friends/request`: Sends a friend request, creating a `friendships` record with `status: 'Pending'`.
    - `PUT /api/friends/respond`: Accepts/declines a request, updating the status.
    - `GET /api/friends`: Retrieves a list of friends (`status: 'Accepted'`).
- **Profile:** Standard CRUD endpoints under `/api/users/profile` protected by the JWT auth guard.

### 4.2 Fantasy Team Creation Module
- **Components:** `TeamsController`, `TeamsService`, `PlayersController`, `Team` & `Player` Entities.
- **Team Creation UI (Next.js):**
    - A multi-panel interface: Player List | Your Squad | Budget/Rule Tracker.
    - Player list fetched from `GET /api/players`. Client-side filtering/searching for performance.
    - State managed using React Context or Zustand for real-time updates to the budget and rule validation.
- **Backend Logic (`TeamsService`):**
    - `POST /api/teams`: Receives an array of 15 `player_id`s.
    - **Transaction:** All logic will be wrapped in a database transaction.
    1.  Validate user does not already have a team.
    2.  Fetch prices for all 15 players.
    3.  Verify total cost is <= $100M.
    4.  Verify all composition rules (min/max roles, max per real team).
    5.  If valid, create `fantasy_teams` and `fantasy_squad_players` records.
    6.  Commit transaction. If any step fails, roll back.
- **Captain Selection (`PUT /api/gameweek-data/{gameweek}`):**
    - Sets the `captain_id` and `vice_captain_id` for the user's team for a specific gameweek.
    - The endpoint will be locked down after the gameweek deadline.

### 4.3 League System Module
- **Components:** `LeaguesController`, `LeaguesService`, `League` Entity.
- **League Creation (`POST /api/leagues`):**
    - If `type: 'Private'`, generate a unique, random `invite_code`.
- **Joining Leagues:**
    - `POST /api/leagues/{leagueId}/join`: For public leagues.
    - `POST /api/leagues/join-private`: With `{ inviteCode }` in the body.
    - In both cases, a `league_memberships` record is created.
- **Leaderboards (Real-time):**
    - **Data Structure:** A **Redis Sorted Set** will be used for each league (`league:<leagueId>:leaderboard`). The `member` will be `fantasy_team_id` and the `score` will be the team's total points.
    - **Update Flow:** When points are calculated (see Scoring Module), the backend updates the score in the sorted set and broadcasts the changes via Socket.IO.
    - **API (`GET /api/leagues/{leagueId}/leaderboard`):** Fetches ranks and scores directly from Redis for ultra-fast reads, satisfying NFR 3.1.3. Periodically syncs back to PostgreSQL.

### 4.4 Scoring & Match Integration Module
- **Components:** `AdminController`, `PointsCalculationService` (Background Worker), `Match` & `PlayerMatchStats` Entities.
- **Admin Data Entry (`Admin Panel`):**
    - A secure frontend (separate React app or protected Next.js pages) for admins.
    - `POST /api/admin/matches/{matchId}/stats`: Admin submits a form with performance stats for each player in a completed match.
- **Background Job Processing:**
    1.  The Admin endpoint does **not** calculate points directly. It validates the input and pushes a job to the **BullMQ** queue. Job payload: `{ matchId }`.
    2.  A separate **Worker Process** listens to this queue.
    3.  **`PointsCalculationService.processMatch(matchId)`:**
        a. Fetches all player stats for the match.
        b. Iterates through each `player_match_stats` record.
        c. Calculates fantasy points based on the scoring rules (`BR 2.4.1` - `2.4.5`).
        d. Updates the `points` column in `player_match_stats`.
        e. Fetches all `fantasy_teams` that have this player in their `gameweek_data` for the current gameweek.
        f. Applies Captain/Vice-Captain multipliers.
        g. Updates the `points` for each `gameweek_data` record and the `total_points` for each `league_memberships` record in a transaction.
        h. Updates the corresponding Redis leaderboards.
        i. Emits a `leaderboard_update` event via Socket.IO with the new data.

### 4.5 Trading & Transfers Module
- **Components:** `TransfersController`, `TransfersService`.
- **Transfer Logic (`POST /api/teams/transfers`):**
    - Receives `{ transfers: [{ playerInId, playerOutId }, ...] }`.
    - Validates against the gameweek deadline.
    - Checks the number of transfers against the user's `transfers_made` for the current gameweek.
    - If `wildcard_used` is true for the user, it allows unlimited transfers.
    - Validates that the new team composition respects all budget and role constraints.
    - All operations performed within a database transaction.
- **Player Price Fluctuation:**
    - A scheduled (cron) background job will run once per gameweek.
    - The job will analyze player selection trends (e.g., number of transfers in/out) and recent performance points.
    - A simple algorithm will be applied to adjust the `price` in the `players` table. E.g., `new_price = old_price * (1 + (transfers_in - transfers_out) / total_users * factor)`.

---

## 5. API Endpoint Design (RESTful)

A summary of key endpoints. All endpoints under `/api` will be prefixed. Auth required where noted.

| Method | Endpoint                               | Description                                     | Auth? |
| ------ | -------------------------------------- | ----------------------------------------------- | ----- |
| POST   | `/auth/register`                       | Register a new user.                            | No    |
| POST   | `/auth/login`                          | Log in a user, receive JWT.                     | No    |
| GET    | `/users/profile`                       | Get current user's profile.                     | Yes   |
| GET    | `/players`                             | Get a list of all available players.            | Yes   |
| POST   | `/teams`                               | Create the user's initial fantasy team.         | Yes   |
| GET    | `/teams/my-team`                       | Get the current user's full squad.              | Yes   |
| PUT    | `/gameweek-data/{gameweek}`            | Set Captain/VC for a specific gameweek.         | Yes   |
| POST   | `/teams/transfers`                     | Perform player transfers for the current gameweek.| Yes   |
| GET    | `/leagues`                             | Get a list of public leagues.                   | Yes   |
| POST   | `/leagues`                             | Create a new league.                            | Yes   |
| GET    | `/leagues/{id}/leaderboard`            | Get the real-time leaderboard for a league.     | Yes   |
| POST   | `/leagues/{id}/join`                   | Join a public league.                           | Yes   |
| POST   | `/admin/matches`                       | (Admin) Create a new match fixture.             | Admin |
| POST   | `/admin/matches/{id}/stats`            | (Admin) Submit player stats for a finished match.| Admin |
| GET    | `/admin/users`                         | (Admin) List all users.                         | Admin |


---

## 6. Implementation Plan & Phasing

The project will be broken down into logical sprints.

-   **Sprint 0: Foundation & Setup**
    -   Initialize Git repositories (Frontend, Backend).
    -   Setup CI/CD pipeline basics.
    -   Setup Docker environment (`docker-compose.yml`).
    -   Finalize and script initial database schema.
    -   Implement core JWT authentication strategy.

-   **Sprint 1: Core Data & User Management**
    -   **Features:** User Registration, Login, Profile Management.
    -   **Admin:** Build the admin panel for CRUD operations on Players and Matches. This is crucial to populate the mocked data.
    -   **Goal:** A user can register and an admin can fully manage the game's base data.

-   **Sprint 2: The Main Event - Team Creation**
    -   **Features:** Full team creation UI/UX (player list, filters, budget tracker, rule validation).
    -   Backend logic for validating and saving a 15-player squad.
    -   **Goal:** A registered user can successfully create a valid fantasy team.

-   **Sprint 3: Let the Games Begin - Leagues**
    -   **Features:** Create public/private leagues. Join leagues. View basic league page with a list of members.
    -   **Goal:** Users can form communities and see who they are competing against.

-   **Sprint 4: The Engine - Scoring & Points**
    -   **Features:** Implement the background worker and `PointsCalculationService`.
    -   Connect the Admin "Submit Stats" endpoint to the job queue.
    -   Develop the logic for calculating points based on all rules.
    -   **Goal:** When an admin submits match results, points are correctly calculated and stored in the database.

-   **Sprint 5: Real-time & Strategy**
    -   **Features:** Implement the real-time leaderboard using Redis and Socket.IO.
    -   Build the Player Transfers interface and backend logic.
    -   Implement the Wildcard feature.
    -   **Goal:** Leaderboards update live, and users can manage their team week-to-week.

-   **Sprint 6: User Hub & Social**
    -   **Features:** Develop the "My Dashboard" page.
    -   Implement the Friends system (search, add, view).
    -   Build the Player Hub with stats and history.
    -   **Goal:** The application feels like a complete, user-centric experience.

-   **Sprint 7 onwards: Polish & Hardening**
    -   End-to-end testing, performance optimization (query analysis), security audit (dependency checks, penetration testing), and bug fixing.