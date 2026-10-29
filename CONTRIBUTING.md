# Contributing to Student Dropout Analytics and Prediction System

Thank you for your interest in contributing to the **Student Dropout Analytics and Prediction System**! Open-source contributions from the community help make this project more reliable, secure, and accessible for educators and students.

---

## Code of Conduct

We are committed to providing a welcoming, inclusive, and harassment-free environment for everyone. Please be respectful and considerate when interacting with other contributors and maintainers.

---

## How Can I Contribute?

You can contribute in many ways:
- **Reporting Bugs**: Open an issue describing the unexpected behavior, including reproduction steps, expected vs. actual behavior, and environment details.
- **Suggesting Enhancements**: Propose new analytics views, ML algorithms, or UI features.
- **Improving Documentation**: Fix typos, add explanations, or improve installation and deployment guides.
- **Writing Code**: Pick up an open issue or submit a feature/bugfix via a Pull Request.
- **Adding Tests**: Expand test coverage for FastAPI endpoints or React components.

---

## Development Setup

### 1. Fork and Clone

1. Fork the repository on GitHub:
   ```bash
   https://github.com/sayyedtohid09-arch/Student-Dropout-analytics-and-prediction-system/fork
   ```
2. Clone your fork locally:
   ```bash
   git clone https://github.com/<your-username>/Student-Dropout-analytics-and-prediction-system.git
   cd Student-Dropout-analytics-and-prediction-system
   ```
3. Add the upstream remote:
   ```bash
   git remote add upstream https://github.com/sayyedtohid09-arch/Student-Dropout-analytics-and-prediction-system.git
   ```

### 2. Backend Setup (FastAPI & Python)

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate

   # Linux/macOS
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy the environment template:
   ```bash
   cp .env.example .env
   ```
5. Run the development server:
   ```bash
   uvicorn app.main:app --reload
   ```
   Interactive Swagger documentation will be available at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

### 3. Frontend Setup (React & Vite)

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install npm dependencies:
   ```bash
   npm install
   ```
3. Start the Vite dev server:
   ```bash
   npm run dev
   ```
   The dashboard will be accessible at [http://localhost:5173](http://localhost:5173).

---

## Testing & Quality Assurance

Before submitting a Pull Request, please ensure all automated checks pass locally.

### Backend Tests
```bash
cd backend
python -m pytest
```

### Frontend Linting & Build
```bash
cd frontend
npm run lint
npm run build
```

---

## Pull Request Guidelines

1. **Create a topic branch**:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/issue-description
   ```
2. **Follow Conventional Commits**:
   Write clear, atomic commit messages following conventional commit prefixes:
   - `feat:` New feature or enhancement
   - `fix:` Bug fix or vulnerability patch
   - `refactor:` Code refactoring without changing functionality
   - `test:` Adding or updating tests
   - `docs:` Documentation updates
   - `ci:` Continuous integration changes
3. **Keep PRs focused**:
   Submit small, self-contained PRs addressing a specific issue or feature rather than combining unrelated changes.
4. **Push and open PR**:
   Push your branch to your fork and submit a Pull Request to the `main` branch of the upstream repository.

---

## License

By contributing to this project, you agree that your contributions will be licensed under the project's repository license.
