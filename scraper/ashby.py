import httpx
from .base import BaseScraper

_API = "https://jobs.ashbyhq.com/api/non-user-graphql?op=ApiJobBoardWithTeams"
_QUERY = """
query ApiJobBoardWithTeams($organizationHostedJobsPageName: String!) {
  jobBoard: jobBoardWithTeams(organizationHostedJobsPageName: $organizationHostedJobsPageName) {
    jobPostings {
      id
      title
      locationName
    }
  }
}
"""


class AshbyScraper(BaseScraper):
    def fetch_jobs(self, company: str) -> list[dict]:
        try:
            resp = self.client().post(
                _API,
                json={
                    "operationName": "ApiJobBoardWithTeams",
                    "variables": {"organizationHostedJobsPageName": company},
                    "query": _QUERY,
                },
            )
            resp.raise_for_status()
        except httpx.HTTPError as e:
            print(f"[ashby/{company}] request failed: {e}")
            return []

        data = resp.json()
        if "errors" in data:
            print(f"[ashby/{company}] GraphQL errors: {data['errors']}")
            return []

        jobs = []
        for job in data["data"]["jobBoard"]["jobPostings"]:
            jobs.append(self.normalize(
                job_id=job["id"],
                title=job["title"],
                company=company,
                url=f"https://jobs.ashbyhq.com/{company}/{job['id']}",
                location=job.get("locationName", ""),
                source="ashby",
            ))
        return jobs
