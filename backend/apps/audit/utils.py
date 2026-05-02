from .models import Audit

def log_audit(teacher, action, target_model, target_id, detail):
    Audit.objects.create(
        teacher=teacher,
        action = action,
        target_model=target_model,
        target_id=target_id,
        detail=detail
    )