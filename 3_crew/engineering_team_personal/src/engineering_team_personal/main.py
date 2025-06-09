#!/usr/bin/env python
import sys
import warnings
import os

from engineering_team_personal.crew import EnhancedEngineeringTeam

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

requirements = """
A comprehensive fantasy cricket web application where users can create teams, join leagues, and compete based on real cricket match performances, using mocked data for demonstration.

The system should allow users to create accounts, build fantasy teams, and participate in competitive leagues.

Core Features:
- **User Management:**
    - User registration and login with profile (name, favorite teams, experience level)
    - User dashboard showing team performance, league standings, and upcoming matches
    - Friend system to invite and compete with friends

- **Fantasy Team Creation:**
    - Squad selection from a pool of cricket players with assigned point values
    - Budget constraints (e.g., $100M salary cap) for team building
    - Player categories: Batsmen, Bowlers, All-rounders, Wicket-keepers
    - Captain and Vice-captain selection (2x and 1.5x points multiplier)
    - Team name and logo customization

- **League System:**
    - Public leagues (anyone can join) and private leagues (invitation only)
    - Different league formats: Season-long, weekly contests, daily fantasy
    - League creation with custom rules and prize structures
    - Real-time league leaderboards and standings

- **Scoring System:**
    - Points for batting: runs (1 point per run), boundaries (1 bonus), centuries (25 bonus)
    - Points for bowling: wickets (25 points), maidens (12 points), economy bonus
    - Points for fielding: catches (8 points), run-outs (12 points)
    - Penalty points for ducks (-2 points) and expensive bowling
    - Live score updates during matches

- **Match Integration:**
    - Display of real match fixtures and results (mocked data)
    - Live match tracking with player performance updates
    - Match predictions and fantasy team recommendations
    - Historical performance analytics for players

- **Trading & Transfers:**
    - Player trading system between users
    - Limited transfers per gameweek (2-3 transfers)
    - Wildcard feature (unlimited transfers once per season)
    - Player price fluctuations based on demand and performance

Pages needed:
- **Homepage:**
    - Live match scores ticker
    - Top fantasy teams leaderboard
    - Featured leagues and contests
    - Player spotlight with recent performances

- **Team Management:**
    - Squad selection interface with budget tracker
    - Formation setup (playing XI selection)
    - Captain selection and team preview
    - Transfer market with player search and filters

- **Leagues & Contests:**
    - Browse public leagues
    - Create/join private leagues
    - League standings and prize breakdown
    - Head-to-head matchup details

- **Player Hub:**
    - Player database with stats, form, and fantasy points
    - Player comparison tool
    - Injury updates and team news
    - Price history and ownership percentages

- **My Dashboard:**
    - Team performance over time
    - Points breakdown by player and match
    - League history and achievements
    - Friends and mini-leagues

- **Admin Panel:**
    - Add/edit player data and match fixtures
    - Manage leagues and user accounts
    - Update scoring rules and point values
    - Generate reports and analytics

Data Management:
- Store user accounts, teams, and league memberships
- Manage player database with stats and fantasy points
- Track match fixtures, results, and live scores (mocked)
- Store league configurations and standings
- Handle transfer history and team changes

Technical Requirements:
- Responsive design for mobile and desktop
- Real-time updates for live matches and scores
- Secure user authentication and data protection
- Efficient database queries for leaderboards and statistics
- Integration-ready architecture for future real cricket data APIs

The system will use comprehensive mocked data including player statistics, match results, and fantasy scoring to create a fully functional fantasy cricket experience.
"""

module_name = "fantasy_cricket.py"
class_name = "FantasyCricket"

def wait_for_approval_prompt(review_file: str):
    print(f"\n{'='*60}")
    print(f"HUMAN REVIEW REQUIRED")
    print(f"Please review: {review_file}")
    print(f"Type 'APPROVED' to continue, or enter feedback to request changes.")
    print(f"{'='*60}")
    feedback = input("Your response: ").strip()
    return feedback

def run():
    """
    Run the crew with human review gates, using direct input prompts.
    """
    inputs = {
        'requirements': requirements,
        'module_name': module_name,
        'class_name': class_name,
    }

    try:
        crew = EnhancedEngineeringTeam().crew()

        # Start main workflow
        result = crew.kickoff(inputs=inputs)

        # Human checkpoints (add more if you have more review steps)
        checkpoints = [
            ("output/REVIEW_REQUIREMENTS.md"),
            ("output/REVIEW_DESIGN.md"),
            ("output/REVIEW_FEATURES.md"),
        ]

        for review_file in checkpoints:
            if os.path.exists(review_file):
                feedback = wait_for_approval_prompt(review_file)
                if feedback != "APPROVED":
                    print(f"Feedback received: {feedback}")
                    inputs['human_feedback'] = feedback
                    # Optionally: you could rerun the step or halt here.
                    # For now, let's just continue to the next checkpoint.

        return result

    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

if __name__ == "__main__":
    run()
