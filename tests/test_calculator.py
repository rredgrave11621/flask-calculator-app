import pytest
from app.calculator import Calculator


class TestCalculator:
    
    def test_addition(self):
        assert Calculator.calculate('+', 2, 3) == 5
        assert Calculator.calculate('+', -1, 1) == 0
        assert Calculator.calculate('+', 0.1, 0.2) == pytest.approx(0.3)
    
    def test_subtraction(self):
        assert Calculator.calculate('-', 5, 3) == 2
        assert Calculator.calculate('-', -1, -1) == 0
        assert Calculator.calculate('-', 0, 5) == -5
    
    def test_multiplication(self):
        assert Calculator.calculate('*', 3, 4) == 12
        assert Calculator.calculate('*', -2, 3) == -6
        assert Calculator.calculate('*', 0, 100) == 0
    
    def test_division(self):
        assert Calculator.calculate('/', 10, 2) == 5
        assert Calculator.calculate('/', 1, 3) == pytest.approx(0.333333, rel=1e-5)
        assert Calculator.calculate('/', -6, 2) == -3
    
    def test_division_by_zero(self):
        with pytest.raises(ValueError, match="Division by zero"):
            Calculator.calculate('/', 5, 0)
    
    def test_power_removed(self):
        # Power operation was removed - test that it properly raises error
        with pytest.raises(ValueError, match="Unknown operation"):
            Calculator.calculate('^', 2, 3)
    
    def test_square_root(self):
        assert Calculator.calculate('sqrt', 4) == 2
        assert Calculator.calculate('sqrt', 9) == 3
        assert Calculator.calculate('sqrt', 2) == pytest.approx(1.414213, rel=1e-5)
    
    def test_square_root_negative(self):
        with pytest.raises(ValueError, match="Cannot calculate square root of negative number"):
            Calculator.calculate('sqrt', -4)
    
    def test_trigonometric_functions(self):
        assert Calculator.calculate('sin', 0) == 0
        assert Calculator.calculate('cos', 0) == 1
        assert Calculator.calculate('tan', 0) == 0
    
    def test_logarithm(self):
        assert Calculator.calculate('log', 10) == 1
        assert Calculator.calculate('log', 100) == 2
        assert Calculator.calculate('ln', 1) == 0
    
    def test_logarithm_invalid(self):
        with pytest.raises(ValueError, match="Cannot calculate logarithm of non-positive number"):
            Calculator.calculate('log', 0)
        with pytest.raises(ValueError, match="Cannot calculate logarithm of non-positive number"):
            Calculator.calculate('ln', -1)
    
    def test_unknown_operation(self):
        with pytest.raises(ValueError, match="Unknown operation"):
            Calculator.calculate('unknown', 1, 2)
    
    def test_missing_operand(self):
        with pytest.raises(ValueError, match="requires two operands"):
            Calculator.calculate('+', 5)
    
    def test_evaluate_expression(self):
        assert Calculator.evaluate_expression("2 + 3") == 5
        assert Calculator.evaluate_expression("10 - 4") == 6
        assert Calculator.evaluate_expression("3 * 4") == 12
        assert Calculator.evaluate_expression("15 / 3") == 5
    
    def test_evaluate_expression_invalid(self):
        with pytest.raises(ValueError, match="Invalid expression"):
            Calculator.evaluate_expression("2 + + 3")
        with pytest.raises(ValueError, match="Invalid expression"):
            Calculator.evaluate_expression("not a number + 3")
        with pytest.raises(ValueError, match="Invalid expression format"):
            Calculator.evaluate_expression("2 3 4")