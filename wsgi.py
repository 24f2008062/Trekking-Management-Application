"""
WSGI Production Entrypoint
Trekking Management Application • Bauhaus Enterprise Edition
"""
import os
from app import app, init_db_and_seed

# Ensure schema and initial administrator exist on startup
init_db_and_seed(app)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "0").lower() in ("1", "true", "yes")
    app.run(host="0.0.0.0", port=port, debug=debug)

