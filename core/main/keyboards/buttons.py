from dataclasses import dataclass


@dataclass
class MainKB:
    main_menu = ['Вернуться в основное меню', 'main_menu']
    info_function = ['Получить информацию о возможностях бота', 'info_function']    # general
    registration_bot = ['Зарегистрироваться в боте', 'registration_bot']    # general
    registration_tournament = ['Зарегистрироваться в турнире', 'registration_tournament']    # general
    cancel = ['Выйти', 'cancel']    # general
    back = ['Назад', 'back']    # general


@dataclass
class RegistrationBotKB:
    your_name = ['Ваше имя', 'your_name']
    your_surname = ['Ваша фамилия', 'your_surname']
    your_phone = ['Ваш телефон', 'your_phone']
    your_handicap = ['Ваш handicap', 'your_handicap']
    confirm = ['Подтвердить регистрацию в боте', 'confirm_registration_bot']


@dataclass
class RegistrationTournamentKB:
    confirm = ['Подтвердить регистрацию в турнире', 'confirm_registration_tournament']


@dataclass
class GameKB:
    start_game = ['Запустить игру', 'start_game']
    list_available_tournament = ['Список доступных турниров', 'list_available_tournament']
    completed_game = ['Завершить игру', 'completed_game']
    back_to_game = ['Вернуться к игре', 'back_to_game']


@dataclass
class AdminKB:
    confirm = ['Войти', 'confirm']
    tournaments = ['Турниры', 'tournaments']
    users = ['Пользователи', 'users']
    admins = ['Админы', 'admins']
    course = ['Гольф-поля', 'course']
    close_admin_panel = ['Закрыть админ панель', 'close_admin_panel']
