from database import platform


class PlatformRepository:
    @staticmethod
    def add_platform(platform_obj):
        return platform.add_platform(platform_obj)

    @staticmethod
    def get_all_platforms():
        return platform.get_all_platforms()

    @staticmethod
    def get_platform(platform_name):
        return platform.get_platform(platform_name)

    @staticmethod
    def update_platform(platform_name, platform_obj):
        return platform.update_platform(platform_name, platform_obj)

    @staticmethod
    def delete_platform(platform_name):
        return platform.delete_platform(platform_name)
