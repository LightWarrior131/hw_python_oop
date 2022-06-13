from dataclasses import dataclass


@dataclass
class InfoMessage:
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    message = ('Тип тренировки: {}; '
                'Длительность: {:0.3f} ч.; '
                'Дистанция: {:0.3f} км; '
                'Ср. скорость: {:0.3f} км/ч; '
                'Потрачено ккал: {:0.3f}.'
               )
    """Информационное сообщение о тренировке."""

    def get_message(self) -> str:
        message = self.message.format(self.training_type,
                                      self.duration,
                                      self.distance,
                                      self.speed,
                                      self.calories
                                      )
        return message


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    M_IN_H = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        self.distance = (self.action * self.LEN_STEP) / self.M_IN_KM
        return self.distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        prepairing_speed = Training.get_distance(self)
        get_mean_speed = prepairing_speed / self.duration
        return get_mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Нужно задать метод в подклассе'
                                  'класса Training' % self.__class__.__name__)

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке. """
        class_name = type(self).__name__
        message = InfoMessage(class_name, self.duration, self.get_distance(),
                              self.get_mean_speed(), self.get_spent_calories())
        return message


class Running(Training):
    """Тренировка: бег."""
    coeff_calorie_1 = 18
    coeff_calorie_2 = 20

    def __init__(self, action: int, duration: float, weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        spent_calories = ((self.coeff_calorie_1 * self.get_mean_speed()
                           - self.coeff_calorie_2)
                          * self.weight / super().M_IN_KM
                          * (self.duration * super().M_IN_H)
                          )
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    coeff_walk_calorie_1 = 0.035
    coeff_walk_calorie_2 = 0.029

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.duration = duration
        self.height = height

    def get_spent_calories(self) -> float:
        spent_calories = ((self.coeff_walk_calorie_1 * self.weight
                           + (super().get_mean_speed() ** 2 // self.height)
                           * self.coeff_walk_calorie_2 * self.weight)
                          * (self.duration * super().M_IN_H)
                          )
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    cof_s_calorie_1 = 1.1
    cof_s_calorie_2 = 2

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        get_mean_speed = (self.length_pool * self.count_pool
                          / super().M_IN_KM / self.duration
                          )
        return get_mean_speed

    def get_spent_calories(self) -> float:
        spent_calories = ((self.get_mean_speed() + self.cof_s_calorie_1)
                          * self.cof_s_calorie_2 * self.weight
                          )
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    training_dictionary = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming
    }

    for workout_type_dict in training_dictionary:
        if workout_type_dict not in training_dictionary:
            print('Это неизвестная тренировка')
        else:
            object_training = training_dictionary[workout_type](*data)
    return object_training


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
