from dataclasses import dataclass, asdict
from typing import List, Dict, Type, Union


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


class Training:
    """Базовый класс тренировки."""
    M_IN_KM = 1000
    LEN_STEP = 0.65
    MINUTES = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

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
    CALORIES_MEAN_SPEED_1 = 18.0
    CALORIES_MEAN_SPEED_2 = 20.0

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        result = ((self.CALORIES_MEAN_SPEED_1 * self.get_mean_speed()
                   - self.CALORIES_MEAN_SPEED_2)
                  * self.weight / super().M_IN_KM
                  * self.duration * self.MINUTES)
        return result


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_MEAN_SPEED_1 = 0.035
    CALORIES_MEAN_SPEED_2 = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        result = ((self.get_mean_speed() ** 2 // self.height
                   * self.CALORIES_MEAN_SPEED_2 * self.weight
                   + self.CALORIES_MEAN_SPEED_1 * self.weight)
                  * self.duration * self.MINUTES)
        return result


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    CALORIES_MEAN_SPEED_1 = 1.1
    CALORIES_MEAN_SPEED_2 = 2.0

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        result: float = self.length_pool * self.count_pool
        result /= super().M_IN_KM
        result /= self.duration
        return result

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        result = ((self.get_mean_speed() + self.CALORIES_MEAN_SPEED_1)
                  * self.CALORIES_MEAN_SPEED_2 * self.weight)
        return result


def read_package(workout_type: str, data: List[Union[int, float]]) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_classes: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type not in workout_classes:
        info_workout_classes = ', '.join(list(workout_classes.keys()))
        info_error = (f'{workout_type} - данный '
                      'трекер неопознан, используйте: '
                      f'{info_workout_classes}')
        raise ValueError(info_error)
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
