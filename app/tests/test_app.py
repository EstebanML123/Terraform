import pytest
import os
import sys

# Añadir el directorio 'app' al path para poder importar el módulo principal
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app import app as flask_app

@pytest.fixture
def app():
    """Crea una instancia del Flask app para pruebas."""
    yield flask_app

@pytest.fixture
def client(app):
    """Crea un cliente de prueba para interactuar con la app."""
    return app.test_client()

def test_login_page(client):
    """Verifica que la página de login carga correctamente."""
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data or b'Iniciar' in response.data  # Acepta versión en español

def test_register_page(client):
    """Verifica que la página de registro carga correctamente."""
    response = client.get('/register')
    assert response.status_code == 200
    # ✅ Acepta texto en inglés o español (según idioma del HTML)
    assert b'Register' in response.data or b'Registro' in response.data

def test_home_page_redirect(client):
    """Verifica que '/' redirige al login cuando no hay sesión activa."""
    response = client.get('/')
    assert response.status_code == 302  # Redirige a /login
    assert '/login' in response.location

def test_valid_email():
    """Verifica la función valid_email de la app."""
    from app import valid_email
    assert valid_email('test@example.com') is not None
    assert valid_email('invalid-email') is None

def test_health_check(client):
    """Verifica que la aplicación responde en /login (chequeo básico de salud)."""
    response = client.get('/login')
    assert response.status_code == 200
