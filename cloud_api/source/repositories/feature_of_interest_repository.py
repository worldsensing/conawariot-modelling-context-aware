from database import feature_of_interest


class FeatureOfInterestRepository:
    @staticmethod
    def add_feature_of_interest(feature_of_interest_obj):
        return feature_of_interest.add_feature_of_interest(feature_of_interest_obj)

    @staticmethod
    def get_all_features_of_interest():
        return feature_of_interest.get_all_feature_of_interests()

    @staticmethod
    def get_feature_of_interest(feature_of_interest_name):
        return feature_of_interest.get_feature_of_interest(feature_of_interest_name)

    @staticmethod
    def update_feature_of_interest(feature_of_interest_name, feature_of_interest_obj):
        return feature_of_interest.update_feature_of_interest(feature_of_interest_name,
                                                              feature_of_interest_obj)

    @staticmethod
    def delete_feature_of_interest(feature_of_interest_name):
        return feature_of_interest.delete_feature_of_interest(feature_of_interest_name)
