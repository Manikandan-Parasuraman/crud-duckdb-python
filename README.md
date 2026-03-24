# FastAPI DuckDB CRUD Service

A production-grade, highly efficient backend service using **FastAPI** and **DuckDB**. This project demonstrates clean architecture patterns, high-performance data access, and DevOps-ready configuration.

---

## Key Features

- **Full CRUD Operations**: Create, Read (single + list with pagination), Update, Delete.
- **DuckDB Powered**: Blazing fast analytical and transactional queries via an in-memory or file-based OLAP database.
- **Clean Architecture**: Decoupled layers (API, Service, Repository, Model).
- **Production Ready**: Structured logging, Dockerized, Pydantic v2 validation, and environment-based configuration.
- **Optimized for DX**: Auto-generated OpenAPI (Swagger) documentation.

---

## Tech Stack

- **Python 3.11+**: Modern, type-safe Python.
- **FastAPI**: High-performance async web framework.
- **DuckDB**: Fast SQL database engine designed for analytical queries but exceptionally fast for local CRUD operations too.
- **SQLAlchemy/DuckDB-Py**: Direct SQL execution for maximum performance and zero ORM overhead.
- **Pydantic v2**: High-speed data validation.
- **Docker + Docker Compose**: Containerization for seamless deployment.
- **Pytest**: Comprehensive test suite.

---

## Project Structure

```text
app/
├── api/
│   ├── v1/
│   │   ├── endpoints/  # API Route handlers
│   │   └── api.py      # Main router aggregator
│   └── deps.py         # Dependency injection functions
├── core/               # App configuration, logging, exceptions
├── db/                 # Database session and initialization
├── models/             # Pydantic schemas and domain models
├── repositories/       # Data access layer (DuckDB queries)
└── services/           # Business logic layer
tests/                  # Unit and integration tests
data/                   # DuckDB persistence storage (local)
Dockerfile              # Multi-stage optimized build
docker-compose.yml      # Service orchestration
requirements.txt        # Project dependencies
```

---

## Getting Started

### 1. Prerequisites
- Python 3.11+ installed.
- (Optional) Docker and Docker Compose.

### 2. Local Setup
1. **Clone the repository**:
   ```bash
   git clone <repo-url>
   cd crud-duckdb-python
   ```

2. **Set up Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   pip install -r requirements.txt
   ```

3. **Run the API**:
   ```bash
   uvicorn app.main:app --reload
   ```
   *Access API at: [http://localhost:8000/docs](http://localhost:8000/docs)*

### 3. Docker Setup
```bash
docker-compose up --build -d
```
*API will be available at [http://localhost:8000](http://localhost:8000)*

---

## API Endpoints & Example Usage

Here are sample `curl` requests for the **Item** entity:

### Create an Item
```bash
curl -X POST "http://localhost:8000/api/v1/items/" \\
     -H "Content-Type: application/json" \\
     -d '{"title": "Laptop", "description": "High performance laptop", "price": 1200.50}'
```

### List Items (with pagination)
```bash
curl -X GET "http://localhost:8000/api/v1/items/?skip=0&limit=10"
```

### Read Single Item
```bash
curl -X GET "http://localhost:8000/api/v1/items/<ITEM_ID>"
```

### Update an Item
```bash
curl -X PUT "http://localhost:8000/api/v1/items/<ITEM_ID>" \\
     -H "Content-Type: application/json" \\
     -d '{"price": 1150.99}'
```

### Delete an Item
```bash
curl -X DELETE "http://localhost:8000/api/v1/items/<ITEM_ID>"
```

---

## Architecture Decision Records (ADR)

### Why DuckDB?
- **Trade-offs**: Unlike PostgreSQL/MySQL, DuckDB is an "in-process" database (like SQLite but columnar). It sacrifices some multi-user write concurrency for massive local read/write speed and ease of distribution.
- **Ideal For**: Local-first apps, internal tools, edge computing, caches, or analytical workloads on small to medium datasets (~100M rows).
- **Limitations**: Not suitable for high-concurrency write-heavy OLTP (e.g., thousands of simultaneous writes).

### Why FastAPI?
- **Performance**: Built on Starlette and Pydantic, it's one of the fastest Python frameworks.
- **Async**: Native support for asynchronous programming allows handling thousands of concurrent connections efficiently.
- **Auto-generated Docs**: Out-of-the-box Swagger and ReDoc reduce developer overhead.

---

## Scalability Plan

DuckDB is powerful, but if your traffic grows:
1. **Vertical to Horizontal**: DuckDB is a local file DB. If you need horizontal scaling (multiple API instances), you should migrate to a client-server DB like **PostgreSQL**.
2. **PostgreSQL Migration**: The repository pattern makes it easy. Simply swap the DuckDB SQL in `ItemRepository` for SQLAlchemy or Psycopg3 queries.
3. **Caching**: Integrate **Redis** to cache frequently read items, reducing the load on the storage engine.
4. **API Gateway**: Use NGINX or Kong as an API gateway for rate limiting and load balancing.

---

## Cost Optimization Strategy

1. **Zero DB Infra Cost**: Using DuckDB eliminates the need for managed RDS (Amazon RDS, Google Cloud SQL), saving \$20–\$100+ per month for small projects.
2. **Low Container Footprint**: DuckDB is embedded; your Docker image only contains the API and the binary engine. It requires less RAM than a standalone DB server.
3. **Efficient Resource Usage**: Multi-stage Docker builds ensure small images, reducing storage and bandwidth costs.
4. **Efficient Queries**: Columnar storage in DuckDB means queries touch less data on disk, leading to lower I/O costs in cloud environments.

---

## Testing

Run simulations:
```bash
pytest
```
*Tests use an isolated `test_data/test.db` to ensure data integrity.*