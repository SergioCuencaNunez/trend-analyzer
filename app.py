from app_instance import app, server
import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    # app.run_server(debug = True)
    app.run_server(host='0.0.0.0', port=port)
