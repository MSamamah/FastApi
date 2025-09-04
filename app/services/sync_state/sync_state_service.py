from sqlalchemy.orm import Session
from app.models.shopify.sync_state.sync_state import SessionLocal, SyncState
from datetime import datetime

def get_sync_state(job_name: str):
    db = SessionLocal()
    try:
        sync_state = db.query(SyncState).filter(SyncState.job_name == job_name).first()
        return sync_state
    finally:
        db.close()

def update_sync_state(job_name: str, last_cursor: str = None, is_completed: bool = None, total_processed: int = None):
    db = SessionLocal()
    try:
        sync_state = db.query(SyncState).filter(SyncState.job_name == job_name).first()
        
        if sync_state:
            if last_cursor is not None:
                sync_state.last_cursor = last_cursor
            if is_completed is not None:
                sync_state.is_completed = is_completed
            if total_processed is not None:
                sync_state.total_processed = total_processed
            sync_state.last_run = datetime.utcnow()
        else:
            sync_state = SyncState(
                job_name=job_name,
                last_cursor=last_cursor,
                is_completed=is_completed if is_completed is not None else False,
                total_processed=total_processed if total_processed is not None else 0,
                last_run=datetime.utcnow()
            )
            db.add(sync_state)
        
        db.commit()
        return sync_state
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()