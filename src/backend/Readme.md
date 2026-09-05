## 1. Create a Python Virtual Environments
```bash
python3.111 -m venv .venv
```
## 2. Activate the Virtual Environments
### On Linux
```bash
pip install --upgrade pip

```
### On Windows
```bash
pip install --upgrade pip
.venv\Scripts\activate
```
## 3. Install Required Packages
```bash
pip install -r requirements.txt
```
## 4. Create a `env` file from example
### On Linux
```bash
cp .env.example .env
```
### On Windows
```bash
copy .env.example .env
```
## 5. Run the FastAPI Application
```bash
uvicorn app.main:app --reload
```