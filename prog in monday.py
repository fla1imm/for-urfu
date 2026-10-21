class Car:
    def __init__(self,
                 amount_of_wheels:int = 4,
                 ice: bool =True,
                 windshield: bool = True,
                 body_type: str = 'Кроссовер',
                 power: int = 115,
                 max_speed: int = 180):
        self.amount_of_wheels = amount_of_wheels
        self.ice = ice
        self.windshield = windshield
        self.body_type =  body_type
        self.power = power
        self.max_speed = max_speed
    def info(self):
        print(f"{self.amount_of_wheels}")
        print(f"{self.ice}")
        print(f"{self.windshield}")
        print(f"{self.body_type}")
        print(f"{self.power}")
        print(f"{self.max_speed}")
        
matiz = Car(
    amount_of_wheels = 67,
    ice = True,
    windshield = False,
    body_type = 'Лимузин-велосипед',
    power = 777,
    max_speed = 1
)