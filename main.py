from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Modelo de datos basado en el Request de Acredita [cite: 43-54]
class PsicoRequest(BaseModel):
    Doc_ID: str
    ClieID: str
    Next: Optional[str] = "0"
    Resp: Optional[str] = None
    TipoTest: str = "C"

# Banco de preguntas de prueba
PREGUNTAS = [
    {"id": "0001", "text": "En una crisis, ¿tienes ahorros suficientes? [cite: 65]"},
    {"id": "0002", "text": "¿Compras productos a mitad de precio aunque no los necesites? [cite: 109]"},
]

@app.post("/psicometrico/mock_score.php")
async def handle_test(req: PsicoRequest):
    current_step = int(req.Next or 0)
    total = len(PREGUNTAS)

    # Si terminamos las preguntas [cite: 164, 176]
    if current_step >= total:
        return {
            "Success": [{
                "Cedula": f"V{req.Doc_ID}",
                "NroQuestion": 0,
                "NroSecuence": 0,
                "message": "Cuestionario Completado... Gracias."
            }]
        }

    # Devolver pregunta actual [cite: 61-83]
    pregunta = PREGUNTAS[current_step]
    return {
        "Success": [{
            "Cedula": f"V{req.Doc_ID}",
            "Question": pregunta["text"],
            "QuestionID": pregunta["id"],
            "NroQuestion": current_step + 1,
            "totalQuestions": total,
            "Option_1_Text": "Totalmente en desacuerdo",
            "Option_2_Value": "En desacuerdo",
            "Option_5_Value": "Totalmente de acuerdo"
        }]
    }
