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
    login = ['Войти', 'confirm']
    backspace = ['Удалить символ', 'backspace']
    save = ['Сохранить изменения', 'save']
    confirm = ['Подтвердить', 'confirm']
    # region Tournaments
    tournaments = ['Турниры', 'tournaments']
    create_tournaments = ['Создать турнир', 'create_tournaments']
    update_tournaments = ['Обновить турнир', 'update_tournaments']
    entered_name = ['Ввести название турнира', 'entered_name']
    entered_type = ['Ввести тип турнира', 'entered_type']
    entered_flights = ['Ввести максимальное количество флайтов', 'entered_flights']
    entered_course_name = ['Ввести название поля', 'entered_course_name']
    entered_start = ['Ввести дату старта', 'entered_start']
    entered_end = ['Ввести дату конца', 'entered_end']
    entered_hcp = ['Ввести HCP', 'entered_hcp']
    start_tournaments = ['Запустить турнир', 'start_tournaments']
    delete_tournaments = ['Удалить турнир', 'delete_tournaments']
    nearest_tournaments = ['Ближайшие за 30 дней турниры', 'nearest_tournaments']
    all_tournaments = ['Все турниры', 'all_tournaments']
    # endregion Tournaments
    # region Users
    users = ['Пользователи', 'users']
    update_handicap = ['Изменить гандикап', 'update_handicap']
    delete_user = ['Удалить пользователя', 'delete_user']
    # endregion Users
    # region Admins
    admins = ['Админы', 'admins']
    # endregion Admins
    # region Courses
    courses = ['Гольф-поля', 'course']
    # endregion Courses
    close_admin_panel = ['Закрыть админ панель', 'close_admin_panel']
    main_admin_panel = ['Основное меню админ панели', 'main_admin_panel']
