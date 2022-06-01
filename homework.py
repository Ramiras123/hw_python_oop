from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    INFO_MASSAGE = ('Тип тренировки: {0}; '
                    'Длительность: {1:.3f} ч.; '
                    'Дистанция: {2:.3f} км; '
                    'Ср. скорость: {3:.3f} км/ч; '
                    'Потрачено ккал: {4:.3f}.')

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Вывод информации о тренировки."""
        return self.INFO_MASSAGE.format(*asdict(self).values())


@dataclass
class Training:
    """Базовый класс тренировки."""
    M_IN_KM = 1000
    LEN_STEP = 0.65
    MINUTES = 60

    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info = InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())
        return info


class Running(Training):
    """Тренировка: бег."""
    LEN_STEP = 0.65
    COEFF1 = 18
    COEFF2 = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        result = ((self.COEFF1 * self.get_mean_speed()
                  - self.COEFF2) * self.weight
                  / super().M_IN_KM * self.duration
                  * self.MINUTES)
        return result


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF1 = 0.035
    COEFF2 = 0.029

    action: int
    duration: float
    weight: float
    height: int

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        result = ((self.get_mean_speed()**2 // self.height
                  * self.COEFF2 * self.weight
                   + self.COEFF1 * self.weight)
                  * self.duration * self.MINUTES)
        return result


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    COEFF1 = 1.1
    COEFF2 = 2

    action: int
    duration: float
    weight: float
    length_pool: int
    count_pool: int

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        result = self.length_pool * self.count_pool
        result /= super().M_IN_KM
        result /= self.duration
        return result

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        result = ((self.get_mean_speed() + self.COEFF1)
                  * self.COEFF2 * self.weight)
        return result


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_classes: dict[str, Training] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type not in workout_classes:
        raise ValueError(f'{workout_type} - данный '
                         f'трекер неопознан, используйте: '
                         f'SWM, RUN, WLK')
    else:
        return workout_classes[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]
    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
