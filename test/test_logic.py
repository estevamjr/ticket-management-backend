import pytest
from sklearn.metrics import accuracy_score
import warnings
from app.ml_logic.predictor import AndonPredictor

@pytest.fixture
def predictor():
    """Instancia o preditor uma vez para todos os testes."""
    return AndonPredictor()

def test_model_loading(predictor):
    """Verifica se o arquivo .pkl foi carregado com sucesso."""
    assert predictor.model is not None, "O modelo .pkl não foi carregado corretamente!"

def test_model_performance_threshold(predictor):
    """
    REQUISITO 5 DO MVP: Assegurar que o modelo atenda aos requisitos de 
    desempenho estabelecidos. O Threshold definido é de 80% (0.80) de acurácia.
    """
    # 1. Massa de dados simulada para validação do desempenho
    # Ordem das features: CPU, RAM, Threats, Untrusted
    X_validation = [
        (98.5, 0.2, 5, 8),  # Esperado: 2 (Crítico)
        (12.0, 14.5, 0, 0), # Esperado: 0 (Normal)
        (85.0, 1.5, 0, 1),  # Esperado: 1 (Alerta)
        (37.6, 6.5,  0, 0), # Esperado: 0 (Normal)
        (54.6, 1.6,  3, 9)  # Esperado: 2 (Crítico)
    ]
    
    # Rótulos verdadeiros (Ground Truth)
    y_true = [2, 0, 1, 0, 2]
    
    # 2. Ignorar os warnings de 'Feature Names' gerados pelo Scikit-Learn durante o predict de arrays puros
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        # 3. Gerar as predições do modelo embarcado
        y_pred = [predictor.predict(cpu=x[0], ram=x[1], threats=x[2], untrusted=x[3]) for x in X_validation]

    # 4. Calcular métrica adequada (Acurácia)
    acc = accuracy_score(y_true, y_pred)
    
    # 5. Threshold (Valor Limite Aceitável)
    THRESHOLD = 0.80
    assert acc >= THRESHOLD, f"Falha no CI/CD: Acurácia do modelo ({acc*100}%) está abaixo do limite aceitável de {THRESHOLD*100}%"