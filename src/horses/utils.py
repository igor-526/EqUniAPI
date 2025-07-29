import datetime
import json
import random
from pathlib import Path
from typing import Any, Dict

from horses.models import Horse


class FakeHorsesGenerator:
    fake_data: Dict[str, Any]
    name: str
    breed: str
    sex: int
    bdate: datetime.datetime
    bdate_mode: int
    ddate: datetime.datetime
    ddate_mode: int
    description: str

    def __init__(self):
        self.name = ""
        self.breed = ""
        self.sex = 0
        self.bdate = None
        self.bdate_mode = 0
        self.ddate = None
        self.ddate_mode = 0
        self.description = ""
        fixture_path = (Path(__file__).parent.parent /
                        "fixtures" / "fake_horses.json")
        with open(fixture_path, "r", encoding="UTF-8") as f:
            self.fake_data = json.load(f)

    def set_name_and_sex(self):
        self.sex = random.randint(0, 2)
        self.name = random.choice(
            self.fake_data['names']['female'] if self.sex == 0
            else self.fake_data['names']['male']
        )

    def set_description(self):
        self.description = random.choice(
            self.fake_data['descriptions']['female'] if self.sex == 0
            else self.fake_data['descriptions']['male']
        )

    def set_breed(self):
        self.breed = random.choice(self.fake_data['breeds'])

    def set_bdate_and_ddate(self):
        year = random.randint(self.fake_data['bdate_year_min'],
                              self.fake_data['bdate_year_max'])

        self.bdate = datetime.datetime(year,
                                       random.randint(1, 12),
                                       random.randint(1, 28))
        self.bdate_mode = random.randint(0, 2)
        self.ddate_mode = random.randint(0, 2)
        dead = random.randint(0, 1)
        if dead:
            self.ddate = datetime.datetime(year + random.randint(10, 24),
                                           random.randint(1, 12),
                                           random.randint(1, 28))
        else:
            self.ddate = None

    def generate(self):
        self.set_name_and_sex()
        self.set_breed()
        self.set_bdate_and_ddate()
        self.set_description()

    def add_to_db(self):
        h = Horse.objects.create(name=self.name,
                                 sex=self.sex,
                                 bdate=self.bdate,
                                 bdate_mode=self.bdate_mode,
                                 ddate=self.ddate,
                                 ddate_mode=self.ddate_mode,
                                 description=self.description)
        h.set_breed(self.breed)
