"""
Pruebas unitarias para auth_service (Servicio de Autenticación)

Este archivo contiene pruebas para las funciones que NO requieren mocking:
- create_access_token: Crea tokens JWT
- verify_token: Verifica y decodifica tokens JWT
"""

import pytest
import warnings
import logging
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from jose import JWTError
from app.services.auth_service import create_access_token, verify_token
from app.core.config import settings

# Suprimir warnings de deprecación durante los tests
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Reducir el nivel de logging durante los tests
logging.getLogger("app").setLevel(logging.ERROR)


class TestAuthService:
    """Clase de pruebas para auth_service"""

    def test_create_access_token_returns_string(self):
        """
        Prueba que create_access_token retorna una cadena
        
        Pasos:
        1. Preparación: Definir datos para el token
        2. Lógica: Crear el token
        3. Validación: Verificar que retorna un string no vacío
        """
        # 1. PREPARACIÓN DE LA PRUEBA (Arrange/Given)
        data = {"sub": "testuser"}
        
        # 2. LÓGICA DE LA PRUEBA (Act/When)
        token = create_access_token(data)
        
        # 3. VALIDACIÓN Y ACEPTACIÓN DE LA PRUEBA (Assert/Then)
        assert isinstance(token, str)
        assert len(token) > 0

    def test_create_access_token_contains_data(self):
        """
        Prueba que el token creado contiene los datos proporcionados
        
        Pasos:
        1. Preparación: Definir datos con múltiples campos
        2. Lógica: Crear token y verificarlo
        3. Validación: Verificar que el payload contiene todos los datos
        """
        # 1. PREPARACIÓN DE LA PRUEBA (Arrange/Given)
        data = {"sub": "testuser", "role": "admin"}
        
        # 2. LÓGICA DE LA PRUEBA (Act/When)
        token = create_access_token(data)
        payload = verify_token(token, HTTPException(status_code=401))
        
        # 3. VALIDACIÓN Y ACEPTACIÓN DE LA PRUEBA (Assert/Then)
        assert payload.get("sub") == "testuser"
        assert payload.get("role") == "admin"

    def test_create_access_token_has_expiration(self):
        """
        Prueba que el token creado tiene fecha de expiración
        
        Pasos:
        1. Preparación: Definir datos para el token
        2. Lógica: Crear token y verificarlo
        3. Validación: Verificar que tiene campo 'exp' y está en el futuro
        """
        # 1. PREPARACIÓN DE LA PRUEBA (Arrange/Given)
        data = {"sub": "testuser"}
        
        # 2. LÓGICA DE LA PRUEBA (Act/When)
        token = create_access_token(data)
        payload = verify_token(token, HTTPException(status_code=401))
        
        # 3. VALIDACIÓN Y ACEPTACIÓN DE LA PRUEBA (Assert/Then)
        assert "exp" in payload
        # Verificar que la expiración es en el futuro
        exp_timestamp = payload["exp"]
        exp_datetime = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc).replace(tzinfo=None)
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        assert exp_datetime > now

    def test_create_access_token_expiration_time(self):
        """
        Prueba que el token expira en el tiempo correcto
        
        Pasos:
        1. Preparación: Definir datos y capturar tiempo antes/después
        2. Lógica: Crear token y verificarlo
        3. Validación: Verificar que la expiración está dentro del rango esperado
        """
        # 1. PREPARACIÓN DE LA PRUEBA (Arrange/Given)
        data = {"sub": "testuser"}
        before_token = datetime.now(timezone.utc).replace(tzinfo=None)
        
        # 2. LÓGICA DE LA PRUEBA (Act/When)
        token = create_access_token(data)
        after_token = datetime.now(timezone.utc).replace(tzinfo=None)
        payload = verify_token(token, HTTPException(status_code=401))
        
        # 3. VALIDACIÓN Y ACEPTACIÓN DE LA PRUEBA (Assert/Then)
        exp_timestamp = payload["exp"]
        exp_datetime = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc).replace(tzinfo=None)
        # La expiración debe ser aproximadamente ACCESS_TOKEN_EXPIRE_MINUTES en el futuro
        expected_exp_min = after_token + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        expected_exp_max = before_token + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES) + timedelta(seconds=2)
        assert exp_datetime >= expected_exp_min - timedelta(seconds=2)
        assert exp_datetime <= expected_exp_max

    def test_create_access_token_multiple_fields(self):
        """
        Prueba create_access_token con múltiples campos
        
        Pasos:
        1. Preparación: Definir datos con múltiples campos
        2. Lógica: Crear token y verificarlo
        3. Validación: Verificar que todos los campos están presentes
        """
        # 1. PREPARACIÓN DE LA PRUEBA (Arrange/Given)
        data = {
            "sub": "testuser",
            "user_id": 123,
            "role": "admin",
            "email": "test@example.com",
            "custom_field": "custom_value"
        }
        
        # 2. LÓGICA DE LA PRUEBA (Act/When)
        token = create_access_token(data)
        payload = verify_token(token, HTTPException(status_code=401))
        
        # 3. VALIDACIÓN Y ACEPTACIÓN DE LA PRUEBA (Assert/Then)
        assert payload.get("sub") == "testuser"
        assert payload.get("user_id") == 123
        assert payload.get("role") == "admin"
        assert payload.get("email") == "test@example.com"
        assert payload.get("custom_field") == "custom_value"

    def test_verify_token_valid_token(self):
        """
        Prueba verify_token con un token válido
        
        Pasos:
        1. Preparación: Crear token válido con datos
        2. Lógica: Verificar el token
        3. Validación: Verificar que retorna el payload correcto
        """
        # 1. PREPARACIÓN DE LA PRUEBA (Arrange/Given)
        data = {"sub": "testuser", "role": "admin"}
        token = create_access_token(data)
        
        # 2. LÓGICA DE LA PRUEBA (Act/When)
        payload = verify_token(token, HTTPException(status_code=401))
        
        # 3. VALIDACIÓN Y ACEPTACIÓN DE LA PRUEBA (Assert/Then)
        assert isinstance(payload, dict)
        assert payload.get("sub") == "testuser"
        assert payload.get("role") == "admin"

    def test_verify_token_invalid_token_format(self):
        """
        Prueba verify_token con un formato de token inválido
        
        Pasos:
        1. Preparación: Definir token con formato inválido
        2. Lógica: Intentar verificar el token
        3. Validación: Verificar que se lanza HTTPException
        """
        # 1. PREPARACIÓN DE LA PRUEBA (Arrange/Given)
        invalid_token = "not.a.valid.token"
        credentials_exception = HTTPException(status_code=401, detail="Invalid token")
        
        # 2. LÓGICA DE LA PRUEBA (Act/When)
        # 3. VALIDACIÓN Y ACEPTACIÓN DE LA PRUEBA (Assert/Then)
        with pytest.raises(HTTPException):
            verify_token(invalid_token, credentials_exception)

    def test_verify_token_expired_token(self):
        """
        Prueba verify_token con token expirado
        
        Pasos:
        1. Preparación: Crear token con expiración en el pasado
        2. Lógica: Intentar verificar el token expirado
        3. Validación: Verificar que se lanza HTTPException
        """
        # 1. PREPARACIÓN DE LA PRUEBA (Arrange/Given)
        data = {"sub": "testuser"}
        to_encode = data.copy()
        from calendar import timegm
        expire_utc = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(minutes=1)
        expire_timestamp = timegm(expire_utc.utctimetuple())
        to_encode.update({"exp": expire_timestamp})
        
        from jose import jwt
        expired_token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        credentials_exception = HTTPException(status_code=401, detail="Token expired")
        
        # 2. LÓGICA DE LA PRUEBA (Act/When)
        # 3. VALIDACIÓN Y ACEPTACIÓN DE LA PRUEBA (Assert/Then)
        with pytest.raises(HTTPException):
            verify_token(expired_token, credentials_exception)

    def test_create_and_verify_round_trip(self):
        """
        Prueba completa: crear token y luego verificarlo
        
        Pasos:
        1. Preparación: Definir lista de datos de prueba
        2. Lógica: Para cada dato, crear token y verificarlo
        3. Validación: Verificar que todos los campos originales están presentes
        """
        # 1. PREPARACIÓN DE LA PRUEBA (Arrange/Given)
        test_data = [
            {"sub": "user1"},
            {"sub": "user2", "role": "admin"},
            {"sub": "user3", "user_id": 456, "email": "test@example.com"}
        ]
        
        # 2. LÓGICA DE LA PRUEBA (Act/When)
        # 3. VALIDACIÓN Y ACEPTACIÓN DE LA PRUEBA (Assert/Then)
        for data in test_data:
            token = create_access_token(data)
            payload = verify_token(token, HTTPException(status_code=401))
            
            # Verificar que todos los campos originales están presentes
            for key, value in data.items():
                assert payload.get(key) == value

    def test_verify_token_returns_payload(self):
        """
        Prueba que verify_token retorna el payload completo
        
        Pasos:
        1. Preparación: Crear token con múltiples campos
        2. Lógica: Verificar el token
        3. Validación: Verificar que retorna diccionario con todos los campos
        """
        # 1. PREPARACIÓN DE LA PRUEBA (Arrange/Given)
        data = {
            "sub": "testuser",
            "user_id": 789,
            "role": "manager",
            "permissions": ["read", "write"]
        }
        
        # 2. LÓGICA DE LA PRUEBA (Act/When)
        token = create_access_token(data)
        payload = verify_token(token, HTTPException(status_code=401))
        
        # 3. VALIDACIÓN Y ACEPTACIÓN DE LA PRUEBA (Assert/Then)
        assert isinstance(payload, dict)
        assert payload.get("sub") == "testuser"
        assert payload.get("user_id") == 789
        assert payload.get("role") == "manager"
        assert payload.get("permissions") == ["read", "write"]
        assert "exp" in payload