
# AGAL Prototype

A Proof of Concept → MVP for the **AGAL Project**.
<br>
<br>

## Deploying Locally

### **Pre-requisites**

- **Docker** (recommended: v28.1.x or newer)

<details>
<summary>For developing/running individual services <i>(optional)</i>:</summary>

- Python v3.9.x
- npm v10.9.x
- Node.js v22.16.x

</details>

<br>

### Setup Steps

1. **Clone the repository:**
   
    ```bash
    git clone https://github.com/InfinityDude007/agal-prototype.git
    cd agal-prototype
    ```

2. **Configure environment variables:**
    - Copy `.env.example` to `.env`:
      
      ```bash
      cp .env.example .env
      ```
      
    - Open `.env` and set all required values.

3. **Build and start the application:**
   
    ```bash
    docker compose up --build
    ```
    
    *Optionally, for faster builds with Docker Buildx:*
   
    ```bash
    export COMPOSE_BAKE=true
    docker compose up --build
    ```

4. **Access the app:**  
   Open [http://localhost:80](http://localhost:80) in your browser.

5. **Stop and clean up:**
    - To stop the app:
      
      ```bash
      docker compose down -v
      ```
      
    - To remove all images/volumes/caches (note: this is destructive!):
      
      ```bash
      docker compose down -v
      docker system prune -a --volumes -f
      ```

<br>

## Notes

- Make sure Docker is running before you start.
- The `.env` file **must** be filled out for the app to work.
- For development, you can run individual services from `/server`, `/client`, or `/nginx` with their respective commands.

<br>

## Project Structure

```
agal-prototype/
├── client/  # Frontend (React/Vite)
├── server/  # Backend (FastAPI)
├── nginx/   # Reverse proxy config
├── docker-compose.yml
├── .env.example
└── ...
```
