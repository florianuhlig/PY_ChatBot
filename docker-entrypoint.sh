#!/bin/bash
set -e

echo "🤖 Starting PY_ChatBot..."
# Create directory for database dynamically based on SQLITE_PATH

DB_DIR=$(dirname "$SQLITE_PATH")
mkdir -p "$DB_DIR" /app/logs

# Set default environment variables if not provided
export DB_TYPE=${DB_TYPE:-sqlite}
export SQLITE_PATH=${SQLITE_PATH:-databases/chatbot.db}
export FLASK_HOST=${FLASK_HOST:-0.0.0.0}
export FLASK_PORT=${FLASK_PORT:-8080}
export FLASK_DEBUG=${FLASK_DEBUG:-false}

# Generate a random secret key if not provided
if [ -z "$FLASK_SECRET_KEY" ]; then
    export FLASK_SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
    echo "⚠️  Generated random secret key. Set FLASK_SECRET_KEY environment variable for production!"
fi

# Initialize database if it doesn't exist
if [ "$DB_TYPE" = "sqlite" ] && [ ! -f "$SQLITE_PATH" ]; then
    echo "📦 Initializing SQLite database at $SQLITE_PATH..."
    python -c "
import sys
sys.path.append('/app')
from config.database import DatabaseConfig
from database import get_database

try:
    db_config = DatabaseConfig()
    db_type, config = db_config.get_database_config()
    database = get_database(db_type, config)
    print('✅ Database initialized successfully!')
    database.disconnect()
except Exception as e:
    print(f'❌ Database initialization failed: {e}')
    sys.exit(1)
"
fi

# Print configuration info
echo "📋 Configuration:"
echo "   - Database Type: $DB_TYPE"
echo "   - Database Path: $SQLITE_PATH"
echo "   - Flask Host: $FLASK_HOST"
echo "   - Flask Port: $FLASK_PORT"
echo "   - Debug Mode: $FLASK_DEBUG"

# Execute the command
exec "$@"
