"""
Pruebas unitarias para UserBL (Business Logic de Usuarios)

Este archivo contiene pruebas para las funciones que NO requieren mocking:
- hash_password: Genera hash de contraseñas
- verify_password: Verifica contraseñas contra hashes
"""

import pytest
import warnings
from app.business_logic.user_bl import UserBL

# Suprimir warnings de deprecación durante los tests
warnings.filterwarnings("ignore", category=DeprecationWarning)


class TestUserBL:
    """Clase de pruebas para UserBL"""

    def test_hash_password_generates_hash(self):
        """
        Prueba que hash_password genera un hash válido
        
        Pasos:
        1. Preparación: Definir una contraseña de prueba
        2. Lógica: Generar el hash de la contraseña
        3. Validación: Verificar que el hash es válido (string no vacío con formato bcrypt)
        """
        # 1. PREPARACIÓN DE LA PRUEBA (Arrange/Given)
        password = "test_password_123"
        
        # 2. LÓGICA DE LA PRUEBA (Act/When)
        hashed = UserBL.hash_password(password)
        
        # 3. VALIDACIÓN Y ACEPTACIÓN DE LA PRUEBA (Assert/Then)
        assert isinstance(hashed, str)
        assert len(hashed) > 0
        # Los hashes de bcrypt tienen un formato específico
        assert hashed.startswith("$2b$") or hashed.startswith("$2a$") or hashed.startswith("$2y$")

    def test_hash_password_different_hashes_for_same_password(self):
        """
        Prueba que hash_password genera hashes diferentes para la misma contraseña (debido a la sal)
        
        Pasos:
        1. Preparación: Definir una contraseña
        2. Lógica: Generar dos hashes de la misma contraseña
        3. Validación: Verificar que los hashes son diferentes
        """
        # 1. PREPARACIÓN DE LA PRUEBA (Arrange/Given)
        password = "same_password"
        
        # 2. LÓGICA DE LA PRUEBA (Act/When)
        hash1 = UserBL.hash_password(password)
        hash2 = UserBL.hash_password(password)
        
        # 3. VALIDACIÓN Y ACEPTACIÓN DE LA PRUEBA (Assert/Then)
        # Los hashes deben ser diferentes debido a la sal aleatoria
        assert hash1 != hash2

    def test_hash_password_special_characters(self):
        """
        Prueba hash_password con caracteres especiales
        
        Pasos:
        1. Preparación: Definir contraseña con caracteres especiales
        2. Lógica: Generar hash
        3. Validación: Verificar que se genera un hash válido
        """
        # 1. PREPARACIÓN DE LA PRUEBA (Arrange/Given)
        password = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        # 2. LÓGICA DE LA PRUEBA (Act/When)
        hashed = UserBL.hash_password(password)
        
        # 3. VALIDACIÓN Y ACEPTACIÓN DE LA PRUEBA (Assert/Then)
        assert isinstance(hashed, str)
        assert len(hashed) > 0

    def test_verify_password_correct_password(self):
        """
        Prueba que verify_password retorna True para contraseña correcta
        
        Pasos:
        1. Preparación: Definir contraseña y generar su hash
        2. Lógica: Verificar la contraseña contra el hash
        3. Validación: Verificar que retorna True
        """
        # 1. PREPARACIÓN DE LA PRUEBA (Arrange/Given)
        password = "test_password_123"
        hashed = UserBL.hash_password(password)
        
        # 2. LÓGICA DE LA PRUEBA (Act/When)
        result = UserBL.verify_password(password, hashed)
        
        # 3. VALIDACIÓN Y ACEPTACIÓN DE LA PRUEBA (Assert/Then)
        assert result is True

    def test_verify_password_empty_password(self):
        """
        Prueba verify_password con contraseña vacía
        
        Pasos:
        1. Preparación: Generar hash de contraseña vacía
        2. Lógica: Verificar contraseña vacía y contraseña incorrecta
        3. Validación: Verificar resultados correctos
        """
        # 1. PREPARACIÓN DE LA PRUEBA (Arrange/Given)
        password = ""
        hashed = UserBL.hash_password(password)
        
        # 2. LÓGICA DE LA PRUEBA (Act/When)
        result_correct = UserBL.verify_password(password, hashed)
        result_wrong = UserBL.verify_password("not_empty", hashed)
        
        # 3. VALIDACIÓN Y ACEPTACIÓN DE LA PRUEBA (Assert/Then)
        assert result_correct is True
        assert result_wrong is False

    def test_verify_password_case_sensitive(self):
        """
        Prueba que verify_password es sensible a mayúsculas/minúsculas
        
        Pasos:
        1. Preparación: Definir contraseña con mayúsculas y generar hash
        2. Lógica: Verificar con diferentes variaciones de mayúsculas/minúsculas
        3. Validación: Verificar que solo la contraseña exacta funciona
        """
        # 1. PREPARACIÓN DE LA PRUEBA (Arrange/Given)
        password = "TestPassword123"
        hashed = UserBL.hash_password(password)
        
        # 2. LÓGICA DE LA PRUEBA (Act/When)
        result_correct = UserBL.verify_password("TestPassword123", hashed)
        result_lowercase = UserBL.verify_password("testpassword123", hashed)
        result_uppercase = UserBL.verify_password("TESTPASSWORD123", hashed)
        
        # 3. VALIDACIÓN Y ACEPTACIÓN DE LA PRUEBA (Assert/Then)
        assert result_correct is True
        assert result_lowercase is False
        assert result_uppercase is False

    def test_verify_password_special_characters(self):
        """
        Prueba verify_password con caracteres especiales
        
        Pasos:
        1. Preparación: Definir contraseña con caracteres especiales y generar hash
        2. Lógica: Verificar contraseña correcta e incorrecta
        3. Validación: Verificar resultados
        """
        # 1. PREPARACIÓN DE LA PRUEBA (Arrange/Given)
        password = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        hashed = UserBL.hash_password(password)
        
        # 2. LÓGICA DE LA PRUEBA (Act/When)
        result = UserBL.verify_password(password, hashed)
        result_wrong = UserBL.verify_password("different_special!@#", hashed)
        
        # 3. VALIDACIÓN Y ACEPTACIÓN DE LA PRUEBA (Assert/Then)
        assert result is True
        assert result_wrong is False

    def test_verify_password_invalid_hash_format(self):
        """
        Prueba verify_password con formato de hash inválido
        
        Pasos:
        1. Preparación: Definir contraseña y hash inválido
        2. Lógica: Intentar verificar con hash inválido
        3. Validación: Verificar que se lanza una excepción
        """
        # 1. PREPARACIÓN DE LA PRUEBA (Arrange/Given)
        password = "test_password"
        invalid_hash = "not_a_valid_hash_format"
        
        # 2. LÓGICA DE LA PRUEBA (Act/When)
        # 3. VALIDACIÓN Y ACEPTACIÓN DE LA PRUEBA (Assert/Then)
        # Debería lanzar una excepción o retornar False
        # passlib generalmente lanza una excepción con hash inválido
        with pytest.raises(Exception):
            UserBL.verify_password(password, invalid_hash)

    def test_hash_and_verify_round_trip(self):
        """
        Prueba completa: hash y luego verificar la misma contraseña
        
        Pasos:
        1. Preparación: Definir lista de contraseñas de prueba
        2. Lógica: Para cada contraseña, generar hash y verificar
        3. Validación: Verificar que la contraseña original funciona y una incorrecta no
        """
        # 1. PREPARACIÓN DE LA PRUEBA (Arrange/Given)
        test_passwords = [
            "simple_password",
            "Complex_P@ssw0rd!",
            "123456789",
            "",
            "ñ_áéíóú_中文",
            "a" * 50  # Contraseña larga pero dentro del límite de bcrypt (72 bytes)
        ]
        
        # 2. LÓGICA DE LA PRUEBA (Act/When)
        for password in test_passwords:
            hashed = UserBL.hash_password(password)
            result_correct = UserBL.verify_password(password, hashed)
            # Verificar que contraseña incorrecta falla
            wrong_password = "completely_different_password_123" if password else "not_empty"
            result_wrong = UserBL.verify_password(wrong_password, hashed)
            
            # 3. VALIDACIÓN Y ACEPTACIÓN DE LA PRUEBA (Assert/Then)
            assert result_correct is True, f"La contraseña '{password}' debería verificarse correctamente"
            assert result_wrong is False, f"La contraseña incorrecta no debería verificarse para '{password}'"

    def test_hash_password_consistency(self):
        """
        Prueba que hash_password siempre genera un hash válido (no None)
        
        Pasos:
        1. Preparación: Definir lista de contraseñas
        2. Lógica: Generar hash para cada contraseña
        3. Validación: Verificar que todos los hashes son válidos
        """
        # 1. PREPARACIÓN DE LA PRUEBA (Arrange/Given)
        passwords = ["test1", "test2", "test3"]
        
        # 2. LÓGICA DE LA PRUEBA (Act/When)
        # 3. VALIDACIÓN Y ACEPTACIÓN DE LA PRUEBA (Assert/Then)
        for password in passwords:
            hashed = UserBL.hash_password(password)
            assert hashed is not None
            assert isinstance(hashed, str)
