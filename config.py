"""
Central configuration for the internship bot.
All sensitive values (API keys, topic names) are pulled from .env.
Everything else can be edited directly in this file.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ── Google Gemini ─────────────────────────────────────────────────────────────
# Your Gemini API key — used to call Gemini for AI-based job scoring.
# Get one at https://aistudio.google.com/app/apikey (free tier available)
GEMINI_API_KEY: str = os.environ["GEMINI_API_KEY"]

# Gemini model used for scoring.
# gemini-2.0-flash is fast and free-tier friendly; gemini-1.5-pro is more capable.
GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

# ── Notifications (ntfy.sh) ──────────────────────────────────────────────────
# A unique topic name that acts as your private push notification channel.
# Subscribe to it in the ntfy app (iOS/Android) at https://ntfy.sh/<topic>
NTFY_TOPIC: str = os.environ["NTFY_TOPIC"]

# Leave as-is unless you self-host an ntfy server.
NTFY_SERVER: str = os.getenv("NTFY_SERVER", "https://ntfy.sh")

# ── Matching ─────────────────────────────────────────────────────────────────
# Gemini scores each job 0–100 against your profile below.
# Only jobs at or above this threshold trigger a notification.
MATCH_THRESHOLD: int = int(os.getenv("MATCH_THRESHOLD", "70"))

# ── Polling ──────────────────────────────────────────────────────────────────
# How often the bot checks for new postings, in minutes.
POLL_INTERVAL_MINUTES: int = int(os.getenv("POLL_INTERVAL_MINUTES", "30"))

# ── Your profile ─────────────────────────────────────────────────────────────
# Gemini reads this when scoring each job. Be specific about your skills,
# target role types, locations, and timeline so scoring is accurate.
CANDIDATE_PROFILE: str = """
TODO: describe yourself and what you're looking for here.

Example:
  CS junior seeking summer 2026 SWE internships. Skilled in Python, React,
  and SQL. Prefer remote or Bay Area roles. Interested in dev tools, ML
  infra, or fintech. Not interested in defense or gambling companies.
""".strip()

# ── Job boards ────────────────────────────────────────────────────────────────
# Maps job board platform → list of company slugs to check.
# Greenhouse and Lever are the two most common ATS platforms used by
# tech companies. The scraper hits each company's board directly.
#
# To add a company: find its job board URL, identify the platform
# (greenhouse.io or lever.co), and add the slug shown in that URL.
#   Greenhouse URL pattern: boards.greenhouse.io/<slug>/jobs
#   Lever URL pattern:      jobs.lever.co/<slug>
COMPANIES: dict[str, list[str]] = {
    # boards-api.greenhouse.io/v1/boards/<slug>/jobs
    "greenhouse": [
        "stripe",
        "figma",
        "anthropic",
        "spacex",
        "databricks",
        "relativity",
        "scaleai",
        # add more greenhouse slugs here
    ],
    # jobs.ashbyhq.com — openai/notion/linear/supabase migrated here from Greenhouse/Lever
    "ashby": [
        "openai",
        "notion",
        "linear",
        "supabase",
        # add more ashby slugs here
    ],
}

# ── Search keywords ───────────────────────────────────────────────────────────
# These are matched against job titles (case-insensitive) to pre-filter
# postings before sending them to Claude. Saves API calls on irrelevant roles.
# A posting passes if its title contains ANY keyword in this list.
SEARCH_KEYWORDS: list[str] = [
    "intern",
    "internship",
    "undergrad",
    # "new grad",
    # "entry level",
]

# ── Hard filters ──────────────────────────────────────────────────────────────
# Applied before AI scoring — jobs that fail a hard filter are skipped
# entirely, saving Claude API calls.

# Skip postings older than this many days. Set to None to disable.
MAX_POSTING_AGE_DAYS: int | None = 7

# Only surface jobs whose location field contains one of these strings
# (case-insensitive substring match). Set to None to allow all locations.
# Example: ["remote", "san francisco", "new york", "seattle"]
ALLOWED_LOCATIONS: list[str] | None = [
    "remote",
    "united states",
    "usa",
    "alabama", "alaska", "arizona", "arkansas", "california",
    "colorado", "connecticut", "delaware", "florida", "georgia",
    "hawaii", "idaho", "illinois", "indiana", "iowa",
    "kansas", "kentucky", "louisiana", "maine", "maryland",
    "massachusetts", "michigan", "minnesota", "mississippi", "missouri",
    "montana", "nebraska", "nevada", "new hampshire", "new jersey",
    "new mexico", "new york", "north carolina", "north dakota", "ohio",
    "oklahoma", "oregon", "pennsylvania", "rhode island", "south carolina",
    "south dakota", "tennessee", "texas", "utah", "vermont",
    "virginia", "washington", "west virginia", "wisconsin", "wyoming",
]
