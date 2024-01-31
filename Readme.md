```bash
docker compose up -d --build
docker compose exec t32_journal migrate
docker compose exec t32_backend migrate
cd t32_backend/
sudo chmod 777 uploads/
```