# app/services/db_utils.py
from sqlalchemy import text
from app import db

def call_procedure(proc_name, params=None):
    """
    Calls a MySQL stored procedure securely.
    """
    connection = db.session.connection()
    try:
        # We use the raw DBAPI connection to call procedures properly
        cursor = connection.connection.cursor()
        
        if params:
            cursor.callproc(proc_name, params)
        else:
            cursor.callproc(proc_name)
            
        # If the procedure returns data (SELECT), fetch it
        results = []
        # Stored procedures can return multiple result sets
        # We loop through them to find the data
        # Note: Implementation depends on specific driver, this is standard for PyMySQL
        results = cursor.fetchall()
        
        cursor.close()
        # Commit to save any INSERT/UPDATE done by the proc
        db.session.commit() 
        return results

    except Exception as e:
        # If the trigger raises an error (SIGNAL SQLSTATE), it is caught here
        db.session.rollback()
        raise e

def check_availability_proc(check_in, check_out, room_type_id):
    """
    Calls the 'CheckAvailability' stored procedure from your SQL.
    """
    return call_procedure('CheckAvailability', [check_in, check_out, room_type_id])

def complete_booking_proc(booking_id):
    """
    Calls the 'CompleteBooking' stored procedure.
    """
    return call_procedure('CompleteBooking', [booking_id])