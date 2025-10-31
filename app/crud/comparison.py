from typing import Optional, List
from app.models.comparison import ComparisonCreate, Comparison
from datetime import datetime
from app.core.firebase import db
import uuid

COLLECTION_NAME = "comparisons"

def create_comparison(comparison: ComparisonCreate) -> Comparison:
    """Crea una nueva comparación en Firestore."""
    comparison_id = str(uuid.uuid4())
    doc_ref = db.collection(COLLECTION_NAME).document(comparison_id)

    comparison_data = {
        "id": comparison_id,
        "user_id": comparison.user_id,
        "component1": comparison.component1,
        "component2": comparison.component2,
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": None,
        "result": None,
        "ai_generated": False,
    }

    doc_ref.set(comparison_data)
    return Comparison(**comparison_data)


def update_comparison_result(comparison_id: str, result: dict) -> Optional[Comparison]:
    """Actualiza una comparación con el resultado generado por IA."""
    doc_ref = db.collection(COLLECTION_NAME).document(comparison_id)
    doc = doc_ref.get()

    if not doc.exists:
        return None

    update_data = {
        "result": result,
        "ai_generated": True,
        "updated_at": datetime.utcnow().isoformat()
    }

    doc_ref.update(update_data)
    updated = {**doc.to_dict(), **update_data}
    return Comparison(**updated)


def get_comparison_by_id(comparison_id: str) -> Optional[Comparison]:
    """Obtiene una comparación específica."""
    doc = db.collection(COLLECTION_NAME).document(comparison_id).get()
    if doc.exists:
        return Comparison(**doc.to_dict())
    return None


def get_comparisons_by_user(user_id: str) -> List[Comparison]:
    """Obtiene todas las comparaciones de un usuario."""
    docs = db.collection(COLLECTION_NAME).where("user_id", "==", user_id).stream()
    return [Comparison(**d.to_dict()) for d in docs]


def get_all_comparisons() -> List[Comparison]:
    """Obtiene todas las comparaciones (modo admin)."""
    docs = db.collection(COLLECTION_NAME).stream()
    return [Comparison(**d.to_dict()) for d in docs]
