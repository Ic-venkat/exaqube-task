# ESL Shipping Line Scraper

This project is designed to extract shipping line information from the ESL website, process the scraped data, and store it in a PostgreSQL database. It also integrates with a local chat application powered by a GenAI toolbox server for querying the data.

---

## 📦 Project Setup

### 1. Install Poetry

Poetry is used to manage dependencies and create a virtual environment.

- Visit the [Poetry website](https://python-poetry.org/docs/) for installation instructions.
- Then, in the project directory, run:

```bash
poetry install --no-root
```

### 2. Activate the Virtual Environment

Start the Poetry shell:

```bash
poetry shell
```

### 3. Configure Environment Variables

Create a `.env` file in the project root and add. Check the `.env.example` file for the exact naming of the environment variables.

- OpenAI API key
- PostgreSQL credentials

**Example `.env` file:**

```env
OPENAI_API_KEY=your-api-key
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_database
DB_USER=your_username
DB_PASSWORD=your_password
```

### 4. Update `tools.yaml`

Make sure to enter the same PostgreSQL credentials in `tools.yaml`. Development credentials are included for reference.

---

## 🚀 Running the Scraper and Processing Data

### Step 1: Scrape Website Data

```bash
python scraper/scraper.py
```

### Step 2: Process and Store the Data

```bash
python scraper/process_files.py
```

> ⚠️ Ensure `.env` is correctly set up with your database details before running this step.

---

## 🧠 Running the Chat Application (GenAI Toolbox)

To enable chat-based data queries, set up the GenAI toolbox:

### 1. Download the Toolbox

Set the appropriate OS environment variable:

```bash
export OS="darwin/amd64"  # Options: linux/amd64, darwin/arm64, darwin/amd64, windows/amd64
```

Download the binary:

```bash
curl -O https://storage.googleapis.com/genai-toolbox/v0.3.0/$OS/toolbox
```

### 2. Make It Executable

```bash
chmod +x toolbox
```

### 3. Start the Toolbox Server

```bash
./toolbox --tools_file "tools.yaml"
```

---

Once the toolbox server is running, open a new terminal with poetry shell and start the chat application:

```bash
python app/chat.py
```

Predefined questions are answered such as:

- “Find shipping lines that offer 20’ Dry equipment.”
- “Can you search for shipping lines in Germany?”
- “Please show me shipping lines that operate in the Port of Hamburg.”
- “Find shipping lines with a free time of 14 Calendar Days.”
- “Can you search for shipping lines that use USD as their currency?”

The chat application will respond based on the data extracted and processed.

> 🔎 Note: Results are limited to **10 entries per query** due to dataset size.

---

## ✅ Summary

- Install and configure Poetry.
- Set environment variables and update `tools.yaml`.
- Scrape, process, and store data in PostgreSQL.
- Run the GenAI toolbox and chat application to query the data interactively.
