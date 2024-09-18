import json
import unittest
from src.utils.settings_manager import SettingsManager


class TestSettings(unittest.TestCase):

    def test_singletone(self):
        manager1 = SettingsManager()
        manager1.open("../settings.json")
        manager2 = SettingsManager()
        self.assertEqual(manager1, manager2)
        self.assertEqual(manager1.settings.inn, manager2.settings.inn)
        self.assertEqual(manager1.settings.organization_name, manager2.settings.organization_name)
        self.assertEqual(manager1.settings.bic, manager2.settings.bic)
        self.assertEqual(manager1.settings.account, manager2.settings.account)
        self.assertEqual(manager1.settings.correspondent_account, manager2.settings.correspondent_account)
        self.assertEqual(manager1.settings.organization_type, manager2.settings.organization_type)

    def test_open_file_fail(self):
        manager = SettingsManager()
        file = manager.open("../settings1.json")
        self.assertEqual(file, False)

    def test_to_dict(self):
        data = {
            "organization_name" : "Рога и копыта",
            "inn": "380930934984",
            "account": "11111111111",
            "correspondent_account": "11111111111",
            "bic": "044525225",
            "organization_type": "12345"
        }
        manager1 = SettingsManager()
        manager1.convert(data)
        self.assertEqual(manager1.settings.inn, "380930934984")
        self.assertEqual(manager1.settings.organization_name, "Рога и копыта")
        self.assertEqual(manager1.settings.bic, "044525225")
        self.assertEqual(manager1.settings.account, "11111111111")
        self.assertEqual(manager1.settings.correspondent_account, "11111111111")
        self.assertEqual(manager1.settings.organization_type, "12345")



if __name__ == '__main__':
    unittest.main()
