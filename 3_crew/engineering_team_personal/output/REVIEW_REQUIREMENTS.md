### **Project Review Checkpoint: Fantasy Cricket Web Application**

**Document:** Business Requirements Summary for Stakeholder Review
**Date:** [Current Date]
**Version:** 1.0
**Status:** PENDING REVIEW

---

### **1. Executive Summary**

This document provides a one-page summary of the business requirements for a new Fantasy Cricket Web Application. The project's initial goal is to build a core platform for cricket fans to create fantasy teams, join leagues, and compete based on player performance. **For this first version, the application will use simulated (mocked) match data to prove the concept and user experience before integrating with live data feeds.**

---

### **2. Core Features & User Experience**

The application will provide the following key capabilities for our users:

*   **User Accounts & Social:** Users can register, log in, manage their profile, and add friends to create a community.
*   **Team Creation & Management:** A guided interface for users to build a 15-player squad based on a budget and specific team composition rules.
*   **Captain & Vice-Captain:** Users can select a Captain (2x points) and Vice-Captain (1.5x points) each week to add a strategic layer.
*   **League System:** Supports both public leagues (open to all) and private leagues (invite-only) with real-time leaderboards.
*   **Player Transfers:** A transfer market allowing users to make a limited number of free player swaps each week, with a "Wildcard" option for unlimited transfers once per season.
*   **Admin Panel:** A secure backend for administrators to manage player data, match fixtures, and user accounts.

---

### **3. Key User Journeys**

To illustrate the user experience, here are the primary user stories that define the application:

*   **New User Registration:**
    > **As a** new visitor, **I want to** register for an account, **so that** I can create a team and join leagues.

*   **Fantasy Team Creation:**
    > **As a** user, **I want to** select 15 players for my squad within a budget, **so that** I can compete in a fantasy league.

*   **Private League Creation:**
    > **As a** user, **I want to** create a private league and get an invite code, **so that** I can play exclusively with my friends.

*   **Making Strategic Transfers:**
    > **As a** user, **I want to** transfer players in and out of my team, **so that** I can adapt my squad to player form and fixtures.

---

### **4. Critical Business Rules for Approval**

The following rules define the core game mechanics. Please review these carefully as they directly impact gameplay and user strategy.

| Category               | Rule                                                                          | Value / Constraint            |
| ---------------------- | ----------------------------------------------------------------------------- | ----------------------------- |
| **Team Creation**      | Total budget for a 15-player squad                                            | **$100M**                     |
|                        | Maximum players from a single real-world team                                 | **7 players**                 |
|                        | Team composition (Wicket-Keepers, Batsmen, All-Rounders, Bowlers)             | Enforced min/max per role     |
| **Scoring**            | Points for a single run                                                       | **+1 point**                  |
|                        | Points for a wicket (bowler)                                                  | **+25 points**                |
|                        | Points for a catch                                                            | **+8 points**                 |
|                        | Captain's points multiplier                                                   | **2x**                        |
|                        | Vice-Captain's points multiplier (if Captain plays)                           | **1.5x**                      |
|                        | Bonus for a half-century (50 runs)                                            | **+8 points**                 |
| **Transfers**          | Free transfers allowed per gameweek                                           | **2 transfers**               |
|                        | "Wildcard" chip (unlimited free transfers for one week)                       | **1 per season**              |

---

### **5. Review & Approval Instructions**

**To all reviewers:** Your feedback is critical to ensure we are building the right product. Please review this summary with the following questions in mind:

1.  **Alignment:** Do these features and rules align with our vision for a fun and engaging fantasy cricket game?
2.  **Clarity:** Are there any business rules (e.g., scoring, budget) that seem unclear, unfair, or could be improved?
3.  **Completeness:** Is there any critical functionality missing for our initial launch? Keep in mind the scope is limited to using mocked data for now.

**How to provide feedback:** Please provide your feedback by [Date] via one of the following methods:
*   Add comments directly to the shared document.
*   Send a consolidated email with your feedback to the project coordinator.

---

### **6. Stakeholder Approval**

By signing below, you confirm that you have reviewed the business requirements summary and approve them for the development team to proceed.

| Name | Title | Signature | Date |
| :--- | :---- | :-------- | :--- |
|      |       |           |      |
|      |       |           |      |
|      |       |           |      |