import enum
import uuid
from datetime import datetime

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Boolean,
    Enum,
    ForeignKey,
    DateTime,
    Numeric,
    UniqueConstraint,
    CheckConstraint
)
from sqlalchemy.orm import relationship, declarative_base, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

# --- Enum Definitions ---
# Using standard Python enums which SQLAlchemy can use directly.

class UserRole(enum.Enum):
    USER = "User"
    ADMIN = "Admin"

class UserExperienceLevel(enum.Enum):
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    EXPERT = "Expert"

class FriendshipStatus(enum.Enum):
    PENDING = "Pending"
    ACCEPTED = "Accepted"
    DECLINED = "Declined"
    BLOCKED = "Blocked"

class PlayerRole(enum.Enum):
    BATSMAN = "Batsman"
    BOWLER = "Bowler"
    ALL_ROUNDER = "All-Rounder"
    WICKET_KEEPER = "Wicket-Keeper"

class PlayerInjuryStatus(enum.Enum):
    ACTIVE = "Active"
    INJURED = "Injured"
    DOUBTFUL = "Doubtful"

class MatchStatus(enum.Enum):
    SCHEDULED = "Scheduled"
    LIVE = "Live"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"

class LeagueType(enum.Enum):
    PUBLIC = "Public"
    PRIVATE = "Private"


# --- Base Class ---
# Using the modern declarative base
Base = declarative_base()

# --- Model Definitions ---

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    display_name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    favorite_team: Mapped[str] = mapped_column(String(100), nullable=True)
    experience_level: Mapped[UserExperienceLevel] = mapped_column(Enum(UserExperienceLevel), nullable=True)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False, default=UserRole.USER)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)

    # Relationships
    fantasy_team: Mapped["FantasyTeam"] = relationship(back_populates="user")
    created_leagues: Mapped[list["League"]] = relationship("League", back_populates="creator")
    
    # Friendships initiated by this user
    sent_friend_requests: Mapped[list["Friendship"]] = relationship(
        "Friendship", foreign_keys="[Friendship.requester_id]", back_populates="requester"
    )
    # Friendships received by this user
    received_friend_requests: Mapped[list["Friendship"]] = relationship(
        "Friendship", foreign_keys="[Friendship.addressee_id]", back_populates="addressee"
    )

class Friendship(Base):
    __tablename__ = "friendships"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    requester_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    addressee_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    status: Mapped[FriendshipStatus] = mapped_column(Enum(FriendshipStatus), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)

    # Relationships
    requester: Mapped["User"] = relationship("User", foreign_keys=[requester_id], back_populates="sent_friend_requests")
    addressee: Mapped["User"] = relationship("User", foreign_keys=[addressee_id], back_populates="received_friend_requests")
    
    __table_args__ = (
        UniqueConstraint("requester_id", "addressee_id", name="uq_friendship"),
    )

class Player(Base):
    __tablename__ = "players"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    real_team_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    role: Mapped[PlayerRole] = mapped_column(Enum(PlayerRole), nullable=False)
    price: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    injury_status: Mapped[PlayerInjuryStatus] = mapped_column(Enum(PlayerInjuryStatus), default=PlayerInjuryStatus.ACTIVE)
    photo_url: Mapped[str] = mapped_column(String(255), nullable=True)

    # Relationships
    match_stats: Mapped[list["PlayerMatchStats"]] = relationship(back_populates="player")
    squad_memberships: Mapped[list["FantasySquadPlayer"]] = relationship(back_populates="player")

class Match(Base):
    __tablename__ = "matches"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    gameweek: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    home_team_name: Mapped[str] = mapped_column(String(100), nullable=False)
    away_team_name: Mapped[str] = mapped_column(String(100), nullable=False)
    match_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[MatchStatus] = mapped_column(Enum(MatchStatus), nullable=False, index=True)

    # Relationship
    player_stats: Mapped[list["PlayerMatchStats"]] = relationship(back_populates="match")

class PlayerMatchStats(Base):
    __tablename__ = "player_match_stats"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    player_id: Mapped[str] = mapped_column(ForeignKey("players.id"), nullable=False)
    match_id: Mapped[str] = mapped_column(ForeignKey("matches.id"), nullable=False)
    
    runs_scored: Mapped[int] = mapped_column(Integer, default=0)
    balls_faced: Mapped[int] = mapped_column(Integer, default=0)
    fours: Mapped[int] = mapped_column(Integer, default=0)
    sixes: Mapped[int] = mapped_column(Integer, default=0)
    wickets_taken: Mapped[int] = mapped_column(Integer, default=0)
    overs_bowled: Mapped[float] = mapped_column(Numeric(3, 1), default=0.0)
    runs_conceded: Mapped[int] = mapped_column(Integer, default=0)
    maidens_bowled: Mapped[int] = mapped_column(Integer, default=0)
    catches: Mapped[int] = mapped_column(Integer, default=0)
    stumpings: Mapped[int] = mapped_column(Integer, default=0)
    run_outs: Mapped[int] = mapped_column(Integer, default=0)
    points: Mapped[int] = mapped_column(Integer, default=0, index=True)

    # Relationships
    player: Mapped["Player"] = relationship("Player", back_populates="match_stats")
    match: Mapped["Match"] = relationship("Match", back_populates="player_stats")
    
    __table_args__ = (
        UniqueConstraint("player_id", "match_id", name="uq_player_match"),
    )

class FantasyTeam(Base):
    __tablename__ = "fantasy_teams"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False, unique=True)
    team_name: Mapped[str] = mapped_column(String(100), nullable=False)
    logo_url: Mapped[str] = mapped_column(String(255), nullable=True)
    bank_balance: Mapped[float] = mapped_column(Numeric(5, 2), default=0.0)
    wildcard_used: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="fantasy_team")
    squad_players: Mapped[list["FantasySquadPlayer"]] = relationship(back_populates="fantasy_team", cascade="all, delete-orphan")
    gameweek_data: Mapped[list["GameweekData"]] = relationship(back_populates="fantasy_team", cascade="all, delete-orphan")
    league_memberships: Mapped[list["LeagueMembership"]] = relationship(back_populates="fantasy_team", cascade="all, delete-orphan")

class FantasySquadPlayer(Base):
    __tablename__ = "fantasy_squad_players"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    fantasy_team_id: Mapped[str] = mapped_column(ForeignKey("fantasy_teams.id"), nullable=False)
    player_id: Mapped[str] = mapped_column(ForeignKey("players.id"), nullable=False)
    purchase_price: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)

    # Relationships
    fantasy_team: Mapped["FantasyTeam"] = relationship("FantasyTeam", back_populates="squad_players")
    player: Mapped["Player"] = relationship("Player", back_populates="squad_memberships")

    __table_args__ = (
        UniqueConstraint("fantasy_team_id", "player_id", name="uq_team_player"),
    )

class GameweekData(Base):
    __tablename__ = "gameweek_data"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    fantasy_team_id: Mapped[str] = mapped_column(ForeignKey("fantasy_teams.id"), nullable=False)
    gameweek: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    captain_id: Mapped[str] = mapped_column(ForeignKey("players.id"), nullable=False)
    vice_captain_id: Mapped[str] = mapped_column(ForeignKey("players.id"), nullable=False)
    points: Mapped[int] = mapped_column(Integer, default=0)
    transfers_made: Mapped[int] = mapped_column(Integer, default=0)

    # Relationships
    fantasy_team: Mapped["FantasyTeam"] = relationship("FantasyTeam", back_populates="gameweek_data")
    captain: Mapped["Player"] = relationship("Player", foreign_keys=[captain_id])
    vice_captain: Mapped["Player"] = relationship("Player", foreign_keys=[vice_captain_id])

    __table_args__ = (
        UniqueConstraint("fantasy_team_id", "gameweek", name="uq_team_gameweek"),
    )

class League(Base):
    __tablename__ = "leagues"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    type: Mapped[LeagueType] = mapped_column(Enum(LeagueType), nullable=False)
    invite_code: Mapped[str] = mapped_column(String(10), unique=True, nullable=True)
    creator_user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    start_gameweek: Mapped[int] = mapped_column(Integer, nullable=False)

    # Relationships
    creator: Mapped["User"] = relationship("User", back_populates="created_leagues")
    memberships: Mapped[list["LeagueMembership"]] = relationship(back_populates="league", cascade="all, delete-orphan")

class LeagueMembership(Base):
    __tablename__ = "league_memberships"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    league_id: Mapped[str] = mapped_column(ForeignKey("leagues.id"), nullable=False)
    fantasy_team_id: Mapped[str] = mapped_column(ForeignKey("fantasy_teams.id"), nullable=False)
    total_points: Mapped[int] = mapped_column(Integer, default=0, index=True)
    rank: Mapped[int] = mapped_column(Integer, nullable=True)

    # Relationships
    league: Mapped["League"] = relationship("League", back_populates="memberships")
    fantasy_team: Mapped["FantasyTeam"] = relationship("FantasyTeam", back_populates="league_memberships")

    __table_args__ = (
        UniqueConstraint("league_id", "fantasy_team_id", name="uq_league_team"),
    )


# Example of how to create the database and tables with SQLite
if __name__ == "__main__":
    # For demonstration purposes, using an in-memory SQLite database
    engine = create_engine("sqlite:///:memory:")
    
    print("Creating database tables...")
    Base.metadata.create_all(engine)
    print("Tables created successfully.")

    # You can add code here to connect and interact with the database
    # from sqlalchemy.orm import sessionmaker
    # Session = sessionmaker(bind=engine)
    # session = Session()
    # ... session.add(...) ... session.commit() ...
    # session.close()
