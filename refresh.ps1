& .\generate-imports.ps1
docker compose down
docker image rm edmachina_challenge_backend
docker build -t edmachina_challenge_backend ./
docker compose up -d