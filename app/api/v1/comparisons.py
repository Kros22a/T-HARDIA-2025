from fastapi import APIRouter, HTTPException
from app.models.comparison import ComparisonCreate, Comparison
from app.crud import comparison as comparison_crud
from app.core.ai_client import compare_components_ai  # ✅ importamos la IA real
import traceback

router = APIRouter(prefix="/comparisons", tags=["Comparisons"])


@router.post("/", response_model=Comparison)
async def create_comparison(comparison: ComparisonCreate):
    """
    Crea una nueva comparación entre dos componentes.
    Usa la IA (Groq) para generar un análisis técnico.
    """
    try:
        # ✅ Llamada al modelo de IA
        ai_text = compare_components_ai(comparison.component1, comparison.component2)

        ai_result = {
            "performance_comparison": ai_text,
            "recommendation": "Análisis técnico generado automáticamente por IA (Groq)."
        }

        # ✅ Guardar la comparación en la base de datos
        new_comparison = comparison_crud.create_comparison(comparison)
        comparison_crud.update_comparison_result(new_comparison.id, ai_result)

        return comparison_crud.get_comparison_by_id(new_comparison.id)

    except Exception as e:
        print("❌ Error en create_comparison:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error al realizar la comparación: {str(e)}")


@router.get("/{comparison_id}", response_model=Comparison)
async def get_comparison(comparison_id: str):
    """
    Obtener una comparación por su ID
    """
    comparison = comparison_crud.get_comparison_by_id(comparison_id)
    if not comparison:
        raise HTTPException(status_code=404, detail="Comparación no encontrada")
    return comparison


@router.get("/user/{user_id}", response_model=list[Comparison])
async def get_user_comparisons(user_id: str):
    """
    Listar todas las comparaciones realizadas por un usuario.
    """
    return comparison_crud.get_comparisons_by_user(user_id)


@router.get("/", response_model=list[Comparison])
async def get_all_comparisons():
    """
    Listar todas las comparaciones (modo administrador o debug).
    """
    return comparison_crud.get_all_comparisons()
