from database import actuation


class ActuationRepository:
    @staticmethod
    def add_actuation(actuation_obj):
        return actuation.add_actuation(actuation_obj)

    @staticmethod
    def get_all_actuations():
        return actuation.get_all_actuations()

    @staticmethod
    def get_actuation(actuation_id):
        return actuation.get_actuation(actuation_id)

    @staticmethod
    def update_actuation(actuation_id, actuation_obj):
        return actuation.update_actuation(actuation_id, actuation_obj)

    @staticmethod
    def delete_actuation(actuation_id):
        return actuation.delete_actuation(actuation_id)
