# Business Requirements Document: Fantasy Cricket Web Application

## 1. Introduction

### 1.1 Project Purpose
This document outlines the business requirements for a new Fantasy Cricket Web Application. The application will provide a comprehensive platform for cricket enthusiasts to create and manage fantasy teams, join various types of leagues, and compete against other users based on the real-life performance of cricket players. For the initial version, the system will utilize mocked data to simulate live matches, player statistics, and scoring.

### 1.2 Project Scope
The scope of this project includes the design, development, and deployment of a web application with the following core functionalities:
- User registration, authentication, and profile management.
- Fantasy team creation and management under a set of rules (e.g., budget cap, player roles).
- A robust league system with public and private options.
- A detailed point-based scoring system.
- Integration with mocked match data for fixtures, live scoring, and results.
- Player transfer and trading market.
- A user dashboard for tracking performance.
- An administrative panel for managing the platform's data and users.

### 1.3 Target Audience
The primary audience for this application includes cricket fans of all levels, from casual followers to passionate statisticians, who enjoy engaging with the sport in an interactive and competitive way.

---

## 2. Functional Requirements, User Stories & Acceptance Criteria

This section breaks down the system's functionalities into modules. Each module includes high-level functional requirements, followed by specific user stories and their corresponding acceptance criteria.

### 2.1 User Management

#### **Functional Requirements**
- **FR 2.1.1:** The system shall allow new users to register for an account using an email address and password.
- **FR 2.1.2:** The system shall authenticate registered users via a login page.
- **FR 2.1.3:** The system shall provide a password recovery mechanism (e.g., "Forgot Password").
- **FR 2.1.4:** Registered users shall have a personal profile where they can set their name, favorite cricket teams, and self-assessed experience level (Beginner, Intermediate, Expert).
- **FR 2.1.5:** The system shall allow users to search for other users and send/accept/decline friend requests.
- **FR 2.1.6:** Users shall have a "My Dashboard" page that serves as a central hub for their activities.

---
#### **User Stories & Acceptance Criteria**

**User Story 1: New User Registration**
> **As a** new visitor,
> **I want to** register for an account,
> **so that** I can create a team and join leagues.

**Acceptance Criteria:**
- **AC 2.1.1.1:** Given I am on the registration page, I must provide a unique email address, a password (with confirmation), and a display name.
- **AC 2.1.1.2:** The system must validate that the email is in a valid format and is not already in use.
- **AC 2.1.1.3:** The system must enforce password complexity rules (e.g., minimum 8 characters, at least one number, one uppercase letter).
- **AC 2.1.1.4:** Upon successful registration, I am automatically logged in and redirected to my dashboard or a "Create Team" page.

**User Story 2: User Login**
> **As a** registered user,
> **I want to** log in to the application,
> **so that** I can access my dashboard and manage my teams.

**Acceptance Criteria:**
- **AC 2.1.2.1:** Given I am on the login page, I must enter my registered email and password.
- **AC 2.1.2.2:** If the credentials are correct, I am redirected to my dashboard.
- **AC 2.1.2.3:** If the credentials are incorrect, an error message "Invalid email or password" is displayed.

**User Story 3: Friends System**
> **As a** registered user,
> **I want to** add friends,
> **so that** I can invite them to private leagues and compare our performance.

**Acceptance Criteria:**
- **AC 2.1.5.1:** I can search for other users by their display name or email.
- **AC 2.1.5.2:** From the search results, I can send a friend request to a user.
- **AC 2.1.5.3:** I can view pending friend requests I've sent and received.
- **AC 2.1.5.4:** I can accept or decline incoming friend requests.
- **AC 2.1.5.5:** My dashboard's "Friends" section lists all my accepted friends.

---
### 2.2 Fantasy Team Creation

#### **Functional Requirements**
- **FR 2.2.1:** The system shall provide a player selection interface for users to build their fantasy squad.
- **FR 2.2.2:** The system shall present a pool of all available cricket players, filterable by team, role, and price.
- **FR 2.2.3:** Each player will be assigned a role (Batsman, Bowler, All-Rounder, Wicket-Keeper) and a virtual monetary value.
- **FR 2.2.4:** The system shall enforce team creation rules, including a total squad budget and player composition constraints.
- **FR 2.2.5:** Users must select a Captain and a Vice-Captain from their chosen squad for each gameweek.
- **FR 2.2.6:** Users shall be able to name their team and optionally upload a custom logo image.

#### **Business Rules**
- **BR 2.2.1:** Total team budget: **$100M**.
- **BR 2.2.2:** Squad size: **15 players**.
- **BR 2.2.3:** Playing XI size: **11 players**.
- **BR 2.2.4:** Team composition rules for the squad of 15:
    - Min 1, Max 2 Wicket-Keepers
    - Min 4, Max 6 Batsmen
    - Min 2, Max 4 All-Rounders
    - Min 4, Max 6 Bowlers
    - Max 7 players from a single real-world cricket team.
- **BR 2.2.5:** Captain's points are multiplied by **2x**.
- **BR 2.2.6:** Vice-Captain's points are multiplied by **1.5x**. If the Captain doesn't play in a gameweek, the Vice-Captain receives the 2x multiplier.

---
#### **User Stories & Acceptance Criteria**

**User Story 4: Team Creation**
> **As a** user,
> **I want to** select 15 players for my squad,
> **so that** I can compete in a fantasy league.

**Acceptance Criteria:**
- **AC 2.2.1.1:** I am presented with a list of players, showing their name, team, role, and price.
- **AC 2.2.1.2:** As I add players, the system must update my remaining budget and the number of slots filled for each player role.
- **AC 2.2.1.3:** The system must prevent me from adding a player if it violates the budget cap or the team composition rules (e.g., too many batsmen, not enough bowlers).
- **AC 2.2.1.4:** I can easily remove a player from my selected squad and add a different one.
- **AC 2.2.1.5:** Once I have selected 15 players who meet all rules, I can save my squad.

**User Story 5: Captain Selection**
> **As a** user,
> **I want to** select a Captain and Vice-Captain from my playing XI for each gameweek,
> **so that** I can earn bonus points.

**Acceptance Criteria:**
- **AC 2.2.5.1:** On the team management page, I can designate one player as Captain (C) and one as Vice-Captain (VC).
- **AC 2.2.5.2:** I cannot select the same player for both roles.
- **AC 2.2.5.3:** The system must save my selection for the upcoming gameweek.
- **AC 2.2.5.4:** My selections are locked once the gameweek deadline passes.

---
### 2.3 League System

#### **Functional Requirements**
- **FR 2.3.1:** The system shall support public leagues that are open for any user to join.
- **FR 2.3.2:** The system shall allow users to create private leagues, which are joinable only via a unique invitation code.
- **FR 2.3.3:** The system shall support multiple league formats:
    - **Season-long:** Classic format lasting the entire tournament/season.
    - **Weekly/Daily Contests:** Shorter-term contests based on a specific round of matches.
- **FR 2.3.4:** League creators can define basic rules, such as the league name and start date.
- **FR 2.3.5:** Each league shall have a leaderboard that updates in real-time during matches, showing team ranks, total points, and points for the current gameweek.

---
#### **User Stories & Acceptance Criteria**

**User Story 6: Joining a Public League**
> **As a** user,
> **I want to** browse and join existing public leagues,
> **so that** I can compete against a wider community.

**Acceptance Criteria:**
- **AC 2.3.1.1:** I can view a list of all available public leagues on the "Leagues & Contests" page.
- **AC 2.3.1.2:** The list displays the league name, number of participants, and league format.
- **AC 2.3.1.3:** I can join any public league with a single click, provided I have a valid team.

**User Story 7: Creating a Private League**
> **As a** user,
> **I want to** create a private league and get an invite code,
> **so that** I can play exclusively with my friends.

**Acceptance Criteria:**
- **AC 2.3.2.1:** I can access a "Create League" form.
- **AC 2.3.2.2:** In the form, I must specify the league name and select the "Private" option.
- **AC 2.3.2.3:** Upon creation, the system generates a unique, shareable code for my league.
- **AC 2.3.2.4:** Other users can join this league only by entering the correct code.

---
### 2.4 Scoring System

#### **Functional Requirements**
- **FR 2.4.1:** The system shall automatically calculate and award points to players based on their performance in a match, using mocked data feeds.
- **FR 2.4.2:** The system shall apply point multipliers for the user's selected Captain (2x) and Vice-Captain (1.5x).
- **FR 2.4.3:** A user's total score for a gameweek is the sum of points from all 11 players in their playing XI.
- **FR 2.4.4:** Player and team scores shall update in near real-time as match events occur.

#### **Business Rules (Scoring)**
- **BR 2.4.1: Batting Points**
    - Run: +1 point
    - Boundary (4) Bonus: +1 point
    - Six (6) Bonus: +2 points
    - Half-Century (50 runs) Bonus: +8 points
    - Century (100 runs) Bonus: +16 points
    - Duck (Batsman, Wicket-Keeper, All-Rounder): -2 points
- **BR 2.4.2: Bowling Points**
    - Wicket: +25 points (excluding run-outs)
    - Maiden Over: +12 points
    - 4-Wicket Haul Bonus: +8 points
    - 5-Wicket Haul Bonus: +16 points
- **BR 2.4.3: Fielding Points**
    - Catch: +8 points
    - Stumping/Run-out (Direct Hit): +12 points
    - Run-out (Thrower/Catcher): +6 points each
- **BR 2.4.4: Economy Rate Bonus (Min 2 overs bowled)**
    - Below 5.00 runs per over: +6 points
    - Between 5.00 and 7.00: +3 points
    - Between 9.00 and 10.00: -3 points
    - Above 10.00: -6 points
- **BR 2.4.5: Strike Rate Penalty (Min 10 balls faced)**
    - Below 70.00 runs per 100 balls: -3 points

---
### 2.5 Trading & Transfers

#### **Functional Requirements**
- **FR 2.5.1:** The system shall allow users to transfer players in and out of their squad between gameweeks.
- **FR 2.5.2:** The system shall enforce a limit on the number of free transfers allowed per gameweek.
- **FR 2.5.3:** The system shall provide a "Wildcard" feature that, when activated, allows for unlimited free transfers for one gameweek.
- **FR 2.5.4:** The system shall simulate player price changes based on their performance and selection popularity (demand).

#### **Business Rules**
- **BR 2.5.1:** Free Transfers per Gameweek: **2**.
- **BR 2.5.2:** Wildcard availability: **Once per season**.
- **BR 2.5.3:** Transfers must be completed before the gameweek deadline.
- **BR 2.5.4:** Player price fluctuations occur once per gameweek, after all matches for that week are complete.

---
#### **User Stories & Acceptance Criteria**

**User Story 8: Making Transfers**
> **As a** user,
> **I want to** transfer players in and out of my team,
> **so that** I can adapt my squad to player form and fixtures.

**Acceptance Criteria:**
- **AC 2.5.1.1:** The "Transfers" page shows my current squad and a list of available players, similar to the initial team creation interface.
- **AC 2.5.1.2:** When I remove a player, the budget from their sale is added to my bank.
- **AC 2.5.1.3:** I can add a new player, and their cost is deducted from my bank. The transfer is only possible if I have sufficient funds.
- **AC 2.5.1.4:** The interface clearly displays how many free transfers I have remaining for the gameweek.
- **AC 2.5.1.5:** I must confirm all my transfers before they are finalized.

---
### 2.6 Admin Panel

#### **Functional Requirements**
- **FR 2.6.1:** An administrator shall be able to log in to a secure admin panel.
- **FR 2.6.2:** The admin shall have CRUD (Create, Read, Update, Delete) capabilities for the player database, including player names, teams, roles, and initial prices.
- **FR 2.6.3:** The admin shall manage match fixtures, including creating new matches, setting dates/times, and inputting final results (for the mocked data system).
- **FR 2.6.4:** The admin shall be able to update player performance data for a match (e.g., runs scored, wickets taken) to trigger the scoring system.
- **FR 2.6.5:** The admin shall be able to view and manage user accounts (e.g., view details, suspend account).
- **FR 2.6.6:** The admin shall be able to configure the global scoring rules and point values.

---
#### **User Stories & Acceptance Criteria**

**User Story 9: Managing Player Data**
> **As an** administrator,
> **I want to** add, edit, and delete players from the database,
> **so that** the player pool is always up-to-date.

**Acceptance Criteria:**
- **AC 2.6.2.1:** I can access a table of all players in the system.
- **AC 2.6.2.2:** I can use a form to add a new player with all required attributes (name, team, role, price).
- **AC 2.6.2.3:** I can edit the attributes of any existing player.

**User Story 10: Managing Match Data**
> **As an** administrator,
> **I want to** input match results and player statistics,
> **so that** fantasy points can be calculated and distributed.

**Acceptance Criteria:**
- **AC 2.6.3.1:** I can create a new match fixture between two teams.
- **AC 2.6.4.1:** For a completed match, I can access an interface to input key performance stats for each participating player (runs, balls, wickets, catches, etc.).
- **AC 2.6.4.2:** Upon saving the match stats, the system automatically triggers a job to calculate and update all fantasy points and league leaderboards related to that match.

---

## 3. Non-Functional Requirements

### 3.1 Performance
- **NFR 3.1.1:** Pages should load within 3 seconds under normal traffic conditions.
- **NFR 3.1.2:** Real-time score updates on leaderboards and dashboards should appear within 10 seconds of the corresponding data being updated in the backend.
- **NFR 3.1.3:** Database queries for generating leaderboards for leagues with up to 10,000 users must execute in under 2 seconds.

### 3.2 Security
- **NFR 3.2.1:** All user passwords must be securely hashed and salted before being stored in the database.
- **NFR 3.2.2:** The entire application must be served over HTTPS to encrypt data in transit.
- **NFR 3.2.3:** The system must be protected against common web vulnerabilities, including SQL Injection, Cross-Site Scripting (XSS), and Cross-Site Request Forgery (CSRF).
- **NFR 3.2.4:** The admin panel must be protected by a separate authentication layer, accessible only to users with administrative privileges.

### 3.3 Usability & Design
- **NFR 3.3.1:** The application must feature a responsive design that provides a consistent and optimal user experience on major desktop browsers (Chrome, Firefox, Safari) and mobile devices (iOS, Android).
- **NFR 3.3.2:** Navigation must be intuitive and clearly labeled.
- **NFR 3.3.3:** Feedback must be provided for user actions (e.g., success messages on saving a team, loading indicators for data).

### 3.4 Scalability & Architecture
- **NFR 3.4.1:** The system architecture must be modular and designed to facilitate future integration with live, third-party cricket data APIs, replacing the initial mocked data system.
- **NFR 3.4.2:** The database schema must be designed for efficient querying and scaling to accommodate a growing user base and historical data.

---

## 4. Data Management

### 4.1 Data Entities
The system must store and manage the following key data entities:
- **User:** UserID, Name, Email, HashedPassword, FavoriteTeam, ExperienceLevel, CreationDate.
- **Friendship:** FriendshipID, User1_ID, User2_ID, Status (Pending, Accepted).
- **Player:** PlayerID, Name, RealTeam, Role, Price, InjuryStatus.
- **Match:** MatchID, Team1_ID, Team2_ID, MatchDate, Status (Scheduled, Live, Completed).
- **PlayerMatchStats:** StatID, PlayerID, MatchID, Runs, Wickets, Catches, etc.
- **FantasyTeam:** TeamID, UserID, TeamName, LogoURL.
- **FantasySquad:** SquadID, TeamID, PlayerID (linking table for the 15 players).
- **GameweekTeam:** GameweekTeamID, TeamID, GameweekNumber, CaptainID, ViceCaptainID, Player1_ID, ..., Player11_ID.
- **League:** LeagueID, Name, Type (Public/Private), InviteCode, CreatorUserID.
- **LeagueMembership:** MembershipID, LeagueID, TeamID.
- **TransferHistory:** TransferID, TeamID, Gameweek, PlayerIn_ID, PlayerOut_ID, Timestamp.

---

## 5. Glossary

- **Gameweek:** A defined period of time, usually a week, during which a round of matches is played. Deadlines for transfers and team selections are set per gameweek.
- **Playing XI:** The 11 players from the 15-player squad selected by the user to score points in a given gameweek.
- **Wildcard:** A special chip that can be used once per season to make unlimited free transfers for a single gameweek.
- **Mocked Data:** Simulated data used for development and demonstration purposes to mimic real-world player stats, match results, and live scores.