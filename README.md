Template of fastapi, sveltekit, tailwindcss, docker.

Showing:

- hot reload
- env vars
- frontend to backend communication
- custom error page
- tailwindcss, daisyui

# Install on Fedora35

Since hot reload is enabled, node and pipenv must be available locally.

Backend:

- pip install pipenv
- cd fastapi && pipenv install --dev && cd -

Frontend:

- dnf install node
- cd sveltekit && npm install --include=dev && cd -

Run:

- docker-compose up --build
