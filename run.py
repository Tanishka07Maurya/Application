from backend.app import create_app

# Create the Flask app instance
app = create_app()

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 3000))
    app.run(debug=True, host='0.0.0.0', port=port)
