"""Программный модуль фитнес-трекера,
 который обрабатывает данные для трёх видов тренировок:
 бега, спортивной ходьбы и плавания."""

from dataclasses import dataclass
from typing import ClassVar


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self):
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


@dataclass
class Training:
    """Базовый класс тренировки."""

    MIN_IN_HOUR: ClassVar[int] = 60
    M_IN_KM: ClassVar[int] = 1000
    LEN_STEP: ClassVar[float] = 0.65

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
        raise (NotImplementedError)

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: ClassVar[int] = 18
    CALORIES_MEAN_SPEED_SHIFT: ClassVar[float] = 1.79

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight
                / self.M_IN_KM * (self.duration * self.MIN_IN_HOUR))


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_1: ClassVar[float] = 0.035
    COEFF_2: ClassVar[float] = 0.029
    SM_M: ClassVar[int] = 100
    MIN_IN_HOUR: ClassVar[int] = 60
    M_SEC: ClassVar[float] = 0.278

    height: int

    def get_spent_calories(self) -> float:
        return ((self.COEFF_1 * self.weight + ((self.get_mean_speed()
                * self.M_SEC) ** 2 / (self.height / self.SM_M))
            * self.COEFF_2 * self.weight) * (self.duration * self.MIN_IN_HOUR))


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: ClassVar[float] = 1.38
    COEFF_1: ClassVar[float] = 1.1
    COEFF_2: ClassVar[int] = 2

    length_pool: int
    count_pool: int

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.COEFF_1)
                * self.COEFF_2 * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    storage_data = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    if workout_type not in storage_data:
        raise ValueError("Неподдерживаемый тип тренировки")
    return storage_data[workout_type](*data)


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
