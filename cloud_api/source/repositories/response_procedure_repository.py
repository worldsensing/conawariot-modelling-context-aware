from database import response_procedure


class ResponseProcedureRepository:
    @staticmethod
    def add_response_procedure(response_procedure_obj):
        return response_procedure.add_response_procedure(response_procedure_obj)

    @staticmethod
    def get_all_response_procedures():
        return response_procedure.get_all_response_procedures()

    @staticmethod
    def get_response_procedure(response_procedure_name):
        return response_procedure.get_response_procedure(response_procedure_name)

    @staticmethod
    def update_response_procedure(response_procedure_name, response_procedure_obj):
        return response_procedure.update_response_procedure(response_procedure_name,
                                                            response_procedure_obj)

    @staticmethod
    def delete_response_procedure(response_procedure_name):
        return response_procedure.delete_response_procedure(response_procedure_name)
