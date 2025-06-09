```python
import unittest
import os
import hashlib
from datetime import datetime
from unittest.mock import patch, MagicMock
import pandas as pd
import sys

# Mock the gradio module as it is not needed for backend logic testing.
# This allows the test file to be run without gradio installed.
sys.modules['gradio'] = MagicMock()
sys.modules['gradio.themes'] = MagicMock()

# The module to be tested
import accounts as fantasy_app

# Import necessary classes and functions from the module
from accounts import (
    Base,
    User,
    Player,
    Match,
    FantasyTeam,
    FantasySquadPlayer,
    League,
    LeagueMembership,
    PlayerMatchStats,
    UserRole,
    UserExperienceLevel,
    PlayerRole,
    PlayerInjuryStatus,
    MatchStatus,
    LeagueType,
    create_engine,
    sessionmaker,
    handle_create_user,
    handle_get_users,
    handle_create_player,
    handle_get_players,
    handle_create_match,
    handle_get_matches,
    handle_add_stats,
    handle_get_match_stats,
    handle_create_fantasy_team,
    handle_get_fantasy_teams,
    handle_add_player_to_squad,
    handle_get_team_details,
    handle_create_league,
    handle_get_leagues,
    handle_join_league,
    handle_get_league_members
)

class TestFantasyCricketApp(unittest.TestCase):
    """
    Comprehensive test suite for the fantasy cricket application's backend logic.
    It uses an in-memory SQLite database to ensure tests are fast and isolated.
    """

    @classmethod
    def setUpClass(cls):
        """Set up an in-memory SQLite database for the entire test class."""
        cls.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(cls.engine)
        cls.TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=cls.engine)

        # Patch the SessionLocal in the 'accounts' module to use our test database.
        # This is a crucial step to redirect all database operations within the
        # handler functions to our in-memory test database.
        cls.session_patcher = patch('accounts.SessionLocal', cls.TestSessionLocal)
        cls.session_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """Stop the patcher after all tests in the class have run."""
        cls.session_patcher.stop()

    def setUp(self):
        """
        This method is called before each test.
        It creates a new session and ensures the database is clean.
        """
        # Create a new session for each test to ensure isolation.
        self.session = self.TestSessionLocal()
        # Clean all data from tables before each test.
        for table in reversed(Base.metadata.sorted_tables):
            self.session.execute(table.delete())
        self.session.commit()

    def tearDown(self):
        """This method is called after each test."""
        self.session.close()

    # --- Test Helper Methods ---

    def _create_test_user(self, display_name="testuser", email="test@example.com", password="password"):
        """Helper function to create and save a User for tests."""
        user = User(
            display_name=display_name,
            email=email,
            password_hash=hashlib.sha256(password.encode()).hexdigest(),
            role=UserRole.USER,
            experience_level=UserExperienceLevel.BEGINNER
        )
        self.session.add(user)
        self.session.commit()
        return user

    def _create_test_player(self, full_name="Virat Kohli", price=10.0, role=PlayerRole.BATSMAN):
        """Helper function to create and save a Player for tests."""
        player = Player(
            full_name=full_name,
            real_team_name="India",
            role=role,
            price=price
        )
        self.session.add(player)
        self.session.commit()
        return player

    def _create_test_fantasy_team(self, user, team_name="Test Titans"):
        """Helper to create a fantasy team for a given user."""
        team = FantasyTeam(user_id=user.id, team_name=team_name)
        self.session.add(team)
        self.session.commit()
        return team
        
    def _create_test_match(self, gameweek=1):
        """Helper to create a match."""
        match = Match(
            gameweek=gameweek,
            home_team_name="Team A",
            away_team_name="Team B",
            match_date=datetime.utcnow(),
            status=MatchStatus.SCHEDULED
        )
        self.session.add(match)
        self.session.commit()
        return match

    # --- User Management Tests ---

    def test_handle_create_user_success(self):
        """Test successful creation of a new user."""
        result_msg, _, _ = handle_create_user(
            email="newuser@example.com",
            display_name="newuser",
            password="password123",
            fav_team="India",
            exp_level="BEGINNER",
            role="USER"
        )
        self.assertIn("created successfully", result_msg)
        user = self.session.query(User).filter_by(email="newuser@example.com").first()
        self.assertIsNotNone(user)
        self.assertEqual(user.display_name, "newuser")
        self.assertEqual(user.role, UserRole.USER)
        self.assertEqual(user.experience_level, UserExperienceLevel.BEGINNER)

    def test_handle_create_user_duplicate_email(self):
        """Test error handling for creating a user with a duplicate email."""
        self._create_test_user(email="test@example.com")
        result_msg, _, _ = handle_create_user(
            email="test@example.com",
            display_name="anotheruser",
            password="password123",
            fav_team="",
            exp_level="EXPERT",
            role="USER"
        )
        self.assertIn("Email 'test@example.com' already exists", result_msg)

    def test_handle_get_users(self):
        """Test retrieving all users as a DataFrame."""
        self._create_test_user("user1", "user1@test.com")
        self._create_test_user("user2", "user2@test.com")
        df = handle_get_users()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 2)
        self.assertIn("user1", df["Display Name"].values)
        self.assertIn("user2@test.com", df["Email"].values)

    # --- Player Management Tests ---

    def test_handle_create_player_success(self):
        """Test successful creation of a player."""
        result_msg, _, _ = handle_create_player(
            full_name="Jasprit Bumrah",
            real_team="India",
            role="BOWLER",
            price=9.5,
            injury_status="ACTIVE"
        )
        self.assertIn("Player 'Jasprit Bumrah' created!", result_msg)
        player = self.session.query(Player).filter_by(full_name="Jasprit Bumrah").first()
        self.assertIsNotNone(player)
        self.assertEqual(player.role, PlayerRole.BOWLER)
        self.assertEqual(player.price, 9.5)

    def test_handle_get_players(self):
        """Test retrieving all players as a DataFrame."""
        self._create_test_player("Player One", 8.0)
        self._create_test_player("Player Two", 8.5)
        df = handle_get_players()
        self.assertEqual(len(df), 2)
        self.assertIn("Player One", df["Name"].values)
        self.assertIn("8.50", df["Price"].values)

    # --- Match & Stats Tests ---
    
    def test_handle_create_match(self):
        """Test successful creation of a match."""
        result_msg, _, _ = handle_create_match(
            gameweek=5,
            home_team="Team X",
            away_team="Team Y",
            match_date=datetime.now(),
            status="SCHEDULED"
        )
        self.assertEqual(result_msg, "Match created successfully!")
        match = self.session.query(Match).filter_by(gameweek=5).first()
        self.assertIsNotNone(match)
        self.assertEqual(match.home_team_name, "Team X")
        
    def test_handle_add_stats_new(self):
        """Test adding a new player stats record for a match."""
        player = self._create_test_player()
        match = self._create_test_match()
        stats_df = pd.DataFrame([{
            "runs_scored": 50, "balls_faced": 30, "fours": 5, "sixes": 2, 
            "wickets_taken": 0, "overs_bowled": 0.0, "runs_conceded": 0, 
            "maidens_bowled": 0, "catches": 1, "stumpings": 0, "run_outs": 0, "points": 60
        }])
        
        result_msg, _ = handle_add_stats(match.id, player.id, stats_df)
        self.assertEqual(result_msg, "Stats added successfully.")
        
        stats = self.session.query(PlayerMatchStats).filter_by(match_id=match.id, player_id=player.id).first()
        self.assertIsNotNone(stats)
        self.assertEqual(stats.runs_scored, 50)
        self.assertEqual(stats.catches, 1)

    def test_handle_add_stats_update(self):
        """Test updating an existing player stats record."""
        player = self._create_test_player()
        match = self._create_test_match()
        initial_stats = PlayerMatchStats(player_id=player.id, match_id=match.id, runs_scored=10, points=10)
        self.session.add(initial_stats)
        self.session.commit()
        
        stats_df = pd.DataFrame([{"runs_scored": 75, "points": 80}]) # Only update some fields
        
        result_msg, _ = handle_add_stats(match.id, player.id, stats_df)
        self.assertEqual(result_msg, "Stats updated successfully.")
        
        updated_stats = self.session.query(PlayerMatchStats).get(initial_stats.id)
        self.assertEqual(updated_stats.runs_scored, 75)
        self.assertEqual(updated_stats.points, 80)

    # --- Fantasy Team Tests ---

    def test_handle_create_fantasy_team_success(self):
        """Test successful creation of a fantasy team."""
        user = self._create_test_user()
        result_msg, _, _ = handle_create_fantasy_team(user.id, "Warriors")
        self.assertEqual(result_msg, "Fantasy team 'Warriors' created!")
        team = self.session.query(FantasyTeam).filter_by(user_id=user.id).first()
        self.assertIsNotNone(team)
        self.assertEqual(team.team_name, "Warriors")
        self.assertEqual(team.bank_balance, 100.0)

    def test_handle_create_fantasy_team_user_already_has_team(self):
        """Test error handling when a user tries to create a second team."""
        user = self._create_test_user()
        self._create_test_fantasy_team(user)
        result_msg, _, _ = handle_create_fantasy_team(user.id, "Another Team")
        self.assertEqual(result_msg, "Error: This user already has a fantasy team.")

    def test_handle_add_player_to_squad_success(self):
        """Test successfully adding a player to a fantasy squad."""
        user = self._create_test_user()
        team = self._create_test_fantasy_team(user)
        player = self._create_test_player(price=8.5)
        
        initial_balance = team.bank_balance
        
        result_msg, new_balance_val, new_squad_df = handle_add_player_to_squad(team.id, player.id)
        
        self.assertIn("added to squad!", result_msg)
        self.assertEqual(float(new_balance_val.get("value")), initial_balance - player.price)
        self.assertEqual(len(new_squad_df), 1)
        
        self.session.refresh(team) # Refresh to get updated balance from DB
        self.assertEqual(team.bank_balance, initial_balance - player.price)
        squad_member = self.session.query(FantasySquadPlayer).filter_by(fantasy_team_id=team.id).first()
        self.assertIsNotNone(squad_member)
        self.assertEqual(squad_member.player_id, player.id)

    def test_handle_add_player_to_squad_insufficient_funds(self):
        """Test error handling for insufficient funds when adding a player."""
        user = self._create_test_user()
        team = self._create_test_fantasy_team(user)
        player = self._create_test_player(price=120.0) # Price > default balance of 100.0
        
        result_msg, _, _ = handle_add_player_to_squad(team.id, player.id)
        
        self.assertIn("Insufficient funds", result_msg)
        squad_member_count = self.session.query(FantasySquadPlayer).filter_by(fantasy_team_id=team.id).count()
        self.assertEqual(squad_member_count, 0)
    
    def test_handle_add_player_to_squad_duplicate_player(self):
        """Test error handling when adding a player who is already in the squad."""
        user = self._create_test_user()
        team = self._create_test_fantasy_team(user)
        player = self._create_test_player(price=10.0)
        
        handle_add_player_to_squad(team.id, player.id) # First successful addition
        
        # Attempt to add the same player again
        result_msg, _, _ = handle_add_player_to_squad(team.id, player.id)
        
        self.assertEqual(result_msg, "Error: Player is already in the squad.")
        squad_member_count = self.session.query(FantasySquadPlayer).filter_by(fantasy_team_id=team.id).count()
        self.assertEqual(squad_member_count, 1)

    # --- League Management Tests ---
    
    def test_handle_create_league_public(self):
        """Test creating a public league."""
        creator = self._create_test_user()
        result_msg, _, _ = handle_create_league("Global League", "PUBLIC", creator.id, 1)
        self.assertEqual(result_msg, "League 'Global League' created!")
        league = self.session.query(League).filter_by(name="Global League").first()
        self.assertIsNotNone(league)
        self.assertEqual(league.type, LeagueType.PUBLIC)
        self.assertIsNone(league.invite_code)

    def test_handle_create_league_private_with_creator_membership(self):
        """Test creating a private league and auto-enrolling the creator's team."""
        creator = self._create_test_user()
        creator_team = self._create_test_fantasy_team(creator, "Creator's Crew")
        
        result_msg, _, _ = handle_create_league("Private Circle", "PRIVATE", creator.id, 1)
        self.assertIn("created!", result_msg)
        
        league = self.session.query(League).filter_by(name="Private Circle").first()
        self.assertIsNotNone(league)
        self.assertEqual(league.type, LeagueType.PRIVATE)
        self.assertIsNotNone(league.invite_code)
        
        # Check if creator's team was automatically added to the league
        membership = self.session.query(LeagueMembership).filter_by(league_id=league.id, fantasy_team_id=creator_team.id).first()
        self.assertIsNotNone(membership)

    def test_handle_join_league_public(self):
        """Test joining a public league."""
        creator = self._create_test_user("creator", "creator@test.com")
        joiner = self._create_test_user("joiner", "joiner@test.com")
        joiner_team = self._create_test_fantasy_team(joiner)
        league = League(name="Public League", type=LeagueType.PUBLIC, creator_user_id=creator.id, start_gameweek=1)
        self.session.add(league)
        self.session.commit()
        
        result_msg, _ = handle_join_league(joiner_team.id, league.id, None)
        self.assertIn("Successfully joined league", result_msg)
        
        membership = self.session.query(LeagueMembership).filter_by(league_id=league.id, fantasy_team_id=joiner_team.id).first()
        self.assertIsNotNone(membership)

    def test_handle_join_league_private_correct_code(self):
        """Test joining a private league with the correct invite code."""
        creator = self._create_test_user("creator", "creator@test.com")
        joiner = self._create_test_user("joiner", "joiner@test.com")
        joiner_team = self._create_test_fantasy_team(joiner)
        league = League(name="Private League", type=LeagueType.PRIVATE, creator_user_id=creator.id, start_gameweek=1, invite_code="SECRET123")
        self.session.add(league)
        self.session.commit()

        result_msg, _ = handle_join_league(joiner_team.id, league.id, "SECRET123")
        self.assertIn("Successfully joined league", result_msg)
        
    def test_handle_join_league_private_incorrect_code(self):
        """Test joining a private league with an incorrect invite code."""
        creator = self._create_test_user("creator", "creator@test.com")
        joiner = self._create_test_user("joiner", "joiner@test.com")
        joiner_team = self._create_test_fantasy_team(joiner)
        league = League(name="Private League", type=LeagueType.PRIVATE, creator_user_id=creator.id, start_gameweek=1, invite_code="SECRET123")
        self.session.add(league)
        self.session.commit()

        result_msg, _ = handle_join_league(joiner_team.id, league.id, "WRONGCODE")
        self.assertEqual(result_msg, "Error: Invalid invite code.")

    def test_handle_get_league_members(self):
        """Test retrieving and ranking league members by points."""
        creator = self._create_test_user("creator", "creator@test.com")
        league = League(name="Test League", type=LeagueType.PUBLIC, creator_user_id=creator.id, start_gameweek=1)
        self.session.add(league)
        self.session.commit()

        # Create users and teams
        user1, user2 = self._create_test_user("u1", "u1@t.com"), self._create_test_user("u2", "u2@t.com")
        team1, team2 = self._create_test_fantasy_team(user1, "Team 1"), self._create_test_fantasy_team(user2, "Team 2")

        # Create memberships with different points
        m1 = LeagueMembership(league_id=league.id, fantasy_team_id=team1.id, total_points=150)
        m2 = LeagueMembership(league_id=league.id, fantasy_team_id=team2.id, total_points=200)
        self.session.add_all([m1, m2])
        self.session.commit()

        df = handle_get_league_members(league.id)
        
        self.assertEqual(len(df), 2)
        # The dataframe rank starts at 1
        self.assertEqual(df.iloc[0]["Rank"], 1)
        self.assertEqual(df.iloc[0]["Team"], "Team 2") # Team 2 has more points
        self.assertEqual(df.iloc[0]["Points"], 200)
        self.assertEqual(df.iloc[1]["Rank"], 2)
        self.assertEqual(df.iloc[1]["Team"], "Team 1")
        self.assertEqual(df.iloc[1]["Points"], 150)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
```