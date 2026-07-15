# Submission Evidence Checklist

This directory is reserved for the two screenshots required by the assignment.
Screenshots must be captured after the committed workflow is pushed and Docker
Hub credentials are configured; they should show real external results rather
than placeholder images.

Add these files before final submission:

1. `github-actions-success.png`
   - Open the repository's **Actions** tab.
   - Select the latest `CI/CD` run on `main`.
   - Capture the run summary with the `test`, `security`, and `deploy` jobs all
     visibly successful.
2. `docker-hub-deployment.png`
   - Open the `matthewferoz/calculator-sql` Docker Hub repository.
   - Open the **Tags** page.
   - Capture both the `latest` tag and the tag matching the deployed Git commit
     SHA, including their recent push timestamps.

After adding the screenshots, embed them below so they render from GitHub:

```markdown
![Successful GitHub Actions workflow](github-actions-success.png)
![Docker Hub image tags](docker-hub-deployment.png)
```

Do not commit a Docker Hub token, GitHub token, `.env` file, browser cookies, or
any screenshot that exposes credentials.
