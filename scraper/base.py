from abc import ABC, abstractmethod
import httpx


class BaseScraper(ABC):
    # Subclasses share one client for connection pooling
    _client: httpx.Client | None = None

    @classmethod
    def client(cls) -> httpx.Client:
        if cls._client is None:
            cls._client = httpx.Client(timeout=15, follow_redirects=True)
        return cls._client

    @abstractmethod
    def fetch_jobs(self, company: str) -> list[dict]:
        """Return a list of normalized job dicts for the given company slug."""
        ...

    @staticmethod
    def normalize(
        *,
        job_id: str,
        title: str,
        company: str,
        url: str,
        location: str,
        source: str,
    ) -> dict:
        return {
            "id": job_id,
            "title": title,
            "company": company,
            "url": url,
            "location": location,
            "source": source,
        }
