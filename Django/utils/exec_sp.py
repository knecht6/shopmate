from django.db import connection

"""ADD DOCUMENTATION"""


def dict_fetchall(cursor):
    """
    Return all rows from a cursor as a dict

    Parameters:
    -cursor (cursor): The cursor to use the Database connection.

    Returns:
    List of rows
    """
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def exec_stored_procedure(sp_name, params, fetchall):
    """
    Executes a Stored Procedure on Database

    Parameters:
    -sp_name (String): Name of the Stored Procedure as it appears on Database

    -params (List): List of parameters of the Stored Procedure. [param1, param2, ..., param-n]

    -fetchall (bool): Indicates if it is necessary to recover all rows of the results set.


    Returns:
    List of rows or None
    """
    results = None
    # Create a cursor
    cursor = connection.cursor()
    try:
        # Execute the stored procedure passing in params as a parameter
        cursor.callproc(sp_name, params)
        if fetchall:
            results = dict_fetchall(cursor)
    finally:
        cursor.close()

    return results
