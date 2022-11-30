from database import session


def add_response_procedure(response_procedure):
    try:
        session.add(response_procedure)
        session.flush()
        name = response_procedure.name
        session.commit()
    except Exception as e:
        session.rollback()
        return None

    return name


def get_all_response_procedures():
    from models.ResponseProcedure import ResponseProcedure

    try:
        response_procedures = session.query(ResponseProcedure) \
            .all()
        session.commit()
    except:
        session.rollback()
        return None

    return response_procedures


def get_response_procedure(response_procedure_name):
    from models.ResponseProcedure import ResponseProcedure

    try:
        response_procedures = session.query(ResponseProcedure) \
            .filter_by(name=response_procedure_name) \
            .first()
        session.commit()
    except:
        session.rollback()
        return None

    return response_procedures


def update_response_procedure(response_procedure_name, response_procedure):
    from models.ResponseProcedure import ResponseProcedure

    try:
        session.query(ResponseProcedure) \
            .filter_by(name=response_procedure_name) \
            .update(response_procedure)
        session.commit()
    except Exception as e:
        session.rollback()
        return None

    return response_procedure_name


def delete_response_procedure(response_procedure_name):
    from models.ResponseProcedure import ResponseProcedure

    try:
        session.query(ResponseProcedure) \
            .filter_by(name=response_procedure_name) \
            .delete()
        session.commit()
    except:
        session.rollback()
        return None

    return response_procedure_name
