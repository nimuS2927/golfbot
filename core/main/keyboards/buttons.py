from dataclasses import dataclass


@dataclass
class MainKB:
    main_menu = ['Вернуться в основное меню', 'main_menu']
    info_function = ['Получить информацию о возможностях бота', 'info_function']    # general
    registration_bot = ['Зарегистрироваться в боте', 'registration_bot']    # general
    registration_tournament = ['Зарегистрироваться в турнире', 'registration_tournament']    # general
    start_game = ['Запустить игру', 'start_game']    # general
    cancel = ['Выйти', 'cancel']    # general
    back = ['Назад', 'back']    # general


@dataclass
class RegistrationBotKB:
    your_name = ['Ваше имя', 'your_name']
    your_surname = ['Ваша фамилия', 'your_surname']
    your_phone = ['Ваш телефон', 'your_phone']
    your_handicap = ['Ваш handicap', 'your_handicap']
    confirm = ['Подтвердить регистрацию в боте', 'confirm_registration_bot']
