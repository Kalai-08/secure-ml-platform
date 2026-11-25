from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.core.audit import log_event
from app.core.database import get_db
from app.deps import require_roles
from app.ml.predictor import predict
from app.models import Role, User
from app.schemas.predict import PredictIn, PredictOut

router = APIRouter(prefix="/predict", tags=["predict"])

@router.post("", response_model=PredictOut)
def predict_tumor(
    payload: PredictIn,
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(Role.admin, Role.analyst))
):
    label, prob_benign = predict(payload.model_dump())
    # model_dump changes payload into python dictionary
    log_event(
        db,
        "predict",
        request=request,
        user_id=user.id,
        email=user.email,
        success=True,
        detail=f"prediction={label}"
    )

    return PredictOut(prediction=label, probability_benign=round(prob_benign,4))