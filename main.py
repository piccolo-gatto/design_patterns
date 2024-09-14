from src.utils.settings_manager import SettingsManager

manager1 = SettingsManager()

print(f"name1: {manager1.settings.organization_name}")

manager2 = SettingsManager()
print(f"name2: {manager2.settings.organization_name}")
# 1 При отключенном методе __new__
# settings1: Рога и копыта
# settings2: Рога и копыта (default)

# 2 При включенном методе __new__
# settings1: Рога и копыта
# settings2: Рога и копыта



