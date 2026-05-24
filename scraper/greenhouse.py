import httpx
from .base import BaseScraper

_API = "https://boards-api.greenhouse.io/v1/boards/{slug}/jobs"


class GreenhouseScraper(BaseScraper):
    def fetch_jobs(self, company: str) -> list[dict]:
        try:
            resp = self.client().get(_API.format(slug=company))
            resp.raise_for_status()
        except httpx.HTTPError as e:
            print(f"[greenhouse/{company}] request failed: {e}")
            return []

        jobs = []
        for job in resp.json().get("jobs", []):
            jobs.append(self.normalize(
                job_id=str(job["id"]),
                title=job["title"],
                company=job.get("company_name", company),
                url=job["absolute_url"],
                location=job.get("location", {}).get("name", ""),
                source="greenhouse",
            ))
        return jobs
