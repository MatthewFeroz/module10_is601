# Module 10 Reflection

## Building on the Previous Module

The most important design decision was to evolve the existing Module 9
calculator instead of replacing it with the instructor repository. That kept
the calculator, raw SQL exercises, Docker Compose services, tests, and commit
history intact while adding the new user-account capability as a set of focused
layers. This made the progression between modules visible and reduced the risk
of breaking features that already worked.

## SQLAlchemy and Pydantic

Separating the SQLAlchemy model from the Pydantic schemas clarified two kinds
of data modeling that initially looked similar. The SQLAlchemy `User` class
describes how trusted data is stored and which guarantees PostgreSQL must
enforce. `UserCreate` instead describes what untrusted input is allowed into the
application. `UserRead` describes what data may safely leave it. This separation
made it straightforward to prove that `password_hash` can be present in the
database model while remaining absent from every public serialization.

Pydantic's `EmailStr` eliminated the need to write a fragile email parser. I
also normalized usernames and emails before checking uniqueness. Without that
step, values such as `Alice` and `alice` could become separate records even
though a user would reasonably consider them the same identifier. Password
validation includes both complexity checks and bcrypt's 72-byte input limit,
including the less obvious case where a short-looking Unicode string occupies
more bytes than characters.

## Password Security

The central security requirement was ensuring a raw password never reaches the
database. The service layer is the only normal path that constructs a user, and
it calls `hash_password` before assigning `password_hash`. Bcrypt generates a
new salt for every call, so two users with the same password still receive
different stored values. Verification performs a one-way comparison and treats
malformed stored hashes as authentication failures instead of application
errors.

This work also reinforced the distinction among hashing, encryption, and
encoding. A password hash is intentionally one-way; the application verifies a
candidate but never decrypts the original password. Tests confirm that hashes
differ from plaintext, repeated hashes differ from one another, correct
passwords verify, and incorrect passwords do not.

## Database Testing Challenges

Database tests require more isolation than ordinary unit tests because commits
can leave state behind. The PostgreSQL fixtures therefore require an explicit
`TEST_DATABASE_URL`, recreate mapped tables at session startup, and delete
committed users after each test. Requiring a separate environment variable was
an important safety measure: the cleanup code cannot silently operate on the
normal development database.

The integration tests exercise both the friendly application-level duplicate
check and PostgreSQL's unique constraint. Both are necessary. The first creates
a useful error for normal requests, while the database constraint protects
against simultaneous requests that pass the initial check at the same time.
Invalid email tests demonstrate that malformed data is rejected before any row
is inserted.

The final local suite ran 84 tests—unit, API integration, real PostgreSQL, and
Playwright end to end—with 100% measured coverage of the application modules.
High coverage was useful here because it revealed defensive error and rollback
branches that could otherwise remain unverified.

## Docker and CI/CD

The pipeline uses three dependent jobs: test, security, and deploy. A failure in
either of the first two jobs prevents publication. The security job goes beyond
building the image: it starts the container, checks the live `/health` endpoint,
and runs Trivy against operating-system and Python packages. The locally built
image ran as an unprivileged user and produced no high or critical findings in
the verification scan.

The deploy job publishes both `latest` and the Git commit SHA. The SHA tag makes
each release traceable and avoids relying only on a mutable label. Multi-platform
builds support AMD64 and ARM64 machines. Third-party GitHub Actions are pinned to
full commit identifiers so a mutable tag cannot silently change the code that
runs with repository access.

The only steps that cannot be reproduced solely from source code are providing
the Docker Hub access token and capturing evidence from the external services.
Those credentials belong in GitHub Secrets rather than the repository. After a
successful main-branch run, the Actions job summary and Docker Hub tags page
provide the two required submission screenshots.

## What I Would Improve Next

In a future module I would add Alembic migrations instead of relying on
`create_all` for a clean coursework database. Migrations would update existing
installations safely without recreating volumes. I would also add user
registration and login routes, rate limiting, password-reset flows, and a secret
manager for signing keys when authentication routes are introduced. The
current model, schemas, service, and tests provide a secure base for those
features without prematurely exposing public endpoints.
