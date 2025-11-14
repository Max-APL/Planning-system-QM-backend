# tests/test_financial_bl_unit.py

import unittest
from unittest.mock import patch, MagicMock
from datetime import date
from app.business_logic.financial_bl import FinancialBL


class TestFinancialBLUnit(unittest.TestCase):
    """Pruebas unitarias para los métodos de FinancialBL usando mocks"""

    # ============================================================
    # PRUEBAS PARA get_budget_variance
    # ============================================================

    def test_get_budget_variance_success_with_materials_and_tools(self):
        """
        Prueba unitaria: Calcula correctamente la varianza del presupuesto
        cuando hay materiales y herramientas asignados
        """
        # 1. PREPARACIÓN DE LA PRUEBA
        project_id = 1
        mock_project = MagicMock()
        mock_project.ID = 1
        mock_project.NOMBRE = "Proyecto Test"
        mock_project.PRESUPUESTO_ASIGNADO = 10000.0

        mock_material_allocation = MagicMock()
        mock_material_allocation.FLUJO_MATERIAL_ID = 10
        mock_material_allocation.CANTIDAD = 5

        mock_tool_allocation = MagicMock()
        mock_tool_allocation.FLUJO_HERRAMIENTA_ID = 20
        mock_tool_allocation.CANTIDAD = 3

        mock_flow_material = MagicMock()
        mock_flow_material.MATERIAL_ID = 100

        mock_flow_tool = MagicMock()
        mock_flow_tool.HERRAMIENTA_ID = 200

        mock_material = MagicMock()
        mock_material.PRECIO_UNITARIO = 100.0

        mock_tool = MagicMock()
        mock_tool.PRECIO_UNITARIO = 50.0

        # 2. LÓGICA DE LA PRUEBA
        with patch('app.business_logic.financial_bl.get_project_by_id', return_value=mock_project), \
             patch('app.business_logic.financial_bl.get_material_allocations_by_project', return_value=[mock_material_allocation]), \
             patch('app.business_logic.financial_bl.get_tool_allocations_by_project', return_value=[mock_tool_allocation]), \
             patch('app.business_logic.financial_bl.get_flow_material_by_id', return_value=mock_flow_material), \
             patch('app.business_logic.financial_bl.get_flow_tool_by_id', return_value=mock_flow_tool), \
             patch('app.business_logic.financial_bl.get_material_by_id', return_value=mock_material), \
             patch('app.business_logic.financial_bl.get_tool_by_id', return_value=mock_tool):
            
            result = FinancialBL.get_budget_variance(project_id)

        # 3. VALIDACIÓN Y ACEPTACIÓN DE LA PRUEBA
        self.assertEqual(result['project_id'], 1)
        self.assertEqual(result['project_name'], "Proyecto Test")
        self.assertEqual(result['assigned_budget'], 10000.0)
        # Material: 100.0 * 5 = 500.0, Tool: 50.0 * 3 = 150.0, Total: 650.0
        self.assertEqual(result['actual_spending'], 650.0)
        self.assertEqual(result['budget_variance'], 9350.0)

    def test_get_budget_variance_project_not_found(self):
        """
        Prueba unitaria: Lanza excepción cuando el proyecto no existe
        """
        # 1. PREPARACIÓN DE LA PRUEBA
        project_id = 999

        # 2. LÓGICA DE LA PRUEBA y 3. VALIDACIÓN Y ACEPTACIÓN DE LA PRUEBA
        with patch('app.business_logic.financial_bl.get_project_by_id', return_value=None):
            with self.assertRaises(ValueError) as context:
                FinancialBL.get_budget_variance(project_id)
            
            self.assertIn("not found", str(context.exception).lower())

    def test_get_budget_variance_only_materials(self):
        """
        Prueba unitaria: Calcula varianza solo con materiales, sin herramientas
        """
        # 1. PREPARACIÓN DE LA PRUEBA
        project_id = 1
        mock_project = MagicMock()
        mock_project.ID = 1
        mock_project.NOMBRE = "Proyecto Solo Materiales"
        mock_project.PRESUPUESTO_ASIGNADO = 5000.0

        mock_material_allocation = MagicMock()
        mock_material_allocation.FLUJO_MATERIAL_ID = 10
        mock_material_allocation.CANTIDAD = 10

        mock_flow_material = MagicMock()
        mock_flow_material.MATERIAL_ID = 100

        mock_material = MagicMock()
        mock_material.PRECIO_UNITARIO = 200.0

        # 2. LÓGICA DE LA PRUEBA
        with patch('app.business_logic.financial_bl.get_project_by_id', return_value=mock_project), \
             patch('app.business_logic.financial_bl.get_material_allocations_by_project', return_value=[mock_material_allocation]), \
             patch('app.business_logic.financial_bl.get_tool_allocations_by_project', return_value=[]), \
             patch('app.business_logic.financial_bl.get_flow_material_by_id', return_value=mock_flow_material), \
             patch('app.business_logic.financial_bl.get_material_by_id', return_value=mock_material):
            
            result = FinancialBL.get_budget_variance(project_id)

        # 3. VALIDACIÓN Y ACEPTACIÓN DE LA PRUEBA
        self.assertEqual(result['actual_spending'], 2000.0)  # 200.0 * 10
        self.assertEqual(result['budget_variance'], 3000.0)  # 5000.0 - 2000.0

    def test_get_budget_variance_negative_variance(self):
        """
        Prueba unitaria: Maneja correctamente presupuesto negativo (gastos exceden presupuesto)
        """
        # 1. PREPARACIÓN DE LA PRUEBA
        project_id = 1
        mock_project = MagicMock()
        mock_project.ID = 1
        mock_project.NOMBRE = "Proyecto Sobregasto"
        mock_project.PRESUPUESTO_ASIGNADO = 1000.0

        mock_material_allocation = MagicMock()
        mock_material_allocation.FLUJO_MATERIAL_ID = 10
        mock_material_allocation.CANTIDAD = 20

        mock_flow_material = MagicMock()
        mock_flow_material.MATERIAL_ID = 100

        mock_material = MagicMock()
        mock_material.PRECIO_UNITARIO = 100.0

        # 2. LÓGICA DE LA PRUEBA
        with patch('app.business_logic.financial_bl.get_project_by_id', return_value=mock_project), \
             patch('app.business_logic.financial_bl.get_material_allocations_by_project', return_value=[mock_material_allocation]), \
             patch('app.business_logic.financial_bl.get_tool_allocations_by_project', return_value=[]), \
             patch('app.business_logic.financial_bl.get_flow_material_by_id', return_value=mock_flow_material), \
             patch('app.business_logic.financial_bl.get_material_by_id', return_value=mock_material):
            
            result = FinancialBL.get_budget_variance(project_id)

        # 3. VALIDACIÓN Y ACEPTACIÓN DE LA PRUEBA
        self.assertEqual(result['actual_spending'], 2000.0)  # 100.0 * 20
        self.assertEqual(result['budget_variance'], -1000.0)  # 1000.0 - 2000.0 (negativo)

    def test_get_budget_variance_material_not_found(self):
        """
        Prueba unitaria: Maneja correctamente cuando un material no se encuentra
        """
        # 1. PREPARACIÓN DE LA PRUEBA
        project_id = 1
        mock_project = MagicMock()
        mock_project.ID = 1
        mock_project.NOMBRE = "Proyecto Test"
        mock_project.PRESUPUESTO_ASIGNADO = 5000.0

        mock_material_allocation = MagicMock()
        mock_material_allocation.FLUJO_MATERIAL_ID = 10
        mock_material_allocation.CANTIDAD = 5

        mock_flow_material = MagicMock()
        mock_flow_material.MATERIAL_ID = 100

        # 2. LÓGICA DE LA PRUEBA
        with patch('app.business_logic.financial_bl.get_project_by_id', return_value=mock_project), \
             patch('app.business_logic.financial_bl.get_material_allocations_by_project', return_value=[mock_material_allocation]), \
             patch('app.business_logic.financial_bl.get_tool_allocations_by_project', return_value=[]), \
             patch('app.business_logic.financial_bl.get_flow_material_by_id', return_value=mock_flow_material), \
             patch('app.business_logic.financial_bl.get_material_by_id', return_value=None):
            
            result = FinancialBL.get_budget_variance(project_id)

        # 3. VALIDACIÓN Y ACEPTACIÓN DE LA PRUEBA
        # Si el material no existe, no se suma al gasto
        self.assertEqual(result['actual_spending'], 0.0)
        self.assertEqual(result['budget_variance'], 5000.0)

    # ============================================================
    # PRUEBAS PARA get_spending_trend
    # ============================================================

    def test_get_spending_trend_success_multiple_dates(self):
        """
        Prueba unitaria: Calcula tendencia de gastos con múltiples fechas
        """
        # 1. PREPARACIÓN DE LA PRUEBA
        project_id = 1
        mock_project = MagicMock()
        mock_project.ID = 1
        mock_project.NOMBRE = "Proyecto Test"

        mock_allocation1 = MagicMock()
        mock_allocation1.FLUJO_MATERIAL_ID = 10
        mock_allocation1.CANTIDAD = 2

        mock_allocation2 = MagicMock()
        mock_allocation2.FLUJO_MATERIAL_ID = 11
        mock_allocation2.CANTIDAD = 3

        mock_flow1 = MagicMock()
        mock_flow1.MATERIAL_ID = 100
        mock_flow1.FECHA = date(2024, 1, 15)

        mock_flow2 = MagicMock()
        mock_flow2.MATERIAL_ID = 101
        mock_flow2.FECHA = date(2024, 1, 20)

        mock_material1 = MagicMock()
        mock_material1.PRECIO_UNITARIO = 100.0

        mock_material2 = MagicMock()
        mock_material2.PRECIO_UNITARIO = 50.0

        # 2. LÓGICA DE LA PRUEBA
        with patch('app.business_logic.financial_bl.get_project_by_id', return_value=mock_project), \
             patch('app.business_logic.financial_bl.get_material_allocations_by_project', return_value=[mock_allocation1, mock_allocation2]), \
             patch('app.business_logic.financial_bl.get_tool_allocations_by_project', return_value=[]), \
             patch('app.business_logic.financial_bl.get_flow_material_by_id', side_effect=[mock_flow1, mock_flow2]), \
             patch('app.business_logic.financial_bl.get_material_by_id', side_effect=[mock_material1, mock_material2]):
            
            result = FinancialBL.get_spending_trend(project_id)

        # 3. VALIDACIÓN Y ACEPTACIÓN DE LA PRUEBA
        self.assertEqual(result['project_id'], 1)
        self.assertEqual(len(result['spending_over_time']), 2)
        # Verificar que las fechas están en orden
        dates = [entry['date'] for entry in result['spending_over_time']]
        self.assertEqual(dates[0], '2024-01-15')
        self.assertEqual(dates[1], '2024-01-20')

    def test_get_spending_trend_with_fase_filter(self):
        """
        Prueba unitaria: Filtra correctamente los gastos por fase
        """
        # 1. PREPARACIÓN DE LA PRUEBA
        project_id = 1
        fase = "desarrollo"
        mock_project = MagicMock()
        mock_project.ID = 1
        mock_project.NOMBRE = "Proyecto Test"

        mock_allocation = MagicMock()
        mock_allocation.FLUJO_MATERIAL_ID = 10
        mock_allocation.CANTIDAD = 5

        mock_flow = MagicMock()
        mock_flow.MATERIAL_ID = 100
        mock_flow.FECHA = date(2024, 1, 15)

        mock_material = MagicMock()
        mock_material.PRECIO_UNITARIO = 100.0

        # 2. LÓGICA DE LA PRUEBA
        with patch('app.business_logic.financial_bl.get_project_by_id', return_value=mock_project), \
             patch('app.business_logic.financial_bl.get_material_allocations_by_project', return_value=[mock_allocation]) as mock_mat_alloc, \
             patch('app.business_logic.financial_bl.get_tool_allocations_by_project', return_value=[]), \
             patch('app.business_logic.financial_bl.get_flow_material_by_id', return_value=mock_flow), \
             patch('app.business_logic.financial_bl.get_material_by_id', return_value=mock_material):
            
            result = FinancialBL.get_spending_trend(project_id, fase=fase)

        # 3. VALIDACIÓN Y ACEPTACIÓN DE LA PRUEBA
        # Verificar que se llamó con la fase correcta
        mock_mat_alloc.assert_called_once_with(project_id, fase)
        self.assertIsInstance(result['spending_over_time'], list)

    def test_get_spending_trend_project_not_found(self):
        """
        Prueba unitaria: Lanza excepción cuando el proyecto no existe
        """
        # 1. PREPARACIÓN DE LA PRUEBA
        project_id = 999

        # 2. LÓGICA DE LA PRUEBA y 3. VALIDACIÓN Y ACEPTACIÓN DE LA PRUEBA
        with patch('app.business_logic.financial_bl.get_project_by_id', return_value=None):
            with self.assertRaises(ValueError) as context:
                FinancialBL.get_spending_trend(project_id)
            
            self.assertIn("not found", str(context.exception).lower())

    def test_get_spending_trend_empty_allocations(self):
        """
        Prueba unitaria: Maneja correctamente cuando no hay asignaciones
        """
        # 1. PREPARACIÓN DE LA PRUEBA
        project_id = 1
        mock_project = MagicMock()
        mock_project.ID = 1
        mock_project.NOMBRE = "Proyecto Sin Gastos"

        # 2. LÓGICA DE LA PRUEBA
        with patch('app.business_logic.financial_bl.get_project_by_id', return_value=mock_project), \
             patch('app.business_logic.financial_bl.get_material_allocations_by_project', return_value=[]), \
             patch('app.business_logic.financial_bl.get_tool_allocations_by_project', return_value=[]):
            
            result = FinancialBL.get_spending_trend(project_id)

        # 3. VALIDACIÓN Y ACEPTACIÓN DE LA PRUEBA
        self.assertEqual(result['project_id'], 1)
        self.assertEqual(len(result['spending_over_time']), 0)

    def test_get_spending_trend_same_date_aggregation(self):
        """
        Prueba unitaria: Agrega correctamente gastos de la misma fecha
        """
        # 1. PREPARACIÓN DE LA PRUEBA
        project_id = 1
        mock_project = MagicMock()
        mock_project.ID = 1
        mock_project.NOMBRE = "Proyecto Test"

        mock_allocation1 = MagicMock()
        mock_allocation1.FLUJO_MATERIAL_ID = 10
        mock_allocation1.CANTIDAD = 2

        mock_allocation2 = MagicMock()
        mock_allocation2.FLUJO_MATERIAL_ID = 11
        mock_allocation2.CANTIDAD = 3

        mock_flow1 = MagicMock()
        mock_flow1.MATERIAL_ID = 100
        mock_flow1.FECHA = date(2024, 1, 15)  # Misma fecha

        mock_flow2 = MagicMock()
        mock_flow2.MATERIAL_ID = 101
        mock_flow2.FECHA = date(2024, 1, 15)  # Misma fecha

        mock_material1 = MagicMock()
        mock_material1.PRECIO_UNITARIO = 100.0

        mock_material2 = MagicMock()
        mock_material2.PRECIO_UNITARIO = 50.0

        # 2. LÓGICA DE LA PRUEBA
        with patch('app.business_logic.financial_bl.get_project_by_id', return_value=mock_project), \
             patch('app.business_logic.financial_bl.get_material_allocations_by_project', return_value=[mock_allocation1, mock_allocation2]), \
             patch('app.business_logic.financial_bl.get_tool_allocations_by_project', return_value=[]), \
             patch('app.business_logic.financial_bl.get_flow_material_by_id', side_effect=[mock_flow1, mock_flow2]), \
             patch('app.business_logic.financial_bl.get_material_by_id', side_effect=[mock_material1, mock_material2]):
            
            result = FinancialBL.get_spending_trend(project_id)

        # 3. VALIDACIÓN Y ACEPTACIÓN DE LA PRUEBA
        # Debe haber solo una entrada con la suma de ambos gastos
        self.assertEqual(len(result['spending_over_time']), 1)
        self.assertEqual(result['spending_over_time'][0]['date'], '2024-01-15')
        # 100.0 * 2 + 50.0 * 3 = 200.0 + 150.0 = 350.0
        self.assertEqual(result['spending_over_time'][0]['amount'], 350.0)



    # ============================================================
    # PRUEBAS PARA get_material_spending
    # ============================================================

    def test_get_material_spending_success_multiple_materials(self):
        """
        Prueba unitaria: Calcula gastos por material con mUltiples materiales
        """
        # 1. PREPARACION DE LA PRUEBA
        project_id = 1
        mock_project = MagicMock()
        mock_project.ID = 1
        mock_project.NOMBRE = "Proyecto Test"

        mock_allocation1 = MagicMock()
        mock_allocation1.FLUJO_MATERIAL_ID = 10
        mock_allocation1.CANTIDAD = 3

        mock_allocation2 = MagicMock()
        mock_allocation2.FLUJO_MATERIAL_ID = 11
        mock_allocation2.CANTIDAD = 2

        mock_flow1 = MagicMock()
        mock_flow1.MATERIAL_ID = 100

        mock_flow2 = MagicMock()
        mock_flow2.MATERIAL_ID = 101

        mock_material1 = MagicMock()
        mock_material1.NOMBRE = "Cemento"
        mock_material1.PRECIO_UNITARIO = 100.0

        mock_material2 = MagicMock()
        mock_material2.NOMBRE = "Arena"
        mock_material2.PRECIO_UNITARIO = 50.0

        # 2. LÓGICA DE LA PRUEBA
        with patch('app.business_logic.financial_bl.get_project_by_id', return_value=mock_project), \
             patch('app.business_logic.financial_bl.get_material_allocations_by_project', return_value=[mock_allocation1, mock_allocation2]), \
             patch('app.business_logic.financial_bl.get_flow_material_by_id', side_effect=[mock_flow1, mock_flow2]), \
             patch('app.business_logic.financial_bl.get_material_by_id', side_effect=[mock_material1, mock_material2]):
            
            result = FinancialBL.get_material_spending(project_id)

        # 3. VALIDACIÓN Y ACEPTACIÓN DE LA PRUEBA
        self.assertEqual(result['project_id'], 1)
        self.assertEqual(len(result['expenses']), 2)
        self.assertEqual(result['total_expense'], 400.0)  # 100.0*3 + 50.0*2
        # Verificar que los materiales están ordenados
        categories = [exp['category'] for exp in result['expenses']]
        self.assertIn('Cemento', categories)
        self.assertIn('Arena', categories)

    def test_get_material_spending_project_not_found(self):
        """
        Prueba unitaria: Lanza excepcion cuando el proyecto no existe
        """
        # 1. PREPARACION DE LA PRUEBA
        project_id = 999

        # 2. LÓGICA DE LA PRUEBA y 3. VALIDACIÓN Y ACEPTACIÓN DE LA PRUEBA
        with patch('app.business_logic.financial_bl.get_project_by_id', return_value=None):
            with self.assertRaises(ValueError) as context:
                FinancialBL.get_material_spending(project_id)
            
            self.assertIn("not found", str(context.exception).lower())

    def test_get_material_spending_same_material_aggregation(self):
        """
        Prueba unitaria: Agrega correctamente gastos del mismo material
        """
        # 1. PREPARACION DE LA PRUEBA
        project_id = 1
        mock_project = MagicMock()
        mock_project.ID = 1
        mock_project.NOMBRE = "Proyecto Test"

        mock_allocation1 = MagicMock()
        mock_allocation1.FLUJO_MATERIAL_ID = 10
        mock_allocation1.CANTIDAD = 2

        mock_allocation2 = MagicMock()
        mock_allocation2.FLUJO_MATERIAL_ID = 11
        mock_allocation2.CANTIDAD = 3

        mock_flow1 = MagicMock()
        mock_flow1.MATERIAL_ID = 100

        mock_flow2 = MagicMock()
        mock_flow2.MATERIAL_ID = 100  # Mismo material

        mock_material = MagicMock()
        mock_material.NOMBRE = "Cemento"
        mock_material.PRECIO_UNITARIO = 100.0

        # 2. LOGICA DE LA PRUEBA
        with patch('app.business_logic.financial_bl.get_project_by_id', return_value=mock_project), \
             patch('app.business_logic.financial_bl.get_material_allocations_by_project', return_value=[mock_allocation1, mock_allocation2]), \
             patch('app.business_logic.financial_bl.get_flow_material_by_id', side_effect=[mock_flow1, mock_flow2]), \
             patch('app.business_logic.financial_bl.get_material_by_id', return_value=mock_material):
            
            result = FinancialBL.get_material_spending(project_id)

        # 3. VALIDACION Y ACEPTACION DE LA PRUEBA
        # Debe haber solo un material con la suma de ambos gastos
        self.assertEqual(len(result['expenses']), 1)
        self.assertEqual(result['expenses'][0]['category'], 'Cemento')
        # 100.0 * 2 + 100.0 * 3 = 500.0
        self.assertEqual(result['expenses'][0]['total_spent'], 500.0)
        self.assertEqual(result['total_expense'], 500.0)

    # ============================================================
    # PRUEBAS PARA get_tool_spending
    # ============================================================

    def test_get_tool_spending_success_multiple_tools(self):
        """
        Prueba unitaria: Calcula gastos por herramienta con multiples herramientas
        """
        # 1. PREPARACION DE LA PRUEBA
        project_id = 1
        mock_project = MagicMock()
        mock_project.ID = 1
        mock_project.NOMBRE = "Proyecto Test"

        mock_allocation1 = MagicMock()
        mock_allocation1.FLUJO_HERRAMIENTA_ID = 20
        mock_allocation1.CANTIDAD = 2

        mock_allocation2 = MagicMock()
        mock_allocation2.FLUJO_HERRAMIENTA_ID = 21
        mock_allocation2.CANTIDAD = 1

        mock_flow1 = MagicMock()
        mock_flow1.HERRAMIENTA_ID = 200

        mock_flow2 = MagicMock()
        mock_flow2.HERRAMIENTA_ID = 201

        mock_tool1 = MagicMock()
        mock_tool1.NOMBRE = "Taladro"
        mock_tool1.PRECIO_UNITARIO = 200.0

        mock_tool2 = MagicMock()
        mock_tool2.NOMBRE = "Martillo"
        mock_tool2.PRECIO_UNITARIO = 50.0

        # 2. LOGICA DE LA PRUEBA
        with patch('app.business_logic.financial_bl.get_project_by_id', return_value=mock_project), \
             patch('app.business_logic.financial_bl.get_tool_allocations_by_project', return_value=[mock_allocation1, mock_allocation2]), \
             patch('app.business_logic.financial_bl.get_flow_tool_by_id', side_effect=[mock_flow1, mock_flow2]), \
             patch('app.business_logic.financial_bl.get_tool_by_id', side_effect=[mock_tool1, mock_tool2]):
            
            result = FinancialBL.get_tool_spending(project_id)

        # 3. VALIDACION Y ACEPTACION DE LA PRUEBA
        self.assertEqual(result['project_id'], 1)
        self.assertEqual(len(result['expenses']), 2)
        self.assertEqual(result['total_expense'], 450.0)  # 200.0*2 + 50.0*1
        categories = [exp['category'] for exp in result['expenses']]
        self.assertIn('Taladro', categories)
        self.assertIn('Martillo', categories)

    def test_get_tool_spending_project_not_found(self):
        """
        Prueba unitaria: Lanza excepción cuando el proyecto no existe
        """
        # 1. PREPARACION DE LA PRUEBA
        project_id = 999

        # 2. LOGICA DE LA PRUEBA y 3. VALIDACION Y ACEPTACION DE LA PRUEBA
        with patch('app.business_logic.financial_bl.get_project_by_id', return_value=None):
            with self.assertRaises(ValueError) as context:
                FinancialBL.get_tool_spending(project_id)
            
            self.assertIn("not found", str(context.exception).lower())

    def test_get_tool_spending_empty_allocations(self):
        """
        Prueba unitaria: Maneja correctamente cuando no hay asignaciones de herramientas
        """
        # 1. PREPARACION DE LA PRUEBA
        project_id = 1
        mock_project = MagicMock()
        mock_project.ID = 1
        mock_project.NOMBRE = "Proyecto Sin Herramientas"

        # 2. LOGICA DE LA PRUEBA
        with patch('app.business_logic.financial_bl.get_project_by_id', return_value=mock_project), \
             patch('app.business_logic.financial_bl.get_tool_allocations_by_project', return_value=[]):
            
            result = FinancialBL.get_tool_spending(project_id)

        # 3. VALIDACION Y ACEPTACION DE LA PRUEBA
        self.assertEqual(result['project_id'], 1)
        self.assertEqual(len(result['expenses']), 0)
        self.assertEqual(result['total_expense'], 0)

    def test_get_tool_spending_tool_not_found(self):
        """
        Prueba unitaria: Maneja correctamente cuando una herramienta no se encuentra
        """
        # 1. PREPARACION DE LA PRUEBA
        project_id = 1
        mock_project = MagicMock()
        mock_project.ID = 1
        mock_project.NOMBRE = "Proyecto Test"

        mock_allocation = MagicMock()
        mock_allocation.FLUJO_HERRAMIENTA_ID = 20
        mock_allocation.CANTIDAD = 2

        mock_flow = MagicMock()
        mock_flow.HERRAMIENTA_ID = 200

        # 2. LOGICA DE LA PRUEBA
        with patch('app.business_logic.financial_bl.get_project_by_id', return_value=mock_project), \
             patch('app.business_logic.financial_bl.get_tool_allocations_by_project', return_value=[mock_allocation]), \
             patch('app.business_logic.financial_bl.get_flow_tool_by_id', return_value=mock_flow), \
             patch('app.business_logic.financial_bl.get_tool_by_id', return_value=None):
            
            result = FinancialBL.get_tool_spending(project_id)

        # 3. VALIDACION Y ACEPTACION DE LA PRUEBA
        # Si la herramienta no existe, no se suma al gasto
        self.assertEqual(len(result['expenses']), 0)
        self.assertEqual(result['total_expense'], 0)

    def test_get_tool_spending_same_tool_aggregation(self):
        """
        Prueba unitaria: Agrega correctamente gastos de la misma herramienta
        """
        # 1. PREPARACION DE LA PRUEBA
        project_id = 1
        mock_project = MagicMock()
        mock_project.ID = 1
        mock_project.NOMBRE = "Proyecto Test"

        mock_allocation1 = MagicMock()
        mock_allocation1.FLUJO_HERRAMIENTA_ID = 20
        mock_allocation1.CANTIDAD = 2

        mock_allocation2 = MagicMock()
        mock_allocation2.FLUJO_HERRAMIENTA_ID = 21
        mock_allocation2.CANTIDAD = 3

        mock_flow1 = MagicMock()
        mock_flow1.HERRAMIENTA_ID = 200

        mock_flow2 = MagicMock()
        mock_flow2.HERRAMIENTA_ID = 200  # Misma herramienta

        mock_tool = MagicMock()
        mock_tool.NOMBRE = "Taladro"
        mock_tool.PRECIO_UNITARIO = 150.0

        # 2. LOGICA DE LA PRUEBA
        with patch('app.business_logic.financial_bl.get_project_by_id', return_value=mock_project), \
             patch('app.business_logic.financial_bl.get_tool_allocations_by_project', return_value=[mock_allocation1, mock_allocation2]), \
             patch('app.business_logic.financial_bl.get_flow_tool_by_id', side_effect=[mock_flow1, mock_flow2]), \
             patch('app.business_logic.financial_bl.get_tool_by_id', return_value=mock_tool):
            
            result = FinancialBL.get_tool_spending(project_id)

        # 3. VALIDACION Y ACEPTACION DE LA PRUEBA
        # Debe haber solo una herramienta con la suma de ambos gastos
        self.assertEqual(len(result['expenses']), 1)
        self.assertEqual(result['expenses'][0]['category'], 'Taladro')
        # 150.0 * 2 + 150.0 * 3 = 750.0
        self.assertEqual(result['expenses'][0]['total_spent'], 750.0)
        self.assertEqual(result['total_expense'], 750.0)




if __name__ == '__main__':
    unittest.main()

